# Agent Optimization Skills

Four portable [Agent Skills](https://agentskills.io/specification) for improving an LLM application or agent. Use them with your project's model, tools, and eval runner.

| Skill | Reach for it when | Output |
| --- | --- | --- |
| [prompt-audit](skills/prompt-audit/SKILL.md) | An agent repeats work, follows conflicting instructions, or behaves differently after a model change. | Findings tied to instructions and traces, with focused edits to test. |
| [cost-optimize](skills/cost-optimize/SKILL.md) | Token use, cost per task, or latency has grown. | A measured baseline and comparisons against a quality floor. |
| [build-eval](skills/build-eval/SKILL.md) | You have examples of the behavior you want to improve. | Cases, grading rules, a runnable eval, and baseline results. |
| [hill-climb](skills/hill-climb/SKILL.md) | You have a runnable eval and want to improve a prompt, skill, or configuration. | A record of candidate edits, comparable scores, and a confirmed result when an untouched test set is available. |

## Use a skill in your project

Copy the complete skill folder into a location your client scans for Agent Skills. You can also ask a coding agent with filesystem access to read the linked `SKILL.md` directly. In a chat without tools, paste the skill and relevant context, then run the commands yourself. Give the model your prompt, runner, or approved traces as appropriate. For example:

> Read `skills/build-eval/SKILL.md`. Use these support traces and the refund policy to build an eval for refund eligibility and ticket routing. Give me the runner command and a baseline report.

The skills can be used independently. For a full pass, audit the existing instructions, measure cost, build a repeatable eval, and tune within the budget and quality limits you set.

## Run the example

The synthetic [support-routing fixture](examples/support-routing/) uses a deterministic router and Python 3.10 or later. Try both variants on the validation cases after inspecting the training cases. The baseline approves every refund. The candidate sends requests after 30 days to review.

```sh
run_dir=$(mktemp -d)
python3 examples/support-routing/evaluate.py baseline train > "$run_dir/train.jsonl"
cat "$run_dir/train.jsonl"
python3 examples/support-routing/evaluate.py baseline validation > "$run_dir/baseline.jsonl"
python3 examples/support-routing/evaluate.py candidate validation > "$run_dir/candidate.jsonl"
python3 skills/hill-climb/scripts/compare_runs.py "$run_dir/baseline.jsonl" "$run_dir/candidate.jsonl"
```

In training, the baseline misroutes `train-2`: it issues a refund 42 days after purchase. The validation score moves from 0.75 to 1.0 on four matched tickets. After choosing the candidate, run both variants with `test` in place of `validation` to check the reserved cases. The example's answer key is separate from router inputs. Keep real answer keys and test traces outside the editing agent's reach.

The [comparison format](skills/hill-climb/SKILL.md#compare-jsonl-results) works with results from any runner that emits the documented rows. Keep model settings, grader version, and pricing basis with your run records. The comparator reports matched scores and any complete cost or latency measurements.

Inspired by [Lance Martin's talk](https://www.youtube.com/watch?v=ys6YQ2yfBpM) and [Anthropic's eval design and hill climbing write-up](https://claude.dev/blog/automating-eval-design-and-hillclimbing/). Released under the [MIT license](LICENSE).
