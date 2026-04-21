#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json

from _recursor_common import ROOT, build_boundary_report, build_readiness_index, min_json, read_json


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Build recursor role readiness surfaces.")
    parser.add_argument("--write", action="store_true", help="Write generated readiness surfaces.")
    parser.add_argument("--check", action="store_true", help="Check generated files match expected outputs.")
    parser.add_argument("--json", action="store_true", help="Print JSON report.")
    args = parser.parse_args(argv)

    index = build_readiness_index(ROOT)
    boundary = build_boundary_report(ROOT)
    pair_contract = read_json(ROOT / "config" / "recursor_pair.seed.json")
    expected = {
        ROOT / "generated" / "recursor_role_readiness.min.json": index,
        ROOT / "generated" / "recursor_pair_contract.min.json": pair_contract,
        ROOT / "generated" / "recursor_agon_boundary_report.min.json": boundary,
    }

    mismatches = []
    if args.write:
        for path, payload in expected.items():
            min_json(path, payload)

    if args.check:
        for path, payload in expected.items():
            if not path.exists():
                mismatches.append({"path": str(path.relative_to(ROOT)), "kind": "missing"})
                continue
            current = json.loads(path.read_text(encoding="utf-8"))
            # generated_at is volatile; compare without it.
            def strip_time(value):
                if isinstance(value, dict):
                    return {k: strip_time(v) for k, v in value.items() if k != "generated_at"}
                if isinstance(value, list):
                    return [strip_time(v) for v in value]
                return value
            if strip_time(current) != strip_time(payload):
                mismatches.append({"path": str(path.relative_to(ROOT)), "kind": "stale_or_different"})
    report = {
        "schema_version": "recursor-readiness-build-report/v1",
        "status": "fail" if index["boundary"]["violations"] or mismatches else "pass",
        "wrote": bool(args.write),
        "checked": bool(args.check),
        "mismatches": mismatches,
        "readiness_index": index,
        "boundary_report": boundary,
    }
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(f"recursor readiness: {report['status']}")
    return 1 if report["status"] == "fail" else 0


if __name__ == "__main__":
    raise SystemExit(main())
