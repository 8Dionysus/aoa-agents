from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor
import importlib.util
import json
import multiprocessing
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
COMPILER_PATH = ROOT / "skills/aoa-summon/scripts/compile_actor_responsibility_receipt.py"
PUBLISHER_PATH = ROOT / "skills/aoa-summon/scripts/publish_actor_responsibility_receipts.py"

compiler_spec = importlib.util.spec_from_file_location("actor_receipt_compiler_for_publisher", COMPILER_PATH)
assert compiler_spec is not None and compiler_spec.loader is not None
COMPILER = importlib.util.module_from_spec(compiler_spec)
compiler_spec.loader.exec_module(COMPILER)

publisher_spec = importlib.util.spec_from_file_location("actor_receipt_publisher", PUBLISHER_PATH)
assert publisher_spec is not None and publisher_spec.loader is not None
PUBLISHER = importlib.util.module_from_spec(publisher_spec)
publisher_spec.loader.exec_module(PUBLISHER)

sys.path.insert(0, str(Path(__file__).parent))
from test_compile_actor_responsibility_receipt import summon_result, write_result  # noqa: E402


PRIOR_EVENT_ID = "actor-responsibility-execution:" + "a" * 64


def _publish_from_independent_process(log_path: str, receipt: dict[str, object]) -> tuple[int, int]:
    return PUBLISHER.append_new_receipts(log_path=Path(log_path), receipts=[receipt])


class ActorResponsibilityReceiptPublisherTests(unittest.TestCase):
    def receipt(self, directory: Path, **overrides: object) -> dict[str, object]:
        result_path = directory / "summon-result.json"
        write_result(result_path, summon_result())
        values: dict[str, object] = {
            "summon_result_path": result_path,
            "result_artifact_ref": "summon-result:actor",
            "observed_at": "2026-08-14T12:00:00Z",
            "run_ref": "run:actor-receipt-test",
            "session_ref": "session:actor-receipt-test",
            "actor_ref": "incarnation:actor",
            "object_ref": {
                "repo": "aoa-agents",
                "kind": "actor-responsibility-execution",
                "id": "summon-request:actor",
                "version": "v1",
            },
        }
        values.update(overrides)
        return COMPILER.compile_actor_responsibility_receipt(**values)

    def test_append_is_explicit_and_event_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            receipt = self.receipt(root)
            log_path = root / "live" / "actor.jsonl"
            appended, skipped = PUBLISHER.append_new_receipts(
                log_path=log_path,
                receipts=[receipt, receipt],
            )
            self.assertEqual((appended, skipped), (1, 1))
            self.assertEqual(len(log_path.read_text(encoding="utf-8").splitlines()), 1)
            appended, skipped = PUBLISHER.append_new_receipts(log_path=log_path, receipts=[receipt])
            self.assertEqual((appended, skipped), (0, 1))
            self.assertEqual(len(log_path.read_text(encoding="utf-8").splitlines()), 1)

    def test_invalid_input_is_rejected_before_append(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            receipt = self.receipt(root)
            invalid = dict(receipt)
            invalid["payload"] = {"schema_version": "forged"}
            log_path = root / "actor.jsonl"
            with self.assertRaises(PUBLISHER.ActorResponsibilityReceiptPublishError):
                PUBLISHER.append_new_receipts(log_path=log_path, receipts=[invalid])
            self.assertFalse(log_path.exists())

    def test_forged_event_id_is_rejected_before_append(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            receipt = self.receipt(root)
            receipt["event_id"] = "actor-responsibility-execution:forged"
            with self.assertRaises(PUBLISHER.ActorResponsibilityReceiptPublishError):
                PUBLISHER.append_new_receipts(log_path=root / "actor.jsonl", receipts=[receipt])

    def test_supersedes_requires_an_existing_prior_event(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            receipt = self.receipt(root, supersedes=PRIOR_EVENT_ID)
            with self.assertRaisesRegex(
                PUBLISHER.ActorResponsibilityReceiptPublishError,
                "unknown prior event",
            ):
                PUBLISHER.append_new_receipts(log_path=root / "actor.jsonl", receipts=[receipt])

    def test_existing_feed_rejects_a_dangling_supersedes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            dangling = self.receipt(root, supersedes=PRIOR_EVENT_ID)
            log_path = root / "actor.jsonl"
            log_path.write_text(json.dumps(dangling, sort_keys=True) + "\n", encoding="utf-8")
            with self.assertRaisesRegex(
                PUBLISHER.ActorResponsibilityReceiptPublishError,
                "existing log line 1 supersedes unknown prior event",
            ):
                PUBLISHER.append_new_receipts(log_path=log_path, receipts=[self.receipt(root)])

    def test_existing_feed_rejects_a_forward_supersedes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            future = self.receipt(
                root,
                result_artifact_ref="summon-result:future",
                observed_at="2026-08-14T12:00:02Z",
                run_ref="run:actor-receipt-test-future",
                session_ref="session:actor-receipt-test-future",
                actor_ref="incarnation:actor-future",
                object_ref={
                    "repo": "aoa-agents",
                    "kind": "actor-responsibility-execution",
                    "id": "summon-request:future",
                    "version": "v1",
                },
            )
            forward = self.receipt(
                root,
                result_artifact_ref="summon-result:forward",
                observed_at="2026-08-14T12:00:01Z",
                run_ref="run:actor-receipt-test-forward",
                session_ref="session:actor-receipt-test-forward",
                actor_ref="incarnation:actor-forward",
                object_ref={
                    "repo": "aoa-agents",
                    "kind": "actor-responsibility-execution",
                    "id": "summon-request:forward",
                    "version": "v1",
                },
                supersedes=future["event_id"],
            )
            log_path = root / "actor.jsonl"
            log_path.write_text(
                json.dumps(forward, sort_keys=True) + "\n" + json.dumps(future, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(
                PUBLISHER.ActorResponsibilityReceiptPublishError,
                "existing log line 1 supersedes unknown prior event",
            ):
                PUBLISHER.append_new_receipts(log_path=log_path, receipts=[self.receipt(root)])

    def test_supersedes_accepts_an_existing_prior_event(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            base = self.receipt(root)
            repair = self.receipt(
                root,
                result_artifact_ref="summon-result:actor-2",
                observed_at="2026-08-14T12:00:01Z",
                run_ref="run:actor-receipt-test-2",
                session_ref="session:actor-receipt-test-2",
                actor_ref="incarnation:actor-2",
                object_ref={
                    "repo": "aoa-agents",
                    "kind": "actor-responsibility-execution",
                    "id": "summon-request:actor-2",
                    "version": "v1",
                },
                supersedes=base["event_id"],
            )
            log_path = root / "actor.jsonl"
            self.assertEqual(PUBLISHER.append_new_receipts(log_path=log_path, receipts=[base]), (1, 0))
            self.assertEqual(PUBLISHER.append_new_receipts(log_path=log_path, receipts=[repair]), (1, 0))
            self.assertEqual(len(log_path.read_text(encoding="utf-8").splitlines()), 2)

    def test_publisher_rejects_mismatched_runtime_state_before_append(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            receipt = self.receipt(root)
            receipt["payload"]["execution"]["runtime_state"] = "failed"
            log_path = root / "actor.jsonl"
            with self.assertRaisesRegex(
                PUBLISHER.ActorResponsibilityReceiptPublishError,
                "runtime_state",
            ):
                PUBLISHER.append_new_receipts(log_path=log_path, receipts=[receipt])
            self.assertFalse(log_path.exists())

    def test_malformed_existing_log_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            receipt = self.receipt(root)
            log_path = root / "actor.jsonl"
            log_path.write_text("{not-json}\n", encoding="utf-8")
            with self.assertRaisesRegex(PUBLISHER.ActorResponsibilityReceiptPublishError, "not valid JSON"):
                PUBLISHER.append_new_receipts(log_path=log_path, receipts=[receipt])
            self.assertEqual(log_path.read_text(encoding="utf-8"), "{not-json}\n")

    def test_append_repairs_a_valid_unterminated_jsonl_line(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            receipt = self.receipt(root)
            log_path = root / "actor.jsonl"
            log_path.write_text(json.dumps(receipt, sort_keys=True), encoding="utf-8")
            result_path = root / "summon-result.json"
            appended_receipt = COMPILER.compile_actor_responsibility_receipt(
                summon_result_path=result_path,
                result_artifact_ref="summon-result:actor-2",
                observed_at="2026-08-14T12:00:01Z",
                run_ref="run:actor-receipt-test-2",
                session_ref="session:actor-receipt-test-2",
                actor_ref="incarnation:actor-2",
                object_ref={
                    "repo": "aoa-agents",
                    "kind": "actor-responsibility-execution",
                    "id": "summon-request:actor-2",
                    "version": "v1",
                },
            )
            appended, skipped = PUBLISHER.append_new_receipts(
                log_path=log_path,
                receipts=[appended_receipt],
            )
            self.assertEqual((appended, skipped), (1, 0))
            lines = log_path.read_text(encoding="utf-8").splitlines()
            self.assertEqual(len(lines), 2)
            json.loads(lines[0])
            json.loads(lines[1])

    def test_cli_rejects_symlink_log_path(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            receipt = self.receipt(root)
            input_path = root / "receipt.json"
            input_path.write_text(json.dumps(receipt), encoding="utf-8")
            real_log = root / "real.jsonl"
            real_log.write_text("", encoding="utf-8")
            symlink_log = root / "link.jsonl"
            symlink_log.symlink_to(real_log)
            completed = subprocess.run(
                [
                    sys.executable,
                    str(PUBLISHER_PATH),
                    "--input",
                    str(input_path),
                    "--log-path",
                    str(symlink_log),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(completed.returncode, 2)
            self.assertIn("symlink", completed.stdout)
            self.assertEqual(real_log.read_text(encoding="utf-8"), "")

    def test_input_loader_rejects_malformed_jsonl_line(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "input.jsonl"
            path.write_text("not-json\n", encoding="utf-8")
            with self.assertRaises(PUBLISHER.ActorResponsibilityReceiptPublishError):
                PUBLISHER.load_receipts([path])

    def test_independent_publishers_share_lock_and_deduplicate(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            receipt = self.receipt(root)
            log_path = root / "actor.jsonl"
            context = multiprocessing.get_context("fork")
            with ProcessPoolExecutor(max_workers=2, mp_context=context) as pool:
                futures = [
                    pool.submit(_publish_from_independent_process, str(log_path), receipt)
                    for _ in range(2)
                ]
                results = [future.result() for future in futures]
            self.assertCountEqual(results, [(1, 0), (0, 1)])
            self.assertEqual(len(log_path.read_text(encoding="utf-8").splitlines()), 1)
            self.assertTrue(PUBLISHER.lock_path_for(log_path).is_file())

    def test_default_owner_root_uses_source_tree_contract(self) -> None:
        self.assertEqual(PUBLISHER._resolve_owner_root(), ROOT.resolve())

    def test_installed_catalog_requires_source_handle_or_explicit_owner_root(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            bundle_dir = Path(directory) / "catalog" / "skills" / "aoa-summon"
            script_path = bundle_dir / "scripts" / "publish_actor_responsibility_receipts.py"
            with self.assertRaisesRegex(PUBLISHER.ActorResponsibilityReceiptPublishError, "canonical owner root"):
                PUBLISHER._resolve_owner_root(script_path=script_path)

            bundle_dir.mkdir(parents=True)
            (bundle_dir / ".aoa-skill-source.json").write_text(
                json.dumps(
                    {
                        "schema_version": "aoa_skill_source_receipt_v2",
                        "name": "aoa-summon",
                        "owner_repo": "aoa-agents",
                        "owner_root": str(ROOT.resolve()),
                        "source_path": "skills/aoa-summon",
                        "version": "0.4.0",
                        "digest": "bundle-digest",
                        "source_fingerprint": "source-fingerprint",
                        "source_fingerprint_scope": "authored-capability-package-v1-excludes-generated-projections",
                        "prompt_description_sha256": "prompt-description-hash",
                    }
                ),
                encoding="utf-8",
            )
            self.assertEqual(PUBLISHER._resolve_owner_root(script_path=script_path), ROOT.resolve())

    def test_installed_catalog_rejects_incomplete_or_mismatched_source_handle(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            bundle_dir = Path(directory) / "catalog" / "skills" / "aoa-summon"
            bundle_dir.mkdir(parents=True)
            script_path = bundle_dir / "scripts" / "publish_actor_responsibility_receipts.py"
            handle = {
                "schema_version": "aoa_skill_source_receipt_v2",
                "name": "aoa-summon",
                "owner_repo": "aoa-agents",
                "owner_root": str(ROOT.resolve()),
                "source_path": "skills/aoa-summon",
                "version": "0.4.0",
                "digest": "bundle-digest",
                "source_fingerprint": "source-fingerprint",
                "source_fingerprint_scope": "authored-capability-package-v1-excludes-generated-projections",
                "prompt_description_sha256": "prompt-description-hash",
            }
            handle_path = bundle_dir / ".aoa-skill-source.json"
            for field in (
                "version",
                "digest",
                "source_fingerprint",
                "source_fingerprint_scope",
                "prompt_description_sha256",
            ):
                with self.subTest(field=field):
                    invalid = dict(handle)
                    invalid.pop(field)
                    handle_path.write_text(json.dumps(invalid), encoding="utf-8")
                    with self.assertRaisesRegex(PUBLISHER.ActorResponsibilityReceiptPublishError, "source handle"):
                        PUBLISHER._resolve_owner_root(script_path=script_path)

            invalid = dict(handle)
            invalid["version"] = "0.3.0"
            handle_path.write_text(json.dumps(invalid), encoding="utf-8")
            with self.assertRaisesRegex(PUBLISHER.ActorResponsibilityReceiptPublishError, "source handle"):
                PUBLISHER._resolve_owner_root(script_path=script_path)

            invalid = dict(handle)
            invalid["capability_graph_hash"] = None
            handle_path.write_text(json.dumps(invalid), encoding="utf-8")
            with self.assertRaisesRegex(PUBLISHER.ActorResponsibilityReceiptPublishError, "capability_graph_hash"):
                PUBLISHER._resolve_owner_root(script_path=script_path)


if __name__ == "__main__":
    unittest.main()
