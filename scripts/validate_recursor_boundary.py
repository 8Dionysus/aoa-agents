#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from _recursor_common import ROOT, build_boundary_report, min_json


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Validate recursor Agon/Codex boundary stop-lines.")
    parser.add_argument("--write", action="store_true", help="Write generated boundary report.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    report = build_boundary_report(ROOT)
    if args.write:
        min_json(ROOT / "generated" / "recursor_agon_boundary_report.min.json", report)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(f"recursor boundary: {report['status']}")
        if report["violations"]:
            for violation in report["violations"]:
                print(f"- {violation.get('kind')}: {violation.get('message')}")
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
