#!/usr/bin/env python3
"""Read-only check for stale URLs or identifiers after a public rename/migration."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

DEFAULT_SUFFIXES = {
    ".css", ".html", ".js", ".json", ".md", ".py", ".ts", ".tsx",
    ".txt", ".xml", ".yaml", ".yml",
}
DEFAULT_EXCLUDED_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv"}


def iter_text_files(root: Path, suffixes=DEFAULT_SUFFIXES, excluded_dirs=DEFAULT_EXCLUDED_DIRS):
    if root.is_file():
        yield root
        return
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in suffixes:
            continue
        if any(part in excluded_dirs for part in path.parts):
            continue
        yield path


def analyze(root: Path, forbidden: list[str], required: list[str]) -> dict:
    stale = []
    seen_required = {value: False for value in required}
    scanned = 0

    for path in iter_text_files(root):
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        scanned += 1
        for value in required:
            if value in text:
                seen_required[value] = True
        for line_no, line in enumerate(text.splitlines(), start=1):
            for value in forbidden:
                if value in line:
                    stale.append({
                        "path": str(path),
                        "line": line_no,
                        "forbidden": value,
                        "text": line.strip()[:240],
                    })

    missing = [value for value, present in seen_required.items() if not present]
    return {
        "ok": not stale and not missing,
        "root": str(root),
        "scanned_files": scanned,
        "stale_references": stale,
        "missing_required": missing,
    }


def render_text(report: dict) -> str:
    lines = [f"scanned {report['scanned_files']} text files"]
    for hit in report["stale_references"]:
        lines.append(f"STALE {hit['path']}:{hit['line']} contains {hit['forbidden']!r}")
    for value in report["missing_required"]:
        lines.append(f"MISSING required reference {value!r}")
    if report["ok"]:
        lines.append("OK: URL/reference contract satisfied")
    return "\n".join(lines)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, help="file or directory to inspect")
    parser.add_argument("--forbid", action="append", default=[], help="substring that must not remain; repeatable")
    parser.add_argument("--require", action="append", default=[], help="substring that must appear somewhere; repeatable")
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    args = parser.parse_args(argv)

    if not args.forbid and not args.require:
        parser.error("provide at least one --forbid or --require value")
    report = analyze(args.path, args.forbid, args.require)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(render_text(report))
    return 0 if report["ok"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
