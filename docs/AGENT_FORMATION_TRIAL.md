# Agent Formation Trial

## Purpose

The Formation Trial is the first pre-protocol Agon judgment inside `aoa-agents`.

It asks one question:

> Can future Agon protocol work read the current actor formation without inventing agent ontology on the fly?

## Inputs

The trial reads:

- `generated/agent_agonic_formation_index.min.json`
- `generated/assistant_civil_formation_index.min.json`
- the five current base role profiles under `profiles/*.profile.json`

## What it judges

The trial checks that every current role home has:

- a surviving base profile
- a Wave I agonic form
- a Wave II assistant variant
- no accidental live arena authority
- no assistant drift into contestant status
- no closer or summon initiator authority in this wave

## Verdicts

`survive_with_split_forms` means the base role house survives as a house with explicit agonic and assistant forms.

`partial_recharter_required` means one side exists but the split is incomplete.

`quarantine_from_agon` means the role must not be read by future Agon protocol surfaces until repaired.

## Stop-line

This is formation judgment, not arena judgment.

It is not a battle, verdict, scar ledger, retention scheduler, runtime packet family, or ToS promotion path.
