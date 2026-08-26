#!/usr/bin/env python3
"""Read and validate the generated Goal participant graph without enrichment."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from build_goal_participant_graph import (
    GRAPH_PATH,
    ROOT,
    GoalParticipantGraphError,
    check_generated,
    read_json,
    validate_graph_payload,
)


def read_goal_participant_graph(
    root: Path = ROOT,
    path: Path | None = None,
) -> dict[str, Any]:
    root = root.resolve()
    graph_path = path if path is not None else root / GRAPH_PATH
    if not graph_path.is_absolute():
        graph_path = root / graph_path
    check_generated(root, graph_path)
    graph = read_json(graph_path)
    validate_graph_payload(root, graph)
    return graph


def main() -> int:
    parser = argparse.ArgumentParser(description="Read the generated aoa-agents Goal participant graph.")
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--path", type=Path, default=None)
    args = parser.parse_args()
    try:
        payload = read_goal_participant_graph(args.root, args.path)
    except GoalParticipantGraphError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
