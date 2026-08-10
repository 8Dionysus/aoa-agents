#!/usr/bin/env python3
"""Resolve an already selected aoa-agents role chain to exact owner refs.

This helper deliberately performs no semantic role selection, model selection,
runtime probing, or activation.  The caller first decides which existing role
can bear an admitted obligation; the resolver only proves that the selected
owner objects form one coherent, clean, content-addressed chain.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
from typing import Any

from jsonschema import Draft202012Validator


SHA256_ZERO = "sha256:" + "0" * 64
SOURCE_SCHEMAS = {
    "base_role": ("schemas/agent-profile.schema.json", "aoa_agent_profile_v1"),
    "specialization": (
        "schemas/role-specialization.schema.json",
        "aoa_role_specialization_v1",
    ),
    "tier": ("schemas/model-tier.schema.json", "aoa_model_tier_v1"),
    "capability_pack": (
        "schemas/capability-pack.schema.json",
        "aoa_capability_pack_v1",
    ),
}


class RoleResolutionError(ValueError):
    """The requested owner chain is absent, ambiguous, dirty, or inconsistent."""


def _load_json(path: Path, *, label: str) -> dict[str, Any]:
    if not path.is_file() or path.is_symlink():
        raise RoleResolutionError(f"{label} is unavailable as a regular file: {path}")
    try:
        payload = json.loads(path.read_bytes())
    except (OSError, json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise RoleResolutionError(f"{label} is not valid JSON: {path}") from exc
    if not isinstance(payload, dict):
        raise RoleResolutionError(f"{label} must be a JSON object: {path}")
    return payload


def _validate_source(root: Path, path: Path, *, kind: str) -> dict[str, Any]:
    schema_ref, _ = SOURCE_SCHEMAS[kind]
    schema = _load_json(root / schema_ref, label=f"{kind} schema")
    payload = _load_json(path, label=kind)
    errors = sorted(
        Draft202012Validator(schema).iter_errors(payload),
        key=lambda item: tuple(str(part) for part in item.absolute_path),
    )
    if errors:
        raise RoleResolutionError(
            f"{kind} does not satisfy {schema_ref}: {errors[0].message}"
        )
    return payload


def _catalog(
    root: Path,
    pattern: str,
    *,
    kind: str,
    identity_field: str,
) -> dict[str, tuple[Path, dict[str, Any]]]:
    records: dict[str, tuple[Path, dict[str, Any]]] = {}
    for path in sorted(root.glob(pattern)):
        payload = _validate_source(root, path, kind=kind)
        identity = payload.get(identity_field)
        if not isinstance(identity, str) or not identity:
            raise RoleResolutionError(f"{kind} has no stable {identity_field}: {path}")
        if identity in records:
            raise RoleResolutionError(f"duplicate {kind} identity: {identity}")
        records[identity] = (path, payload)
    return records


def _git(root: Path, *args: str) -> str:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), *args],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise RoleResolutionError(
            f"cannot verify aoa-agents Git source: {' '.join(args)}"
        ) from exc
    return result.stdout.strip()


def _exact_source_ref(root: Path, selected_paths: tuple[Path, ...]) -> str:
    try:
        top = Path(_git(root, "rev-parse", "--show-toplevel")).resolve(strict=True)
        resolved_root = root.resolve(strict=True)
    except OSError as exc:
        raise RoleResolutionError("aoa-agents owner root is unavailable") from exc
    if top != resolved_root:
        raise RoleResolutionError(
            "--root must name the exact aoa-agents Git worktree root"
        )
    source_ref = _git(root, "rev-parse", "HEAD")
    if re.fullmatch(r"[0-9a-f]{40}", source_ref) is None:
        raise RoleResolutionError("aoa-agents HEAD is not a full SHA-1 source ref")
    relative_paths = [path.relative_to(root).as_posix() for path in selected_paths]
    status = _git(root, "status", "--porcelain=v1", "--", *relative_paths)
    if status:
        raise RoleResolutionError(
            "selected aoa-agents role sources are dirty relative to the owner source ref"
        )
    return source_ref


def _provenance_ref(
    root: Path,
    path: Path,
    *,
    source_ref: str,
    kind: str,
) -> dict[str, str]:
    schema_ref, schema_version = SOURCE_SCHEMAS[kind]
    raw = path.read_bytes()
    return {
        "owner_repo": "aoa-agents",
        "artifact_ref": path.relative_to(root).as_posix(),
        "source_ref": source_ref,
        "artifact_digest": "sha256:" + hashlib.sha256(raw).hexdigest(),
        "schema_ref": schema_ref,
        "schema_version": schema_version,
    }


def _canonical_digest(payload: dict[str, Any]) -> str:
    canonical = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return "sha256:" + hashlib.sha256(canonical).hexdigest()


def assert_resolution_digest(payload: dict[str, Any]) -> None:
    expected = _canonical_digest(payload | {"resolution_digest": SHA256_ZERO})
    if payload.get("resolution_digest") != expected:
        raise RoleResolutionError(
            f"role resolution digest mismatch: expected {expected}"
        )


def resolve_role_binding(
    root: Path,
    *,
    role_id: str,
    tier_id: str,
    specialization_id: str | None = None,
) -> dict[str, Any]:
    """Resolve caller-selected IDs without choosing or ranking them."""

    root = root.resolve(strict=True)
    roles = _catalog(
        root,
        "agents/roles/*/profile.json",
        kind="base_role",
        identity_field="name",
    )
    specializations = _catalog(
        root,
        "agents/roles/*/specializations/*/specialization.json",
        kind="specialization",
        identity_field="id",
    )
    tiers = _catalog(
        root,
        "agents/operating-model/tiers/*.tier.json",
        kind="tier",
        identity_field="id",
    )
    capability_packs = _catalog(
        root,
        "agents/operating-model/capabilities/packs/*.capability.json",
        kind="capability_pack",
        identity_field="id",
    )

    try:
        role_path, role = roles[role_id]
    except KeyError as exc:
        raise RoleResolutionError(f"unknown aoa-agents base role: {role_id}") from exc
    if role.get("status") not in {"active", "experimental"}:
        raise RoleResolutionError(f"base role is not currently usable: {role_id}")
    if tier_id not in role.get("preferred_tier_ids", []):
        raise RoleResolutionError(
            f"tier {tier_id} is not declared by base role {role_id}"
        )
    try:
        tier_path, tier = tiers[tier_id]
    except KeyError as exc:
        raise RoleResolutionError(f"unknown aoa-agents tier: {tier_id}") from exc
    if tier.get("status") not in {"active", "experimental"}:
        raise RoleResolutionError(f"tier is not currently usable: {tier_id}")

    specialization_path: Path | None = None
    capability_path: Path | None = None
    if specialization_id is not None:
        try:
            specialization_path, specialization = specializations[specialization_id]
        except KeyError as exc:
            raise RoleResolutionError(
                f"unknown aoa-agents specialization: {specialization_id}"
            ) from exc
        if specialization.get("status") not in {"active", "experimental"}:
            raise RoleResolutionError(
                f"specialization is not currently usable: {specialization_id}"
            )
        if specialization.get("role_id") != role_id:
            raise RoleResolutionError(
                f"specialization {specialization_id} does not belong to role {role_id}"
            )
        expected_inheritance = role_path.relative_to(root).as_posix()
        if specialization.get("inherits_from") != expected_inheritance:
            raise RoleResolutionError(
                f"specialization {specialization_id} does not inherit exact base role source"
            )
        capability_ref = specialization.get("capability_pack_ref")
        capability_match = next(
            (
                item
                for item in capability_packs.values()
                if item[0].relative_to(root).as_posix() == capability_ref
            ),
            None,
        )
        if capability_match is None:
            raise RoleResolutionError(
                f"specialization {specialization_id} capability pack does not resolve"
            )
        capability_path, capability = capability_match
        if capability.get("status") not in {"active", "experimental"}:
            raise RoleResolutionError(
                f"capability pack is not currently usable: {capability.get('id')}"
            )

    selected_paths = tuple(
        path
        for path in (role_path, specialization_path, tier_path, capability_path)
        if path is not None
    )
    source_ref = _exact_source_ref(root, selected_paths)
    resolution_id_parts = ["role-resolution", role_id]
    if specialization_id is not None:
        resolution_id_parts.append(specialization_id.split(".", 1)[-1])
    resolution_id_parts.append(tier_id)
    payload: dict[str, Any] = {
        "schema_version": "aoa_role_resolution_v1",
        "resolution_id": ":".join(resolution_id_parts),
        "owner_repo": "aoa-agents",
        "owner_source_ref": source_ref,
        "role_id": role_id,
        "base_role_ref": _provenance_ref(
            root, role_path, source_ref=source_ref, kind="base_role"
        ),
        "specialization_id": specialization_id,
        "specialization_ref": (
            None
            if specialization_path is None
            else _provenance_ref(
                root,
                specialization_path,
                source_ref=source_ref,
                kind="specialization",
            )
        ),
        "tier_id": tier_id,
        "tier_ref": _provenance_ref(
            root, tier_path, source_ref=source_ref, kind="tier"
        ),
        "capability_pack_refs": (
            []
            if capability_path is None
            else [
                _provenance_ref(
                    root,
                    capability_path,
                    source_ref=source_ref,
                    kind="capability_pack",
                )
            ]
        ),
        "selection_authority": {
            "semantic_selection_performed": False,
            "model_selection_performed": False,
            "runtime_activation_performed": False,
        },
        "resolution_digest": SHA256_ZERO,
    }
    payload["resolution_digest"] = _canonical_digest(payload)
    schema = _load_json(
        Path(__file__).resolve().parents[1]
        / "references"
        / "role-resolution-v1.schema.json",
        label="role resolution schema",
    )
    errors = list(Draft202012Validator(schema).iter_errors(payload))
    if errors:
        raise RoleResolutionError(
            f"resolved role chain violates its output schema: {errors[0].message}"
        )
    assert_resolution_digest(payload)
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Resolve an already selected aoa-agents role chain to exact refs."
    )
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--role-id", required=True)
    parser.add_argument("--specialization-id")
    parser.add_argument("--tier-id", required=True)
    args = parser.parse_args()
    try:
        result = resolve_role_binding(
            args.root,
            role_id=args.role_id,
            specialization_id=args.specialization_id,
            tier_id=args.tier_id,
        )
    except RoleResolutionError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2, sort_keys=True)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
