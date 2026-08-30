#!/usr/bin/env python3
"""Retry Guard: classify whether an interrupted automation should retry.

This tiny CLI is designed for automation pipelines that persist a receipt or
incident record after each external side effect. It intentionally prefers
reconciliation over blind retries when the outcome is uncertain.

Input: JSON object via --file or stdin.
Recognized fields:
  status: succeeded | failed | blocked | human_gate | ...
  receipt_present: bool
  side_effect: none | confirmed | unknown
  attempts: int
  max_attempts: int (default 3)

Output: one of SKIP_COMPLETED, RETRY, RECONCILE, HUMAN_REVIEW.

Example:
  echo '{"status":"failed","side_effect":"unknown"}' | python tools/retry_guard.py
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Mapping

DECISIONS = {"SKIP_COMPLETED", "RETRY", "RECONCILE", "HUMAN_REVIEW"}


def decide(record: Mapping[str, Any]) -> str:
    status = str(record.get("status", "")).strip().lower()
    receipt_value = record.get("receipt_present", False)
    if not isinstance(receipt_value, bool):
        raise ValueError("receipt_present must be a boolean")
    receipt_present = receipt_value
    side_effect = str(record.get("side_effect", "unknown")).strip().lower()

    try:
        attempts = int(record.get("attempts", 0))
        max_attempts = int(record.get("max_attempts", 3))
    except (TypeError, ValueError) as exc:
        raise ValueError("attempts and max_attempts must be integers") from exc

    if attempts < 0 or max_attempts < 0:
        raise ValueError("attempts and max_attempts must be >= 0")

    if receipt_present or status == "succeeded":
        return "SKIP_COMPLETED"

    if side_effect in {"confirmed", "unknown"}:
        return "RECONCILE"

    if status in {"blocked", "human_gate"}:
        return "HUMAN_REVIEW"

    if attempts >= max_attempts:
        return "HUMAN_REVIEW"

    if side_effect == "none":
        return "RETRY"

    raise ValueError("side_effect must be one of: none, confirmed, unknown")


def load_record(path: str | None) -> Mapping[str, Any]:
    if path:
        text = Path(path).read_text(encoding="utf-8")
    else:
        text = sys.stdin.read()

    if not text.strip():
        raise ValueError("expected a JSON object on stdin or via --file")

    value = json.loads(text)
    if not isinstance(value, dict):
        raise ValueError("input JSON must be an object")
    return value


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Safely classify retry decisions from an automation receipt."
    )
    parser.add_argument("--file", help="Path to a JSON receipt; defaults to stdin")
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit a JSON object instead of a plain decision string",
    )
    args = parser.parse_args()

    try:
        record = load_record(args.file)
        decision = decide(record)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"retry_guard: {exc}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps({"decision": decision}, separators=(",", ":")))
    else:
        print(decision)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
