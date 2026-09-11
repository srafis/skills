"""Read only the current task's telemetry; estimate using dated standard API rates."""
import json
import os
from pathlib import Path
import sys

# USD per million: uncached input, cached input, output. Verified 2026-09-10:
# https://developers.openai.com/api/docs/pricing
RATES = {
    "gpt-6-astra": (10, 1, 50),
    "gpt-5.6-sol": (4, .4, 20),
    "gpt-5.6-terra": (2, .2, 12),
    "gpt-5.6-luna": (.2, .02, 1.2),
}
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
                # ponytail: conservative short-context ceiling; add verified per-model
                # long-context thresholds and rates when a task exceeds 128K per call.
                last = info.get("last_token_usage") or {}
                if last.get("input_tokens", delta[0]) > 128_000:
                    raise ValueError("This task needs verified long-context rates; request a rate update.")
                inp, cached, out = delta
                if not 0 <= cached <= inp:
                    raise ValueError("Invalid cached-input counters; cannot estimate reliably.")
                rates = RATES[selected]
                cost += ((inp - cached) * rates[0] + cached * rates[1] + out * rates[2]) / 1_000_000
                totals = [a + b for a, b in zip(totals, delta)]
                models.add(selected)
    if not seen:
        raise ValueError("No token telemetry available for the current task.")
    return totals, cost, models


def main():
    thread = os.environ.get("CODEX_THREAD_ID")
    if not thread:
        raise ValueError("Current task ID unavailable; cannot identify this session's token log.")
    override = "-".join(" ".join(sys.argv[1:]).lower().split()) or None
    root = Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex")))
    paths = list((root / "sessions").glob(f"**/*{thread}*.jsonl"))
    totals, cost, models = collect(paths, thread, override)
    inp, cached, out = totals
    print(f"Model: {', '.join(sorted(models))}" + (" (override)" if override else ""))
    print(f"Input: {human(inp)}\nOutput: {human(out)}\nCached input: {human(cached)}\nUncached input: {human(inp - cached)}")
    print(f"Estimated USD: ${cost:.4f}")
    print("Standard API rates, 2026-09-10 snapshot; excludes tool fees and this report's remaining usage. Not a subscription charge.")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, KeyError, StopIteration) as error:
        sys.exit(str(error) or "Session log is empty or incomplete.")
