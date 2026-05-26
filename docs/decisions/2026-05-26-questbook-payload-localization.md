# 2026-05-26: Questbook Payload Localization

## Status

Accepted.

## Context

The questbook mechanic already owned quest-facing role posture, but the active
quest catalog doc and quest source records still lived at the repository root.
That kept questbook behavior split between a mechanic package and a root
payload district.

The YAML quest records feed generated quest catalog and dispatch readers. The
Agon quest notes are quest-facing posture records, not playbook choreography or
proof verdicts.

## Decision

Move the active quest catalog doc and YAML quest records into the
`quest-catalog` part. Move Agon quest notes into the `agon-quest-surfaces`
part.

Keep generated quest catalog and dispatch readers in `generated/` as derived
consumer surfaces, with their `source_path` values pointing to the new
repo-relative source routes.

Preserve former root lookup only through questbook `PROVENANCE.md` and
`legacy/`.

## Consequences

- `mechanics/questbook/parts/quest-catalog/` owns the active catalog doc and
  YAML quest records.
- `mechanics/questbook/parts/agon-quest-surfaces/` owns Agon quest notes.
- `scripts/validate_agents.py` validates the new source paths and generated
  quest readers.
- Playbook scenario choreography, proof verdicts, and durable memory truth
  remain outside this repository.

## Verification

```bash
python scripts/validate_agents.py
python scripts/validate_semantic_agents.py
python scripts/validate_nested_agents.py
python -m pytest -q tests
python scripts/release_check.py
```
