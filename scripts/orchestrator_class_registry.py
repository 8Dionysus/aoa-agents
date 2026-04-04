from __future__ import annotations

import json
from pathlib import Path

from agent_profile_registry import BuildError, describe_path, read_json

REPO_ROOT = Path(__file__).resolve().parents[1]
ORCHESTRATOR_CLASSES_DIR = REPO_ROOT / "orchestrator_classes"
ORCHESTRATOR_CLASS_SUFFIX = ".class.json"
ORCHESTRATOR_CLASS_ORDER = (
    "router",
    "review",
    "bounded_execution",
)
ORCHESTRATOR_CLASS_CATALOG_PATH = REPO_ROOT / "generated" / "orchestrator_class_catalog.min.json"
ORCHESTRATOR_CLASS_CAPSULES_PATH = REPO_ROOT / "generated" / "orchestrator_class_capsules.json"
ORCHESTRATOR_CLASS_SECTIONS_PATH = REPO_ROOT / "generated" / "orchestrator_class_sections.full.json"

CATALOG_ENTRY_FIELDS = (
    "id",
    "name",
    "status",
    "summary",
    "primary_goal",
    "allowed_owner_layers",
)
CAPSULE_ENTRY_FIELDS = (
    "id",
    "name",
    "status",
    "summary",
    "primary_goal",
    "read_order",
    "required_surfaces",
    "forbidden_surfaces",
    "expected_outputs",
    "verify_refs",
    "boundary_note",
)


def iter_orchestrator_class_paths(
    orchestrator_classes_dir: Path = ORCHESTRATOR_CLASSES_DIR,
) -> list[Path]:
    if not orchestrator_classes_dir.is_dir():
        raise BuildError(f"missing required directory: {describe_path(orchestrator_classes_dir)}")
    paths = sorted(orchestrator_classes_dir.glob(f"*{ORCHESTRATOR_CLASS_SUFFIX}"))
    if not paths:
        raise BuildError(
            f"no source-authored orchestrator classes found in {describe_path(orchestrator_classes_dir)}"
        )
    return paths


def load_orchestrator_classes(
    orchestrator_classes_dir: Path = ORCHESTRATOR_CLASSES_DIR,
) -> list[dict[str, object]]:
    classes: list[dict[str, object]] = []
    order_index = {class_id: index for index, class_id in enumerate(ORCHESTRATOR_CLASS_ORDER)}
    for path in iter_orchestrator_class_paths(orchestrator_classes_dir):
        payload = read_json(path)
        if not isinstance(payload, dict):
            raise BuildError(f"{describe_path(path)} must contain a JSON object")
        expected_id = path.name[: -len(ORCHESTRATOR_CLASS_SUFFIX)]
        actual_id = payload.get("id")
        if not isinstance(actual_id, str):
            raise BuildError(f"{describe_path(path)} must declare a string 'id'")
        if actual_id != expected_id:
            raise BuildError(
                f"{describe_path(path)} id '{actual_id}' must match file stem '{expected_id}'"
            )
        if actual_id not in order_index:
            raise BuildError(
                f"{describe_path(path)} uses unsupported orchestrator class id '{actual_id}'"
            )
        classes.append(payload)
    classes.sort(key=lambda payload: order_index[str(payload.get("id", ""))])
    return classes


def build_orchestrator_class_catalog_payload(
    classes: list[dict[str, object]],
) -> dict[str, object]:
    entries: list[dict[str, object]] = []
    for payload in classes:
        entry: dict[str, object] = {}
        for key in CATALOG_ENTRY_FIELDS:
            if key not in payload:
                raise BuildError(
                    f"source orchestrator class '{payload.get('id', '<unknown>')}' is missing required key '{key}'"
                )
            entry[key] = payload[key]
        class_id = str(payload["id"])
        source_path = f"orchestrator_classes/{class_id}{ORCHESTRATOR_CLASS_SUFFIX}"
        entry["source_path"] = source_path
        entry["inspect_key"] = class_id
        entry["expand_key"] = class_id
        entries.append(entry)
    return {
        "catalog_version": 1,
        "layer": "aoa-agents",
        "family": "orchestrator_classes",
        "orchestrator_classes": entries,
    }


def build_orchestrator_class_capsules_payload(
    classes: list[dict[str, object]],
) -> dict[str, object]:
    entries: list[dict[str, object]] = []
    for payload in classes:
        entry: dict[str, object] = {}
        for key in CAPSULE_ENTRY_FIELDS:
            if key not in payload:
                raise BuildError(
                    f"source orchestrator class '{payload.get('id', '<unknown>')}' is missing required key '{key}'"
                )
            entry[key] = payload[key]
        class_id = str(payload["id"])
        entry["source_path"] = f"orchestrator_classes/{class_id}{ORCHESTRATOR_CLASS_SUFFIX}"
        entries.append(entry)
    return {
        "capsule_version": 1,
        "layer": "aoa-agents",
        "family": "orchestrator_classes",
        "orchestrator_classes": entries,
    }


def _build_section(
    class_id: str,
    *,
    ordinal: int,
    heading: str,
    summary: str,
    body: str,
) -> dict[str, object]:
    section_slug = heading.lower().replace(" ", "-")
    return {
        "section_id": f"{class_id}#{section_slug}",
        "heading": heading,
        "ordinal": ordinal,
        "summary": summary,
        "body": body,
    }


def build_orchestrator_class_sections_payload(
    classes: list[dict[str, object]],
) -> dict[str, object]:
    entries: list[dict[str, object]] = []
    for payload in classes:
        class_id = str(payload["id"])
        source_path = f"orchestrator_classes/{class_id}{ORCHESTRATOR_CLASS_SUFFIX}"
        read_order = payload.get("read_order", [])
        required_surfaces = payload.get("required_surfaces", [])
        forbidden_surfaces = payload.get("forbidden_surfaces", [])
        expected_outputs = payload.get("expected_outputs", [])
        verify_refs = payload.get("verify_refs", [])
        allowed_owner_layers = payload.get("allowed_owner_layers", [])
        sections = [
            _build_section(
                class_id,
                ordinal=1,
                heading="Identity and Boundaries",
                summary="Names the class identity, primary goal, allowed owner layers, and boundary note.",
                body=(
                    f"{payload['name']}. {payload['summary']} "
                    f"Primary goal: {payload['primary_goal']} "
                    f"Allowed owner layers: {', '.join(allowed_owner_layers)}. "
                    f"Boundary note: {payload['boundary_note']}"
                ),
            ),
            _build_section(
                class_id,
                ordinal=2,
                heading="Read Order and Required Surfaces",
                summary="Captures the expected read order and the surfaces this class must ground on first.",
                body=(
                    "Read order: "
                    + " -> ".join(str(item) for item in read_order)
                    + ". Required surfaces: "
                    + "; ".join(str(item) for item in required_surfaces)
                    + "."
                ),
            ),
            _build_section(
                class_id,
                ordinal=3,
                heading="Forbidden Surfaces and Outputs",
                summary="Preserves what this class must not absorb and what outputs it is expected to produce.",
                body=(
                    "Forbidden surfaces: "
                    + "; ".join(str(item) for item in forbidden_surfaces)
                    + ". Expected outputs: "
                    + ", ".join(str(item) for item in expected_outputs)
                    + "."
                ),
            ),
            _build_section(
                class_id,
                ordinal=4,
                heading="Verification and Escalation",
                summary="Lists the verification anchors that keep the class compact and reviewable.",
                body="Verify against: " + "; ".join(str(item) for item in verify_refs) + ".",
            ),
        ]
        entries.append(
            {
                "id": class_id,
                "name": payload["name"],
                "status": payload["status"],
                "source_path": source_path,
                "sections": sections,
            }
        )
    return {
        "sections_version": 1,
        "layer": "aoa-agents",
        "family": "orchestrator_classes",
        "orchestrator_classes": entries,
    }


def write_orchestrator_class_surfaces() -> tuple[dict[str, object], dict[str, object], dict[str, object]]:
    classes = load_orchestrator_classes()
    catalog = build_orchestrator_class_catalog_payload(classes)
    capsules = build_orchestrator_class_capsules_payload(classes)
    sections = build_orchestrator_class_sections_payload(classes)
    ORCHESTRATOR_CLASS_CATALOG_PATH.write_text(json.dumps(catalog, indent=2) + "\n", encoding="utf-8")
    ORCHESTRATOR_CLASS_CAPSULES_PATH.write_text(json.dumps(capsules, indent=2) + "\n", encoding="utf-8")
    ORCHESTRATOR_CLASS_SECTIONS_PATH.write_text(json.dumps(sections, indent=2) + "\n", encoding="utf-8")
    return catalog, capsules, sections
