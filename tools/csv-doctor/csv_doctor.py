#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

ENCODINGS = ("utf-8-sig", "utf-8", "cp932")
DELIMITERS = (",", "\t", ";", "|")


def detect_encoding(data: bytes) -> str:
    for encoding in ENCODINGS:
        try:
            data.decode(encoding)
            return encoding
        except UnicodeDecodeError:
            continue
    raise ValueError("unable to decode input as utf-8/utf-8-sig/cp932")


def detect_delimiter(text: str) -> str:
    sample = "\n".join(text.splitlines()[:50])
    try:
        return csv.Sniffer().sniff(sample, delimiters="".join(DELIMITERS)).delimiter
    except csv.Error:
        counts = {d: sample.count(d) for d in DELIMITERS}
        delimiter = max(counts, key=counts.get)
        if counts[delimiter] == 0:
            return ","
        return delimiter


def is_blank_row(row: list[str]) -> bool:
    return all(not cell.strip() for cell in row)


def row_fingerprint(row: list[str]) -> str:
    payload = "\x1f".join(row).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def analyze(path: Path) -> dict:
    data = path.read_bytes()
    encoding = detect_encoding(data)
    text = data.decode(encoding)
    delimiter = detect_delimiter(text)
    rows = list(csv.reader(text.splitlines(), delimiter=delimiter))

    if not rows:
        return {
            "path": str(path),
            "encoding": encoding,
            "delimiter": delimiter,
            "rows_total": 0,
            "data_rows": 0,
            "columns_expected": 0,
            "blank_rows": [],
            "duplicate_rows": [],
            "inconsistent_rows": [],
            "issues": 0,
        }

    expected = len(rows[0])
    blank_rows = []
    duplicate_rows = []
    inconsistent_rows = []
    seen: dict[str, int] = {}

    for index, row in enumerate(rows[1:], start=2):
        if is_blank_row(row):
            blank_rows.append(index)
            continue
        if len(row) != expected:
            inconsistent_rows.append(
                {"row": index, "columns": len(row), "expected": expected}
            )
        fingerprint = row_fingerprint(row)
        if fingerprint in seen:
            duplicate_rows.append({"row": index, "first_seen_row": seen[fingerprint]})
        else:
            seen[fingerprint] = index

    issues = len(blank_rows) + len(duplicate_rows) + len(inconsistent_rows)
    return {
        "path": str(path),
        "encoding": encoding,
        "delimiter": delimiter,
        "rows_total": len(rows),
        "data_rows": max(0, len(rows) - 1),
        "columns_expected": expected,
        "blank_rows": blank_rows,
        "duplicate_rows": duplicate_rows,
        "inconsistent_rows": inconsistent_rows,
        "issues": issues,
    }


def clean_copy(source: Path, destination: Path, report: dict) -> dict:
    data = source.read_bytes()
    text = data.decode(report["encoding"])
    rows = list(csv.reader(text.splitlines(), delimiter=report["delimiter"]))
    if not rows:
        destination.write_text("", encoding="utf-8")
        return {"written_rows": 0, "removed_blank_rows": 0, "removed_duplicate_rows": 0}

    output = [rows[0]]
    seen = set()
    removed_blank = 0
    removed_duplicate = 0

    for row in rows[1:]:
        if is_blank_row(row):
            removed_blank += 1
            continue
        fingerprint = row_fingerprint(row)
        if fingerprint in seen:
            removed_duplicate += 1
            continue
        seen.add(fingerprint)
        output.append(row)

    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle, delimiter=report["delimiter"])
        writer.writerows(output)

    return {
        "written_rows": len(output),
        "removed_blank_rows": removed_blank,
        "removed_duplicate_rows": removed_duplicate,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Report common CSV/TSV structural problems without modifying the input."
    )
    parser.add_argument("file", type=Path)
    parser.add_argument(
        "--clean-out",
        type=Path,
        help="Write a cleaned copy with blank/duplicate data rows removed.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit with status 2 when issues are found.",
    )
    args = parser.parse_args(argv)

    report = analyze(args.file)
    if args.clean_out:
        report["clean"] = clean_copy(args.file, args.clean_out, report)
        report["clean"]["output"] = str(args.clean_out)

    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 2 if args.strict and report["issues"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
