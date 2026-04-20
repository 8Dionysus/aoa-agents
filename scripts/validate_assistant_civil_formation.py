#!/usr/bin/env python3
"""Validate assistant civil formation surfaces.

This validator checks the Agon Wave II invariants without importing jsonschema.
It is deliberately strict about assistant anti-drift law.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any


EXPECTED_BASE_ROLES = ["architect", "coder", "reviewer", "evaluator", "memory-keeper"]
REQUIRED_FAMILIES = {
    "assistant_variant": ".variant",
    "assistant_service_identity": ".identity",
    "assistant_service_contract": ".contract",
    "assistant_service_governance": ".governance",
    "assistant_service_certification": ".certification",
    "assistant_arena_exclusion": ".arena_exclusion",
}
FORBIDDEN_KEYS = {
    "scar_ledger",
    "battle_history",
    "verdict_logic",
    "runtime_packets",
    "tos_promotion",
    "retention_checks",
    "durable_incident_log",
    "durable_revision_log",
}


def repo_root_from_script() -> Path:
    return Path(__file__).resolve().parents[1]


def load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise SystemExit(f"missing file: {path}")
    except json.JSONDecodeError as exc:
        raise SystemExit(f"invalid json: {path}: {exc}")


def fail(message: str) -> None:
    raise SystemExit(message)


def read_family(root: Path, family: str, suffix: str) -> dict[str, dict[str, Any]]:
    path = root / "profiles" / "adjuncts" / family
    if not path.exists():
        fail(f"missing adjunct family: {path}")
    out: dict[str, dict[str, Any]] = {}
    for file in sorted(path.glob(f"*{suffix}.json")):
        data = load_json(file)
        variant_id = data.get("variant_id")
        if not isinstance(variant_id, str):
            fail(f"{file} missing string variant_id")
        out[variant_id] = data
    if not out:
        fail(f"empty adjunct family: {path}")
    return out


def assert_no_forbidden_keys(data: Any, path: str) -> None:
    if isinstance(data, dict):
        for key, value in data.items():
            if key in FORBIDDEN_KEYS:
                fail(f"forbidden key {key!r} at {path}")
            assert_no_forbidden_keys(value, f"{path}.{key}")
    elif isinstance(data, list):
        for idx, value in enumerate(data):
            assert_no_forbidden_keys(value, f"{path}[{idx}]")


def import_builder(root: Path):
    builder_path = root / "scripts" / "build_assistant_civil_formation_index.py"
    spec = importlib.util.spec_from_file_location("assistant_civil_builder", builder_path)
    if spec is None or spec.loader is None:
        fail(f"cannot import builder: {builder_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate(root: Path) -> None:
    for role in EXPECTED_BASE_ROLES:
        profile = root / "profiles" / f"{role}.profile.json"
        if not profile.exists():
            fail(f"missing base profile expected by Wave II: {profile}")

    families = {
        name: read_family(root, name, suffix)
        for name, suffix in REQUIRED_FAMILIES.items()
    }

    expected_variant_ids = {f"{role}.assistant" for role in EXPECTED_BASE_ROLES}
    got_variant_ids = set(families["assistant_variant"])
    if got_variant_ids != expected_variant_ids:
        fail(
            "assistant variant set mismatch: "
            f"expected={sorted(expected_variant_ids)} got={sorted(got_variant_ids)}"
        )

    for family_name, family in families.items():
        if set(family) != expected_variant_ids:
            fail(f"{family_name} variant mismatch")

    for variant_id in sorted(expected_variant_ids):
        base_role = variant_id.removesuffix(".assistant")

        variant = families["assistant_variant"][variant_id]
        identity = families["assistant_service_identity"][variant_id]
        contract = families["assistant_service_contract"][variant_id]
        governance = families["assistant_service_governance"][variant_id]
        certification = families["assistant_service_certification"][variant_id]
        exclusion = families["assistant_arena_exclusion"][variant_id]

        all_docs = [variant, identity, contract, governance, certification, exclusion]
        for doc in all_docs:
            assert_no_forbidden_keys(doc, variant_id)

        if variant.get("kind") != "assistant":
            fail(f"{variant_id}: kind must be assistant")
        if variant.get("evolution_mode") != "exogenous_reactive":
            fail(f"{variant_id}: evolution_mode must be exogenous_reactive")
        if variant.get("base_role_id") != base_role:
            fail(f"{variant_id}: base_role_id must be {base_role}")
        anchoring = variant.get("anchoring", {})
        if anchoring.get("does_not_create_public_role") is not True:
            fail(f"{variant_id}: assistant must not create public role")
        if anchoring.get("does_not_override_base_profile") is not True:
            fail(f"{variant_id}: assistant must not override base profile")
        if anchoring.get("profile_path") != f"profiles/{base_role}.profile.json":
            fail(f"{variant_id}: wrong profile_path")

        arena_status = variant.get("arena_status", {})
        for key in [
            "contestant_eligible",
            "judge_eligible",
            "closer_eligible",
            "summon_initiator_eligible",
        ]:
            if arena_status.get(key) is not False:
                fail(f"{variant_id}: arena_status.{key} must be false")
        if not arena_status.get("service_seats_allowed"):
            fail(f"{variant_id}: must name allowed service seats")

        if identity.get("operational_affects") and any(
            not (0 <= value <= 1)
            for value in identity["operational_affects"].values()
        ):
            fail(f"{variant_id}: operational affect outside 0..1")

        receipts = contract.get("receipts", {})
        if receipts.get("required") is not True:
            fail(f"{variant_id}: receipts.required must be true")
        if "escalation_decision" not in receipts.get("must_include", []):
            fail(f"{variant_id}: receipt must include escalation_decision")
        if not contract.get("escalation_rules"):
            fail(f"{variant_id}: escalation_rules required")

        if governance.get("self_revision_allowed") is not False:
            fail(f"{variant_id}: self_revision_allowed must be false")
        if governance.get("persistent_policy_change_allowed") is not False:
            fail(f"{variant_id}: persistent_policy_change_allowed must be false")
        if governance.get("versioning") != "release_governed":
            fail(f"{variant_id}: versioning must be release_governed")
        if governance.get("rollback_required") is not True:
            fail(f"{variant_id}: rollback_required must be true")
        memory_boundary = governance.get("memory_boundary", {})
        if memory_boundary.get("stores_durable_memory_here") is not False:
            fail(f"{variant_id}: must not store durable memory here")

        if certification.get("certification_required") is not True:
            fail(f"{variant_id}: certification_required must be true")
        for required_profile in ["boundary_discipline", "receipt_fidelity", "arena_exclusion"]:
            if required_profile not in certification.get("certification_profiles", []):
                fail(f"{variant_id}: missing certification profile {required_profile}")

        for key in [
            "contestant_eligible",
            "judge_eligible",
            "summon_initiator_eligible",
            "closer_eligible",
            "scar_writer_eligible",
            "tos_promotion_eligible",
        ]:
            if exclusion.get(key) is not False:
                fail(f"{variant_id}: exclusion.{key} must be false")
        if exclusion.get("agonic_recharter_required") is not True:
            fail(f"{variant_id}: agonic_recharter_required must be true")
        for prohibited in ["issue_verdict", "write_scar", "grant_closure", "promote_to_ToS"]:
            if prohibited not in exclusion.get("prohibited_moves", []):
                fail(f"{variant_id}: missing prohibited move {prohibited}")

    builder = import_builder(root)
    built = builder.build_index(root)
    generated_path = root / "generated" / "assistant_civil_formation_index.min.json"
    generated = load_json(generated_path)
    if built != generated:
        fail(f"generated index drift: {generated_path}")

    print("ok: assistant civil formation validates")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=repo_root_from_script())
    args = parser.parse_args(argv)

    validate(args.root.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
