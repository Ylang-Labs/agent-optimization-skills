---
name: cost-optimize
description: Profile and reduce an LLM or agent workflow's cost, token use, or latency against a quality floor. Use when asked to investigate repeated tool calls, cache misses, model routing, effort settings, or expensive requests.
license: MIT
---

# Optimize cost per task

1. Define the unit of work and the target metric, such as dollars per ticket or time to a completed task. Agree on the quality floor, any critical case groups, and the run budget. Reuse an existing eval and usage records when they cover the decision.
2. Establish a baseline on representative cases. Record the model, settings, request count, tool calls, and observed latency. Use billed usage or the relevant rate schedule for cost. Separate input, output, cached reads, cache writes, retries, and tool charges when their rates differ. Report tokens or an estimate with its assumptions when dollar cost is unavailable.
3. Rank candidates by the observed source of spend. If the provider supports prompt caching, inspect repeated request content and confirm that the expected cache reads occur. Investigate redundant tool calls, repeated context, and oversized outputs. Try cheaper model or effort settings where the model supports them. Keep the cases and grading rules fixed and change one lever at a time when you need to attribute the savings.
4. Compare the baseline and candidate on the same cases and number of repeats. Use comparable pricing, cache state, and concurrency. Check the quality floor overall and on the critical case groups. A reduction in tokens can still increase the bill when the candidate uses a different rate.

Report the measured change in cost or latency alongside quality, the main cause of the savings, and any estimates or missing measurements. When an experiment needs new paid runs, use the approved budget or establish one before running them.
