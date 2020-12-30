import unittest
from pathlib import Path
from optimistic_replay.core import replay_updates as evaluate
from optimistic_replay.fixture_check import check


class CoreTests(unittest.TestCase):

    def test_failure_rolls_back_to_a_newer_refreshed_value(self):
        result = evaluate({"value": 10, "version": 2, "events": [{"action": "begin", "id": "a", "value": 11},
            {"action": "refresh", "value": 15, "version": 3}, {"action": "resolve", "id": "a", "success": False}]})
        self.assertEqual((result["value"], result["version"], result["pending"]), (15, 3, None))
        self.assertEqual(result["results"][-1]["outcome"], "rolled_back")

    def test_newer_server_version_prevents_old_success_from_overwriting_it(self):
        result = evaluate({"value": 0, "version": 0, "events": [{"action": "begin", "id": "a", "value": 1},
            {"action": "refresh", "value": 20, "version": 4}, {"action": "resolve", "id": "a", "success": True}]})
        self.assertEqual(result["value"], 20)
        self.assertEqual(result["results"][-1]["outcome"], "conflict")

    def test_input_is_unchanged_and_unmatched_resolution_fails(self):
        from copy import deepcopy
        data = {"value": 0, "version": 0, "events": [{"action": "begin", "id": "a", "value": 1}]}
        original = deepcopy(data)
        evaluate(data)
        self.assertEqual(data, original)
        with self.assertRaises(ValueError):
            evaluate({"value": 0, "version": 0, "events": [{"action": "resolve", "id": "a", "success": True}]})

    def test_complete_fixture_corpus(self):
        self.assertGreaterEqual(check(Path(__file__).resolve().parents[1] / "fixtures/cases.jsonl", evaluate), 500)


if __name__ == "__main__":
    unittest.main()
