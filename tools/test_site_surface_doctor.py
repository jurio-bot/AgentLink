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

    def test_incomplete_mit_license_is_blocking(self):
        root = self.make_site()
        (root / "index.html").write_text('Home', encoding="utf-8")
        (root / "LICENSE").write_text(
            'MIT License\n\nCopyright (c) 2026 example\n\n'
            'Permission is hereby granted, free of charge, to any person obtaining a copy\n'
            'The above copyright notice and this permission notice shall be included\n'
            'THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED.\n',
            encoding="utf-8",
        )
        result = scan(root)
        self.assertFalse(result["ok"])
        findings = [f for f in result["findings"] if f["kind"] == "incomplete_mit_license"]
        self.assertEqual(len(findings), 1)
        self.assertIn("liability", findings[0]["detail"])
        self.assertIn("connection", findings[0]["detail"])

    def test_complete_mit_license_is_clean_and_non_mit_is_ignored(self):
        root = self.make_site()
        (root / "index.html").write_text('Home', encoding="utf-8")
        (root / "LICENSE").write_text(
            'MIT License\n\nCopyright (c) 2026 example\n\n'
            'Permission is hereby granted, free of charge, to any person obtaining a copy\n'
            'The above copyright notice and this permission notice shall be included\n'
            'THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND\n'
            'IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE\n'
            'OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.\n',
            encoding="utf-8",
        )
        self.assertTrue(scan(root)["ok"])
        (root / "LICENSE").write_text('Custom showcase notice\n', encoding="utf-8")
        self.assertTrue(scan(root)["ok"])

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

    def test_allowed_external_prefix_skips_only_matching_root_relative_missing(self):
        root = self.make_site()
        (root / "index.html").write_text(
            '<a href="/creator-gear-router/">Sibling Pages project</a>'
            '<a href="/still-missing/">Still missing</a>',
            encoding="utf-8",
        )
        result = scan(root, allow_external_prefixes=["/creator-gear-router/"])
        missing = [f["detail"] for f in result["findings"] if f["kind"] == "missing_internal"]
        self.assertEqual(missing, ["/still-missing/"])

    def test_allowed_external_prefix_does_not_hide_relative_or_escape_paths(self):
        root = self.make_site()
        (root / "index.html").write_text(
            '<a href="creator-gear-router/missing.html">relative remains local</a>'
            '<a href="../creator-gear-router/secret.html">escape remains blocking</a>',
            encoding="utf-8",
        )
        result = scan(root, allow_external_prefixes=["/creator-gear-router/"])
        kinds = [f["kind"] for f in result["findings"]]
        self.assertIn("missing_internal", kinds)
        self.assertIn("path_escape", kinds)

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

    def test_srcset_missing_asset_is_blocking(self):
        root = self.make_site()
        (root / "ok.webp").write_bytes(b"x")
        (root / "index.html").write_text(
            '<img src="ok.webp" srcset="ok.webp 1x, missing@2x.webp 2x">', encoding="utf-8"
        )
        result = scan(root)
        self.assertFalse(result["ok"])
        self.assertIn("missing_internal", [f["kind"] for f in result["findings"]])
        self.assertIn("missing@2x.webp", [f["detail"] for f in result["findings"]])

    def test_embedded_media_assets_are_checked(self):
        root = self.make_site()
        (root / "index.html").write_text(
            '<video src="missing.mp4" poster="missing-poster.webp"></video>'
            '<audio src="missing.mp3"></audio>'
            '<track src="missing.vtt">'
            '<iframe src="missing-frame.html"></iframe>',
            encoding="utf-8",
        )
        result = scan(root)
        details = {f["detail"] for f in result["findings"] if f["kind"] == "missing_internal"}
        self.assertFalse(result["ok"])
        self.assertEqual(
            details,
            {"missing.mp4", "missing-poster.webp", "missing.mp3", "missing.vtt", "missing-frame.html"},
        )

    def test_data_uri_srcset_is_ignored_without_false_missing(self):
        root = self.make_site()
        (root / "index.html").write_text(
            '<img srcset="data:image/svg+xml,%3Csvg%3E 1x">', encoding="utf-8"
        )
        result = scan(root)
        self.assertTrue(result["ok"])
        self.assertEqual(result["blocking_count"], 0)

    def test_mixed_data_uri_and_local_srcset_keeps_local_checks(self):
        root = self.make_site()
        (root / "index.html").write_text(
            '<img srcset="data:image/svg+xml,%3Csvg%3E 1x, missing@2x.webp 2x">',
            encoding="utf-8",
        )
        result = scan(root)
        self.assertFalse(result["ok"])
        self.assertIn("missing@2x.webp", [f["detail"] for f in result["findings"]])

    def test_descriptorless_data_uri_does_not_swallow_next_local_candidate(self):
        root = self.make_site()
        (root / "index.html").write_text(
            '<img srcset="data:image/svg+xml,%3Csvg%3E, missing@2x.webp 2x">',
            encoding="utf-8",
        )
        result = scan(root)
        self.assertFalse(result["ok"])
        self.assertIn("missing@2x.webp", [f["detail"] for f in result["findings"]])


if __name__ == "__main__":
    unittest.main()
