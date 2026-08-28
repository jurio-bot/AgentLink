#!/usr/bin/env python3
"""Validate a small RAG execution trace without calling external services."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def validate_trace(trace: dict[str, Any]) -> list[str]:
    issues: list[str] = []

    run_id = trace.get("run_id")
    if not isinstance(run_id, str) or not run_id.strip():
        issues.append("missing_or_empty_run_id")

    agent_id = trace.get("agent_id")
    if not isinstance(agent_id, str) or not agent_id.strip():
        issues.append("missing_or_empty_agent_id")

    sources = trace.get("sources")
    if not isinstance(sources, list):
        issues.append("sources_must_be_list")
        return issues
    if not sources:
        issues.append("sources_empty")
        return issues

    seen: set[str] = set()
    for index, source in enumerate(sources):
        if not isinstance(source, dict):
            issues.append(f"source_{index}_must_be_object")
            continue

        source_id = source.get("source_id")
        if not isinstance(source_id, str) or not source_id.strip():
            issues.append(f"source_{index}_missing_source_id")
        elif source_id in seen:
            issues.append(f"duplicate_source_id:{source_id}")
        else:
            seen.add(source_id)

        if "score" in source:
            score = source["score"]
            if isinstance(score, bool) or not isinstance(score, (int, float)):
                issues.append(f"source_{index}_score_not_numeric")
            elif not 0 <= float(score) <= 1:
                issues.append(f"source_{index}_score_out_of_range")

    return issues


def load_trace(path: str | None) -> dict[str, Any]:
    raw = Path(path).read_text(encoding="utf-8") if path else sys.stdin.read()
    data = json.loads(raw)
    if not isinstance(data, dict):
        raise ValueError("trace must be a JSON object")
    return data


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate a dependency-free RAG trace contract")
    parser.add_argument("path", nargs="?", help="JSON trace file; reads stdin when omitted")
    parser.add_argument("--json", action="store_true", dest="json_output")
    args = parser.parse_args(argv)

    try:
        trace = load_trace(args.path)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        if args.json_output:
            print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False))
        else:
            print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    issues = validate_trace(trace)
    if args.json_output:
        print(json.dumps({"ok": not issues, "issues": issues}, ensure_ascii=False, indent=2))
    elif issues:
        for issue in issues:
            print(issue)
    else:
        print("OK")
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
