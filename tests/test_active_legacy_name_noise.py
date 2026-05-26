from __future__ import annotations

import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
LEGACY_NAME_RE = re.compile(
    r"(?:wave(?:1|2|2_5|3|5|14|15|16)|"
    r"current_direction|roadmap_parity|downstream_feed|"
    r"test_validate_agents|test_validate_semantic_agents)",
    re.IGNORECASE,
)
EXCLUDED_PARTS = {
    ".git",
    ".deps",
    ".pytest_cache",
    "__pycache__",
    "legacy",
    "memo",
    "captured",
}
EXCLUDED_PREFIXES = (
    Path("docs/decisions"),
    Path("mechanics/codex-projection/PROVENANCE.md"),
    Path("mechanics/experience/PROVENANCE.md"),
    Path("mechanics/recurrence/PROVENANCE.md"),
)


def is_excluded(path: Path) -> bool:
    rel = path.relative_to(REPO_ROOT)
    if any(part in EXCLUDED_PARTS for part in rel.parts):
        return True
    return any(rel == prefix or prefix in rel.parents for prefix in EXCLUDED_PREFIXES)


class ActiveLegacyNameNoiseTests(unittest.TestCase):
    def test_active_route_paths_do_not_use_legacy_names(self) -> None:
        noisy_paths = []
        for path in REPO_ROOT.rglob("*"):
            if is_excluded(path):
                continue
            rel = path.relative_to(REPO_ROOT).as_posix()
            if LEGACY_NAME_RE.search(rel):
                noisy_paths.append(rel)

        self.assertEqual(noisy_paths, [])


if __name__ == "__main__":
    unittest.main()
