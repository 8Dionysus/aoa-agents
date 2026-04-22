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

    seen_names: dict[str, str] = {}
    seen_bearers: dict[str, dict] = {}
    active_names: set[str] = set()

    for b in bearers_doc.get("bearers", []):
        bid = b.get("bearer_id")
        name = b.get("titan_name")
        role_key = b.get("role_key")
        status = b.get("status")
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
            if name in seen_names:
                errors.append(f"duplicate titan_name without explicit lineage relation: {name}")
            seen_names[name] = bid
            if status == "active":
                if name in active_names:
                    errors.append(f"duplicate active titan_name: {name}")
                active_names.add(name)
        mp = b.get("memory_policy") or {}
        if mp.get("remember_as_person") is not True:
            errors.append(f"bearer {bid} must remember_as_person=true")
        if mp.get("allow_name_reuse") is True and not b.get("successor_of"):
            errors.append(f"bearer {bid} allows name reuse without successor_of")

    event_ids: set[str] = set()
    for ev in ledger_doc.get("events", []):
        eid = ev.get("event_id")
        etype = ev.get("event_type")
        bid = ev.get("bearer_id")
        if eid in event_ids:
            errors.append(f"duplicate event_id: {eid}")
        event_ids.add(eid)
        if etype not in VALID_EVENTS:
            errors.append(f"event {eid} has invalid event_type {etype!r}")
        if bid not in seen_bearers:
            errors.append(f"event {eid} references unknown bearer_id {bid!r}")
        if not ev.get("source_ref"):
            errors.append(f"event {eid} missing source_ref")

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
