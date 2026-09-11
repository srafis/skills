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


if __name__ == "__main__":
    test_cost()
