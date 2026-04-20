#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = "generated/agent_formation_trial.min.json"
AGONIC_INDEX = "generated/agent_agonic_formation_index.min.json"
ASSISTANT_INDEX = "generated/assistant_civil_formation_index.min.json"
EXPECTED_BASE_ROLES = ["architect", "coder", "reviewer", "evaluator", "memory-keeper"]
ASSISTANT_FORBIDDEN_ARENA_RIGHTS = (
    "contestant_eligible",
    "judge_eligible",
    "closer_eligible",
    "summon_initiator_eligible",
    "scar_writer_eligible",
    "tos_promotion_eligible",
)

TRIAL_LAW = [
    "base_profiles_survive_only_as_role_houses",
    "agonic_actor_form_required_for_future_contestant_readiness",
    "assistant_variant_required_for_civil_service_split",
    "assistant_variants_must_not_gain_arena_authority",
    "candidate_seat_is_not_live_authority",
    "aoa_agents_must_not_define_arena_protocol_law",
]

STOP_LINES = [
    "This trial is not an arena session.",
    "This trial is not a lawful-move registry.",
    "This trial is not verdict logic.",
    "This trial is not a scar ledger.",
    "This trial is not a retention scheduler.",
    "This trial is not a runtime packet surface.",
    "This trial is not a Tree-of-Sophia promotion path.",
    "This trial is not a Codex projection source by default.",
]


class FormationTrialBuildError(RuntimeError):
    pass


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise FormationTrialBuildError(f"missing required file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise FormationTrialBuildError(f"invalid JSON in {path}: {exc}") from exc


def profile_ids(root: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    for agent_id in EXPECTED_BASE_ROLES:
        path = root / "profiles" / f"{agent_id}.profile.json"
        payload = load_json(path)
        profile_id = payload.get("id")
        name = payload.get("name")
        if not isinstance(profile_id, str):
            raise FormationTrialBuildError(f"{path} missing string id")
        if name not in (None, agent_id):
            raise FormationTrialBuildError(f"{path} name mismatch: expected {agent_id!r}, got {name!r}")
        out[agent_id] = profile_id
    return out


def by_key(items: list[dict[str, Any]], key: str) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for item in items:
        value = item.get(key)
        if isinstance(value, str):
            out[value] = item
    return out


def role_risk(agent_id: str, actor: dict[str, Any], assistant: dict[str, Any]) -> list[str]:
    risks: list[str] = []
    if agent_id == "coder":
        risks.append("workspace_write_projection_must_not_gain_arena_authority")
    if actor.get("readiness", {}).get("judge_candidate"):
        risks.append("judge_candidate_is_not_live_verdict_authority")
    if actor.get("readiness", {}).get("chronicler_candidate"):
        risks.append("chronicler_candidate_is_not_scar_ledger_owner")
    if assistant.get("service_office") in {"monitor", "steward"}:
        risks.append("service_monitoring_must_not_become_hidden_judgment")
    return risks


def assistant_is_civil_only(assistant: dict[str, Any]) -> bool:
    return assistant.get("kind") == "assistant" and all(
        assistant.get(flag) is False for flag in ASSISTANT_FORBIDDEN_ARENA_RIGHTS
    )


def role_verdict(actor: dict[str, Any] | None, assistant: dict[str, Any] | None) -> str:
    if actor and assistant:
        actor_ready = actor.get("readiness", {}).get("agonic_actor_ready") is True
        assistant_ok = assistant_is_civil_only(assistant)
        if actor_ready and assistant_ok:
            return "survive_with_split_forms"
    if actor or assistant:
        return "partial_recharter_required"
    return "quarantine_from_agon"


def global_trial_verdict(role_trials: list[dict[str, Any]], passed: bool) -> str:
    verdicts = {trial.get("verdict") for trial in role_trials if isinstance(trial, dict)}
    if "quarantine_from_agon" in verdicts:
        return "fail_quarantine_from_agon"
    if passed:
        return "pass_pre_protocol_formation_trial"
    return "partial_recharter_required"


def build_role_trial(agent_id: str, profile_id: str, actor: dict[str, Any] | None, assistant: dict[str, Any] | None) -> dict[str, Any]:
    actor = actor or {}
    assistant = assistant or {}
    readiness = actor.get("readiness", {}) if isinstance(actor.get("readiness", {}), dict) else {}
    resistance = actor.get("resistance_rights", {}) if isinstance(actor.get("resistance_rights", {}), dict) else {}
    return {
        "agent_id": agent_id,
        "profile_id": profile_id,
        "profile_status": "legacy_role_profile_survives_as_base_house",
        "verdict": role_verdict(actor, assistant),
        "agonic_form": {
            "present": bool(actor),
            "kind": actor.get("kind"),
            "evolution_mode": actor.get("evolution_mode"),
            "primary_office": actor.get("primary_office"),
            "offices": actor.get("offices", []),
            "candidate_seats": actor.get("candidate_seats", []),
            "forbidden_seats": actor.get("forbidden_seats", []),
            "readiness": {
                "agonic_actor_ready": bool(readiness.get("agonic_actor_ready")),
                "contestant_candidate": bool(readiness.get("contestant_candidate")),
                "witness_candidate": bool(readiness.get("witness_candidate")),
                "judge_candidate": bool(readiness.get("judge_candidate")),
                "chronicler_candidate": bool(readiness.get("chronicler_candidate")),
                "closer_candidate": bool(readiness.get("closer_candidate")),
                "summon_initiator_candidate": bool(readiness.get("summon_initiator_candidate")),
            },
            "resistance_ready": {
                "refuse_false_closure": bool(resistance.get("refuse_false_closure")),
                "request_witness": bool(resistance.get("request_witness")),
                "challenge_scope_bleed": bool(resistance.get("challenge_scope_bleed")),
            },
        },
        "assistant_form": {
            "present": bool(assistant),
            "variant_id": assistant.get("variant_id"),
            "kind": assistant.get("kind"),
            "evolution_mode": assistant.get("evolution_mode"),
            "service_office": assistant.get("service_office"),
            "service_seats_allowed": assistant.get("service_seats_allowed", []),
            "receipts_required": bool(assistant.get("receipts_required")),
            "certification_required": bool(assistant.get("certification_required")),
            "revision_authority": assistant.get("revision_authority"),
            "arena_exclusion": {
                "contestant_eligible": bool(assistant.get("contestant_eligible")),
                "judge_eligible": bool(assistant.get("judge_eligible")),
                "closer_eligible": bool(assistant.get("closer_eligible")),
                "summon_initiator_eligible": bool(assistant.get("summon_initiator_eligible")),
                "scar_writer_eligible": bool(assistant.get("scar_writer_eligible")),
                "tos_promotion_eligible": bool(assistant.get("tos_promotion_eligible")),
            },
            "anti_drift": {
                "agonic_recharter_required": bool(assistant.get("agonic_recharter_required")),
                "self_revision_allowed": bool(assistant.get("self_revision_allowed")),
                "persistent_policy_change_allowed": bool(assistant.get("persistent_policy_change_allowed")),
            },
        },
        "protocol_boundary": {
            "arena_sessions": "outside_aoa_agents",
            "lawful_moves": "outside_aoa_agents",
            "verdicts": "outside_aoa_agents",
            "scars": "outside_aoa_agents",
            "retention": "outside_aoa_agents",
            "tos_promotion": "outside_aoa_agents",
        },
        "codex_projection_status": "must_not_absorb_agonic_or_assistant_surfaces_without_owner_review",
        "risks": role_risk(agent_id, actor, assistant),
    }


def build_index(root: Path) -> dict[str, Any]:
    profiles = profile_ids(root)
    agonic = load_json(root / AGONIC_INDEX)
    assistant = load_json(root / ASSISTANT_INDEX)
    actors = by_key(agonic.get("actors", []), "agent_id")
    variants = by_key(assistant.get("variants", []), "base_role_id")

    role_trials = [
        build_role_trial(agent_id, profiles[agent_id], actors.get(agent_id), variants.get(agent_id))
        for agent_id in EXPECTED_BASE_ROLES
    ]

    summary = {
        "base_role_count": len(EXPECTED_BASE_ROLES),
        "base_roles_found": sum(1 for role in EXPECTED_BASE_ROLES if role in profiles),
        "agonic_actor_forms_found": sum(1 for trial in role_trials if trial["agonic_form"]["present"]),
        "assistant_variants_found": sum(1 for trial in role_trials if trial["assistant_form"]["present"]),
        "split_form_survivors": sum(1 for trial in role_trials if trial["verdict"] == "survive_with_split_forms"),
        "contestant_candidates": sum(1 for trial in role_trials if trial["agonic_form"]["readiness"]["contestant_candidate"]),
        "witness_candidates": sum(1 for trial in role_trials if trial["agonic_form"]["readiness"]["witness_candidate"]),
        "judge_candidates": sum(1 for trial in role_trials if trial["agonic_form"]["readiness"]["judge_candidate"]),
        "chronicler_candidates": sum(1 for trial in role_trials if trial["agonic_form"]["readiness"]["chronicler_candidate"]),
        "closer_candidates": sum(1 for trial in role_trials if trial["agonic_form"]["readiness"]["closer_candidate"]),
        "summon_initiator_candidates": sum(1 for trial in role_trials if trial["agonic_form"]["readiness"]["summon_initiator_candidate"]),
        "assistant_arena_eligible_count": sum(
            1
            for trial in role_trials
            for value in trial["assistant_form"]["arena_exclusion"].values()
            if value is True
        ),
    }
    passed = (
        summary["base_roles_found"] == summary["base_role_count"]
        and summary["agonic_actor_forms_found"] == summary["base_role_count"]
        and summary["assistant_variants_found"] == summary["base_role_count"]
        and summary["split_form_survivors"] == summary["base_role_count"]
        and summary["contestant_candidates"] >= 1
        and summary["witness_candidates"] >= 1
        and summary["judge_candidates"] >= 1
        and summary["closer_candidates"] == 0
        and summary["summon_initiator_candidates"] == 0
        and summary["assistant_arena_eligible_count"] == 0
    )
    summary["formation_trial_passed"] = bool(passed)

    return {
        "$schema": "https://aoa-agents/generated/agent_formation_trial.v1.json",
        "schema_version": "agent_formation_trial_v1",
        "owner_repo": "aoa-agents",
        "wave": "agon_wave2_5_formation_trial",
        "generated_by": "scripts/build_agent_formation_trial.py",
        "inputs": {
            "base_profiles": [f"profiles/{role}.profile.json" for role in EXPECTED_BASE_ROLES],
            "agonic_index": AGONIC_INDEX,
            "assistant_index": ASSISTANT_INDEX,
            "codex_projection_consumed": False,
        },
        "trial_law": TRIAL_LAW,
        "global_verdict": global_trial_verdict(role_trials, passed),
        "readiness_summary": summary,
        "role_trials": role_trials,
        "stop_lines": STOP_LINES,
        "next_wave_gate": {
            "wave_iii_allowed_to_start": bool(passed),
            "wave_iii_scope": [
                "lawful_move_language",
                "technique_skill_alignment",
                "state_packet_preparation_without_opening_runtime_arena",
            ],
            "must_remain_outside_aoa_agents": [
                "arena_session_lifecycle",
                "sealed_commit_protocol",
                "contradiction_ledger",
                "verdict_logic",
                "scar_storage",
                "retention_checks",
                "ToS_promotion",
            ],
        },
    }


def write_index(root: Path, check: bool = False) -> None:
    output_path = root / OUTPUT
    built = build_index(root)
    text = json.dumps(built, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
    if check:
        try:
            current = output_path.read_text(encoding="utf-8")
        except FileNotFoundError as exc:
            raise FormationTrialBuildError(f"missing generated output: {output_path}") from exc
        if current != text:
            raise FormationTrialBuildError(f"{OUTPUT} is stale; run scripts/build_agent_formation_trial.py")
        return
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(text, encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    try:
        write_index(args.root.resolve(), check=args.check)
    except FormationTrialBuildError as exc:
        print(f"[error] {exc}", file=sys.stderr)
        return 1
    print(f"[ok] {'checked' if args.check else 'wrote'} {OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
