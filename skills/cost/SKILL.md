---
name: cost
description: Quickly report the current Codex task's input, output, cached and uncached tokens in K/M notation and estimated USD cost. Use for /cost, $cost, or a request for this session's cost breakdown; accepts an optional model name.
---

# Cost

Run the bundled script once using Python 3. Resolve its path relative to this SKILL.md. Do not read the script, browse, inspect account limits, read other tasks, delegate, or research pricing during a routine report.

```sh
python3 /home/mohiwalla/.codex/skills/cost/scripts/cost.py
```

For `/cost <model>` or `$cost <model>`, pass the supplied name as a single quoted argument. The script normalizes names such as `GPT 6 Astra`. This overrides the logged model for this estimate. Without an override it reads each turn's model from the current task's local log, identified by CODEX_THREAD_ID. Never infer model identity from how an agent describes itself.

Return the script's compact report verbatim. If it reports missing model, immediately say `I need the model to proceed. Use /cost <model>.` If the task ID, telemetry, or saved price is unavailable, return that specific error and stop. Never substitute another task or model, invent a rate, or perform a broad search. A user can supply missing rates or explicitly request a rate update.

Input includes cached input. Output includes reasoning tokens; do not add reasoning a second time. The script computes differences between cumulative counters within each log segment, rather than summing cumulative events. Separate segments of the same task are combined. Other tasks and subagents are excluded.

Costs use the saved **2026-09-10 standard API rate snapshot**, not live prices, Codex credit conversion, subscription charges, or Fast mode pricing. Clearly retain this label. No web verification is needed to calculate against an explicitly dated snapshot. Updating that snapshot is a separate request and requires official pricing verification at https://developers.openai.com/api/docs/pricing .

The report is a snapshot before the report itself completes. Do not repeatedly refresh it to chase the cost of generating the report.
