#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


REPO_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = REPO_ROOT / "agents" / "source_home.manifest.json"
SCHEMA_PATH = REPO_ROOT / "schemas" / "agent-source-home.schema.json"

EXPECTED_FAMILY_IDS = {
    "base_profiles",
    "profile_adjuncts",
    "role_specializations",
    "capability_packs",
    "model_tiers",
    "orchestrator_classes",
    "cohort_patterns",
    "runtime_seam_bindings",
}
EXPECTED_BRANCH_IDS = {
    "role_houses",
    "operating_model",
}
EXPECTED_DIRECT_DIRS = {
    "roles",
    "operating-model",
}
FORBIDDEN_DIRECT_DIRS = {
    "profiles",
    "model_tiers",
    "orchestrator_classes",
    "cohort_patterns",
    "runtime_seam",
}


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def display(path: Path, repo_root: Path) -> str:
    try:
        return path.relative_to(repo_root).as_posix()
    except ValueError:
        return path.as_posix()


def validate_schema(manifest: dict[str, Any], schema: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    Draft202012Validator.check_schema(schema)
    errors = sorted(
        Draft202012Validator(schema).iter_errors(manifest),
        key=lambda error: (list(error.absolute_path), error.message),
    )
    for error in errors:
        location = ".".join(str(part) for part in error.absolute_path)
        if location:
            issues.append(f"manifest schema violation at {location}: {error.message}")
        else:
            issues.append(f"manifest schema violation: {error.message}")
    return issues


def require_existing_file(repo_root: Path, rel: str, context: str, issues: list[str]) -> None:
    path = repo_root / rel
    if not path.is_file():
        issues.append(f"{context}: missing file {rel}")


def require_existing_dir(repo_root: Path, rel: str, context: str, issues: list[str]) -> None:
    path = repo_root / rel
    if not path.is_dir():
        issues.append(f"{context}: missing directory {rel}")


def validate_manifest(repo_root: Path = REPO_ROOT) -> list[str]:
    issues: list[str] = []
    manifest_path = repo_root / "agents" / "source_home.manifest.json"
    schema_path = repo_root / "schemas" / "agent-source-home.schema.json"

    if not manifest_path.is_file():
        return [f"missing manifest: {display(manifest_path, repo_root)}"]
    if not schema_path.is_file():
        return [f"missing schema: {display(schema_path, repo_root)}"]

    manifest = read_json(manifest_path)
    schema = read_json(schema_path)
    if not isinstance(manifest, dict):
        return ["agent source home manifest must be a JSON object"]
    if not isinstance(schema, dict):
        return ["agent source home schema must be a JSON object"]

    issues.extend(validate_schema(manifest, schema))
    if issues:
        return issues

    families = manifest["families"]
    family_ids = [family["id"] for family in families]
    duplicate_ids = sorted({family_id for family_id in family_ids if family_ids.count(family_id) > 1})
    if duplicate_ids:
        issues.append(f"duplicate family ids: {', '.join(duplicate_ids)}")

    missing_ids = sorted(EXPECTED_FAMILY_IDS - set(family_ids))
    extra_ids = sorted(set(family_ids) - EXPECTED_FAMILY_IDS)
    if missing_ids:
        issues.append(f"missing required source home families: {', '.join(missing_ids)}")
    if extra_ids:
        issues.append(f"unexpected source home families: {', '.join(extra_ids)}")

    branches = manifest["branches"]
    branch_ids = [branch["id"] for branch in branches]
    duplicate_branch_ids = sorted({branch_id for branch_id in branch_ids if branch_ids.count(branch_id) > 1})
    if duplicate_branch_ids:
        issues.append(f"duplicate branch ids: {', '.join(duplicate_branch_ids)}")
    missing_branch_ids = sorted(EXPECTED_BRANCH_IDS - set(branch_ids))
    extra_branch_ids = sorted(set(branch_ids) - EXPECTED_BRANCH_IDS)
    if missing_branch_ids:
        issues.append(f"missing required source home branches: {', '.join(missing_branch_ids)}")
    if extra_branch_ids:
        issues.append(f"unexpected source home branches: {', '.join(extra_branch_ids)}")

    direct_dirs = {
        path.name
        for path in (repo_root / "agents").iterdir()
        if path.is_dir() and path.name != "__pycache__"
    }
    missing_direct_dirs = sorted(EXPECTED_DIRECT_DIRS - direct_dirs)
    if missing_direct_dirs:
        issues.append(f"missing direct agents source directories: {', '.join(missing_direct_dirs)}")
    forbidden_direct_dirs = sorted(FORBIDDEN_DIRECT_DIRS & direct_dirs)
    if forbidden_direct_dirs:
        issues.append(f"flat legacy agents source directories still active: {', '.join(forbidden_direct_dirs)}")
    unexpected_direct_dirs = sorted(direct_dirs - EXPECTED_DIRECT_DIRS - FORBIDDEN_DIRECT_DIRS)
    if unexpected_direct_dirs:
        issues.append(f"unexpected direct agents source directories: {', '.join(unexpected_direct_dirs)}")

    covered_direct_dirs = {
        Path(family["path"]).parts[1]
        for family in families
        if len(Path(family["path"]).parts) > 1 and Path(family["path"]).parts[0] == "agents"
    }
    uncovered = sorted(EXPECTED_DIRECT_DIRS - covered_direct_dirs)
    if uncovered:
        issues.append(f"agents/source_home.manifest.json does not cover direct dirs: {', '.join(uncovered)}")

    branch_families: set[str] = set()
    for branch in branches:
        context = f"branch {branch['id']}"
        require_existing_dir(repo_root, branch["path"], context, issues)
        require_existing_file(repo_root, branch["owner_surface"], context, issues)
        branch_families.update(branch["families"])
    missing_branch_family_routes = sorted(EXPECTED_FAMILY_IDS - branch_families)
    if missing_branch_family_routes:
        issues.append(f"branches do not route source families: {', '.join(missing_branch_family_routes)}")

    for family in families:
        context = f"family {family['id']}"
        require_existing_dir(repo_root, family["path"], context, issues)
        require_existing_file(repo_root, family["owner_surface"], context, issues)

        source_dir = repo_root / family["path"]
        if source_dir.is_dir():
            matches = sorted(source_dir.glob(family["object_pattern"]))
            if not matches:
                issues.append(
                    f"{context}: object_pattern {family['object_pattern']!r} matched no files in {family['path']}"
                )

        for rel in family["schema_refs"]:
            require_existing_file(repo_root, rel, context, issues)
        for rel in family["publishes_to"]:
            require_existing_file(repo_root, rel, context, issues)
        for rel in family["builders"]:
            require_existing_file(repo_root, rel, context, issues)
        for rel in family["validators"]:
            require_existing_file(repo_root, rel, context, issues)
        for rel in family["reader_routes"]:
            require_existing_file(repo_root, rel, context, issues)

    readme_text = (repo_root / "agents" / "README.md").read_text(encoding="utf-8")
    agents_card_text = (repo_root / "agents" / "AGENTS.md").read_text(encoding="utf-8")
    for required_text, rel in (
        ("source_home.manifest.json", "agents/README.md"),
        ("source home manifest", "agents/AGENTS.md"),
    ):
        text = readme_text if rel == "agents/README.md" else agents_card_text
        if required_text not in text:
            issues.append(f"{rel}: missing required source-home route text {required_text!r}")

    return issues


def main() -> int:
    issues = validate_manifest(REPO_ROOT)
    if issues:
        print("Agent source home validation failed.", file=sys.stderr)
        for issue in issues:
            print(f"- {issue}", file=sys.stderr)
        return 1
    print("[ok] agent source home manifest is valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
