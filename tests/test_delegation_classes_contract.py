from __future__ import annotations

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "skills/aoa-agents-skills/references/contract.yaml"
DOC = ROOT / "skills/aoa-agents-skills/references/delegation-classes.md"


def test_owner_contract_keeps_the_two_delegation_classes_distinct() -> None:
    payload = yaml.safe_load(CONTRACT.read_text(encoding="utf-8"))
    classes = payload["delegation_classes"]

    ephemeral = classes["ephemeral_read_worker_v1"]
    assert ephemeral["responsibility"] == "parent_retained"
    assert ephemeral["role_formation"] == "forbidden"
    assert ephemeral["durable_transfer"] == "forbidden"
    assert "content_addressed_result" in ephemeral["required_posture"]

    external = classes["external_incarnation_v1"]
    assert external["responsibility"] == "transferred_and_reviewed_return"
    assert external["role_formation"] == "required"
    assert external["durable_transfer"] == "required"
    assert set(external["pre_launch_refs"]) == {
        "role_contract_ref",
        "actor_mandate_ref",
        "responsibility_transfer_ref",
        "incarnation_binding_ref",
    }
    assert external["post_return_refs"] == ["reviewed_return_ref"]
    assert external["stronger_owner_refs"]["model_realization"] == "aoa-models"
    assert external["stronger_owner_refs"]["incarnation_binding"] == "aoa-sdk"


def test_owner_contract_and_procedure_keep_lifecycle_claims_separate() -> None:
    payload = yaml.safe_load(CONTRACT.read_text(encoding="utf-8"))
    assert payload["delegation_class_rules"]["provider_neutral_abi"] == (
        "aoa_delegation_class_v1"
    )
    assert payload["delegation_class_rules"][
        "builtin_codex_child_as_external_incarnation"
    ] == "forbidden"
    assert payload["delegation_class_rules"]["lifecycle_separation"].startswith(
        "Eval, closeout, and acceptance"
    )

    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "parent holder keeps responsibility",
        "responsibility transfer",
        "process, session, and event evidence",
        "eval, closeout, and acceptance",
        "Codex CLI",
        "local/provider adapter",
        "Built-in Codex child-agent lanes",
        "d0-baseline:baseline-ready",
    ):
        assert phrase in text
