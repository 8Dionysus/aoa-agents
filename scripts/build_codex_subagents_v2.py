#!/usr/bin/env python3
"""Build Codex custom-agent TOML files from aoa-agents profiles."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from agent_profile_registry import BuildError
from codex_subagent_projection import (
    build_agents,
    build_manifest,
    build_projection_file_texts,
    load_wiring,
    write_projection_file_texts,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profiles-root", type=Path, default=Path("profiles"))
    parser.add_argument("--wiring", type=Path, default=Path("config/codex_subagent_wiring.v2.json"))
    parser.add_argument("--output-dir", type=Path, default=Path("generated/codex_agents/agents"))
    parser.add_argument(
        "--emit-config-snippet",
        type=Path,
        default=Path("generated/codex_agents/config.subagents.generated.toml"),
    )
    parser.add_argument(
        "--emit-manifest",
        type=Path,
        default=Path("generated/codex_agents/projection_manifest.json"),
    )
    parser.add_argument("--config-file-prefix", default="agents")
    parser.add_argument("--check", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        wiring = load_wiring(args.wiring)
        texts = build_projection_file_texts(
            args.profiles_root,
            wiring,
            args.output_dir,
            args.emit_config_snippet,
            args.emit_manifest,
            config_file_prefix=args.config_file_prefix,
        )
        write_projection_file_texts(texts, check=args.check)
        agents = build_agents(args.profiles_root, wiring)
        manifest = build_manifest(agents, wiring, config_file_prefix=args.config_file_prefix)
    except BuildError as exc:
        print(f"[error] {exc}", file=sys.stderr)
        return 1

    if args.check:
        print("Codex subagent projection is up to date.")
    else:
        print(f"Generated {len(manifest['generated_agents'])} Codex custom agents in {args.output_dir}")
        print(f"Config snippet: {args.emit_config_snippet}")
        print(f"Projection manifest: {args.emit_manifest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
