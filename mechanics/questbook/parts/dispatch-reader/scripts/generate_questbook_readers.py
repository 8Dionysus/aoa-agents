#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from validate_agents import (
    QUEST_CATALOG_EXAMPLE_PATH,
    QUEST_CATALOG_PATH,
    QUEST_DISPATCH_EXAMPLE_PATH,
    QUEST_DISPATCH_PATH,
    build_quest_catalog_projection,
    build_quest_dispatch_projection,
)


def _min_json(payload: Any) -> str:
    return json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + "\n"


def _pretty_json(payload: Any) -> str:
    return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _expected() -> dict[Path, str]:
    catalog = build_quest_catalog_projection(REPO_ROOT)
    dispatch = build_quest_dispatch_projection(REPO_ROOT)
    return {
        QUEST_CATALOG_PATH: _min_json(catalog),
        QUEST_CATALOG_EXAMPLE_PATH: _pretty_json(catalog),
        QUEST_DISPATCH_PATH: _min_json(dispatch),
        QUEST_DISPATCH_EXAMPLE_PATH: _pretty_json(dispatch),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate Questbook catalog and dispatch readers.")
    parser.add_argument("--check", action="store_true", help="Check generated readers without writing.")
    args = parser.parse_args(argv)

    mismatches: list[str] = []
    for path, content in _expected().items():
        if args.check:
            if not path.exists():
                mismatches.append(f"{path.relative_to(REPO_ROOT).as_posix()}: missing")
            elif path.read_text(encoding="utf-8") != content:
                mismatches.append(f"{path.relative_to(REPO_ROOT).as_posix()}: stale")
        else:
            _write(path, content)

    if mismatches:
        for mismatch in mismatches:
            print(mismatch)
        return 1

    if args.check:
        print("[ok] questbook generated readers are current")
    else:
        print("[ok] wrote questbook generated readers")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
