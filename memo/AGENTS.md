# AGENTS.md

## Applies to

This card applies to `memo/`.

## Role

`memo/` is the aoa-agents local memory port. It holds role-layer memory
candidates, receipts, exports, and local notes before reviewed landing in
`aoa-memo`.

## Boundaries

Use this port for `write_candidate_only` work. Keep role/profile truth in
`aoa-agents` source surfaces; use this port for recall, candidate memory,
receipts, and reviewed handoff.

Use `PORT.yaml` for the local port contract and `INDEX.md` / `index.min.json`
as generated read models. Use `candidates/` for proposed memory, `receipts/`
for review or handoff traces, `exports/` for packets meant for `aoa-memo`, and
`local/` for role-layer memory that stays local for now.

## Candidate Route

Create role-layer candidates through the stack MCP helper. Memo-port
validation requires an explicitly configured `AOA_MEMO_ROOT`; do not infer a
sibling checkout path. Use the repository validation map for the owner
commands.

Validate the emitted candidate path through the repository validation map.

## Reviewed Landing Route

`landing-plan` is an access-plane check. Durable memory lands only in
`aoa-memo` through reviewed intake, generated read models, validators, and
review.

## Validation
Use the repository [validation map](../VALIDATION.md) and the nearest owner check when this route is relevant.

For repo-wide release posture, use the root `AGENTS.md` validation route.

## Closeout

Report candidate path, evidence refs, validation result, and whether the item
stayed local, was exported for reviewed intake, or was landed in `aoa-memo`.
