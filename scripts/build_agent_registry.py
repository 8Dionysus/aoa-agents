#!/usr/bin/env python3
from __future__ import annotations

import sys

from agent_profile_registry import BuildError, write_agent_registry


def main() -> int:
    try:
        write_agent_registry()
    except BuildError as exc:
        print(f"[error] {exc}", file=sys.stderr)
        return 1

    print("[ok] wrote generated/agent_registry.min.json from profiles/*.profile.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
