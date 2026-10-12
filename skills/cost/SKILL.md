---
name: cost
description: Quickly report the current Codex task's input, output, cached and uncached tokens in K/M notation and estimated USD cost. Use for /cost, $cost, or a request for this session's cost breakdown; accepts an optional model name.
---

# Cost

Run the bundled script once using Python 3. Resolve its path relative to this SKILL.md. Do not read the script, browse, inspect account limits, read other tasks, delegate, or research pricing during a routine report.

```sh
python3 /home/mohiwalla/.agents/skills/skills/cost/scripts/cost.py
```

For `/cost <model>` or `$cost <model>`, pass the supplied name as a single quoted argument. The script normalizes names such as `GPT 6 Astra`. This overrides the logged model for this estimate. Without an override it reads each turn's model from the current task's local log, identified by CODEX_THREAD_ID. Never infer model identity from how an agent describes itself.

Return the script's Markdown table and footer verbatim, rendered directly without a code fence, introduction, or extra commentary. Use exactly these columns and row order: `Metric`, `Value`; `Model`, `Total input`, `Cached input`, `Uncached input`, `Output`, `Estimated cost`. Model names are human-readable, such as `GPT 6.1 Sol`. Token counts use two decimal places in K/M notation followed by `tokens`. Bold the USD cost with four decimal places. Leave one blank line after the table, then use `Standard API rates, **<date> snapshot**. Excludes tool fees and subsequent usage. Not a subscription charge.` For multiple snapshot dates, retain the script's date list and plural `snapshots`.

If it reports missing model, immediately say `I need the model to proceed. Use /cost <model>.` If the task ID, telemetry, or saved price is unavailable, return that specific error and stop. Never substitute another task or model, invent a rate, or perform a broad search. A user can supply missing rates or explicitly request a rate update.

Input includes cached input. Output includes reasoning tokens; do not add reasoning a second time. The script computes differences between cumulative counters within each log segment, rather than summing cumulative events. Separate segments of the same task are combined. Other tasks and subagents are excluded.

Costs use saved **standard API rate snapshots**, not live prices, Codex credit conversion, subscription charges, or Fast mode pricing. GPT-6.1 Sol was verified on **2026-10-07**; the other saved models retain their **2026-09-10** snapshot. Clearly retain the date label emitted by the script. No web verification is needed for a routine report. Updating rates is a separate request and requires official pricing verification at https://developers.openai.com/api/docs/pricing .

GPT-6.1 Sol uses $2 input, $0.10 cached input, and $10 output per 1M tokens for requests with up to 272K input tokens. Above 272K, use $4, $0.20, and $15 for the entire request. The script selects the tier using per-request input telemetry, never the session's total input. It stops when missing telemetry makes tier selection ambiguous. See https://developers.openai.com/api/docs/models/gpt-6.1-sol . Cache-write tokens are not reported separately by this telemetry and are not priced separately by this estimate.

The report is a snapshot before the report itself completes. Do not repeatedly refresh it to chase the cost of generating the report.
