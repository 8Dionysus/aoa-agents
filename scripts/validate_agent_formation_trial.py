#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

EXPECTED_BASE_ROLES = ["architect", "coder", "reviewer", "evaluator", "memory-keeper"]
REQUIRED_DOCS = [
    "docs/AGENT_FORMATION_TRIAL.md",
    "docs/AGON_PRE_PROTOCOL_AGENT_BOUNDARY.md",
    "docs/FORMATION_TRIAL_READINESS.md",
    "docs/CODEX_PROJECTION_AGON_BOUNDARY.md",
    "docs/AGON_WAVE2_5_LANDING.md",
]
FORBIDDEN_LIVE_KEYS = {
    "arena_session",
    "sealed_commit",
    "challenge_packet",
    "contradiction_ledger",
    "verdict_logic",
    "scar_ledger",
    "retention_scheduler",
    "tos_promotion_path",
}


class FormationTrialValidationError(RuntimeError):
    pass


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise FormationTrialValidationError(f"missing required file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise FormationTrialValidationError(f"invalid JSON in {path}: {exc}") from exc


def require(condition: bool, message: str) -> None:
    if not condition:
        raise FormationTrialValidationError(message)


def iter_keys(payload: Any):
    if isinstance(payload, dict):
        for key, value in payload.items():
            yield key
            yield from iter_keys(value)
    elif isinstance(payload, list):
        for value in payload:
            yield from iter_keys(value)


def import_builder(root: Path):
    builder_path = root / "scripts" / "build_agent_formation_trial.py"
    spec = importlib.util.spec_from_file_location("agent_formation_trial_builder", builder_path)
    if spec is None or spec.loader is None:
        raise FormationTrialValidationError(f"cannot import builder: {builder_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate_schema(root: Path) -> None:
    schema = load_json(root / "schemas" / "agent_formation_trial_v1.json")
    require(schema.get("$schema") == "https://json-schema.org/draft/2020-12/schema", "trial schema must use draft 2020-12")
    require(schema.get("additionalProperties") is False, "trial schema must be closed by default")


def validate_docs(root: Path) -> None:
    for rel in REQUIRED_DOCS:
        path = root / rel
        require(path.exists(), f"missing doc: {rel}")
        text = path.read_text(encoding="utf-8")
        require("Agon" in text or "Formation" in text, f"doc does not look like an Agon formation doc: {rel}")


def validate_generated(root: Path, builder) -> dict[str, Any]:
    expected = builder.build_index(root)
    actual = load_json(root / builder.OUTPUT)
    require(actual == expected, f"{builder.OUTPUT} is stale; rebuild it")
    return actual


def validate_trial_payload(payload: dict[str, Any]) -> None:
    require(payload.get("$schema") == "https://aoa-agents/generated/agent_formation_trial.v1.json", "wrong generated schema marker")
    require(payload.get("schema_version") == "agent_formation_trial_v1", "wrong schema_version")
    require(payload.get("owner_repo") == "aoa-agents", "owner_repo must be aoa-agents")
    require(payload.get("wave") == "agon_wave2_5_formation_trial", "wrong wave marker")
    require(payload.get("global_verdict") == "pass_pre_protocol_formation_trial", "formation trial must pass before Wave III")

    bad = sorted(FORBIDDEN_LIVE_KEYS.intersection(set(iter_keys(payload))))
    require(not bad, f"formation trial contains live protocol keys: {bad}")

    role_trials = payload.get("role_trials")
    require(isinstance(role_trials, list), "role_trials must be a list")
    by_agent = {trial.get("agent_id"): trial for trial in role_trials if isinstance(trial, dict)}
    require(set(by_agent) == set(EXPECTED_BASE_ROLES), f"role trial set mismatch: {sorted(by_agent)}")

    summary = payload.get("readiness_summary", {})
    require(summary.get("base_roles_found") == 5, "expected five base roles")
    require(summary.get("agonic_actor_forms_found") == 5, "expected five agonic actor forms")
    require(summary.get("assistant_variants_found") == 5, "expected five assistant variants")
    require(summary.get("split_form_survivors") == 5, "all five role homes must survive as split forms")
    require(summary.get("contestant_candidates", 0) >= 1, "at least one contestant candidate required")
    require(summary.get("witness_candidates", 0) >= 1, "at least one witness candidate required")
    require(summary.get("judge_candidates", 0) >= 1, "at least one judge candidate required")
    require(summary.get("closer_candidates") == 0, "closer authority must remain withheld")
    require(summary.get("summon_initiator_candidates") == 0, "summon initiator authority must remain withheld")
    require(summary.get("assistant_arena_eligible_count") == 0, "assistants must have zero arena authority")
    require(summary.get("formation_trial_passed") is True, "formation_trial_passed must be true")

    for agent_id in EXPECTED_BASE_ROLES:
        trial = by_agent[agent_id]
        require(trial.get("verdict") == "survive_with_split_forms", f"{agent_id} must survive with split forms")
        agonic = trial.get("agonic_form", {})
        assistant = trial.get("assistant_form", {})
        require(agonic.get("present") is True, f"{agent_id} missing agonic form")
        require(assistant.get("present") is True, f"{agent_id} missing assistant form")
        require(agonic.get("readiness", {}).get("closer_candidate") is False, f"{agent_id} cannot be closer candidate")
        require(agonic.get("readiness", {}).get("summon_initiator_candidate") is False, f"{agent_id} cannot be summon initiator")
        exclusion = assistant.get("arena_exclusion", {})
        require(all(value is False for value in exclusion.values()), f"{agent_id} assistant must have no arena authority")
        anti_drift = assistant.get("anti_drift", {})
        require(anti_drift.get("agonic_recharter_required") is True, f"{agent_id} assistant must require agonic recharter")
        require(anti_drift.get("self_revision_allowed") is False, f"{agent_id} assistant must not self-revise")
        require(anti_drift.get("persistent_policy_change_allowed") is False, f"{agent_id} assistant must not change persistent policy")

    gate = payload.get("next_wave_gate", {})
    require(gate.get("wave_iii_allowed_to_start") is True, "Wave III gate must be open after passing trial")
    blocked = set(gate.get("must_remain_outside_aoa_agents", []))
    for expected in ["arena_session_lifecycle", "verdict_logic", "scar_storage", "retention_checks", "ToS_promotion"]:
        require(expected in blocked, f"next_wave_gate must keep {expected} outside aoa-agents")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args(argv)
    root = args.root.resolve()
    try:
        validate_schema(root)
        validate_docs(root)
        builder = import_builder(root)
        payload = validate_generated(root, builder)
        validate_trial_payload(payload)
    except Exception as exc:
        print(f"[error] {exc}", file=sys.stderr)
        return 1
    print("[ok] validated Agon Wave II.5 Formation Trial")
    print("[ok] validated split-form survivors, assistant arena exclusion, and pre-protocol stop-lines")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
