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
    (
        "run antifragility stress tests",
        [
            sys.executable,
            "-m",
            "unittest",
            "discover",
            "-s",
            "mechanics/antifragility/parts/stress-posture/tests",
            "-p",
            "test_*.py",
        ],
    ),
    (
        "run Titan mechanic tests",
        [
            sys.executable,
            "-m",
            "unittest",
            "discover",
            "-s",
            "mechanics/titan/tests",
            "-p",
            "test_*.py",
        ],
    ),
    (
        "run runtime artifact contract tests",
        [
            sys.executable,
            "-m",
            "unittest",
            "discover",
            "-s",
            "mechanics/runtime-seam/parts/artifact-contracts/tests",
            "-p",
            "test_*.py",
        ],
    ),
    (
        "run checkpoint contract tests",
        [
            sys.executable,
            "-m",
            "unittest",
            "discover",
            "-s",
            "mechanics/checkpoint/tests",
            "-p",
            "test_*.py",
        ],
    ),
    (
        "run recurrence recursor tests",
        [
            sys.executable,
            "-m",
            "unittest",
            "discover",
            "-s",
            "mechanics/recurrence/tests",
            "-p",
            "test_*.py",
        ],
    ),
    (
        "run recurrence component manifest tests",
        [
            sys.executable,
            "-m",
            "unittest",
            "discover",
            "-s",
            "mechanics/recurrence/parts/component-manifests/tests",
            "-p",
            "test_*.py",
        ],
    ),
    (
        "run RPG progression tests",
        [
            sys.executable,
            "-m",
            "unittest",
            "discover",
            "-s",
            "mechanics/rpg/parts/progression-model/tests",
            "-p",
            "test_*.py",
        ],
    ),
    (
        "run Codex refresh-law tests",
        [
            sys.executable,
            "-m",
            "unittest",
            "discover",
            "-s",
            "mechanics/codex-projection/parts/refresh-law/tests",
            "-p",
            "test_*.py",
        ],
    ),
    (
        "run assistant projection resolver tests",
        [
            sys.executable,
            "-m",
            "unittest",
            "discover",
            "-s",
            "mechanics/codex-projection/parts/assistant-projection/tests",
            "-p",
            "test_*.py",
        ],
    ),
    (
        "run Agon formation tests",
        [
            sys.executable,
            "-m",
            "unittest",
            "discover",
            "-s",
            "mechanics/agon/parts/formation/tests",
            "-p",
            "test_*.py",
        ],
    ),
    (
        "run Agon package tests",
        [
            sys.executable,
            "-m",
            "unittest",
            "discover",
            "-s",
            "mechanics/agon/tests",
            "-p",
            "test_*.py",
        ],
    ),
    (
        "run Agon arena-rank-school tests",
        [
            sys.executable,
            "-m",
            "unittest",
            "discover",
            "-s",
            "mechanics/agon/parts/arena-rank-school/tests",
            "-p",
            "test_*.py",
        ],
    ),
    (
        "run Agon epistemic-actor tests",
        [
            sys.executable,
            "-m",
            "unittest",
            "discover",
            "-s",
            "mechanics/agon/parts/epistemic-actor/tests",
            "-p",
            "test_*.py",
        ],
    ),
    (
        "run Experience package tests",
        [
            sys.executable,
            "-m",
            "unittest",
            "discover",
            "-s",
            "mechanics/experience/tests",
            "-p",
            "test_*.py",
        ],
    ),
    (
        "run Experience assistant-civil-service tests",
        [
            sys.executable,
            "-m",
            "unittest",
            "discover",
            "-s",
            "mechanics/experience/parts/assistant-civil-service/tests",
            "-p",
            "test_*.py",
        ],
    ),
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
