#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import build_agent_agonic_formation_index as formation_builder

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_AGENTS = formation_builder.REQUIRED_AGENTS

SCHEMA_CONSTS = {
    "kind": "https://aoa-agents/schemas/agent_kind_v1.json",
    "subjectivity": "https://aoa-agents/schemas/agent_subjectivity_v1.json",
    "office": "https://aoa-agents/schemas/agent_office_overlay_v1.json",
    "arena": "https://aoa-agents/schemas/agent_arena_eligibility_v1.json",
    "resistance": "https://aoa-agents/schemas/agent_resistance_revision_v1.json",
}

FORBIDDEN_KEYS = {
    "arena_session",
    "battle_session",
    "sealed_commit",
    "challenge_packet",
    "contradiction_ledger",
    "verdict",
    "verdicts",
    "scar_ledger",
    "scars",
    "retention_check",
    "retention_checks",
    "runtime_packet",
    "tree_promotion",
    "tos_promotion",
}


class FormationValidationError(RuntimeError):
    pass


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise FormationValidationError(f"missing required file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise FormationValidationError(f"invalid JSON in {path}: {exc}") from exc


def iter_keys(payload: Any):
    if isinstance(payload, dict):
        for key, value in payload.items():
            yield key
            yield from iter_keys(value)
    elif isinstance(payload, list):
        for value in payload:
            yield from iter_keys(value)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise FormationValidationError(message)


def load_adjunct(agent_id: str, family: str, suffix: str) -> dict[str, Any]:
    rel_dir = formation_builder.SOURCE_DIRS[family]
    path = ROOT / rel_dir / f"{agent_id}{suffix}"
    payload = read_json(path)
    require(payload.get("agent_id") == agent_id, f"{path} agent_id mismatch")
    return payload


def validate_schema_files() -> None:
    for filename in [
        "schemas/agent_kind_v1.json",
        "schemas/agent_subjectivity_v1.json",
        "schemas/agent_office_overlay_v1.json",
        "schemas/agent_arena_eligibility_v1.json",
        "schemas/agent_resistance_revision_v1.json",
    ]:
        payload = read_json(ROOT / filename)
        require(payload.get("$schema") == "https://json-schema.org/draft/2020-12/schema", f"{filename} has wrong JSON schema marker")
        require(payload.get("additionalProperties") is False, f"{filename} must be closed by default")


def validate_profile_cross_refs() -> dict[str, str]:
    profiles_dir = ROOT / "profiles"
    require(profiles_dir.exists(), "profiles/ directory missing; run after merging seed into aoa-agents")
    profiles: dict[str, str] = {}
    for path in sorted(profiles_dir.glob("*.profile.json")):
        payload = read_json(path)
        name = payload.get("name")
        profile_id = payload.get("id")
        if isinstance(name, str) and isinstance(profile_id, str):
            profiles[name] = profile_id

    for agent_id in REQUIRED_AGENTS:
        require(agent_id in profiles, f"base profile for {agent_id!r} not found under profiles/*.profile.json")

    return profiles


def validate_agent(agent_id: str, profiles: dict[str, str]) -> dict[str, Any]:
    kind = load_adjunct(agent_id, "kind", ".kind.json")
    subjectivity = load_adjunct(agent_id, "subjectivity", ".subjectivity.json")
    office = load_adjunct(agent_id, "office", ".office.json")
    arena = load_adjunct(agent_id, "arena", ".arena_eligibility.json")
    resistance = load_adjunct(agent_id, "resistance", ".resistance_revision.json")

    adjuncts = {
        "kind": kind,
        "subjectivity": subjectivity,
        "office": office,
        "arena": arena,
        "resistance": resistance,
    }

    for label, payload in adjuncts.items():
        require(payload.get("$schema") == SCHEMA_CONSTS[label], f"{agent_id} {label} schema const mismatch")
        require(payload.get("profile_id") == profiles[agent_id], f"{agent_id} {label} profile_id does not match base profile")
        bad_keys = sorted(FORBIDDEN_KEYS.intersection(set(iter_keys(payload))))
        require(not bad_keys, f"{agent_id} {label} contains forbidden protocol/memory keys: {bad_keys}")

    require(kind["kind"] == "agonic", f"{agent_id} must be agonic in Wave I")
    require(kind["evolution_mode"] == "endogenous_under_future_charter", f"{agent_id} has wrong evolution mode")
    require(kind["not_protocol_law"] is True, f"{agent_id} kind adjunct must deny protocol law")

    seats = arena["candidate_seats"]
    require(seats["summon_initiator"] is False, f"{agent_id} cannot be summon initiator in Wave I")
    require(seats["closer"] is False, f"{agent_id} cannot be closer in Wave I")
    require(arena["requires_center_charter"] is True, f"{agent_id} arena eligibility must require center charter")
    require(arena["not_live_authority"] is True, f"{agent_id} arena eligibility must not be live authority")

    offices = office["offices"]
    require(sum(1 for entry in offices if entry.get("primary")) == 1, f"{agent_id} must have exactly one primary office")
    require("summoner" in office["forbidden_offices"], f"{agent_id} must forbid summoner office in Wave I")
    require("closer" in office["forbidden_offices"], f"{agent_id} must forbid closer office in Wave I")

    require(len(subjectivity["beliefs"]) >= 2, f"{agent_id} must have at least two beliefs")
    require(len(subjectivity["operational_affects"]) >= 2, f"{agent_id} must have at least two operational affects")
    require(subjectivity["thought_posture"]["delta_obligation"], f"{agent_id} must declare delta obligation")
    require(resistance["resistance_rights"]["refuse_false_closure"] is True, f"{agent_id} must be able to refuse false closure")
    require(len(resistance["external_boundaries"]) >= 2, f"{agent_id} must name external boundaries")

    return {
        "agent_id": agent_id,
        "contestant": bool(seats["contestant"]),
        "witness": bool(seats["witness"]),
        "chronicler": bool(seats["chronicler"]),
        "judge": bool(seats["judge"]),
    }


def validate_generated_index() -> None:
    expected = formation_builder.build_index(ROOT)
    actual = read_json(ROOT / formation_builder.OUTPUT)
    require(actual == expected, f"{formation_builder.OUTPUT} is stale; rebuild it")


def validate_docs() -> None:
    for filename in [
        "docs/AGONIC_ACTOR_RECHARTERING.md",
        "docs/AGENT_KIND_MODEL.md",
        "docs/AGENT_SUBJECTIVITY_MODEL.md",
        "docs/AGENT_OFFICE_MODEL.md",
        "docs/AGENT_ARENA_ELIGIBILITY_MODEL.md",
        "docs/AGENT_RESISTANCE_REVISION_POSTURE.md",
        "docs/AGON_WAVE1_LANDING.md",
    ]:
        path = ROOT / filename
        require(path.exists(), f"missing doc: {filename}")
        require("Agon" in path.read_text(encoding="utf-8") or "Agent" in path.name, f"{filename} does not look like a Wave I doc")


def main() -> int:
    try:
        validate_schema_files()
        profiles = validate_profile_cross_refs()
        summaries = [validate_agent(agent_id, profiles) for agent_id in REQUIRED_AGENTS]
        validate_generated_index()
        validate_docs()

        require(any(item["contestant"] for item in summaries), "Wave I needs at least one contestant candidate")
        require(any(item["witness"] for item in summaries), "Wave I needs at least one witness candidate")
        require(any(item["judge"] for item in summaries), "Wave I needs at least one judge candidate")
    except (FormationValidationError, formation_builder.FormationBuildError) as exc:
        print(f"[error] {exc}", file=sys.stderr)
        return 1

    print("[ok] validated Agon Wave I agonic actor rechartering surfaces")
    print("[ok] validated no closer or summon initiator authority in Wave I")
    print("[ok] validated generated/agent_agonic_formation_index.min.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
