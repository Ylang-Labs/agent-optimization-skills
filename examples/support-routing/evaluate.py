"""Score a deterministic support router on one split of synthetic tickets."""

import argparse
import json
from pathlib import Path


FIXTURE_DIR = Path(__file__).resolve().parent


def route(ticket: dict, variant: str) -> str:
    if ticket["kind"] == "refund":
        if variant == "candidate" and ticket["days_since_purchase"] > 30:
            return "review"
        return "refund"
    return {"login": "account", "invoice": "billing"}[ticket["kind"]]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("variant", choices=("baseline", "candidate"))
    parser.add_argument("split", choices=("train", "validation", "test"))
    args = parser.parse_args()

    labels = json.loads((FIXTURE_DIR / "expected.json").read_text(encoding="utf-8"))
    with (FIXTURE_DIR / "cases.jsonl").open(encoding="utf-8") as stream:
        for line in stream:
            case = json.loads(line)
            if case["split"] != args.split:
                continue
            action = route(case["input"], args.variant)
            print(json.dumps({
                "case_id": case["case_id"],
                "split": args.split,
                "repeat": 1,
                "status": "ok",
                "action": action,
                "score": int(action == labels[case["case_id"]]),
            }))


if __name__ == "__main__":
    main()
