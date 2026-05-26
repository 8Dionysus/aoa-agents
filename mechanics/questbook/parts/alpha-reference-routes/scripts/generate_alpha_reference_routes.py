#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[5]
EXAMPLES_ROOT = REPO_ROOT / "mechanics" / "questbook" / "parts" / "alpha-reference-routes" / "examples"
OUTPUT_RELATIVE_PATH = (
    "mechanics/questbook/parts/alpha-reference-routes/generated/alpha-reference-routes.min.json"
)
OUTPUT_PATH = REPO_ROOT / OUTPUT_RELATIVE_PATH
FILE_ORDER = (
    "local-stack-diagnosis.example.json",
    "self-agent-checkpoint-rollout.example.json",
    "validation-driven-remediation.example.json",
    "long-horizon-model-tier-orchestra.example.json",
    "restartable-inquiry-loop.example.json",
)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        raise SystemExit(f"[error] missing required file: {path.relative_to(REPO_ROOT).as_posix()}")


def read_json(path: Path) -> object:
    try:
        return json.loads(read_text(path))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"[error] invalid JSON in {path.relative_to(REPO_ROOT).as_posix()}: {exc}")


def build_alpha_reference_route_payload() -> dict[str, object]:
    entries: list[dict[str, object]] = []
    for filename in FILE_ORDER:
        path = EXAMPLES_ROOT / filename
        payload = read_json(path)
        if not isinstance(payload, dict):
            raise SystemExit(f"[error] {path.relative_to(REPO_ROOT).as_posix()} must contain an object")
        handoff_sequence = payload.get("handoff_sequence", [])
        entries.append(
            {
                "playbook_id": payload.get("playbook_id"),
                "playbook_name": payload.get("playbook_name"),
                "route_id": payload.get("route_id"),
                "cohort_pattern": payload.get("cohort_pattern"),
                "phase_order": payload.get("phase_order"),
                "handoff_roles": [
                    item.get("role_name")
                    for item in handoff_sequence
                    if isinstance(item, dict) and isinstance(item.get("role_name"), str)
                ],
                "required_artifacts": payload.get("required_artifacts"),
                "allowed_reentry_modes": payload.get("allowed_reentry_modes"),
                "required_memo_writeback_kinds": payload.get("required_memo_writeback_kinds"),
                "required_eval_anchors": payload.get("required_eval_anchors"),
                "runtime_paths": payload.get("runtime_paths"),
                "source_example_ref": path.relative_to(REPO_ROOT).as_posix(),
            }
        )

    return {
        "schema_version": 1,
        "layer": "aoa-agents",
        "source_of_truth": {
            "cohort_registry": "generated/cohort_composition_registry.json",
            "alpha_reference_route_examples": "mechanics/questbook/parts/alpha-reference-routes/examples/*.example.json",
        },
        "routes": entries,
    }


def write_output(payload: dict[str, object]) -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate compact Alpha reference-route surfaces.")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Validate the generated output without writing files.",
    )
    args = parser.parse_args(argv)

    payload = build_alpha_reference_route_payload()
    if args.check:
        current = read_json(OUTPUT_PATH)
        if current != payload:
            raise SystemExit(
                f"[error] {OUTPUT_RELATIVE_PATH} is out of date; "
                "run mechanics/questbook/parts/alpha-reference-routes/scripts/generate_alpha_reference_routes.py"
            )
        print("[ok] alpha reference-route generated reader is current")
        return 0

    write_output(payload)
    print(f"[ok] wrote {OUTPUT_RELATIVE_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
