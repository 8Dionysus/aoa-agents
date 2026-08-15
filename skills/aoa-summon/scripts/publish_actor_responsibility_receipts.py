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


DEFAULT_LOG_RELATIVE_PATH = Path(
    ".aoa/live_receipts/actor-responsibility-execution-receipts.jsonl"
)


class ActorResponsibilityReceiptPublishError(ValueError):
    """A receipt or existing log line is not safe to publish."""


def _validated_owner_root(root: Path, *, label: str) -> Path:
    candidate = root.expanduser()
    if not candidate.is_absolute():
        raise ActorResponsibilityReceiptPublishError(f"{label} must be an absolute path")
    candidate = candidate.resolve()
    if not candidate.is_dir():
        raise ActorResponsibilityReceiptPublishError(f"{label} is not a directory: {candidate}")
    manifest_path = candidate / "skills" / "port.manifest.json"
    skill_path = candidate / "skills" / "aoa-summon" / "SKILL.md"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ActorResponsibilityReceiptPublishError(
            f"{label} does not expose a valid aoa-agents skill-home manifest"
        ) from exc
    bundles = manifest.get("bundles") if isinstance(manifest, dict) else None
    if not (
        isinstance(manifest, dict)
        and manifest.get("owner_repo") == "aoa-agents"
        and isinstance(bundles, list)
        and any(
            isinstance(bundle, dict)
            and bundle.get("name") == "aoa-summon"
            and bundle.get("path") == "skills/aoa-summon"
            for bundle in bundles
        )
        and skill_path.is_file()
    ):
        raise ActorResponsibilityReceiptPublishError(
            f"{label} is not the canonical aoa-agents owner root: {candidate}"
        )
    return candidate


def _owner_root_from_source_handle(bundle_dir: Path) -> Path | None:
    handle_path = bundle_dir / ".aoa-skill-source.json"
    if not handle_path.exists():
        return None
    if handle_path.is_symlink() or not handle_path.is_file():
        raise ActorResponsibilityReceiptPublishError("same-bundle source handle is not a regular file")
    try:
        handle = json.loads(handle_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ActorResponsibilityReceiptPublishError("same-bundle source handle is not valid JSON") from exc
    if not isinstance(handle, dict):
        raise ActorResponsibilityReceiptPublishError("same-bundle source handle must be an object")
    source_path = handle.get("source_path")
    schema_version = handle.get("schema_version")
    if (
        schema_version not in {"aoa_skill_source_receipt_v1", "aoa_skill_source_receipt_v2"}
        or handle.get("name") != "aoa-summon"
        or handle.get("owner_repo") != "aoa-agents"
        or handle.get("version") != "0.4.0"
        or not isinstance(handle.get("owner_root"), str)
        or not isinstance(source_path, str)
        or not source_path
        or Path(source_path).is_absolute()
        or ".." in Path(source_path).parts
        or source_path != "skills/aoa-summon"
    ):
        raise ActorResponsibilityReceiptPublishError("same-bundle source handle is not an aoa-summon owner handle")
    if schema_version == "aoa_skill_source_receipt_v2":
        for field in (
            "digest",
            "source_fingerprint",
            "source_fingerprint_scope",
            "prompt_description_sha256",
        ):
            if not isinstance(handle.get(field), str) or not handle[field]:
                raise ActorResponsibilityReceiptPublishError(
                    f"same-bundle source handle v2 field {field} is missing"
                )
        if "capability_graph_hash" in handle and (
            not isinstance(handle["capability_graph_hash"], str)
            or not handle["capability_graph_hash"]
        ):
            raise ActorResponsibilityReceiptPublishError(
                "same-bundle source handle v2 capability_graph_hash is invalid"
            )
    return _validated_owner_root(Path(handle["owner_root"]), label="source-handle owner_root")


def _resolve_owner_root(
    explicit_root: str | Path | None = None,
    *,
    script_path: str | Path | None = None,
) -> Path:
    """Resolve the canonical owner root without trusting the install catalog path."""

    if explicit_root is not None:
        return _validated_owner_root(Path(explicit_root), label="--owner-root")
    script = Path(script_path or __file__).resolve()
    bundle_dir = script.parent.parent
    handle_root = _owner_root_from_source_handle(bundle_dir)
    if handle_root is not None:
        return handle_root
    source_root = bundle_dir.parent.parent
    try:
        return _validated_owner_root(source_root, label="source-tree owner root")
    except ActorResponsibilityReceiptPublishError as exc:
        raise ActorResponsibilityReceiptPublishError(
            "canonical owner root is unavailable; use --owner-root or a valid same-bundle source handle"
        ) from exc


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
        supersedes = receipt.get("supersedes")
        if supersedes is not None and supersedes not in event_ids:
            raise ActorResponsibilityReceiptPublishError(
                f"existing log line {line_number} supersedes unknown prior event {supersedes}"
            )
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
        known_ids = set(existing_ids)
        needs_separator = _needs_line_separator(log_path)
        appendable: list[dict[str, Any]] = []
        skipped = 0
        for receipt in receipts:
            event_id = receipt["event_id"]
            if event_id in known_ids:
                skipped += 1
                continue
            supersedes = receipt.get("supersedes")
            if supersedes is not None and supersedes not in known_ids:
                raise ActorResponsibilityReceiptPublishError(
                    f"input receipt {event_id} supersedes unknown prior event {supersedes}"
                )
            known_ids.add(event_id)
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
    result.add_argument("--owner-root", help="Explicit canonical aoa-agents owner root when no source handle is available")
    result.add_argument("--log-path", help="Owner-local JSONL feed path")
    return result


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        owner_root = _resolve_owner_root(args.owner_root)
        receipts = load_receipts([Path(path).expanduser() for path in args.input])
        appended, skipped = append_new_receipts(
            log_path=(
                Path(args.log_path).expanduser()
                if args.log_path
                else owner_root / DEFAULT_LOG_RELATIVE_PATH
            ),
            receipts=receipts,
        )
    except (ActorResponsibilityReceiptPublishError, OSError, ValueError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, sort_keys=True))
        return 2
    print(json.dumps({"ok": True, "appended": appended, "skipped": skipped}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
