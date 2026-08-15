#!/usr/bin/env python3
"""Explicitly append validated actor responsibility receipts to an owner log.

Publication is intentionally separate from compilation.  The default path is
the owner-local live receipt feed, while tests and operators can provide a
dedicated local JSONL path.  Existing log corruption fails closed.
"""

from __future__ import annotations

import argparse
from contextlib import contextmanager
import json
import os
from pathlib import Path
import sys
from typing import Any

try:
    import fcntl
except ImportError:  # pragma: no cover - the owner publisher runs on POSIX hosts
    fcntl = None  # type: ignore[assignment]

try:
    from compile_actor_responsibility_receipt import (
        ActorResponsibilityReceiptError,
        validate_receipt,
    )
except ModuleNotFoundError:  # pragma: no cover - supports direct module loading in tests
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from compile_actor_responsibility_receipt import (  # type: ignore[no-redef]
        ActorResponsibilityReceiptError,
        validate_receipt,
    )


REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_LOG_PATH = REPO_ROOT / ".aoa" / "live_receipts" / "actor-responsibility-executions.jsonl"


class ActorResponsibilityReceiptPublishError(ValueError):
    """A receipt or existing log line is not safe to publish."""


def _load_json(path: Path, *, label: str) -> Any:
    location = path.resolve()
    if path.is_symlink() or not location.is_file():
        raise ActorResponsibilityReceiptPublishError(f"{label} must be a regular non-symlink file: {path}")
    try:
        return json.loads(location.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ActorResponsibilityReceiptPublishError(f"{label} is not valid JSON") from exc


def _validate(receipt: Any, *, location: str) -> dict[str, Any]:
    if not isinstance(receipt, dict):
        raise ActorResponsibilityReceiptPublishError(f"{location}: receipt must be an object")
    try:
        validate_receipt(receipt)
    except ActorResponsibilityReceiptError as exc:
        raise ActorResponsibilityReceiptPublishError(f"{location}: {exc}") from exc
    return receipt


def load_receipts(paths: list[Path]) -> list[dict[str, Any]]:
    """Load and validate JSON, JSON arrays, or JSONL receipt inputs."""

    if not paths:
        raise ActorResponsibilityReceiptPublishError("no receipt input files were provided")
    receipts: list[dict[str, Any]] = []
    for path in paths:
        if path.suffix == ".jsonl":
            location = path.resolve()
            if path.is_symlink() or not location.is_file():
                raise ActorResponsibilityReceiptPublishError(f"receipt input must be a regular non-symlink file: {path}")
            try:
                lines = location.read_text(encoding="utf-8").splitlines()
            except (OSError, UnicodeDecodeError) as exc:
                raise ActorResponsibilityReceiptPublishError(f"{path}: cannot read JSONL input") from exc
            for line_number, raw_line in enumerate(lines, start=1):
                line = raw_line.strip()
                if not line:
                    continue
                try:
                    item = json.loads(line)
                except json.JSONDecodeError as exc:
                    raise ActorResponsibilityReceiptPublishError(f"{path}:{line_number}: invalid JSON") from exc
                receipts.append(_validate(item, location=f"{path}:{line_number}"))
            continue
        candidate = _load_json(path, label="receipt input")
        if isinstance(candidate, dict):
            receipts.append(_validate(candidate, location=str(path)))
            continue
        if not isinstance(candidate, list):
            raise ActorResponsibilityReceiptPublishError(f"{path}: receipt input must be an object, array, or JSONL file")
        for index, item in enumerate(candidate):
            receipts.append(_validate(item, location=f"{path}[{index}]"))
    return receipts


def load_existing_ids(path: Path) -> set[str]:
    """Validate every existing line before returning its event IDs."""

    if not path.exists():
        return set()
    if path.is_symlink() or not path.is_file():
        raise ActorResponsibilityReceiptPublishError("existing log must be a regular non-symlink file")
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError) as exc:
        raise ActorResponsibilityReceiptPublishError("existing log cannot be read") from exc
    event_ids: set[str] = set()
    for line_number, raw_line in enumerate(lines, start=1):
        line = raw_line.strip()
        if not line:
            continue
        try:
            candidate = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ActorResponsibilityReceiptPublishError(f"existing log line {line_number} is not valid JSON") from exc
        receipt = _validate(candidate, location=f"{path}:{line_number}")
        event_ids.add(receipt["event_id"])
    return event_ids


def _needs_line_separator(path: Path) -> bool:
    """Return whether an existing JSONL file needs a newline before append."""

    try:
        if path.stat().st_size == 0:
            return False
        with path.open("rb") as handle:
            handle.seek(-1, os.SEEK_END)
            return handle.read(1) != b"\n"
    except FileNotFoundError:
        return False
    except OSError as exc:
        raise ActorResponsibilityReceiptPublishError("existing log cannot be inspected") from exc


def lock_path_for(log_path: Path) -> Path:
    """Return the owner-local advisory lock path for one receipt log."""

    return log_path.with_name(log_path.name + ".lock")


@contextmanager
def _exclusive_log_lock(log_path: Path):
    """Serialize all publisher reads and appends for one owner-local log."""

    if fcntl is None:
        raise ActorResponsibilityReceiptPublishError(
            "concurrency-safe publication requires a POSIX advisory-lock host"
        )
    if log_path.is_symlink():
        raise ActorResponsibilityReceiptPublishError("log path must not be a symlink")
    log_path.parent.mkdir(parents=True, exist_ok=True)
    lock_path = lock_path_for(log_path)
    if lock_path.is_symlink():
        raise ActorResponsibilityReceiptPublishError("log lock path must not be a symlink")
    try:
        with lock_path.open("a+", encoding="utf-8") as lock_handle:
            fcntl.flock(lock_handle.fileno(), fcntl.LOCK_EX)
            try:
                yield
            finally:
                fcntl.flock(lock_handle.fileno(), fcntl.LOCK_UN)
    except OSError as exc:
        raise ActorResponsibilityReceiptPublishError("could not acquire actor responsibility receipt log lock") from exc


def append_new_receipts(*, log_path: Path, receipts: list[dict[str, Any]]) -> tuple[int, int]:
    """Validate, deduplicate, then append receipts to one JSONL log."""

    for index, receipt in enumerate(receipts):
        _validate(receipt, location=f"input[{index}]")
    with _exclusive_log_lock(log_path):
        existing_ids = load_existing_ids(log_path)
        needs_separator = _needs_line_separator(log_path)
        appendable: list[dict[str, Any]] = []
        skipped = 0
        for receipt in receipts:
            event_id = receipt["event_id"]
            if event_id in existing_ids:
                skipped += 1
                continue
            existing_ids.add(event_id)
            appendable.append(receipt)
        if not appendable:
            return 0, skipped
        try:
            with log_path.open("a", encoding="utf-8") as handle:
                if needs_separator:
                    handle.write("\n")
                for receipt in appendable:
                    handle.write(json.dumps(receipt, ensure_ascii=False, sort_keys=True) + "\n")
                handle.flush()
                os.fsync(handle.fileno())
        except OSError as exc:
            raise ActorResponsibilityReceiptPublishError("could not append actor responsibility receipts") from exc
        return len(appendable), skipped


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--input", action="append", default=[], help="JSON or JSONL receipt input; may be repeated")
    result.add_argument("--log-path", default=str(DEFAULT_LOG_PATH), help="Owner-local JSONL feed path")
    return result


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        receipts = load_receipts([Path(path).expanduser() for path in args.input])
        appended, skipped = append_new_receipts(
            log_path=Path(args.log_path).expanduser(),
            receipts=receipts,
        )
    except (ActorResponsibilityReceiptPublishError, OSError, ValueError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, sort_keys=True))
        return 2
    print(json.dumps({"ok": True, "appended": appended, "skipped": skipped}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
