#!/usr/bin/env python3
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def _env() -> dict[str, str]:
    env = os.environ.copy()
    candidates = [
        env.get("AOA_EVALS_ROOT"),
        str((REPO_ROOT / ".deps" / "aoa-evals").resolve()),
        str((REPO_ROOT.parent / "aoa-evals").resolve()),
    ]
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            env["AOA_EVALS_ROOT"] = str(Path(candidate).resolve())
            break
    return env


COMMANDS = [
    ("validate agents", [sys.executable, "scripts/validate_agents.py"]),
    ("run tests", [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py"]),
    ("rebuild published surfaces", [sys.executable, "scripts/build_published_surfaces.py"]),
    ("check generated drift", ["git", "diff", "--exit-code", "--", "generated"]),
]


def run_step(label: str, command: list[str]) -> int:
    print(f"[run] {label}: {subprocess.list2cmdline(command)}", flush=True)
    completed = subprocess.run(command, cwd=REPO_ROOT, env=_env(), check=False)
    if completed.returncode != 0:
        print(f"[error] {label} failed with exit code {completed.returncode}", flush=True)
        return completed.returncode
    print(f"[ok] {label}", flush=True)
    return 0


def main() -> int:
    for label, command in COMMANDS:
        exit_code = run_step(label, command)
        if exit_code != 0:
            return exit_code
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
