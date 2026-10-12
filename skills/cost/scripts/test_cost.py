import json
from pathlib import Path
from tempfile import TemporaryDirectory

from cost import collect, human


def test_cost():
    with TemporaryDirectory() as folder:
        path = Path(folder) / "session.jsonl"
        events = [
            {"payload": {"id": "test"}},
            {"type": "turn_context", "payload": {"model": "gpt-6-astra"}},
        ]
        for index, counts in enumerate([(1000, 800, 100), (2000, 1600, 200)]):
            events.append({"timestamp": str(index), "payload": {"type": "token_count", "info": {"total_token_usage": dict(zip(("input_tokens", "cached_input_tokens", "output_tokens"), counts))}}})
        path.write_text("\n".join(map(json.dumps, events)))
        totals, dollars, models = collect([path], "test")
        assert totals == [2000, 1600, 200]
        assert abs(dollars - .0156) < 1e-10
        assert models == {"gpt-6-astra"}
        assert human(1250) == "1.25K" and human(1250000) == "1.25M"
        try:
            collect([path], "test", "unknown")
        except ValueError as error:
            assert "No saved USD rates" in str(error)
        else:
            raise AssertionError("Unknown model must stop")
    print("Checks passed")


def test_sol_rates():
    with TemporaryDirectory() as folder:
        path = Path(folder) / "session.jsonl"

        def run(usages, override=None, omit_last=False):
            events = [
                {"payload": {"id": "test"}},
                {"type": "turn_context", "payload": {"model": "gpt-6.1-sol"}},
            ]
            totals = [0, 0, 0]
            keys = ("input_tokens", "cached_input_tokens", "output_tokens")
            for index, counts in enumerate(usages):
                totals = [a + b for a, b in zip(totals, counts)]
                info = {"total_token_usage": dict(zip(keys, totals))}
                if not omit_last:
                    info["last_token_usage"] = dict(zip(keys, counts))
                events.append({"timestamp": str(index), "payload": {"type": "token_count", "info": info}})
            path.write_text("\n".join(map(json.dumps, events)))
            return collect([path], "test", override)

        # More than 272K across the session still uses short rates per request.
        totals, dollars, models = run([(200_000, 150_000, 1000)] * 2)
        assert totals == [400_000, 300_000, 2000]
        assert abs(dollars - .25) < 1e-10
        assert models == {"gpt-6.1-sol"}

        # Exactly 272K is short; 272001 makes the full request long context.
        _, dollars, _ = run([(272_000, 200_000, 1000)])
        assert abs(dollars - .174) < 1e-10
        _, dollars, _ = run([(272_001, 200_000, 1000)])
        assert abs(dollars - .343004) < 1e-10
        _, dollars, _ = run([(1000, 800, 100)], "gpt-6.1-sol")
        assert abs(dollars - .00148) < 1e-10

        try:
            run([(300_000, 200_000, 1000)], omit_last=True)
        except ValueError as error:
            assert "Per-request input telemetry unavailable" in str(error)
        else:
            raise AssertionError("Ambiguous context tier must stop")
    print("GPT-6.1 Sol short/long-context checks passed")


if __name__ == "__main__":
    test_cost()
    test_sol_rates()
