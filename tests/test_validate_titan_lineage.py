from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_titan_lineage.py"


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def valid_roles() -> dict[str, object]:
    return {
        "role_classes": [
            {
                "role_key": "architect",
            }
        ]
    }


def bearer(
    bearer_id: str,
    titan_name: str,
    *,
    status: str = "active",
    successor_of: str | None = None,
    allow_name_reuse: bool = False,
) -> dict[str, object]:
    return {
        "bearer_id": bearer_id,
        "titan_name": titan_name,
        "role_key": "architect",
        "status": status,
        "memory_policy": {
            "remember_as_person": True,
            "allow_name_reuse": allow_name_reuse,
        },
        "successor_of": successor_of,
    }


def event(event_id: str, bearer_id: str) -> dict[str, object]:
    return {
        "event_id": event_id,
        "event_type": "first_appearance",
        "bearer_id": bearer_id,
        "occurred_at": "2026-04-22",
        "summary": "A lineage event with stable evidence.",
        "source_ref": "Dionysus/tenth_wave.manifest.json",
    }


def run_validator(tmp: Path, bearers: dict[str, object], ledger: dict[str, object]) -> subprocess.CompletedProcess[str]:
    roles_path = tmp / "roles.json"
    bearers_path = tmp / "bearers.json"
    ledger_path = tmp / "ledger.json"
    write_json(roles_path, valid_roles())
    write_json(bearers_path, bearers)
    write_json(ledger_path, ledger)
    return subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--roles",
            str(roles_path),
            "--bearers",
            str(bearers_path),
            "--ledger",
            str(ledger_path),
        ],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


class ValidateTitanLineageTests(unittest.TestCase):
    def test_rejects_events_missing_required_fields(self) -> None:
        with tempfile.TemporaryDirectory(prefix="aoa-agents-titan-lineage-") as temp_dir:
            tmp = Path(temp_dir)
            bad_event = event("evt:atlas:first", "titan:atlas:founder")
            del bad_event["event_id"]
            result = run_validator(
                tmp,
                {"bearers": [bearer("titan:atlas:founder", "Atlas")]},
                {"events": [bad_event]},
            )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("missing required field event_id", result.stderr)

    def test_allows_lineage_linked_titan_name_reuse(self) -> None:
        with tempfile.TemporaryDirectory(prefix="aoa-agents-titan-lineage-") as temp_dir:
            tmp = Path(temp_dir)
            result = run_validator(
                tmp,
                {
                    "bearers": [
                        bearer("titan:atlas:founder", "Atlas", status="retired"),
                        bearer(
                            "titan:atlas:successor",
                            "Atlas",
                            successor_of="titan:atlas:founder",
                            allow_name_reuse=True,
                        ),
                    ]
                },
                {
                    "events": [
                        event("evt:atlas:first", "titan:atlas:founder"),
                        event("evt:atlas:successor", "titan:atlas:successor"),
                    ]
                },
            )

        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)


if __name__ == "__main__":
    unittest.main()
