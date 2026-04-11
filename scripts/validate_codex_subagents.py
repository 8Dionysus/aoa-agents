#!/usr/bin/env python3
"""Validate generated Codex subagent projection surfaces."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from agent_profile_registry import BuildError
from codex_subagent_projection import collect_projection_validation_errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profiles-root", type=Path, required=True)
    parser.add_argument("--wiring", type=Path, required=True)
    parser.add_argument("--agents-dir", type=Path, required=True)
    parser.add_argument("--config-snippet", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, default=None)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        errors = collect_projection_validation_errors(
            args.profiles_root,
            args.wiring,
            args.agents_dir,
            args.config_snippet,
            manifest_path=args.manifest,
        )
    except BuildError as exc:
        print(f"[error] {exc}", file=sys.stderr)
        return 1

    if errors:
        print("Validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("Codex subagent projection surfaces are valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
