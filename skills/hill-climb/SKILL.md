---
name: hill-climb
description: Improve an LLM app, agent prompt, skill, or configuration through bounded iterations against a runnable eval. Use when asked to tune an existing workflow toward higher quality or lower cost or latency with a measured quality floor.
license: MIT
---

# Hill climb against an eval

1. Verify the runner and baseline before editing. Establish the objective, acceptance threshold, allowed files or settings, and run budget. Check whether the eval has enough headroom and repeatability to detect the change. An eval at its quality ceiling can still support a cost or latency objective with a quality floor.
2. Keep the grader and case splits fixed. Give the editor training traces, including recurring failures and representative successes. Use aggregate validation scores to choose changes. Keep validation traces and the final test set outside the editor's reach during selection. For a dataset too small for reliable splits, treat repeated full-set runs as exploratory.
3. Starting from the best accepted version, propose one testable change and record the reason. Limit edits to the agreed scope. Run the candidate with the same cases and repeat count as the comparison version. Compare the objective and check the quality floor or critical cases before accepting it. Investigate a gain on training that fails to carry over to validation. Save the patch and run records so the experiment can resume or revert safely.
4. Stop at the budget or when gains are smaller than normal run variation. If a grader is repaired, rescore stored outputs for both versions under the new grader. If task inputs change, rerun both versions. After selection, compare the original baseline and winner on the reserved test set. Record the result, evaluated cases, cost basis, and remaining uncertainty.

## Compare JSONL results

When the runner emits per-attempt JSONL, use [scripts/compare_runs.py](scripts/compare_runs.py) from this skill's directory with Python 3.10 or later.

```sh
python3 scripts/compare_runs.py baseline.jsonl candidate.jsonl
```

Each file contains one split. A completed row looks like this.

```json
{"case_id":"ticket-07","split":"validation","repeat":1,"status":"ok","score":1,"cost_usd":0.002,"latency_ms":450}
```

The script requires matching case IDs, equal repeat counts for each case, unique rows, completed grades, and scores from 0 to 1. It reports the mean score and counts of paired attempts that improved or regressed. Optional cost and latency means require measurements for every matched attempt in both files. Check case coverage against the runner's expected cases and use the summary with the acceptance threshold and baseline variation.
