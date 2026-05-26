#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[5]
REFRESH_LAW_PART = Path("mechanics/codex-projection/parts/refresh-law")
EXAMPLE_DIR = REFRESH_LAW_PART / "examples"
EXAMPLE_NAME = "subagent-refresh-law.example.json"

ALLOWED_ROUTE_CLASSES = {
    "observe",
    "revalidate",
    "rebuild",
    "reexport",
    "regenerate",
    "reproject",
    "repair",
    "defer",
}
FORMER_ROOT_PATHS = {
    Path("examples") / ("subagent" + "_projection_refresh_law.example.json"),
    Path("scripts") / "validate_codex_refresh_law_contracts.py",
}


class CodexRefreshLawContractsValidationError(RuntimeError):
    pass


def _read_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise CodexRefreshLawContractsValidationError(f"missing required file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise CodexRefreshLawContractsValidationError(f"invalid JSON in {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise CodexRefreshLawContractsValidationError(f"{path} must contain a JSON object")
    return payload


def _resolve_pattern(root: Path, pattern: str) -> list[Path]:
    return list(root.glob(pattern))


def collect_codex_refresh_law_contract_errors(root: Path = ROOT) -> list[str]:
    root = root.resolve()
    errors: list[str] = []

    for former_path in sorted(FORMER_ROOT_PATHS):
        former_path = root / former_path
        if former_path.exists():
            errors.append(f"former root Codex refresh-law path is still active: {former_path.relative_to(root).as_posix()}")

    actual_examples = {path.name for path in (root / EXAMPLE_DIR).glob("*.json")}
    if actual_examples != {EXAMPLE_NAME}:
        missing = sorted({EXAMPLE_NAME} - actual_examples)
        extra = sorted(actual_examples - {EXAMPLE_NAME})
        details: list[str] = []
        if missing:
            details.append("missing: " + ", ".join(missing))
        if extra:
            details.append("unexpected: " + ", ".join(extra))
        errors.append("Codex refresh-law example file set drifted (" + "; ".join(details) + ")")

    example_path = root / EXAMPLE_DIR / EXAMPLE_NAME
    try:
        payload = _read_json(example_path)
    except CodexRefreshLawContractsValidationError as exc:
        errors.append(str(exc))
        return errors

    expected_scalars = {
        "schema_version": "aoa_component_refresh_law_v1",
        "component_ref": "component:codex-subagents:projection",
        "owner_repo": "aoa-agents",
        "followthrough_home": "aoa-playbooks:component-refresh-cycle",
    }
    for key, expected in expected_scalars.items():
        if payload.get(key) != expected:
            errors.append(f"{EXAMPLE_NAME} must keep {key}={expected!r}")

    for key in (
        "source_authored_inputs",
        "generated_surfaces",
        "projected_or_installed_surfaces",
        "drift_signals",
        "proof_commands",
        "rollback_anchors",
    ):
        if not payload.get(key):
            errors.append(f"{EXAMPLE_NAME} must keep non-empty {key}")

    for pattern in payload.get("source_authored_inputs", []):
        if isinstance(pattern, str) and not _resolve_pattern(root, pattern):
            errors.append(f"source pattern has no matches: {pattern}")

    for pattern in payload.get("generated_surfaces", []):
        if isinstance(pattern, str) and not _resolve_pattern(root, pattern):
            errors.append(f"generated pattern has no matches: {pattern}")

    refresh_window = payload.get("refresh_window")
    if not isinstance(refresh_window, dict):
        errors.append(f"{EXAMPLE_NAME} must keep refresh_window object")
    else:
        expected_window = {"stale_after_days": 7, "repeat_trigger_threshold": 2, "open_window_days": 5}
        for key, expected in expected_window.items():
            if refresh_window.get(key) != expected:
                errors.append(f"{EXAMPLE_NAME} must keep refresh_window.{key}={expected!r}")

    routes = payload.get("refresh_routes")
    if not isinstance(routes, dict):
        errors.append(f"{EXAMPLE_NAME} must keep refresh_routes object")
    else:
        execute = routes.get("execute", [])
        validate = routes.get("validate", [])
        if "python scripts/build_published_surfaces.py" not in execute:
            errors.append(f"{EXAMPLE_NAME} must route execute through build_published_surfaces.py")
        if "python mechanics/codex-projection/parts/subagent-projection/scripts/build_codex_subagents_v2.py" not in execute:
            errors.append(f"{EXAMPLE_NAME} must route execute through build_codex_subagents_v2.py")
        if "python -m pytest -q tests" not in validate:
            errors.append(f"{EXAMPLE_NAME} must keep tests in validate route")

    for idx, signal in enumerate(payload.get("drift_signals", [])):
        if not isinstance(signal, dict):
            errors.append(f"{EXAMPLE_NAME} drift_signals[{idx}] must be an object")
            continue
        route_class = signal.get("recommended_route_class")
        if route_class not in ALLOWED_ROUTE_CLASSES:
            errors.append(f"{EXAMPLE_NAME} drift_signals[{idx}] has invalid route class: {route_class!r}")

    for anchor in payload.get("rollback_anchors", []):
        if isinstance(anchor, str) and not (root / anchor).exists():
            errors.append(f"missing rollback anchor: {anchor}")

    return errors


def validate_codex_refresh_law_contracts(root: Path = ROOT) -> None:
    errors = collect_codex_refresh_law_contract_errors(root)
    if errors:
        raise CodexRefreshLawContractsValidationError("\n".join(errors))


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Codex refresh-law part-local example.")
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    try:
        validate_codex_refresh_law_contracts(args.root.resolve())
    except CodexRefreshLawContractsValidationError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print("Codex refresh-law contract validation passed. examples=1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
