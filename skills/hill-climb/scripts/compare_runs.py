"""Summarize two eval runs on the same split, cases, and repetitions."""

import argparse
from collections import Counter
import json
import math
from pathlib import Path
from statistics import mean


METRICS = ("score", "cost_usd", "latency_ms")


def read_run(path: Path) -> tuple[str, dict[tuple[str, int], dict[str, float]]]:
    split = ""
    rows = {}
    with path.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            if not line.strip():
                continue
            location = f"{path}:{line_number}"
            try:
                row = json.loads(line)
            except ValueError as exc:
                raise ValueError(f"{location}: invalid JSON") from exc
            if not isinstance(row, dict):
                raise ValueError(f"{location}: expected an object")
            case_id = row.get("case_id")
            repeat = row.get("repeat")
            row_split = row.get("split")
            if not isinstance(case_id, str) or not case_id.strip():
                raise ValueError(f"{location}: case_id must be a nonempty string")
            if type(repeat) is not int or repeat < 1:
                raise ValueError(f"{location}: repeat must be a positive integer")
            if not isinstance(row_split, str) or not row_split.strip():
                raise ValueError(f"{location}: split must be a nonempty string")
            if split and row_split != split:
                raise ValueError(f"{location}: each run must contain a single split")
            if row.get("status") != "ok":
                raise ValueError(f"{location}: expected a completed attempt with status ok")
            key = (case_id, repeat)
            if key in rows:
                raise ValueError(f"{location}: duplicate case and repeat")

            metrics = {}
            for metric in METRICS:
                value = row.get(metric)
                if value is None and metric != "score":
                    continue
                if type(value) not in (int, float) or not math.isfinite(value) or value < 0:
                    raise ValueError(f"{location}: {metric} must be a finite nonnegative number")
                if metric == "score" and value > 1:
                    raise ValueError(f"{location}: score must be between 0 and 1")
                metrics[metric] = value
            split = row_split
            rows[key] = metrics
    if not rows:
        raise ValueError(f"{path}: no attempts")
    attempts_by_case = Counter(case_id for case_id, _ in rows)
    if len(set(attempts_by_case.values())) != 1:
        raise ValueError(f"{path}: every case must have the same number of repeats")
    return split, rows


def compare(baseline_path: Path, candidate_path: Path) -> dict:
    baseline_split, baseline = read_run(baseline_path)
    candidate_split, candidate = read_run(candidate_path)
    if baseline_split != candidate_split:
        raise ValueError("runs must use the same split")
    if baseline.keys() != candidate.keys():
        raise ValueError("runs must contain the same case IDs and repetitions")

    summary = {
        "split": baseline_split,
        "cases": len({case_id for case_id, _ in baseline}),
        "attempts": len(baseline),
        "improved": sum(candidate[key]["score"] > baseline[key]["score"] for key in baseline),
        "regressed": sum(candidate[key]["score"] < baseline[key]["score"] for key in baseline),
    }
    for metric in METRICS:
        if any(metric not in baseline[key] or metric not in candidate[key] for key in baseline):
            summary[metric] = None
            continue
        before = mean(row[metric] for row in baseline.values())
        after = mean(row[metric] for row in candidate.values())
        summary[metric] = {"baseline": before, "candidate": after, "delta": after - before}
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("baseline", type=Path)
    parser.add_argument("candidate", type=Path)
    args = parser.parse_args()
    try:
        summary = compare(args.baseline, args.candidate)
    except (OSError, ValueError, OverflowError) as exc:
        parser.error(str(exc))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
