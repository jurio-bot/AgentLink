#!/usr/bin/env python3
"""Aggregate image-generation benchmark scores across diverse prompt categories."""
from __future__ import annotations

import argparse
import json
import statistics
import sys
from collections import defaultdict
from pathlib import Path

REQUIRED_CATEGORIES = ("photo", "illustration", "manga", "complex_composition")
DEFAULT_DIMENSIONS = (
    "composition",
    "prompt_adherence",
    "subject_consistency",
    "background_logic",
    "artifact_control",
)


def _load(path: str):
    if path == "-":
        return json.load(sys.stdin)
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _validate(records):
    if not isinstance(records, list) or not records:
        raise ValueError("input must be a non-empty JSON array")
    normalized = []
    for idx, row in enumerate(records):
        if not isinstance(row, dict):
            raise ValueError(f"record {idx}: expected object")
        model = str(row.get("model", "")).strip()
        category = str(row.get("category", "")).strip()
        scores = row.get("scores")
        if not model or not category or not isinstance(scores, dict) or not scores:
            raise ValueError(f"record {idx}: model, category and non-empty scores are required")
        clean_scores = {}
        for name, value in scores.items():
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise ValueError(f"record {idx}: score {name!r} must be numeric")
            value = float(value)
            if not 0 <= value <= 5:
                raise ValueError(f"record {idx}: score {name!r} must be between 0 and 5")
            clean_scores[str(name)] = value
        normalized.append({"model": model, "category": category, "scores": clean_scores})
    return normalized


def summarize(records, required_categories=REQUIRED_CATEGORIES):
    rows = _validate(records)
    grouped = defaultdict(list)
    for row in rows:
        grouped[row["model"]].append(row)
    result = []
    for model, model_rows in sorted(grouped.items()):
        case_scores, per_category = [], defaultdict(list)
        dimensions = defaultdict(list)
        for row in model_rows:
            score = statistics.fmean(row["scores"].values())
            case_scores.append(score)
            per_category[row["category"]].append(score)
            for name, value in row["scores"].items():
                dimensions[name].append(value)
        present = set(per_category)
        missing = [c for c in required_categories if c not in present]
        category_means = {k: round(statistics.fmean(v), 3) for k, v in sorted(per_category.items())}
        result.append({
            "model": model,
            "cases": len(model_rows),
            "overall_mean": round(statistics.fmean(case_scores), 3),
            "worst_case": round(min(case_scores), 3),
            "category_means": category_means,
            "dimension_means": {k: round(statistics.fmean(v), 3) for k, v in sorted(dimensions.items())},
            "missing_required_categories": missing,
            "coverage": round((len(required_categories) - len(missing)) / len(required_categories), 3),
        })
    result.sort(key=lambda x: (x["coverage"], x["worst_case"], x["overall_mean"]), reverse=True)
    return result


def _render_text(summary):
    lines = []
    for rank, row in enumerate(summary, 1):
        missing = ",".join(row["missing_required_categories"]) or "none"
        lines.append(
            f"{rank}. {row['model']} mean={row['overall_mean']:.3f} "
            f"worst={row['worst_case']:.3f} coverage={row['coverage']:.0%} missing={missing}"
        )
        cats = " ".join(f"{k}={v:.3f}" for k, v in row["category_means"].items())
        lines.append(f"   categories: {cats}")
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="JSON array file, or - for stdin")
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    args = parser.parse_args(argv)
    try:
        summary = summarize(_load(args.input))
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(_render_text(summary))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
