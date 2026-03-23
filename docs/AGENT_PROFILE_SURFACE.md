# AGENT PROFILE SURFACE

## Purpose

This document defines the source-authored profile surface for bounded agent roles
in `aoa-agents`.

It exists to keep role contracts reviewable in their own files instead of
treating the compact generated registry as the only place where agent meaning
is authored.

## Source of truth

The canonical source-authored profile files live at:

- `profiles/*.profile.json`
- `schemas/agent-profile.schema.json`

The compact published registry remains:

- `generated/agent_registry.min.json`

That registry is derived from the profile sources through:

- `scripts/build_agent_registry.py`

## What a source profile may contain

A source-authored agent profile may carry:

- compact identity fields such as `id`, `name`, `role`, `status`, and `summary`
- bounded role-contract wording such as `mission`, `owns`, and `does_not_own`
- handoff posture such as `handoff_rule` and `handoff_triggers`
- memory posture such as `memory_posture` and `memory_rights`
- evaluation posture such as `evaluation_posture` and `evaluation_focus`
- composition hints such as `preferred_cohort_patterns`
- tier-facing hints such as `preferred_tier_ids`
- traceability refs such as `source_surfaces`
- preferred skill families as references to adjacent execution layers

The generated registry intentionally stays smaller than the source profiles.
It publishes the stable compact fields needed by current consumers without
erasing the fuller role contract from the source layer.

## Boundaries to preserve

Source-authored profiles may point toward adjacent layers.
They must not absorb those layers as primary canon.

Keep these boundaries explicit:

- preferred skill families do not turn an agent into a skill bundle
- preferred cohort patterns do not turn a profile into a playbook
- memory posture does not turn a profile into a memory-object schema
- evaluation posture does not turn a profile into eval doctrine
- preferred tier hints do not turn a profile into routing policy
- source traceability refs do not turn a profile into a copied doctrine archive

If a field starts describing executable workflow steps, scenario canon, memory
objects, verdict doctrine, or dispatch logic, it belongs in a neighboring AoA
repository instead.

## Editing flow

When profile sources change:

1. edit the target file under `profiles/`
2. regenerate `generated/agent_registry.min.json` with `python scripts/build_agent_registry.py`
3. validate the repository with `python scripts/validate_agents.py`

This keeps the authored role contract distinct from the compact published
registry while preserving a deterministic review surface.
