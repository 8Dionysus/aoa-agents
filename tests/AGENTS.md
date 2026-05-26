# AGENTS.md

## Guidance for `tests/`

`tests/` protects repo-level role contracts, generated registries, runtime seam examples,
and shared consumer seams. Mechanic-specific tests may live under the owning
`mechanics/*/tests/` or `mechanics/*/parts/*/tests/` route when release validation
still runs them explicitly.

Tests should expose role-boundary drift, unsupported authority, schema mismatch, and handoff ambiguity. Avoid freezing incidental formatting unless formatting is the contract.

Do not update generated expected outputs without rebuilding and checking the source-authored profile, tier, class, cohort, or seam.

Keep fixtures public-safe. No private prompts, secrets, hidden credentials, or unreduced operator traces.

Verify with:

```bash
python -m pytest -q tests
python scripts/validate_semantic_agents.py
```
