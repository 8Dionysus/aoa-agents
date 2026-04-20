#!/usr/bin/env python3
"""Build the compact assistant civil formation index.

This script is intentionally stdlib-only. It reads source-authored assistant
adjuncts and writes `generated/assistant_civil_formation_index.min.json`.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT_MARKERS = ("profiles", "schemas", "generated")


def repo_root_from_script() -> Path:
    return Path(__file__).resolve().parents[1]


def load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise SystemExit(f"missing file: {path}")
    except json.JSONDecodeError as exc:
        raise SystemExit(f"invalid json: {path}: {exc}")


def compact_json(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"


def read_family(root: Path, family: str, suffix: str) -> dict[str, dict[str, Any]]:
    family_dir = root / "profiles" / "adjuncts" / family
    if not family_dir.exists():
        raise SystemExit(f"missing assistant adjunct family: {family_dir}")

    out: dict[str, dict[str, Any]] = {}
    for path in sorted(family_dir.glob(f"*{suffix}.json")):
        data = load_json(path)
        variant_id = data.get("variant_id")
        if not isinstance(variant_id, str):
            raise SystemExit(f"{path} is missing string variant_id")
        if variant_id in out:
            raise SystemExit(f"duplicate variant_id {variant_id} in {family}")
        out[variant_id] = data

    if not out:
        raise SystemExit(f"no assistant adjunct files found in {family_dir}")
    return out


def build_index(root: Path) -> dict[str, Any]:
    variants = read_family(root, "assistant_variant", ".variant")
    identities = read_family(root, "assistant_service_identity", ".identity")
    contracts = read_family(root, "assistant_service_contract", ".contract")
    governance = read_family(root, "assistant_service_governance", ".governance")
    certifications = read_family(root, "assistant_service_certification", ".certification")
    exclusions = read_family(root, "assistant_arena_exclusion", ".arena_exclusion")

    expected = set(variants)
    families = {
        "assistant_service_identity": identities,
        "assistant_service_contract": contracts,
        "assistant_service_governance": governance,
        "assistant_service_certification": certifications,
        "assistant_arena_exclusion": exclusions,
    }

    for family_name, family_data in families.items():
        got = set(family_data)
        if got != expected:
            missing = sorted(expected - got)
            extra = sorted(got - expected)
            raise SystemExit(
                f"variant mismatch for {family_name}: missing={missing} extra={extra}"
            )

    records: list[dict[str, Any]] = []
    for variant_id in sorted(expected):
        variant = variants[variant_id]
        identity = identities[variant_id]
        contract = contracts[variant_id]
        gov = governance[variant_id]
        cert = certifications[variant_id]
        exclusion = exclusions[variant_id]

        records.append(
            {
                "variant_id": variant_id,
                "base_role_id": variant["base_role_id"],
                "kind": variant["kind"],
                "evolution_mode": variant["evolution_mode"],
                "service_office": variant["service_office"],
                "profile_path": variant["anchoring"]["profile_path"],
                "service_promise": identity["service_promise"],
                "mandate": contract["mandate"],
                "receipts_required": contract["receipts"]["required"],
                "revision_authority": gov["revision_authority"],
                "self_revision_allowed": gov["self_revision_allowed"],
                "persistent_policy_change_allowed": gov["persistent_policy_change_allowed"],
                "certification_required": cert["certification_required"],
                "contestant_eligible": exclusion["contestant_eligible"],
                "judge_eligible": exclusion["judge_eligible"],
                "closer_eligible": exclusion["closer_eligible"],
                "summon_initiator_eligible": exclusion["summon_initiator_eligible"],
                "scar_writer_eligible": exclusion["scar_writer_eligible"],
                "tos_promotion_eligible": exclusion["tos_promotion_eligible"],
                "agonic_recharter_required": exclusion["agonic_recharter_required"],
                "service_seats_allowed": variant["arena_status"]["service_seats_allowed"],
                "escalation_triggers": exclusion["escalation_triggers"],
            }
        )

    return {
        "schema_version": "assistant_civil_formation_index_v1",
        "owner_repo": "aoa-agents",
        "wave": "agon_wave2_assistant_civil_rechartering",
        "source_families": [
            "profiles/adjuncts/assistant_variant",
            "profiles/adjuncts/assistant_service_identity",
            "profiles/adjuncts/assistant_service_contract",
            "profiles/adjuncts/assistant_service_governance",
            "profiles/adjuncts/assistant_service_certification",
            "profiles/adjuncts/assistant_arena_exclusion",
        ],
        "invariants": [
            "assistant_variants_do_not_create_public_roles",
            "assistant_variants_do_not_override_base_profiles",
            "assistant_variants_are_not_contestants",
            "assistant_variants_are_externally_revised",
            "assistant_variants_require_receipts",
            "assistant_variants_require_certification",
            "assistant_variants_escalate_to_agonic_review_when_boundary_is_hit",
            "assistant_variants_do_not_store_durable_memory_or_scar_ledgers_here",
        ],
        "count": len(records),
        "variants": records,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=repo_root_from_script())
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)

    root = args.root.resolve()
    data = build_index(root)
    output = root / "generated" / "assistant_civil_formation_index.min.json"
    rendered = compact_json(data)

    if args.check:
        if not output.exists():
            print(f"missing generated index: {output}", file=sys.stderr)
            return 1
        existing = output.read_text(encoding="utf-8")
        if existing != rendered:
            print(f"generated index drift: {output}", file=sys.stderr)
            return 1
        print(f"ok: {output}")
        return 0

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(rendered, encoding="utf-8")
    print(f"wrote {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
