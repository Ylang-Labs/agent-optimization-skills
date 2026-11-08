---
name: build-eval
description: Build or repair a repeatable eval for an LLM application, agent, or skill using examples, expected outcomes, grading rules, and a runnable baseline. Use when the user wants to measure task performance before tuning an existing workflow.
license: MIT
---

# Build a repeatable eval

1. Pick an observable outcome and define what counts as success. For a support agent, score whether its final refund or routing action matches the approved policy. Reuse the app's existing eval harness if it can exercise that behavior.
2. Draw cases from approved traces, documented failures, and meaningful boundary conditions. Use synthetic cases to fill gaps and label them as synthetic. Review uncertain labels with the user. Give each case a stable ID, input, and category. Keep labels and grading rules separate from the app's inputs. Replay tool results or use isolated test resources for actions with side effects.
3. Choose the simplest grader that checks the outcome. Use a rule or end-state assertion for verifiable decisions. For a model judge, define a rubric with examples, check its judgments against human labels, and fix the judge model and rubric for a comparison. Separate execution errors from completed responses that score poorly.
4. Build or adapt the runner so it runs a fixed set of cases with a defined repeat count. If the eval will guide tuning, reserve a validation set for selection and an untouched test set when the data supports it. Keep near duplicates together and retain the important categories across splits. For small sets, document which cases were available during tuning and qualify the result.
5. Run a baseline within the agreed budget. Check failed and passing cases against their labels, surface execution errors, and record score variation across repeats. Save the runner command, case and grader versions, model settings, and per-case results.

For interoperable results, emit one JSONL row per attempt with `case_id`, `split`, `repeat` (starting at 1), `status`, and a `score` from 0 to 1 for completed attempts. Use status `ok` for graded attempts and `error` for execution failures. Add `cost_usd` and `latency_ms` when measured. Keep trace content and labels separate from these summary rows.

Deliver the case files, grader, runnable command, and baseline report. If execution is blocked, state which run is pending and what it needs.
