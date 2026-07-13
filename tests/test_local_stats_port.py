from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
READINESS_PATH = REPO_ROOT / (
    "mechanics/codex-projection/parts/specialization-eligibility/generated/"
    "specialization-eligibility-readiness.min.json"
)
PACKET_PATH = REPO_ROOT / "stats/packets/specialization-projection-eligible-ratio.reference.json"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def eligibility_census() -> tuple[int, int]:
    records = load_json(READINESS_PATH)["records"]
    eligible = sum(record["decision_status"] == "eligible" for record in records)
    return eligible, len(records)


def assert_packet_matches_owner_readiness(packet: dict) -> None:
    eligible, population_size = eligibility_census()

    assert packet["population"]["size"] == population_size
    assert packet["sample"]["size"] == population_size
    assert packet["value"]["numerator"] == eligible, (
        "packet numerator must match explicit eligible decisions"
    )
    assert packet["value"]["denominator"] == population_size
    assert packet["value"]["number"] == eligible / population_size
    assert packet["progress"] == {
        "state": "terminal",
        "completed": population_size,
        "total": population_size,
    }


class LocalStatsPortTests(unittest.TestCase):
    def test_reference_ratio_matches_current_eligibility_records(self) -> None:
        packet = load_json(PACKET_PATH)
        eligible, population_size = eligibility_census()

        self.assertEqual(population_size, 5)
        self.assertEqual(eligible, 0)
        assert_packet_matches_owner_readiness(packet)

    def test_false_all_eligible_packet_is_rejected(self) -> None:
        false_packet = deepcopy(load_json(PACKET_PATH))
        false_packet["value"]["numerator"] = false_packet["value"]["denominator"]
        false_packet["value"]["number"] = 1.0

        with self.assertRaisesRegex(
            AssertionError,
            "packet numerator must match explicit eligible decisions",
        ):
            assert_packet_matches_owner_readiness(false_packet)


if __name__ == "__main__":
    unittest.main()
