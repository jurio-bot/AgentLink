import tempfile
import unittest
from pathlib import Path

import csv_doctor


class CsvDoctorTests(unittest.TestCase):
    def test_clean_file_has_no_issues(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "ok.csv"
            path.write_text("a,b\n1,2\n3,4\n", encoding="utf-8")
            report = csv_doctor.analyze(path)
            self.assertEqual(report["issues"], 0)
            self.assertEqual(report["columns_expected"], 2)

    def test_detects_blank_duplicate_and_inconsistent_rows(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "bad.csv"
            path.write_text("a,b\n1,2\n,\n1,2\n3,4,5\n", encoding="utf-8")
            report = csv_doctor.analyze(path)
            self.assertEqual(report["blank_rows"], [3])
            self.assertEqual(
                report["duplicate_rows"],
                [{"row": 4, "first_seen_row": 2}],
            )
            self.assertEqual(
                report["inconsistent_rows"],
                [{"row": 5, "columns": 3, "expected": 2}],
            )

    def test_detects_tab_delimiter(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "data.tsv"
            path.write_text("a\tb\n1\t2\n", encoding="utf-8")
            self.assertEqual(csv_doctor.analyze(path)["delimiter"], "\t")

    def test_cp932_input(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "jp.csv"
            path.write_bytes("名前,値\n太郎,1\n".encode("cp932"))
            self.assertEqual(csv_doctor.analyze(path)["encoding"], "cp932")

    def test_clean_copy_removes_only_blank_and_duplicates(self):
        with tempfile.TemporaryDirectory() as d:
            source = Path(d) / "bad.csv"
            dest = Path(d) / "clean.csv"
            source.write_text("a,b\n1,2\n,\n1,2\n3,4,5\n", encoding="utf-8")
            report = csv_doctor.analyze(source)
            clean = csv_doctor.clean_copy(source, dest, report)
            self.assertEqual(clean["removed_blank_rows"], 1)
            self.assertEqual(clean["removed_duplicate_rows"], 1)
            out = dest.read_text(encoding="utf-8-sig")
            self.assertIn("3,4,5", out)


if __name__ == "__main__":
    unittest.main()
