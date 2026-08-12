from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/aoa-summon/scripts/prepare_external_actor.py"
SPEC = importlib.util.spec_from_file_location("external_actor_preparer", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
PREPARER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PREPARER)


def _input(input_id: str, path: Path) -> tuple[dict[str, str], Path]:
    return ({"input_id": input_id}, path)


def test_review_evidence_closure_accepts_supplied_transitive_input(
    tmp_path: Path,
) -> None:
    report = tmp_path / "writer-report.json"
    report.write_text(
        '{"evidence_refs":["immutable:repair-review#L2-L4"]}',
        encoding="utf-8",
    )
    repair = tmp_path / "repair-review.json"
    repair.write_text("{}", encoding="utf-8")

    PREPARER._assert_review_evidence_closure(
        (_input("writer-report", report), _input("repair-review", repair))
    )


def test_review_evidence_closure_rejects_unforwarded_writer_anchor(
    tmp_path: Path,
) -> None:
    report = tmp_path / "writer-report.json"
    report.write_text(
        '{"evidence_refs":["immutable:repair-review#L2-L4"]}',
        encoding="utf-8",
    )

    with pytest.raises(
        PREPARER.PreparationError,
        match="writer-report -> repair-review",
    ):
        PREPARER._assert_review_evidence_closure((_input("writer-report", report),))


def test_independent_review_dag_is_terminal_without_nested_reviewer(
    tmp_path: Path,
) -> None:
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
        evidence_inputs=(_input("writer-report", tmp_path / "report.json"),),
        runtime_profile_id="landing-readonly-v1",
    )

    assert [node["kind"] for node in topology["nodes"]] == [
        "independent-review-obligation"
    ]
    assert topology["edges"] == []
    assert topology["execution_stages"] == [["actor:eval-review"]]


def test_preparer_uses_runtime_canonical_wake_event_kinds() -> None:
    assert PREPARER.COMPLETED_WAKE_EVENT_KIND == "result.validated"
    assert PREPARER.REVIEW_REQUIRED_WAKE_EVENT_KIND == "result.review_required"
