#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[5]
PART_ROOT = Path("mechanics/codex-projection/parts/specialization-eligibility")
RECORDS_DIR = PART_ROOT / "records"
READINESS_PATH = PART_ROOT / "generated" / "specialization-eligibility-readiness.min.json"


class SpecializationEligibilityReadinessError(RuntimeError):
    pass


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SpecializationEligibilityReadinessError(f"missing JSON file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SpecializationEligibilityReadinessError(f"invalid JSON in {path}: {exc}") from exc


def compact_json(payload: Any) -> str:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"


def record_paths(root: Path) -> list[Path]:
    records_root = root / RECORDS_DIR
    return sorted(path for path in records_root.glob("*.eligibility.json") if path.is_file())


def build_readiness_payload(root: Path = ROOT) -> dict[str, Any]:
    root = root.resolve()
    records: list[dict[str, Any]] = []
    decision_counts: Counter[str] = Counter()
    install_counts: Counter[str] = Counter()
    consent_counts: Counter[str] = Counter()

    source_refs: list[str] = [
        "generated/codex_agents/projection_manifest.json",
        "generated/role_specialization_catalog.min.json",
        "generated/capability_pack_registry.min.json",
    ]

    for path in record_paths(root):
        relative_path = path.relative_to(root).as_posix()
        record = read_json(path)
        decision_status = record["decision"]["status"]
        install_state = record["codex_install"]["install_state"]
        consent_state = record["owner_consent"]["consent_state"]
        missing_refs = record["evidence"]["missing_refs"]

        decision_counts[decision_status] += 1
        install_counts[install_state] += 1
        consent_counts[consent_state] += 1
        source_refs.append(relative_path)

        records.append(
            {
                "id": record["id"],
                "path": relative_path,
                "specialization_id": record["specialization_id"],
                "specialization_ref": record["specialization_ref"],
                "base_role_id": record["base_role_id"],
                "capability_pack_ref": record["capability_pack_ref"],
                "proposed_agent_name": record["codex_install"]["proposed_agent_name"],
                "decision_status": decision_status,
                "install_state": install_state,
                "consent_state": consent_state,
                "missing_ref_count": len(missing_refs),
                "missing_refs": missing_refs,
                "next_review_trigger": record["decision"]["next_review_trigger"],
            }
        )

    records.sort(key=lambda item: item["specialization_id"])

    return {
        "schema_version": "codex_specialization_eligibility_readiness_v1",
        "kind": "codex_specialization_eligibility_readiness",
        "owner_repo": "aoa-agents",
        "projection_scope": "base_role_profiles_only",
        "projection_boundary": {
            "generated_surface_policy": "no_generated_change",
            "workspace_install_policy": "no_workspace_install",
            "runtime_activation_policy": "no_runtime_activation",
        },
        "counts": {
            "records": len(records),
            "by_decision_status": dict(sorted(decision_counts.items())),
            "by_install_state": dict(sorted(install_counts.items())),
            "by_consent_state": dict(sorted(consent_counts.items())),
        },
        "records": records,
        "source_refs": sorted(source_refs),
    }


def write_readiness(root: Path, output: Path) -> None:
    payload = build_readiness_payload(root)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(compact_json(payload), encoding="utf-8")


def check_readiness(root: Path, output: Path) -> None:
    expected = compact_json(build_readiness_payload(root))
    try:
        actual = output.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise SpecializationEligibilityReadinessError(f"missing readiness reader: {output}") from exc
    if actual != expected:
        raise SpecializationEligibilityReadinessError(
            f"readiness reader is stale: {output.relative_to(root).as_posix()}"
        )


def main() -> int:
    parser = argparse.ArgumentParser(description="Build Codex specialization eligibility readiness reader.")
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--out", type=Path, default=None)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    root = args.root.resolve()
    output = args.out if args.out is not None else root / READINESS_PATH
    if not output.is_absolute():
        output = root / output

    try:
        if args.check:
            check_readiness(root, output)
            print(f"Codex specialization eligibility readiness is current: {output.relative_to(root).as_posix()}")
        else:
            write_readiness(root, output)
            payload = build_readiness_payload(root)
            print(
                "Wrote Codex specialization eligibility readiness: "
                f"{output.relative_to(root).as_posix()} records={payload['counts']['records']}"
            )
    except SpecializationEligibilityReadinessError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
