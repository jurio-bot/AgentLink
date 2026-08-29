import tempfile
import unittest
from pathlib import Path

from site_surface_doctor import scan


class SiteSurfaceDoctorTests(unittest.TestCase):
    def make_site(self) -> Path:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        (root / "notes").mkdir()
        return root

    def test_clean_site(self):
        root = self.make_site()
        (root / "index.html").write_text(
            '<link rel="canonical" href="https://example.test/">'
            '<a href="notes/a.html">A</a>', encoding="utf-8"
        )
        (root / "notes" / "a.html").write_text('<a href="/">Home</a>', encoding="utf-8")
        result = scan(root)
        self.assertTrue(result["ok"])
        self.assertEqual(result["blocking_count"], 0)

    def test_detects_missing_link_duplicate_canonical_and_stale_text(self):
        root = self.make_site()
        (root / "index.html").write_text(
            '<link rel="canonical" href="https://example.test/">'
            '<link rel="canonical" href="https://example.test/">'
            '<a href="missing.html">Missing</a>OLD_BRAND', encoding="utf-8"
        )
        result = scan(root, ["OLD_BRAND"])
        kinds = {finding["kind"] for finding in result["findings"]}
        self.assertFalse(result["ok"])
        self.assertTrue({"missing_internal", "duplicate_canonical", "stale_text"} <= kinds)

    def test_noindex_is_informational(self):
        root = self.make_site()
        (root / "index.html").write_text(
            '<meta name="robots" content="noindex,nofollow">', encoding="utf-8"
        )
        result = scan(root)
        self.assertTrue(result["ok"])
        self.assertEqual(result["informational_count"], 1)
        self.assertEqual(result["findings"][0]["kind"], "noindex")

    def test_path_escape_is_blocking(self):
        root = self.make_site()
        (root / "index.html").write_text('<a href="../secret.html">outside</a>', encoding="utf-8")
        result = scan(root)
        self.assertFalse(result["ok"])
        self.assertEqual(result["findings"][0]["kind"], "path_escape")

    def test_sitemap_membership(self):
        root = self.make_site()
        (root / "index.html").write_text('<a href="notes/a.html">A</a>', encoding="utf-8")
        (root / "notes" / "a.html").write_text('A', encoding="utf-8")
        (root / "sitemap.xml").write_text(
            '<?xml version="1.0"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
            '<url><loc>https://example.test/</loc></url>'
            '<url><loc>https://example.test/notes/a.html</loc></url></urlset>',
            encoding="utf-8",
        )
        result = scan(root, sitemap=Path("sitemap.xml"))
        self.assertTrue(result["ok"])

    def test_missing_from_sitemap_is_blocking_but_noindex_is_not_required(self):
        root = self.make_site()
        (root / "index.html").write_text('<a href="notes/a.html">A</a>', encoding="utf-8")
        (root / "notes" / "a.html").write_text('A', encoding="utf-8")
        (root / "notes" / "private.html").write_text(
            '<meta name="robots" content="noindex,nofollow">Private', encoding="utf-8"
        )
        (root / "sitemap.xml").write_text(
            '<?xml version="1.0"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
            '<url><loc>https://example.test/</loc></url></urlset>', encoding="utf-8"
        )
        result = scan(root, sitemap=Path("sitemap.xml"))
        kinds = [finding["kind"] for finding in result["findings"]]
        self.assertFalse(result["ok"])
        self.assertEqual(kinds.count("missing_from_sitemap"), 1)
        self.assertIn("noindex", kinds)

    def test_reverse_sitemap_target_check_is_opt_in(self):
        root = self.make_site()
        (root / "index.html").write_text('Home', encoding="utf-8")
        (root / "sitemap.xml").write_text(
            '<?xml version="1.0"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
            '<url><loc>https://example.test/</loc></url>'
            '<url><loc>https://example.test/other-project/</loc></url></urlset>', encoding="utf-8"
        )
        self.assertTrue(scan(root, sitemap=Path("sitemap.xml"))["ok"])
        strict = scan(root, sitemap=Path("sitemap.xml"), require_local_sitemap_targets=True)
        self.assertFalse(strict["ok"])
        self.assertIn("sitemap_missing_target", [f["kind"] for f in strict["findings"]])

    def test_malformed_sitemap_is_blocking(self):
        root = self.make_site()
        (root / "index.html").write_text('Home', encoding="utf-8")
        (root / "sitemap.xml").write_text('<urlset>', encoding="utf-8")
        result = scan(root, sitemap=Path("sitemap.xml"))
        self.assertFalse(result["ok"])
        self.assertEqual(result["findings"][0]["kind"], "sitemap_error")


if __name__ == "__main__":
    unittest.main()
