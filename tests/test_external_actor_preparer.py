from __future__ import annotations

import importlib.util
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/aoa-summon/scripts/prepare_external_actor.py"
SPEC = importlib.util.spec_from_file_location("external_actor_preparer", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
PREPARER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PREPARER)


def _input(input_id: str, path: Path) -> tuple[dict[str, str], Path]:
    return ({"input_id": input_id}, path)


class ExternalActorPreparerTests(unittest.TestCase):
    def test_continuation_return_owner_projects_the_exact_holder(self) -> None:
        projected = PREPARER._concrete_return_owner_provenance(
            {
                "object_id": "holder:goal",
                "owner_repo": "codex-goal",
                "schema_version": "holder-v1",
                "digest": "sha256:" + "1" * 64,
            },
            {
                "owner_repo": "codex-goal",
                "artifact_ref": "goal-anchor.json",
                "source_ref": "goal:root",
                "artifact_digest": "sha256:" + "2" * 64,
                "schema_ref": "goal-anchor-v1",
                "schema_version": "goal-anchor-v1",
            },
        )

        self.assertEqual(projected["artifact_ref"], "holder:goal")
        self.assertEqual(projected["artifact_digest"], "sha256:" + "1" * 64)
        self.assertEqual(projected["owner_repo"], "codex-goal")
        self.assertEqual(projected["source_ref"], "goal:root")
        self.assertEqual(projected["schema_version"], "holder-v1")

    def test_review_evidence_closure_accepts_supplied_transitive_input(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            report = temp_path / "writer-report.json"
            report.write_text(
                '{"evidence_refs":["immutable:repair-review#L2-L4"]}',
                encoding="utf-8",
            )
            repair = temp_path / "repair-review.json"
            repair.write_text("{}", encoding="utf-8")

            PREPARER._assert_review_evidence_closure(
                (_input("writer-report", report), _input("repair-review", repair))
            )

    def test_review_evidence_closure_rejects_unforwarded_writer_anchor(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            report = Path(temp_dir) / "writer-report.json"
            report.write_text(
                '{"evidence_refs":["immutable:repair-review#L2-L4"]}',
                encoding="utf-8",
            )

            with self.assertRaisesRegex(
                PREPARER.PreparationError,
                "writer-report -> repair-review",
            ):
                PREPARER._assert_review_evidence_closure(
                    (_input("writer-report", report),)
                )

    def test_independent_review_dag_is_terminal_without_nested_reviewer(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            topology = PREPARER._dag_topology(
                route_id="eval-review",
                execution_posture="independent_review",
                mandate={
                    "role_binding": {"role_id": "reviewer"},
                    "domain_owner": "aoa-evals",
                    "return_owner": {"object_id": "goal:root"},
                    "authority": {"stop_line": "Return judgment; do not mutate."},
                },
                execution={"effect_class": "read_only"},
                named_outputs=("independent-review",),
                evidence_inputs=(
                    _input("writer-report", Path(temp_dir) / "report.json"),
                ),
                runtime_profile_id="landing-readonly-v1",
            )

        self.assertEqual(
            [node["kind"] for node in topology["nodes"]],
            ["independent-review-obligation"],
        )
        self.assertEqual(topology["edges"], [])
        self.assertEqual(topology["execution_stages"], [["actor:eval-review"]])

    def test_preparer_uses_runtime_canonical_wake_event_kinds(self) -> None:
        self.assertEqual(PREPARER.COMPLETED_WAKE_EVENT_KIND, "result.validated")
        self.assertEqual(
            PREPARER.REVIEW_REQUIRED_WAKE_EVENT_KIND,
            "result.review_required",
        )


if __name__ == "__main__":
    unittest.main()
