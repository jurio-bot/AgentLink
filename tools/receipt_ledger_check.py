#!/usr/bin/env python3
"""Validate a JSONL ledger of external-effect receipts.

Dependency-free public utility. It never performs external actions.
"""
import argparse
import json
import sys
from collections import Counter

TERMINAL = {"completed", "succeeded", "failed", "cancelled", "blocked"}


def load_lines(fp):
    records = []
    errors = []
    for lineno, raw in enumerate(fp, 1):
        raw = raw.strip()
        if not raw:
            continue
        try:
            obj = json.loads(raw)
            if not isinstance(obj, dict):
                raise ValueError("receipt must be a JSON object")
            records.append((lineno, obj))
        except Exception as exc:
            errors.append({"line": lineno, "kind": "invalid_json", "detail": str(exc)})
    return records, errors


def validate(records, parse_errors):
    issues = list(parse_errors)
    keys = []
    completed_provider_ids = []
    for lineno, row in records:
        key = row.get("idempotency_key")
        status = str(row.get("status", "")).lower()
        provider_id = row.get("provider_object_id") or row.get("provider_id")
        if not key:
            issues.append({"line": lineno, "kind": "missing_idempotency_key"})
        else:
            keys.append((lineno, str(key)))
        if status and status not in TERMINAL and status not in {"pending", "running", "unknown"}:
            issues.append({"line": lineno, "kind": "unknown_status", "value": status})
        if status in {"completed", "succeeded"} and not provider_id:
            issues.append({"line": lineno, "kind": "completed_without_provider_id"})
        if status in {"completed", "succeeded"} and provider_id:
            completed_provider_ids.append((lineno, str(provider_id)))

    key_counts = Counter(k for _, k in keys)
    for key, count in key_counts.items():
        if count > 1:
            lines = [line for line, value in keys if value == key]
            issues.append({"kind": "duplicate_idempotency_key", "key": key, "lines": lines})

    provider_counts = Counter(v for _, v in completed_provider_ids)
    for provider_id, count in provider_counts.items():
        if count > 1:
            lines = [line for line, value in completed_provider_ids if value == provider_id]
            issues.append({"kind": "duplicate_completed_provider_id", "provider_id": provider_id, "lines": lines})

    return issues


def main():
    parser = argparse.ArgumentParser(description="Validate receipt-ledger JSONL consistency")
    parser.add_argument("path", nargs="?", help="JSONL file; stdin when omitted")
    parser.add_argument("--json", action="store_true", dest="json_output")
    args = parser.parse_args()
    fp = open(args.path, "r", encoding="utf-8") if args.path else sys.stdin
    try:
        records, parse_errors = load_lines(fp)
    finally:
        if args.path:
            fp.close()
    issues = validate(records, parse_errors)
    result = {"records": len(records), "issues": issues, "ok": not issues}
    if args.json_output:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("OK" if not issues else f"ISSUES={len(issues)}")
        for issue in issues:
            print(json.dumps(issue, ensure_ascii=False, sort_keys=True))
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
