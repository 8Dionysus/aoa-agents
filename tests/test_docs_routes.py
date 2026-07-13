from __future__ import annotations

import re
import subprocess
from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
EXECUTABLE_MARKDOWN_PREFIXES = (".agents/skills/",)
SHELL_FENCE_PATTERN = re.compile(
    r"^ {0,3}```(?:bash|console|sh|shell|zsh)(?:\s+.*)?$",
    re.IGNORECASE | re.MULTILINE,
)
FENCE_OPEN_PATTERN = re.compile(r"^ {0,3}```")
COMMAND_BLOCK_LINE_PATTERN = re.compile(
    r"^[ \t]*(?:(?:[-*]|\d+[.)])[ \t]+)?(?:\$[ \t]+)?"
    r"(?:python3?|pytest|uv|pip3?|aoa|git|ruff|mypy|make|tox|hatch|poetry)"
    r"(?:[ \t]+(?![=:])\S+)"
)
REPO_COMMAND_LINE_PATTERN = re.compile(
    r"^[ \t]*(?:(?:[-*]|\d+[.)])[ \t]+)?`?(?:"
    r"python3?(?:[ \t]+-m)?[ \t]+|pytest(?=[ \t])|"
    r"uv[ \t]+run[ \t]+pytest\b|pip3?[ \t]+|"
    r"git[ \t]+(?:status|diff|commit|push|fetch|checkout|switch|merge|tag)\b|"
    r"aoa[ \t]+|ruff[ \t]+(?:check|format)\b|mypy(?=[ \t]))",
    re.MULTILINE,
)
INLINE_REPO_COMMAND_PATTERN = re.compile(
    r"(?<!`)`(?!``)(?:python3?(?:\s+-m)?\s+|pytest(?=\s)|"
    r"uv\s+run\s+pytest\b|pip3?\s+|"
    r"git\s+(?:status|diff|commit|push|fetch|checkout|switch|merge|tag)\b|"
    r"aoa\s+|ruff\s+(?:check|format)\b|mypy(?=\s))[^`\n]+`(?!`)"
)
IMPERATIVE_SCRIPT_PATTERN = re.compile(
    r"\b(?:run|execute|invoke|call|validate with|check with|regenerate with)\s+"
    r"(?:the\s+)?`(?:[^`]+/)+[^`]+\.(?:py|sh)`",
    re.IGNORECASE,
)


def tracked_markdown_paths() -> tuple[Path, ...]:
    completed = subprocess.run(
        ("git", "ls-files", "--cached", "--others", "--exclude-standard", "--", "*.md"),
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return tuple(Path(line) for line in completed.stdout.splitlines() if line)


def fenced_command_block_present(content: str) -> bool:
    in_fence = False
    for line in content.splitlines():
        if not in_fence and FENCE_OPEN_PATTERN.match(line):
            in_fence = True
            continue
        if in_fence and line.strip() == "```":
            in_fence = False
            continue
        if in_fence and COMMAND_BLOCK_LINE_PATTERN.match(line):
            return True
    return False


def markdown_command_violations(content: str) -> set[str]:
    violations: set[str] = set()
    if SHELL_FENCE_PATTERN.search(content):
        violations.add("shell command block")
    elif fenced_command_block_present(content):
        violations.add("command block")
    if REPO_COMMAND_LINE_PATTERN.search(content):
        violations.add("repo command line")
    if INLINE_REPO_COMMAND_PATTERN.search(content):
        violations.add("inline repo command")
    if IMPERATIVE_SCRIPT_PATTERN.search(content):
        violations.add("imperative script instruction")
    return violations


class DocumentationCommandRouteTests(unittest.TestCase):
    def test_non_owner_markdown_routes_commands_to_executable_owners(self) -> None:
        offenders: list[str] = []
        for relative_path in tracked_markdown_paths():
            route = relative_path.as_posix()
            if route.startswith(EXECUTABLE_MARKDOWN_PREFIXES):
                continue
            if relative_path.name in {"AGENTS.md", "VALIDATION.md"}:
                continue
            content = (REPO_ROOT / relative_path).read_text(encoding="utf-8")
            for violation in sorted(markdown_command_violations(content)):
                offenders.append(f"{route}: {violation}")

        self.assertEqual(offenders, [])

    def test_guard_rejects_scattered_command_forms(self) -> None:
        content = """# Drift

```bash
python scripts/validate_agents.py
```

- `python -m pytest -q`
- git status -sb
Run `scripts/validate_agents.py`.
"""

        self.assertEqual(
            markdown_command_violations(content),
            {
                "imperative script instruction",
                "inline repo command",
                "repo command line",
                "shell command block",
            },
        )
        self.assertEqual(
            markdown_command_violations("```text\n- aoa surfaces detect .\n```\n"),
            {"command block", "repo command line"},
        )
        self.assertEqual(
            markdown_command_violations("```python\nfrom pathlib import Path\n```\n"),
            set(),
        )


if __name__ == "__main__":
    unittest.main()
