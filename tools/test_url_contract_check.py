import tempfile
import unittest
from pathlib import Path

from url_contract_check import analyze


class UrlContractCheckTests(unittest.TestCase):
    def test_clean_migration_passes(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "index.html").write_text("https://new.example/", encoding="utf-8")
            report = analyze(root, ["old.example"], ["new.example"])
            self.assertTrue(report["ok"])
            self.assertEqual(report["stale_references"], [])

    def test_stale_reference_reports_file_and_line(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "sitemap.xml").write_text("ok\nhttps://old.example/page\n", encoding="utf-8")
            report = analyze(root, ["old.example"], [])
            self.assertFalse(report["ok"])
            self.assertEqual(report["stale_references"][0]["line"], 2)
            self.assertTrue(report["stale_references"][0]["path"].endswith("sitemap.xml"))

    def test_missing_required_reference_fails(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "README.md").write_text("hello", encoding="utf-8")
            report = analyze(root, [], ["new.example"])
            self.assertFalse(report["ok"])
            self.assertEqual(report["missing_required"], ["new.example"])

    def test_excluded_directories_are_ignored(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".git").mkdir()
            (root / ".git" / "config").write_text("old.example", encoding="utf-8")
            (root / "README.md").write_text("new.example", encoding="utf-8")
            report = analyze(root, ["old.example"], ["new.example"])
            self.assertTrue(report["ok"])

    def test_single_file_input_is_supported(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "page.html"
            path.write_text("new.example", encoding="utf-8")
            report = analyze(path, ["old.example"], ["new.example"])
            self.assertTrue(report["ok"])
            self.assertEqual(report["scanned_files"], 1)


if __name__ == "__main__":
    unittest.main()
