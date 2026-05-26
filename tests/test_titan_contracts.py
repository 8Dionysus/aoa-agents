from __future__ import annotations

import copy
import json
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]


def load_json(relative_path: str) -> dict:
    return json.loads((ROOT / relative_path).read_text(encoding="utf-8"))


class TitanContractTests(unittest.TestCase):
    def test_titan_report_requires_evidence_backed_findings(self) -> None:
        schema = load_json("mechanics/titan/parts/runtime-roster/schemas/agent-report.schema.json")
        validator = Draft202012Validator(schema)
        payload = {
            "schema_version": "titan_agent_report/v1",
            "report_id": "report:delta:example",
            "task_id": "task:delta:example",
            "titan_name": "Delta",
            "source_refs": ["receipt:example"],
            "findings": [
                {
                    "summary": "Closeout evidence is sufficient.",
                    "evidence_refs": ["receipt:example"],
                }
            ],
        }

        self.assertFalse(list(validator.iter_errors(payload)))

        without_findings = copy.deepcopy(payload)
        without_findings["findings"] = []
        self.assertTrue(list(validator.iter_errors(without_findings)))

        without_evidence = copy.deepcopy(payload)
        without_evidence["findings"] = [{"summary": "unsupported"}]
        self.assertTrue(list(validator.iter_errors(without_evidence)))

    def test_titan_role_assignment_schema_id_matches_filename(self) -> None:
        schema = load_json("mechanics/titan/parts/summon-boundary/schemas/agent-role-assignment.schema.json")

        self.assertEqual(
            schema["$id"],
            "https://aoa.local/schemas/titan_agent_role_assignment.schema.json",
        )


if __name__ == "__main__":
    unittest.main()
