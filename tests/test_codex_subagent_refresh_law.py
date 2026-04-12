from __future__ import annotations

import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
EXAMPLE_PATH = REPO_ROOT / "examples" / "subagent_projection_refresh_law.example.json"
ALLOWED_ROUTE_CLASSES = {
    "observe",
    "revalidate",
    "rebuild",
    "reexport",
    "regenerate",
    "reproject",
    "repair",
    "defer",
}


def _load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def _resolve_pattern(pattern: str) -> list[Path]:
    return list(REPO_ROOT.glob(pattern))


class CodexSubagentRefreshLawTests(unittest.TestCase):
    def test_refresh_law_is_linked_and_bounded(self) -> None:
        readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
        agents = (REPO_ROOT / "AGENTS.md").read_text(encoding="utf-8")
        docs_readme = (REPO_ROOT / "docs" / "README.md").read_text(encoding="utf-8")
        projection = (REPO_ROOT / "docs" / "CODEX_SUBAGENT_PROJECTION.md").read_text(
            encoding="utf-8"
        )
        law = (REPO_ROOT / "docs" / "CODEX_SUBAGENT_REFRESH_LAW.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("docs/CODEX_SUBAGENT_REFRESH_LAW.md", readme)
        self.assertIn("docs/CODEX_SUBAGENT_REFRESH_LAW.md", agents)
        self.assertIn("CODEX_SUBAGENT_REFRESH_LAW", docs_readme)
        self.assertIn("CODEX_SUBAGENT_REFRESH_LAW.md", projection)

        for token in (
            "component:codex-subagents:projection",
            "It does not make",
            "Do not hand-author workspace `.codex/agents/*.toml`",
            "Do not turn repeated projection refresh into hidden recursive autonomy.",
        ):
            self.assertIn(token, law)

    def test_projection_refresh_example_tracks_live_surfaces(self) -> None:
        payload = _load_json(EXAMPLE_PATH)

        self.assertEqual(payload["schema_version"], "aoa_component_refresh_law_v1")
        self.assertEqual(payload["component_ref"], "component:codex-subagents:projection")
        self.assertEqual(payload["owner_repo"], "aoa-agents")
        self.assertEqual(payload["followthrough_home"], "aoa-playbooks:component-refresh-cycle")

        for key in (
            "source_authored_inputs",
            "generated_surfaces",
            "projected_or_installed_surfaces",
            "drift_signals",
            "proof_commands",
            "rollback_anchors",
        ):
            self.assertTrue(payload[key], msg=f"{key} must not be empty")

        for pattern in payload["source_authored_inputs"]:
            matches = _resolve_pattern(pattern)
            self.assertTrue(matches, msg=f"expected matches for source pattern {pattern!r}")

        for pattern in payload["generated_surfaces"]:
            matches = _resolve_pattern(pattern)
            self.assertTrue(matches, msg=f"expected matches for generated pattern {pattern!r}")

        refresh_window = payload["refresh_window"]
        self.assertEqual(refresh_window["stale_after_days"], 7)
        self.assertEqual(refresh_window["repeat_trigger_threshold"], 2)
        self.assertEqual(refresh_window["open_window_days"], 5)

        routes = payload["refresh_routes"]
        self.assertIn("python scripts/build_published_surfaces.py", routes["execute"])
        self.assertIn("python scripts/build_codex_subagents_v2.py", routes["execute"])
        self.assertIn("python -m pytest -q tests", routes["validate"])

        for signal in payload["drift_signals"]:
            self.assertIn(signal["recommended_route_class"], ALLOWED_ROUTE_CLASSES)

        for anchor in payload["rollback_anchors"]:
            self.assertTrue((REPO_ROOT / anchor).exists(), msg=f"missing rollback anchor {anchor}")


if __name__ == "__main__":
    unittest.main()
