#!/usr/bin/env python3
"""Conservative preflight for outward-facing editorial drafts.

This does not score writing quality. It only raises review flags for shapes that
commonly look substantial while carrying little argument or lived context.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

TENSION = re.compile(
    r"(でも|ただ|一方|逆に|違う|とは限らない|けれど|however|but|yet|on the other hand)",
    re.IGNORECASE,
)
TRIGGER = re.compile(
    r"(今日|最近|実際|さっき|今回|この前|when I|today|recently|in practice)",
    re.IGNORECASE,
)
TEMPLATE_HEADING = re.compile(
    r"^#{1,4}\s*(結論|まとめ|メリット|デメリット|conclusion|summary|pros|cons)\b",
    re.IGNORECASE | re.MULTILINE,
)
NUMBERED = re.compile(r"^\s*(?:[①-⑩]|\d+[.、)])\s*", re.MULTILINE)

def analyze(text: str, mode: str = "flagship") -> dict:
    body = re.sub(r"^# .+\n+", "", text, count=1)
    chars = len(re.sub(r"\s+", "", body))
    headings = len(re.findall(r"^#{2,4}\s+", body, re.MULTILINE))
    flags: list[str] = []

    if mode == "flagship" and chars < 900:
        flags.append("too_short_for_flagship")
    if mode == "flagship" and headings >= 5 and chars < 1800:
        flags.append("outline_heavier_than_thought")
    if TEMPLATE_HEADING.search(body):
        flags.append("template_heading")
    if len(NUMBERED.findall(body)) >= 4:
        flags.append("listicle_shape")
    if mode == "flagship" and not TENSION.search(body):
        flags.append("no_visible_tension_or_counterangle")
    if mode == "flagship" and not TRIGGER.search(body):
        flags.append("no_concrete_trigger_signal")

    return {
        "mode": mode,
        "chars_no_whitespace": chars,
        "headings": headings,
        "flags": flags,
        "pass": not flags,
        "note": "Heuristic preflight only; a clean result is not a quality score.",
    }

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, help="Markdown or plain-text draft")
    parser.add_argument(
        "--mode", choices=("flagship", "micro"), default="flagship",
        help="flagship applies depth gates; micro only checks structural red flags",
    )
    args = parser.parse_args()
    result = analyze(args.path.read_text(encoding="utf-8"), args.mode)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["pass"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
