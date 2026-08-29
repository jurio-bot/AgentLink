#!/usr/bin/env python3
"""Read-only check for stale URLs or identifiers after a public rename/migration."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

DEFAULT_SUFFIXES = {
    ".css", ".html", ".js", ".json", ".md", ".py", ".ts", ".tsx",
    ".txt", ".xml", ".yaml", ".yml",
}
DEFAULT_EXCLUDED_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv"}
GITHUB_API = "https://api.github.com"


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


def _github_json(path: str, timeout: float = 8.0):
    request = Request(
        f"{GITHUB_API}{path}",
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "url-contract-check/1",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    with urlopen(request, timeout=timeout) as response:
        return json.load(response)


def github_public_surfaces(repo: str) -> list[dict[str, str]]:
    """Return public issue/PR and release text without requiring credentials."""
    if repo.count("/") != 1 or any(not part.strip() for part in repo.split("/")):
        raise ValueError("GitHub repo must be owner/name")
    encoded = quote(repo, safe="/")
    surfaces: list[dict[str, str]] = []

    issues = _github_json(f"/repos/{encoded}/issues?state=all&per_page=100")
    for item in issues:
        number = item.get("number")
        kind = "pr" if "pull_request" in item else "issue"
        text = "\n".join(
            value for value in (item.get("title"), item.get("body"), item.get("html_url"))
            if isinstance(value, str)
        )
        surfaces.append({"source": f"github:{repo}:{kind}#{number}", "text": text})

    releases = _github_json(f"/repos/{encoded}/releases?per_page=100")
    for item in releases:
        tag = item.get("tag_name") or item.get("id")
        text = "\n".join(
            value for value in (item.get("name"), item.get("tag_name"), item.get("body"), item.get("html_url"))
            if isinstance(value, str)
        )
        surfaces.append({"source": f"github:{repo}:release:{tag}", "text": text})
    return surfaces


def _scan_text(source: str, text: str, forbidden: list[str], required_seen: dict[str, bool], stale: list[dict]):
    for value in required_seen:
        if value in text:
            required_seen[value] = True
    for line_no, line in enumerate(text.splitlines(), start=1):
        for value in forbidden:
            if value in line:
                stale.append({
                    "path": source,
                    "line": line_no,
                    "forbidden": value,
                    "text": line.strip()[:240],
                })


def analyze(root: Path, forbidden: list[str], required: list[str], github_repos: list[str] | None = None) -> dict:
    stale: list[dict] = []
    seen_required = {value: False for value in required}
    scanned = 0
    scanned_remote = 0
    remote_errors: list[dict[str, str]] = []

    for path in iter_text_files(root):
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        scanned += 1
        _scan_text(str(path), text, forbidden, seen_required, stale)

    for repo in github_repos or []:
        try:
            surfaces = github_public_surfaces(repo)
        except (ValueError, HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
            remote_errors.append({"repo": repo, "error": f"{type(exc).__name__}: {exc}"})
            continue
        scanned_remote += len(surfaces)
        for surface in surfaces:
            _scan_text(surface["source"], surface["text"], forbidden, seen_required, stale)

    missing = [value for value, present in seen_required.items() if not present]
    return {
        "ok": not stale and not missing and not remote_errors,
        "root": str(root),
        "scanned_files": scanned,
        "scanned_remote_surfaces": scanned_remote,
        "github_repos": github_repos or [],
        "stale_references": stale,
        "missing_required": missing,
        "remote_errors": remote_errors,
    }


def render_text(report: dict) -> str:
    lines = [f"scanned {report['scanned_files']} text files"]
    if report.get("github_repos"):
        lines.append(f"scanned {report['scanned_remote_surfaces']} GitHub issue/PR/release surfaces")
    for hit in report["stale_references"]:
        lines.append(f"STALE {hit['path']}:{hit['line']} contains {hit['forbidden']!r}")
    for value in report["missing_required"]:
        lines.append(f"MISSING required reference {value!r}")
    for error in report.get("remote_errors", []):
        lines.append(f"REMOTE ERROR {error['repo']}: {error['error']}")
    if report["ok"]:
        lines.append("OK: URL/reference contract satisfied")
    return "\n".join(lines)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, help="file or directory to inspect")
    parser.add_argument("--forbid", action="append", default=[], help="substring that must not remain; repeatable")
    parser.add_argument("--require", action="append", default=[], help="substring that must appear somewhere; repeatable")
    parser.add_argument(
        "--github-repo",
        action="append",
        default=[],
        metavar="OWNER/NAME",
        help="also inspect up to 100 public issues/PRs and 100 releases; repeatable",
    )
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    args = parser.parse_args(argv)

    if not args.forbid and not args.require:
        parser.error("provide at least one --forbid or --require value")
    report = analyze(args.path, args.forbid, args.require, args.github_repo)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(render_text(report))
    return 0 if report["ok"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
