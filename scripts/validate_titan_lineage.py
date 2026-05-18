#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


VALID_STATUSES = {"active", "dormant", "retired", "fallen", "quarantined", "succeeded", "archived"}
VALID_EVENTS = {
    "first_appearance",
    "summon",
    "incarnation_opened",
    "incarnation_closed",
    "gate_opened",
    "fall",
    "lesson_recorded",
    "successor_named",
    "retired",
    "reinstated",
    "remembrance",
}
REQUIRED_EVENT_FIELDS = ("event_id", "event_type", "bearer_id", "occurred_at", "summary", "source_ref")


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--roles", required=True, type=Path)
    ap.add_argument("--bearers", required=True, type=Path)
    ap.add_argument("--ledger", required=True, type=Path)
    args = ap.parse_args()

    roles_doc = load(args.roles)
    bearers_doc = load(args.bearers)
    ledger_doc = load(args.ledger)

    errors: list[str] = []

    roles = {r.get("role_key"): r for r in roles_doc.get("role_classes", [])}
    if not roles:
        errors.append("no role_classes found")

    bearers_by_name: dict[str, list[dict]] = {}
    seen_bearers: dict[str, dict] = {}

    for b in bearers_doc.get("bearers", []):
        bid = b.get("bearer_id")
        name = b.get("titan_name")
        role_key = b.get("role_key")
        status = b.get("status")
        mp = b.get("memory_policy") or {}
        if not bid:
            errors.append("bearer missing bearer_id")
            continue
        if bid in seen_bearers:
            errors.append(f"duplicate bearer_id: {bid}")
        seen_bearers[bid] = b
        if role_key not in roles:
            errors.append(f"bearer {bid} references unknown role_key {role_key!r}")
        if status not in VALID_STATUSES:
            errors.append(f"bearer {bid} has invalid status {status!r}")
        if not name:
            errors.append(f"bearer {bid} missing titan_name")
        else:
            bearers_by_name.setdefault(name, []).append(b)
        if mp.get("remember_as_person") is not True:
            errors.append(f"bearer {bid} must remember_as_person=true")
        if mp.get("allow_name_reuse") is True and not b.get("successor_of"):
            errors.append(f"bearer {bid} allows name reuse without successor_of")

    for bid, b in seen_bearers.items():
        predecessor_id = b.get("successor_of")
        if predecessor_id and predecessor_id not in seen_bearers:
            errors.append(f"bearer {bid} references unknown successor_of {predecessor_id!r}")

    for name, name_bearers in bearers_by_name.items():
        active_count = sum(1 for b in name_bearers if b.get("status") == "active")
        if active_count > 1:
            errors.append(f"duplicate active titan_name: {name}")
        if len(name_bearers) <= 1:
            continue

        root_bearers = [b for b in name_bearers if not b.get("successor_of")]
        if len(root_bearers) != 1:
            errors.append(f"duplicate titan_name without a single root bearer: {name}")

        for b in name_bearers:
            predecessor_id = b.get("successor_of")
            if not predecessor_id:
                continue
            predecessor = seen_bearers.get(predecessor_id)
            lineage_reuse_allowed = (
                (b.get("memory_policy") or {}).get("allow_name_reuse") is True
                and predecessor is not None
                and predecessor.get("titan_name") == name
            )
            if not lineage_reuse_allowed:
                errors.append(f"duplicate titan_name without explicit lineage relation: {name}")

        same_name_bearer_ids = {b.get("bearer_id") for b in name_bearers}
        successor_ids_by_predecessor: dict[str, list[str]] = {}
        for b in name_bearers:
            bearer_id = b.get("bearer_id")
            predecessor_id = b.get("successor_of")
            if (
                isinstance(bearer_id, str)
                and isinstance(predecessor_id, str)
                and predecessor_id in same_name_bearer_ids
            ):
                successor_ids_by_predecessor.setdefault(predecessor_id, []).append(bearer_id)

        for predecessor_id, successor_ids in successor_ids_by_predecessor.items():
            if len(successor_ids) > 1:
                errors.append(
                    f"duplicate titan_name successor chain branches for {name}: "
                    f"{predecessor_id} -> {sorted(successor_ids)}"
                )

        if len(root_bearers) == 1:
            root_id = root_bearers[0].get("bearer_id")
            visited_ids: set[str] = set()
            current_id = root_id if isinstance(root_id, str) else None
            while current_id and current_id not in visited_ids:
                visited_ids.add(current_id)
                next_ids = successor_ids_by_predecessor.get(current_id, [])
                current_id = next_ids[0] if len(next_ids) == 1 else None
            if len(visited_ids) != len(name_bearers):
                errors.append(f"duplicate titan_name successor chain is not linear from root: {name}")

    event_ids: set[str] = set()
    for ev in ledger_doc.get("events", []):
        eid = ev.get("event_id")
        etype = ev.get("event_type")
        bid = ev.get("bearer_id")
        event_label = eid or "<missing>"
        for field in REQUIRED_EVENT_FIELDS:
            if not ev.get(field):
                errors.append(f"event {event_label} missing required field {field}")
        if eid and eid in event_ids:
            errors.append(f"duplicate event_id: {eid}")
        if eid:
            event_ids.add(eid)
        if etype not in VALID_EVENTS:
            errors.append(f"event {event_label} has invalid event_type {etype!r}")
        if bid not in seen_bearers:
            errors.append(f"event {event_label} references unknown bearer_id {bid!r}")

    fall_events = {ev.get("bearer_id") for ev in ledger_doc.get("events", []) if ev.get("event_type") == "fall"}
    for bid, b in seen_bearers.items():
        if b.get("status") == "fallen" and bid not in fall_events:
            errors.append(f"fallen bearer {bid} has no fall event")

    if errors:
        print("Titan lineage validation failed:", file=sys.stderr)
        for e in errors:
            print(f"- {e}", file=sys.stderr)
        return 1

    print("Titan lineage validation passed.")
    print(f"roles={len(roles)} bearers={len(seen_bearers)} events={len(event_ids)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
