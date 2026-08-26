from __future__ import annotations

import copy
from contextlib import contextmanager
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[5]
SCRIPT_DIR = ROOT / "mechanics/boundary-bridge/parts/participant-relations/scripts"
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from build_goal_participant_graph import (  # noqa: E402
    CONTRACT_PATH,
    CONTRACT_SCHEMA_VERSION,
    GRAPH_PATH,
    GRAPH_SCHEMA_PATH,
    RELATION_SCHEMA_ID,
    REQUIRED_PRIVACY_OMISSIONS,
    RELATION_SCHEMA_PATH,
    SOURCE_SCHEMA_PATH,
    SOURCE_PATH,
    PUBLICATION_SCHEMA_PATH,
    GoalParticipantGraphError,
    admission_receipt_id,
    build_graph_payload,
    main as build_graph_main,
    compact_json,
    check_generated,
    publication_payload_digest,
    read_json,
    ref_for_file,
    relation_key_digest,
    relation_endpoint_refs,
    validate_admission_receipt,
    validate_graph_payload,
    validate_relation,
    validate_source_payload,
)
from admit_goal_participant_publication import (  # noqa: E402
    build_admission_receipt,
    build_source_payload,
    validate_publication,
)
from read_goal_participant_graph import read_goal_participant_graph  # noqa: E402
from validate_goal_participant_graph import validate_goal_participant_graph  # noqa: E402


class GoalParticipantGraphTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.example = read_json(
            ROOT / "mechanics/boundary-bridge/parts/participant-relations/examples/goal-participant-relation.example.json"
        )
        cls.relation_schema = read_json(ROOT / RELATION_SCHEMA_PATH)
        cls.source = read_json(ROOT / SOURCE_PATH)

    def test_complete_part_is_valid_and_generated_reader_is_current(self) -> None:
        validate_goal_participant_graph(ROOT)
        check_generated(ROOT, ROOT / GRAPH_PATH)
        self.assertEqual(build_graph_payload(ROOT), read_goal_participant_graph(ROOT))

    def test_source_is_empty_deferred_and_does_not_claim_no_participant(self) -> None:
        self.assertEqual(self.source["records"], [])
        self.assertEqual(self.source["evidence_class"], "empty_deferred")
        self.assertEqual(self.source["currentness"]["state"], "deferred")
        self.assertIn("No exact owner-published", self.source["currentness"]["reason"])

    def test_example_keeps_five_dimensions_separate(self) -> None:
        self.assertEqual(
            set(self.example["dimensions"]),
            {"identity", "obligation_role", "task_assignment", "model_realization", "runtime_incarnation"},
        )
        self.assertTrue(all(item["state"] == "present" for item in self.example["dimensions"].values()))
        endpoint_ids = {item["object_id"] for item in self.example["relation_key"]["endpoint_refs"]}
        self.assertIn("goal:public-example-001", endpoint_ids)
        self.assertIn("realization:public-example-001", endpoint_ids)
        self.assertNotIn("public-example-001", endpoint_ids)

    def test_dimension_owner_repositories_are_declared_and_enforced(self) -> None:
        record = copy.deepcopy(self.example)
        dimension = record["dimensions"]["model_realization"]
        dimension["owner_ref"]["owner_repo"] = "codex-app-server"
        for value_ref in dimension["value"].values():
            value_ref["owner_repo"] = "codex-app-server"
        record["relation_key"]["endpoint_refs"] = [
            json.loads(value) for value in sorted(relation_endpoint_refs(record))
        ]
        with self.assertRaises(GoalParticipantGraphError):
            validate_relation(record, relation_schema=self.relation_schema, label="wrong-model-owner")

    def test_ref_source_repository_must_match_owner_repository(self) -> None:
        dimension_mismatch = copy.deepcopy(self.example)
        dimension_mismatch["dimensions"]["model_realization"]["owner_ref"]["source_ref"] = (
            "repo:codex-app-server/model-identity/get"
        )
        dimension_mismatch["relation_key"]["endpoint_refs"] = [
            json.loads(value) for value in sorted(relation_endpoint_refs(dimension_mismatch))
        ]
        with self.assertRaises(GoalParticipantGraphError):
            validate_relation(
                dimension_mismatch,
                relation_schema=self.relation_schema,
                label="mismatched-model-source-owner",
            )

        scope_mismatch = copy.deepcopy(self.example)
        scope_mismatch["scope"]["goal_ref"]["source_ref"] = "repo:aoa-models/goal/get"
        scope_mismatch["relation_key"]["endpoint_refs"] = [
            json.loads(value) for value in sorted(relation_endpoint_refs(scope_mismatch))
        ]
        with self.assertRaises(GoalParticipantGraphError):
            validate_relation(scope_mismatch, relation_schema=self.relation_schema, label="mismatched-goal-source-owner")

        for source_ref in ("repo:codex-app-server", "repo:codex-app-server/"):
            missing_path = copy.deepcopy(self.example)
            missing_path["scope"]["goal_ref"]["source_ref"] = source_ref
            missing_path["relation_key"]["endpoint_refs"] = [
                json.loads(value) for value in sorted(relation_endpoint_refs(missing_path))
            ]
            with self.subTest(source_ref=source_ref), self.assertRaises(GoalParticipantGraphError):
                validate_relation(
                    missing_path,
                    relation_schema=self.relation_schema,
                    label="missing-source-path",
                )

    def test_nonpresent_dimension_has_no_value_or_fallback(self) -> None:
        record = copy.deepcopy(self.example)
        identity = record["dimensions"]["identity"]
        identity["state"] = "unknown"
        identity.pop("owner_ref")
        identity.pop("observed_at")
        identity.pop("value")
        record["relation_key"]["endpoint_refs"] = [
            ref
            for ref in record["relation_key"]["endpoint_refs"]
            if ref["object_id"] != "actor:public-example-001"
        ]
        validate_relation(record, relation_schema=self.relation_schema, label="unknown-dimension")
        self.assertNotIn("value", record["dimensions"]["identity"])
        self.assertNotIn("Participant N", json.dumps(record))

    def test_nonpresent_dimension_refs_still_obey_declared_owners(self) -> None:
        for ref_field in ("owner_ref", "evidence_refs"):
            record = copy.deepcopy(self.example)
            dimension = record["dimensions"]["model_realization"]
            dimension["state"] = "unknown"
            dimension.pop("value")
            dimension.pop("observed_at")
            if ref_field == "owner_ref":
                dimension["owner_ref"]["owner_repo"] = "codex-app-server"
            else:
                dimension.pop("owner_ref")
                dimension["evidence_refs"] = [copy.deepcopy(self.example["scope"]["goal_ref"])]
            record["relation_key"]["endpoint_refs"] = [
                json.loads(value) for value in sorted(relation_endpoint_refs(record))
            ]
            with self.subTest(ref_field=ref_field), self.assertRaises(GoalParticipantGraphError):
                validate_relation(record, relation_schema=self.relation_schema, label="unknown-model-owner")

    def test_heuristic_key_and_missing_digest_are_rejected(self) -> None:
        heuristic = copy.deepcopy(self.example)
        heuristic["relation_key"]["key_id"] = "rel:luna"
        with self.assertRaises(GoalParticipantGraphError):
            validate_relation(heuristic, relation_schema=self.relation_schema, label="heuristic-key")

        compact_heuristic = copy.deepcopy(self.example)
        compact_heuristic["relation_key"]["key_id"] = "rel:goal123"
        with self.assertRaises(GoalParticipantGraphError):
            validate_relation(compact_heuristic, relation_schema=self.relation_schema, label="compact-heuristic-key")

        missing_digest = copy.deepcopy(self.example)
        del missing_digest["dimensions"]["identity"]["owner_ref"]["content_digest"]
        with self.assertRaises(GoalParticipantGraphError):
            validate_relation(missing_digest, relation_schema=self.relation_schema, label="missing-digest")

    def test_scope_and_assignment_must_match_exactly(self) -> None:
        mismatched = copy.deepcopy(self.example)
        mismatched["dimensions"]["task_assignment"]["value"]["master_thread_ref"]["object_id"] = (
            "thread:other-example"
        )
        with self.assertRaises(GoalParticipantGraphError):
            validate_relation(mismatched, relation_schema=self.relation_schema, label="mismatched-scope")

    def test_pagination_and_currentness_are_preserved_fail_closed(self) -> None:
        paginated = copy.deepcopy(self.source)
        paginated["pagination"]["has_more"] = True
        paginated["currentness"]["state"] = "deferred"
        with self.assertRaises(GoalParticipantGraphError):
            validate_source_payload(ROOT, paginated)

        stale_empty = copy.deepcopy(self.source)
        stale_empty["currentness"]["state"] = "stale"
        with self.assertRaises(GoalParticipantGraphError):
            validate_source_payload(ROOT, stale_empty)

    def test_pagination_cursor_source_repository_must_match_owner(self) -> None:
        source = copy.deepcopy(self.source)
        source["pagination"]["has_more"] = True
        source["pagination"]["next_cursor_ref"] = copy.deepcopy(self.example["scope"]["goal_ref"])
        source["pagination"]["next_cursor_ref"]["source_ref"] = "repo:aoa-models/continuation-cursor"
        with self.assertRaises(GoalParticipantGraphError):
            validate_source_payload(ROOT, source)

    def test_optional_task_ref_obeys_task_assignment_owner(self) -> None:
        record = copy.deepcopy(self.example)
        record["dimensions"]["task_assignment"]["value"]["task_ref"] = copy.deepcopy(
            self.example["dimensions"]["model_realization"]["owner_ref"]
        )
        record["relation_key"]["endpoint_refs"] = [
            json.loads(value) for value in sorted(relation_endpoint_refs(record))
        ]
        with self.assertRaises(GoalParticipantGraphError):
            validate_relation(record, relation_schema=self.relation_schema, label="wrong-task-owner")

    def test_builder_handles_external_output_paths(self) -> None:
        original_argv = sys.argv
        try:
            with tempfile.TemporaryDirectory() as directory:
                output = Path(directory) / "goal-participant-graph.min.json"
                sys.argv = [
                    "build_goal_participant_graph.py",
                    "--root",
                    str(ROOT),
                    "--out",
                    str(output),
                ]
                self.assertEqual(build_graph_main(), 0)
                self.assertTrue(output.is_file())
                sys.argv = [
                    "build_goal_participant_graph.py",
                    "--root",
                    str(ROOT),
                    "--out",
                    str(output),
                    "--check",
                ]
                self.assertEqual(build_graph_main(), 0)
        finally:
            sys.argv = original_argv

    def _valid_publication(self) -> dict:
        record = copy.deepcopy(self.example)
        record["evidence_class"] = "owner_published"
        contract_ref = ref_for_file(
            root=ROOT,
            path=ROOT / CONTRACT_PATH,
            object_id="contract:goal-participant-relations",
            schema_version=CONTRACT_SCHEMA_VERSION,
        )
        record["relation_key"]["publisher_ref"] = contract_ref
        record["relation_key"]["content_digest"] = relation_key_digest(record["relation_key"])
        record["privacy_omissions"]["policy_ref"] = ref_for_file(
            root=ROOT,
            path=ROOT / CONTRACT_PATH,
            object_id="privacy:goal-participant-relations-v1",
            schema_version=CONTRACT_SCHEMA_VERSION,
        )
        record["claim_limit"] = "Owner-published exact relation only; no live or acceptance claim."
        producer_ref = {
            "owner_repo": "codex-app-server",
            "object_id": "producer:public-example-001",
            "source_ref": "repo:codex-app-server/participant-relation-producer",
            "schema_version": "codex_app_server_participant_producer_v1",
            "content_digest": "sha256:" + "1" * 64,
        }
        publication_ref = {
            "owner_repo": "codex-app-server",
            "object_id": "publication:public-example-001",
            "source_ref": "repo:codex-app-server/participant-relation-publication",
            "schema_version": "codex_app_server_participant_publication_v1",
            "content_digest": "sha256:" + "2" * 64,
        }
        publication = {
            "schema_version": "aoa_agents_goal_participant_relation_publication_v1",
            "kind": "aoa_agents_goal_participant_relation_publication",
            "evidence_class": "owner_published",
            "publisher_ref": contract_ref,
            "producer_ref": producer_ref,
            "publication_ref": publication_ref,
            "relation_contract_ref": contract_ref,
            "scope": copy.deepcopy(record["scope"]),
            "currentness": {
                "state": "current",
                "observed_at": "2026-08-23T20:00:00Z",
                "reason": "Exact owner publication observed at the producer boundary.",
            },
            "pagination": {
                "page_index": 0,
                "page_size": 100,
                "has_more": False,
                "next_cursor_ref": None,
            },
            "privacy_omissions": sorted(REQUIRED_PRIVACY_OMISSIONS),
            "records": [record],
            "claim_limit": "One exact owner publication; no live or acceptance claim.",
        }
        publication["payload_digest"] = publication_payload_digest(publication["records"])
        return publication

    @contextmanager
    def _temporary_nonempty_graph(self, publication: dict):
        with tempfile.TemporaryDirectory() as directory:
            temp_root = Path(directory)
            shutil.copytree(ROOT / "mechanics/boundary-bridge/parts/participant-relations", temp_root / "mechanics/boundary-bridge/parts/participant-relations")
            source = build_source_payload(temp_root, publication)
            (temp_root / SOURCE_PATH).write_text(compact_json(source), encoding="utf-8")
            graph = build_graph_payload(temp_root)
            (temp_root / GRAPH_PATH).write_text(compact_json(graph), encoding="utf-8")
            yield temp_root, graph

    def test_typed_publication_admits_without_changing_checked_in_source(self) -> None:
        publication = self._valid_publication()
        validate_publication(ROOT, publication)
        receipt = build_admission_receipt(ROOT, publication)
        self.assertEqual(receipt["admission_state"], "admitted")
        self.assertEqual(receipt["scope"], publication["scope"])
        source = build_source_payload(ROOT, publication)
        self.assertEqual(source["evidence_class"], "owner_published")
        self.assertEqual(source["admission_receipt"], receipt)
        self.assertEqual(self.source["evidence_class"], "empty_deferred")
        self.assertEqual(self.source["records"], [])

    def test_publication_rejects_synthetic_record(self) -> None:
        publication = self._valid_publication()
        publication["records"][0]["evidence_class"] = "synthetic_public_example"
        with self.assertRaises(GoalParticipantGraphError):
            validate_publication(ROOT, publication)

    def test_publication_rejects_relation_key_digest_drift(self) -> None:
        publication = self._valid_publication()
        publication["records"][0]["relation_key"]["content_digest"] = "sha256:" + "f" * 64
        with self.assertRaises(GoalParticipantGraphError):
            validate_publication(ROOT, publication)

    def test_publication_rejects_scope_mismatch_and_missing_owner_digest(self) -> None:
        mismatched_scope = self._valid_publication()
        mismatched_scope["scope"]["goal_ref"]["object_id"] = "goal:other-public-example"
        with self.assertRaises(GoalParticipantGraphError):
            validate_publication(ROOT, mismatched_scope)

        missing_digest = self._valid_publication()
        del missing_digest["records"][0]["dimensions"]["identity"]["owner_ref"]["content_digest"]
        missing_digest["payload_digest"] = publication_payload_digest(missing_digest["records"])
        with self.assertRaises(GoalParticipantGraphError):
            validate_publication(ROOT, missing_digest)

    def test_current_paginated_publication_stays_deferred(self) -> None:
        publication = self._valid_publication()
        publication["pagination"]["has_more"] = True
        with self.assertRaises(GoalParticipantGraphError):
            validate_publication(ROOT, publication)

        noninitial = self._valid_publication()
        noninitial["pagination"]["page_index"] = 1
        with self.assertRaises(GoalParticipantGraphError):
            validate_publication(ROOT, noninitial)

    def test_publication_rejects_invalid_currentness_date_time(self) -> None:
        publication = self._valid_publication()
        publication["currentness"]["observed_at"] = "not-a-date"
        with self.assertRaises(GoalParticipantGraphError):
            validate_publication(ROOT, publication)

    def test_claim_limits_cannot_widen_structural_admission(self) -> None:
        record = copy.deepcopy(self.example)
        record["claim_limit"] = "This proves liveness and Goal completion."
        with self.assertRaises(GoalParticipantGraphError):
            validate_relation(record, relation_schema=self.relation_schema, label="widened-record-claim")

        dimension = copy.deepcopy(self.example)
        dimension["dimensions"]["runtime_incarnation"]["claim_limit"] = "This establishes runtime health."
        with self.assertRaises(GoalParticipantGraphError):
            validate_relation(dimension, relation_schema=self.relation_schema, label="widened-dimension-claim")

        publication = self._valid_publication()
        publication["claim_limit"] = "This confirms live presence."
        with self.assertRaises(GoalParticipantGraphError):
            validate_publication(ROOT, publication)

        split_negation = self._valid_publication()
        split_negation["records"][0]["claim_limit"] = "This proves liveness and is not a draft."
        with self.assertRaises(GoalParticipantGraphError):
            validate_publication(ROOT, split_negation)

        punctuation_boundary = self._valid_publication()
        punctuation_boundary["claim_limit"] = "Not a draft: this proves liveness."
        with self.assertRaises(GoalParticipantGraphError):
            validate_publication(ROOT, punctuation_boundary)

        inflected_acceptance = self._valid_publication()
        inflected_acceptance["claim_limit"] = "The actor accepted the Goal."
        with self.assertRaises(GoalParticipantGraphError):
            validate_publication(ROOT, inflected_acceptance)

        inflected_completion = self._valid_publication()
        inflected_completion["claim_limit"] = "The Goal was completed."
        with self.assertRaises(GoalParticipantGraphError):
            validate_publication(ROOT, inflected_completion)

        receipt = build_admission_receipt(ROOT, self._valid_publication())
        receipt["claim_limit"] = "This proves Goal completion."
        receipt["receipt_id"] = admission_receipt_id(receipt)
        with self.assertRaises(GoalParticipantGraphError):
            validate_admission_receipt(ROOT, receipt)

    def test_publication_requires_distinct_scope_endpoints(self) -> None:
        publication = self._valid_publication()
        duplicate = copy.deepcopy(publication["scope"]["goal_ref"])
        publication["scope"]["goal_instance_ref"] = duplicate
        record = publication["records"][0]
        record["dimensions"]["task_assignment"]["value"]["goal_instance_ref"] = copy.deepcopy(duplicate)
        record["relation_key"]["endpoint_refs"] = [
            json.loads(value) for value in sorted(relation_endpoint_refs(record))
        ]
        record["relation_key"]["content_digest"] = relation_key_digest(record["relation_key"])
        publication["payload_digest"] = publication_payload_digest(publication["records"])
        with self.assertRaises(GoalParticipantGraphError):
            validate_publication(ROOT, publication)

        digest_only_duplicate = self._valid_publication()
        duplicate_master = copy.deepcopy(digest_only_duplicate["scope"]["goal_ref"])
        duplicate_master["content_digest"] = "sha256:" + "f" * 64
        digest_only_duplicate["scope"]["master_thread_ref"] = duplicate_master
        record = digest_only_duplicate["records"][0]
        record["scope"]["master_thread_ref"] = copy.deepcopy(duplicate_master)
        record["dimensions"]["task_assignment"]["value"]["master_thread_ref"] = copy.deepcopy(
            duplicate_master
        )
        record["relation_key"]["endpoint_refs"] = [
            json.loads(value) for value in sorted(relation_endpoint_refs(record))
        ]
        record["relation_key"]["content_digest"] = relation_key_digest(record["relation_key"])
        digest_only_duplicate["payload_digest"] = publication_payload_digest(digest_only_duplicate["records"])
        with self.assertRaises(GoalParticipantGraphError):
            validate_publication(ROOT, digest_only_duplicate)

    def test_owner_published_source_requires_receipt(self) -> None:
        source = build_source_payload(ROOT, self._valid_publication())
        source["admission_receipt"] = None
        with self.assertRaises(GoalParticipantGraphError):
            validate_source_payload(ROOT, source)

    def test_nonempty_graph_read_requires_and_binds_admission_receipt(self) -> None:
        with self._temporary_nonempty_graph(self._valid_publication()) as (temp_root, graph):
            graph["source"]["admission_receipt"] = None
            graph_path = temp_root / GRAPH_PATH
            graph_path.write_text(compact_json(graph), encoding="utf-8")
            with self.assertRaises(GoalParticipantGraphError):
                read_goal_participant_graph(temp_root)

            bound = copy.deepcopy(graph)
            bound["source"]["admission_receipt"] = copy.deepcopy(
                build_admission_receipt(ROOT, self._valid_publication())
            )
            bound["source"]["admission_receipt"]["relation_ids"] = ["rel-record:other"]
            bound["source"]["admission_receipt"]["receipt_id"] = admission_receipt_id(
                bound["source"]["admission_receipt"]
            )
            graph_path.write_text(compact_json(bound), encoding="utf-8")
            with self.assertRaises(GoalParticipantGraphError):
                read_goal_participant_graph(temp_root)

    def test_admission_receipt_identity_is_central_and_recomputed(self) -> None:
        receipt = build_admission_receipt(ROOT, self._valid_publication())
        self.assertEqual(receipt["receipt_id"], admission_receipt_id(receipt))
        tampered = copy.deepcopy(receipt)
        tampered["claim_limit"] = "A widened claim is not structural admission."
        with self.assertRaises(GoalParticipantGraphError):
            validate_admission_receipt(ROOT, tampered)

    def test_admission_receipt_rechecks_producer_provenance(self) -> None:
        publication = self._valid_publication()
        receipt = build_admission_receipt(ROOT, publication)

        same_ref = copy.deepcopy(receipt)
        same_ref["producer_ref"] = copy.deepcopy(same_ref["publication_ref"])
        same_ref["receipt_id"] = admission_receipt_id(same_ref)
        with self.assertRaises(GoalParticipantGraphError):
            validate_admission_receipt(ROOT, same_ref)

        different_owner = copy.deepcopy(receipt)
        different_owner["producer_ref"]["owner_repo"] = "aoa-agents"
        different_owner["receipt_id"] = admission_receipt_id(different_owner)
        with self.assertRaises(GoalParticipantGraphError):
            validate_admission_receipt(ROOT, different_owner)

    def test_currentness_watermark_source_repository_must_match_owner(self) -> None:
        publication = self._valid_publication()
        watermark = copy.deepcopy(publication["producer_ref"])
        watermark["source_ref"] = "repo:aoa-models/currentness-watermark"
        publication["currentness"]["source_watermark_ref"] = watermark
        with self.assertRaises(GoalParticipantGraphError):
            validate_publication(ROOT, publication)

    def test_source_rejects_duplicate_publisher_relation_key(self) -> None:
        source = build_source_payload(ROOT, self._valid_publication())
        duplicate = copy.deepcopy(source["records"][0])
        duplicate["relation_id"] = "rel-record:other"
        source["records"].append(duplicate)
        receipt = source["admission_receipt"]
        receipt["relation_ids"] = [record["relation_id"] for record in source["records"]]
        receipt["payload_digest"] = publication_payload_digest(source["records"])
        receipt["receipt_id"] = admission_receipt_id(receipt)
        with self.assertRaises(GoalParticipantGraphError):
            validate_source_payload(ROOT, source)

    def test_relation_privacy_omission_and_policy_parity_is_enforced(self) -> None:
        omissions_drift = self._valid_publication()
        omissions_drift["records"][0]["privacy_omissions"]["omitted_fields"] = ["human_display_name"]
        omissions_drift["payload_digest"] = publication_payload_digest(omissions_drift["records"])
        with self.assertRaises(GoalParticipantGraphError):
            validate_publication(ROOT, omissions_drift)

        policy_drift = self._valid_publication()
        policy_drift["records"][0]["privacy_omissions"]["policy_ref"]["content_digest"] = "sha256:" + "0" * 64
        policy_drift["payload_digest"] = publication_payload_digest(policy_drift["records"])
        with self.assertRaises(GoalParticipantGraphError):
            validate_publication(ROOT, policy_drift)

    def test_container_schemas_reference_the_exact_relation_schema(self) -> None:
        for schema_path in (SOURCE_SCHEMA_PATH, PUBLICATION_SCHEMA_PATH, GRAPH_SCHEMA_PATH):
            schema = read_json(ROOT / schema_path)
            self.assertEqual(schema["properties"]["records"]["items"], {"$ref": RELATION_SCHEMA_ID})

    def test_generated_read_rejects_stale_contract_or_source_content_digest(self) -> None:
        with self._temporary_nonempty_graph(self._valid_publication()) as (temp_root, graph):
            for ref_name in ("contract_ref", "source_ref"):
                tampered = copy.deepcopy(graph)
                tampered["source"][ref_name]["content_digest"] = "sha256:" + "0" * 64
                (temp_root / GRAPH_PATH).write_text(compact_json(tampered), encoding="utf-8")
                with self.assertRaises(GoalParticipantGraphError):
                    read_goal_participant_graph(temp_root)

    def test_generated_read_rejects_self_consistent_tampered_records(self) -> None:
        with self._temporary_nonempty_graph(self._valid_publication()) as (temp_root, graph):
            tampered = copy.deepcopy(graph)
            tampered["records"][0]["claim_limit"] = "A tampered graph is not source truth."
            receipt = tampered["source"]["admission_receipt"]
            receipt["payload_digest"] = publication_payload_digest(tampered["records"])
            receipt["receipt_id"] = admission_receipt_id(receipt)
            validate_graph_payload(temp_root, tampered)
            graph_path = temp_root / GRAPH_PATH
            graph_path.write_text(compact_json(tampered), encoding="utf-8")
            with self.assertRaises(GoalParticipantGraphError):
                read_goal_participant_graph(temp_root)

    def test_valid_publication_intake_and_generated_read_round_trip(self) -> None:
        with self._temporary_nonempty_graph(self._valid_publication()) as (temp_root, expected):
            actual = read_goal_participant_graph(temp_root)
            self.assertEqual(actual, expected)
            self.assertEqual(actual["currentness"]["state"], "current")
            self.assertIsNotNone(actual["source"]["admission_receipt"])


if __name__ == "__main__":
    unittest.main()
