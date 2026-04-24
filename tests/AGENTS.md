# AGENTS.md

## Guidance for `tests/`

`tests/` protects role contracts, generated registries, runtime seam examples, self-agent checkpoints, and reference routes.

Tests should expose role-boundary drift, unsupported authority, schema mismatch, and handoff ambiguity. Avoid freezing incidental formatting unless formatting is the contract.

Do not update generated expected outputs without rebuilding and checking the source-authored profile, tier, class, cohort, or seam.

Keep fixtures public-safe. No private prompts, secrets, hidden credentials, or unreduced operator traces.

Verify with:

```bash
python -m pytest -q tests
python scripts/validate_semantic_agents.py
```
