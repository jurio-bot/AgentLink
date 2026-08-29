#!/usr/bin/env python3
"""Read-only checks for common static-site surface mistakes."""

from __future__ import annotations

import argparse
import json
import xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit


class SurfaceParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []
        self.canonicals: list[str] = []
        self.robots: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = {key: value or "" for key, value in attrs}
        if tag in {"a", "link"} and data.get("href"):
            self.links.append(data["href"])
        if tag in {"img", "script", "source"} and data.get("src"):
            self.links.append(data["src"])
        if tag == "link" and data.get("rel", "").lower() == "canonical":
            self.canonicals.append(data.get("href", ""))
        if tag == "meta" and data.get("name", "").lower() == "robots":
            self.robots.append(data.get("content", ""))


@dataclass(frozen=True)
class Finding:
    kind: str
    file: str
    detail: str


def local_target(root: Path, source: Path, raw_url: str) -> Path | None:
    if not raw_url or raw_url.startswith(("#", "mailto:", "tel:", "//")):
        return None
    parsed = urlsplit(raw_url)
    if parsed.scheme or parsed.netloc:
        return None
    clean = parsed.path
    if not clean:
        return None
    target = root / clean.lstrip("/") if clean.startswith("/") else source.parent / clean
    if clean.endswith("/"):
        target = target / "index.html"
    return target.resolve()


def site_path(root: Path, path: Path) -> str:
    rel = path.relative_to(root).as_posix()
    if rel == "index.html":
        return "/"
    if rel.endswith("/index.html"):
        return f"/{rel[:-10]}"
    return f"/{rel}"


def sitemap_paths(path: Path) -> set[str]:
    tree = ET.parse(path)
    paths: set[str] = set()
    for node in tree.getroot().iter():
        if node.tag.rsplit("}", 1)[-1] != "loc" or not node.text:
            continue
        parsed = urlsplit(node.text.strip())
        value = parsed.path or "/"
        if not value.startswith("/"):
            value = f"/{value}"
        paths.add(value)
    return paths


def scan(
    root: Path,
    stale_text: list[str] | None = None,
    sitemap: Path | None = None,
) -> dict[str, object]:
    root = root.resolve()
    stale_text = stale_text or []
    findings: list[Finding] = []
    html_files = sorted(root.rglob("*.html"))
    indexable: list[Path] = []

    for path in html_files:
        text = path.read_text(encoding="utf-8", errors="replace")
        rel = str(path.relative_to(root))
        parser = SurfaceParser()
        parser.feed(text)
        is_noindex = any("noindex" in value.lower() for value in parser.robots)

        if len(parser.canonicals) > 1:
            findings.append(Finding("duplicate_canonical", rel, str(len(parser.canonicals))))
        if is_noindex:
            findings.append(Finding("noindex", rel, "robots meta contains noindex"))
        else:
            indexable.append(path)
        for needle in stale_text:
            if needle and needle in text:
                findings.append(Finding("stale_text", rel, needle))
        for raw_url in parser.links:
            target = local_target(root, path, raw_url)
            if target is None:
                continue
            try:
                target.relative_to(root)
            except ValueError:
                findings.append(Finding("path_escape", rel, raw_url))
                continue
            if not target.exists():
                findings.append(Finding("missing_internal", rel, raw_url))

    if sitemap is not None:
        sitemap_file = sitemap if sitemap.is_absolute() else root / sitemap
        try:
            listed = sitemap_paths(sitemap_file)
        except (OSError, ET.ParseError) as exc:
            findings.append(Finding("sitemap_error", str(sitemap), str(exc)))
        else:
            for path in indexable:
                expected = site_path(root, path)
                if expected not in listed:
                    findings.append(
                        Finding("missing_from_sitemap", str(path.relative_to(root)), expected)
                    )

    blocking = [item for item in findings if item.kind != "noindex"]
    return {
        "root": str(root),
        "html_files": len(html_files),
        "blocking_count": len(blocking),
        "informational_count": len(findings) - len(blocking),
        "ok": not blocking,
        "findings": [asdict(item) for item in findings],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Check static HTML surface integrity without network access.")
    parser.add_argument("root", nargs="?", default=".")
    parser.add_argument("--stale-text", action="append", default=[], help="Fail when this exact text remains; repeatable.")
    parser.add_argument("--sitemap", help="Optional local sitemap XML path, relative to root unless absolute.")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON.")
    args = parser.parse_args()

    result = scan(Path(args.root), args.stale_text, Path(args.sitemap) if args.sitemap else None)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"HTML files: {result['html_files']}")
        print(f"Blocking findings: {result['blocking_count']}")
        print(f"Informational findings: {result['informational_count']}")
        for finding in result["findings"]:
            print(f"{finding['kind']}: {finding['file']}: {finding['detail']}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
