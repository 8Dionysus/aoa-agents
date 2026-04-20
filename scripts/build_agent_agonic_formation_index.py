#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

SOURCE_DIRS = {
    "kind": Path("profiles/adjuncts/kind"),
    "subjectivity": Path("profiles/adjuncts/subjectivity"),
    "office": Path("profiles/adjuncts/office_overlay"),
    "arena": Path("profiles/adjuncts/arena_eligibility"),
    "resistance": Path("profiles/adjuncts/resistance_revision"),
}

REQUIRED_AGENTS = ["architect", "coder", "reviewer", "evaluator", "memory-keeper"]
OUTPUT = Path("generated/agent_agonic_formation_index.min.json")


class FormationBuildError(RuntimeError):
    pass


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise FormationBuildError(f"missing required file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise FormationBuildError(f"invalid JSON in {path}: {exc}") from exc


def write_compact_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )


def collect_by_agent(root: Path, rel_dir: Path, suffix: str) -> dict[str, Any]:
    directory = root / rel_dir
    if not directory.exists():
        raise FormationBuildError(f"missing source directory: {rel_dir}")

    records: dict[str, Any] = {}
    for path in sorted(directory.glob(f"*{suffix}")):
        payload = read_json(path)
        agent_id = payload.get("agent_id")
        if not isinstance(agent_id, str):
            raise FormationBuildError(f"{path} does not contain string agent_id")
        if agent_id in records:
            raise FormationBuildError(f"duplicate agent_id {agent_id!r} in {rel_dir}")
        if path.name.split(".")[0] != agent_id:
            raise FormationBuildError(f"{path} file stem does not match agent_id {agent_id!r}")
        records[agent_id] = payload
    return records


def build_index(root: Path = ROOT) -> dict[str, Any]:
    kind = collect_by_agent(root, SOURCE_DIRS["kind"], ".kind.json")
    subjectivity = collect_by_agent(root, SOURCE_DIRS["subjectivity"], ".subjectivity.json")
    office = collect_by_agent(root, SOURCE_DIRS["office"], ".office.json")
    arena = collect_by_agent(root, SOURCE_DIRS["arena"], ".arena_eligibility.json")
    resistance = collect_by_agent(root, SOURCE_DIRS["resistance"], ".resistance_revision.json")

    required = set(REQUIRED_AGENTS)
    seen_sets = {
        "kind": set(kind),
        "subjectivity": set(subjectivity),
        "office": set(office),
        "arena": set(arena),
        "resistance": set(resistance),
    }

    for label, seen in seen_sets.items():
        missing = sorted(required - seen)
        if missing:
            raise FormationBuildError(f"{label} adjuncts missing required agents: {missing}")

    for label, seen in seen_sets.items():
        extras = sorted(seen - required)
        if extras:
            raise FormationBuildError(f"{label} adjuncts contain non-Wave-I agents: {extras}")

    actors = []
    for agent_id in REQUIRED_AGENTS:
        kind_item = kind[agent_id]
        subj_item = subjectivity[agent_id]
        office_item = office[agent_id]
        arena_item = arena[agent_id]
        resistance_item = resistance[agent_id]

        profile_ids = {
            kind_item.get("profile_id"),
            subj_item.get("profile_id"),
            office_item.get("profile_id"),
            arena_item.get("profile_id"),
            resistance_item.get("profile_id"),
        }
        if len(profile_ids) != 1:
            raise FormationBuildError(f"profile_id mismatch across adjuncts for {agent_id}: {sorted(profile_ids)}")

        offices = [entry["office_id"] for entry in office_item["offices"]]
        primary = [entry["office_id"] for entry in office_item["offices"] if entry.get("primary")]
        if len(primary) != 1:
            raise FormationBuildError(f"{agent_id} must have exactly one primary office")

        seats = arena_item["candidate_seats"]
        active_seats = sorted([seat for seat, enabled in seats.items() if enabled])

        actors.append(
            {
                "agent_id": agent_id,
                "profile_id": profile_ids.pop(),
                "kind": kind_item["kind"],
                "evolution_mode": kind_item["evolution_mode"],
                "primary_office": primary[0],
                "offices": offices,
                "candidate_seats": active_seats,
                "forbidden_seats": arena_item["forbidden_seats"],
                "readiness": {
                    "agonic_actor_ready": True,
                    "contestant_candidate": bool(seats["contestant"]),
                    "witness_candidate": bool(seats["witness"]),
                    "chronicler_candidate": bool(seats["chronicler"]),
                    "judge_candidate": bool(seats["judge"]),
                    "summon_initiator_candidate": bool(seats["summon_initiator"]),
                    "closer_candidate": bool(seats["closer"]),
                },
                "doctrine_seed": subj_item["doctrine_seed"]["statement"],
                "resistance_rights": resistance_item["resistance_rights"],
                "external_boundaries": resistance_item["external_boundaries"],
            }
        )

    summary = {
        "actor_count": len(actors),
        "contestant_candidates": sum(1 for actor in actors if actor["readiness"]["contestant_candidate"]),
        "witness_candidates": sum(1 for actor in actors if actor["readiness"]["witness_candidate"]),
        "chronicler_candidates": sum(1 for actor in actors if actor["readiness"]["chronicler_candidate"]),
        "judge_candidates": sum(1 for actor in actors if actor["readiness"]["judge_candidate"]),
        "summon_initiator_candidates": sum(1 for actor in actors if actor["readiness"]["summon_initiator_candidate"]),
        "closer_candidates": sum(1 for actor in actors if actor["readiness"]["closer_candidate"]),
    }

    return {
        "$schema": "https://aoa-agents/generated/agent_agonic_formation_index.v1.json",
        "formation": "Agon Wave I / Agonic Actor Rechartering",
        "generated_by": "scripts/build_agent_agonic_formation_index.py",
        "source_surfaces": [
            "profiles/adjuncts/kind/*.kind.json",
            "profiles/adjuncts/subjectivity/*.subjectivity.json",
            "profiles/adjuncts/office_overlay/*.office.json",
            "profiles/adjuncts/arena_eligibility/*.arena_eligibility.json",
            "profiles/adjuncts/resistance_revision/*.resistance_revision.json",
        ],
        "readiness_summary": summary,
        "actors": actors,
        "stop_lines": [
            "This index is not an arena protocol.",
            "This index is not a scar ledger.",
            "This index is not a verdict surface.",
            "This index is not a Codex subagent projection source by default.",
        ],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build the Agon Wave I agonic formation index.")
    parser.add_argument("--check", action="store_true", help="Verify generated index is current without rewriting it.")
    args = parser.parse_args(argv)

    try:
        payload = build_index(ROOT)
        output_path = ROOT / OUTPUT
        if args.check:
            current = read_json(output_path)
            if current != payload:
                raise FormationBuildError(
                    f"{OUTPUT} is stale. Run python scripts/build_agent_agonic_formation_index.py"
                )
            print(f"[ok] {OUTPUT} is current")
        else:
            write_compact_json(output_path, payload)
            print(f"[ok] wrote {OUTPUT}")
    except FormationBuildError as exc:
        print(f"[error] {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
