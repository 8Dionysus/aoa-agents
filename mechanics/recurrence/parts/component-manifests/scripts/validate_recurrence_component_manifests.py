#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shlex
import sys
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[5]
MANIFEST_ROOT = ROOT / "mechanics" / "recurrence" / "parts" / "component-manifests" / "manifests"
COMPONENTS_DIR = MANIFEST_ROOT / "components"
HOOKS_DIR = MANIFEST_ROOT / "hooks"

EXPECTED_COMPONENT_FILES = {
    "agon-actor-formation-surfaces.json",
    "agon-epistemic-actor-posture.json",
    "agon-rank-jurisdiction-surfaces.json",
    "agon-school-campaign-posture.json",
    "codex-subagent-projection.json",
    "recursor-codex-projection-candidates.json",
    "recursor-readiness.json",
}
EXPECTED_HOOK_FILES = {
    "agon-actor-formation-surfaces.json",
    "agon-epistemic-actor-posture.json",
    "agon-rank-jurisdiction-surfaces.json",
    "agon-school-campaign-posture.json",
}
PATH_FIELD_SUFFIXES = (
    "_surfaces",
    "_inputs",
    "_anchors",
    "_targets",
    "_globs",
)
PATH_FIELD_NAMES = {
    "path_globs",
    "rollback_anchors",
    "candidate_targets",
    "documentation_surfaces",
    "decision_surfaces",
    "observes",
    "source",
    "surfaces",
}
REPO_PATH_PREFIXES = (
    "agents/",
    "generated/",
    "mechanics/",
    "schemas/",
    "examples/",
    "scripts/",
    "quests/",
)
FORMER_ROOT_PATHS = {
    Path("scripts") / "validate_recurrence_component_manifests.py",
    Path("tests") / "test_recurrence_component_manifests.py",
}
OLD_ACTIVE_NAMESPACE_FRAGMENTS = tuple(
    "".join(parts)
    for parts in (
        ("component", ".agents."),
        ("component", ".agon."),
        ("component", ".codex-subagents."),
    )
)
OLD_ACTIVE_PREFIXES = tuple(
    "".join(parts)
    for parts in (
        ("component:agon", "."),
        ("hooks:agon", "."),
    )
)


class ManifestValidationError(RuntimeError):
    pass


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ManifestValidationError(f"missing manifest: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ManifestValidationError(f"invalid JSON in {path}: {exc}") from exc


def describe(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return str(path)


def iter_manifest_files(root: Path) -> tuple[list[Path], list[Path]]:
    components = sorted((root / COMPONENTS_DIR.relative_to(ROOT)).glob("*.json"))
    hooks = sorted((root / HOOKS_DIR.relative_to(ROOT)).glob("*.json"))
    return components, hooks


def collect_strings(value: Any) -> Iterable[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, list):
        for item in value:
            yield from collect_strings(item)
    elif isinstance(value, dict):
        for item in value.values():
            yield from collect_strings(item)


def collect_field_strings(value: Any, *, field_name: str | None = None) -> Iterable[tuple[str, str]]:
    if isinstance(value, dict):
        for key, item in value.items():
            yield from collect_field_strings(item, field_name=str(key))
    elif isinstance(value, list):
        for item in value:
            yield from collect_field_strings(item, field_name=field_name)
    elif isinstance(value, str) and field_name is not None:
        yield field_name, value


def is_path_field(field_name: str) -> bool:
    return field_name in PATH_FIELD_NAMES or field_name.endswith(PATH_FIELD_SUFFIXES)


def is_repo_path(value: str) -> bool:
    return value.startswith(REPO_PATH_PREFIXES)


def validate_command(value: str, *, root: Path, label: str, errors: list[str]) -> None:
    try:
        parts = shlex.split(value)
    except ValueError as exc:
        errors.append(f"{label}: invalid command string {value!r}: {exc}")
        return
    if len(parts) < 2 or parts[0] != "python":
        return
    script = parts[1]
    if script.startswith("scripts/") and not (root / script).is_file():
        errors.append(f"{label}: command references missing script {script}")


def validate_repo_path(value: str, *, root: Path, label: str, errors: list[str]) -> None:
    if value.startswith("docs/"):
        errors.append(f"{label}: manifest still references root docs path {value!r}")
        return
    if value.startswith("manifests/"):
        errors.append(f"{label}: manifest still references former root manifest path {value!r}")
        return
    if not is_repo_path(value):
        return
    if "*" in value:
        matches = list(root.glob(value))
        if not matches:
            errors.append(f"{label}: glob does not match any files: {value}")
        return
    path = root / value
    if not path.exists():
        errors.append(f"{label}: path does not exist: {value}")


def validate_active_payload_text(value: str, *, label: str, errors: list[str]) -> None:
    if "wave16" in value and "aoa_" + "agents" in value:
        errors.append(f"{label}: old wave16 component name remains in active payload")
    if any(fragment in value for fragment in OLD_ACTIVE_NAMESPACE_FRAGMENTS):
        errors.append(f"{label}: old dot-scoped component namespace remains in active payload")
    if value.startswith(OLD_ACTIVE_PREFIXES):
        errors.append(f"{label}: old dot-scoped active manifest id remains in active payload")


def collect_manifest_errors(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    for former_path in sorted(FORMER_ROOT_PATHS):
        if (root / former_path).exists():
            errors.append(f"former root path is still active: {former_path.as_posix()}")

    components, hooks = iter_manifest_files(root)

    component_names = {path.name for path in components}
    hook_names = {path.name for path in hooks}
    if component_names != EXPECTED_COMPONENT_FILES:
        errors.append(
            "component manifest file set mismatch: "
            f"expected={sorted(EXPECTED_COMPONENT_FILES)} actual={sorted(component_names)}"
        )
    if hook_names != EXPECTED_HOOK_FILES:
        errors.append(
            "hook manifest file set mismatch: "
            f"expected={sorted(EXPECTED_HOOK_FILES)} actual={sorted(hook_names)}"
        )

    component_refs: set[str] = set()
    payloads: list[tuple[Path, dict[str, Any], str]] = []
    for path in components:
        payload = read_json(path)
        if not isinstance(payload, dict):
            errors.append(f"{describe(path, root)}: component manifest must be a JSON object")
            continue
        ref = payload.get("component_ref") or payload.get("component_id")
        if not isinstance(ref, str) or not ref:
            errors.append(f"{describe(path, root)}: component manifest missing component_ref/component_id")
        else:
            if ref in component_refs:
                errors.append(f"{describe(path, root)}: duplicate component ref {ref}")
            component_refs.add(ref)
        payloads.append((path, payload, "component"))

    for path in hooks:
        payload = read_json(path)
        if not isinstance(payload, dict):
            errors.append(f"{describe(path, root)}: hook manifest must be a JSON object")
            continue
        observed = payload.get("component_ref") or payload.get("observes_component") or payload.get("component_id")
        if not isinstance(observed, str) or not observed:
            errors.append(f"{describe(path, root)}: hook manifest missing observed component ref")
        elif observed not in component_refs:
            errors.append(f"{describe(path, root)}: hook observes unknown component {observed}")
        payloads.append((path, payload, "hook"))

    for path, payload, kind in payloads:
        label = f"{kind} {describe(path, root)}"
        owner = payload.get("owner_repo")
        if owner is not None and owner != "aoa-agents":
            errors.append(f"{label}: owner_repo must be aoa-agents when present")
        for text in collect_strings(payload):
            validate_active_payload_text(text, label=label, errors=errors)
        for field_name, value in collect_field_strings(payload):
            if value.startswith("python ") and field_name in {"commands", "proof_surfaces"}:
                validate_command(value, root=root, label=label, errors=errors)
            if is_path_field(field_name):
                validate_repo_path(value, root=root, label=label, errors=errors)
    return errors


def validate_recurrence_component_manifests(root: Path = ROOT) -> None:
    errors = collect_manifest_errors(root)
    if errors:
        raise ManifestValidationError("\n".join(errors))


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate recurrence component manifests.")
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    root = args.root.resolve()
    try:
        validate_recurrence_component_manifests(root)
    except ManifestValidationError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    components, hooks = iter_manifest_files(root)
    print(f"recurrence component manifests: pass components={len(components)} hooks={len(hooks)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
