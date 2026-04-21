#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from _recursor_common import ROOT, build_readiness_index


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Validate recursor role readiness source contracts.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    index = build_readiness_index(ROOT)
    status = index["boundary"]["status"]
    if args.json:
        print(json.dumps(index, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        if status == "pass":
            print("recursor role readiness: pass")
        else:
            print("recursor role readiness: fail")
            for violation in index["boundary"]["violations"]:
                print(f"- {violation.get('kind')}: {violation.get('message')}")
    return 0 if status == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
