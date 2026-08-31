# agents/roles/AGENTS.md

## Purpose

`agents/roles/` is the source-authored role-contract surface for reusable
agent roles in `aoa-agents`.

## Owner boundary

Base role meaning lives in `agents/roles/*/profile.json`; Agon and assistant
forms remain additive under `agents/roles/*/forms/`, and specializations reference
capability packs without becoming new base roles. Keep profiles, forms, and
specializations bounded, reviewable, and separate from workflows, proof,
memory truth, routing policy, playbooks, and runtime implementation.

## Derived routes

Published readers include `generated/agent_registry.min.json`,
`generated/role_specialization_catalog.min.json`, and the formation indexes.
Public contract explanation lives in `docs/AGENT_PROFILE_SURFACE.md`; schemas
and mechanic-local validators remain stronger owners for their contracts.

## Validation

Use the repository [validation map](../../VALIDATION.md) and the nearest
formation or source-owner check when this route is relevant.

## Closeout

Report the role house or adjunct family changed, source and generated owners
consulted, checks run, checks skipped, and any stronger-owner handoff.
