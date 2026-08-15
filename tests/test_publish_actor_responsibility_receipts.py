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


def _publish_from_independent_process(log_path: str, receipt: dict[str, object]) -> tuple[int, int]:
    return PUBLISHER.append_new_receipts(log_path=Path(log_path), receipts=[receipt])


class ActorResponsibilityReceiptPublisherTests(unittest.TestCase):
    def receipt(self, directory: Path) -> dict[str, object]:
        result_path = directory / "summon-result.json"
        write_result(result_path, summon_result())
        return COMPILER.compile_actor_responsibility_receipt(
            summon_result_path=result_path,
            observed_at="2026-08-14T12:00:00Z",
            run_ref="run:actor-receipt-test",
            session_ref="session:actor-receipt-test",
            actor_ref="incarnation:actor",
            object_ref={
                "repo": "aoa-agents",
                "kind": "actor-responsibility-execution",
                "id": "summon-request:actor",
                "version": "v1",
            },
        )

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


if __name__ == "__main__":
    unittest.main()
