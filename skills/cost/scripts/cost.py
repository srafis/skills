"""Read only the current task's telemetry; estimate using dated standard API rates."""
import json
import os
from pathlib import Path
import sys

# USD per million: uncached input, cached input, output.
# https://developers.openai.com/api/docs/pricing
RATES = {
    "gpt-6-astra": (10, 1, 50),
    "gpt-6.1-sol": (2, .1, 10),
    "gpt-5.6-sol": (4, .4, 20),
    "gpt-5.6-terra": (2, .2, 12),
    "gpt-5.6-luna": (.2, .02, 1.2),
}
RATE_DATES = {model: "2026-09-10" for model in RATES}
RATE_DATES["gpt-6.1-sol"] = "2026-10-07"
# Applied to the full request when its input exceeds the threshold.
# https://developers.openai.com/api/docs/models/gpt-6.1-sol
LONG_CONTEXT_RATES = {"gpt-6.1-sol": (272_000, (4, .2, 15))}
KEYS = ("input_tokens", "cached_input_tokens", "output_tokens")


def human(n):
    scale, suffix = (1_000_000, "M") if n >= 1_000_000 else (1000, "K")
    return f"{n / scale:.2f}{suffix}"


def collect(paths, thread, override=None):
    totals = [0, 0, 0]
    cost = 0
    models = set()
    seen = set()
    for path in sorted(paths):
        previous = [0, 0, 0]
        model = None
        with path.open() as stream:
            meta = json.loads(next(stream))
            if meta.get("payload", {}).get("id") != thread:
                continue
            for line in stream:
                try:
                    event = json.loads(line)
                except json.JSONDecodeError:
                    continue  # Active logs can end with an unfinished write.
                payload = event.get("payload", {})
                if event.get("type") == "turn_context":
                    model = payload.get("model")
                if payload.get("type") != "token_count":
                    continue
                info = payload.get("info") or {}
                usage = info.get("total_token_usage")
                if not usage:
                    continue
                current = [usage[k] for k in KEYS]
                delta = [a - b for a, b in zip(current, previous)]
                if any(n < 0 for n in delta):
                    raise ValueError("Token counters reset inside a log; cannot estimate reliably.")
                previous = current
                identity = (event.get("timestamp"), tuple(current))
                if identity in seen or not any(delta):
                    continue
                seen.add(identity)
                selected = override or model
                if not selected:
                    raise ValueError("I need the model to proceed. Use /cost <model>.")
                if selected not in RATES:
                    raise ValueError(f"No saved USD rates for {selected}. Supply its input, cached-input and output rates per 1M tokens, or request a rate update.")
                last = info.get("last_token_usage") or {}
                request_input = last.get("input_tokens", delta[0])
                rates = RATES[selected]
                policy = LONG_CONTEXT_RATES.get(selected)
                if policy:
                    threshold, long_rates = policy
                    if "input_tokens" not in last and delta[0] > threshold:
                        raise ValueError("Per-request input telemetry unavailable; cannot select the long-context rate reliably.")
                    if request_input > threshold:
                        rates = long_rates
                elif request_input > 128_000:
                    raise ValueError("This task needs verified long-context rates; request a rate update.")
                inp, cached, out = delta
                if not 0 <= cached <= inp:
                    raise ValueError("Invalid cached-input counters; cannot estimate reliably.")
                cost += ((inp - cached) * rates[0] + cached * rates[1] + out * rates[2]) / 1_000_000
                totals = [a + b for a, b in zip(totals, delta)]
                models.add(selected)
    if not seen:
        raise ValueError("No token telemetry available for the current task.")
    return totals, cost, models


def format_report(totals, cost, models):
    inp, cached, out = totals
    names = [" ".join(part.upper() if part == "gpt" else part.capitalize()
                      for part in model.split("-")) for model in sorted(models)]
    dates = sorted({RATE_DATES[model] for model in models})
    snapshot = f"{dates[0]} snapshot" if len(dates) == 1 else f"{' / '.join(dates)} snapshots"
    return "\n".join([
        "| Metric | Value |",
        "|---|---:|",
        f"| Model | {', '.join(names)} |",
        f"| Total input | {human(inp)} tokens |",
        f"| Cached input | {human(cached)} tokens |",
        f"| Uncached input | {human(inp - cached)} tokens |",
        f"| Output | {human(out)} tokens |",
        f"| Estimated cost | **${cost:.4f}** |",
        "",
        f"Standard API rates, **{snapshot}**. Excludes tool fees and subsequent usage. Not a subscription charge.",
    ])


def main():
    thread = os.environ.get("CODEX_THREAD_ID")
    if not thread:
        raise ValueError("Current task ID unavailable; cannot identify this session's token log.")
    override = "-".join(" ".join(sys.argv[1:]).lower().split()) or None
    root = Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex")))
    paths = list((root / "sessions").glob(f"**/*{thread}*.jsonl"))
    totals, cost, models = collect(paths, thread, override)
    print(format_report(totals, cost, models))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, KeyError, StopIteration) as error:
        sys.exit(str(error) or "Session log is empty or incomplete.")
