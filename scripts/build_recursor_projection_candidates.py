#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json

from _recursor_common import ROOT, min_json, read_json, validate_projection_candidate, stable_hash, utc_now


def build_projection() -> dict:
    projection = read_json(ROOT / "config" / "codex_recursor_projection.candidate.json")
    violations = validate_projection_candidate(projection)
    return {
        "schema_version": "recursor-projection-candidates-index/v1",
        "generated_at": utc_now(),
        "owner_repo": "aoa-agents",
        "projection_status": projection.get("projection_status"),
        "install_by_default": projection.get("install_by_default"),
        "requires_owner_review": projection.get("requires_owner_review"),
        "candidate_agents": projection.get("candidate_agents", []),
        "source_hash": stable_hash(projection),
        "boundary": {
            "status": "fail" if violations else "pass",
            "violations": violations,
        },
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Build Codex recursor projection candidate surface.")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    payload = build_projection()
    path = ROOT / "generated" / "recursor_projection_candidates.min.json"
    mismatches = []
    if args.write:
        min_json(path, payload)
    if args.check:
        if not path.exists():
            mismatches.append({"path": str(path.relative_to(ROOT)), "kind": "missing"})
        else:
            current = json.loads(path.read_text(encoding="utf-8"))
            def strip_time(value):
                if isinstance(value, dict):
                    return {k: strip_time(v) for k, v in value.items() if k != "generated_at"}
                if isinstance(value, list):
                    return [strip_time(v) for v in value]
                return value
            if strip_time(current) != strip_time(payload):
                mismatches.append({"path": str(path.relative_to(ROOT)), "kind": "stale_or_different"})
    report = {
        "schema_version": "recursor-projection-build-report/v1",
        "status": "fail" if payload["boundary"]["violations"] or mismatches else "pass",
        "wrote": bool(args.write),
        "checked": bool(args.check),
        "mismatches": mismatches,
        "projection": payload,
    }
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(f"recursor projection candidates: {report['status']}")
    return 1 if report["status"] == "fail" else 0


if __name__ == "__main__":
    raise SystemExit(main())
