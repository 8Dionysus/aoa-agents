# AGENTS.md

## Guidance for `scripts/`

`scripts/` contains repo-level builders, validators, and publication helpers
for the agent role layer. Mechanic-specific scripts may live under the owning
`mechanics/*/scripts/` or `mechanics/*/parts/*/scripts/` route once the package
or part has local validation and provenance accounting.

Keep scripts deterministic and repo-relative. Avoid hidden network calls, private prompts, local-only paths, and ambient credentials.

Builder changes must preserve the distinction between source-authored role contracts and generated registries, capsules, or sections.

Validator changes should catch identity drift, role-boundary widening, unsupported handoff claims, and generated/source mismatch without turning style preference into noise.

Use the repository [validation map](../VALIDATION.md) and the nearest owner check when this route is relevant.
