# AGENTS.md

## Guidance for `docs/`

`docs/` explains the agent model, role contracts, handoff posture, memory posture, evaluation posture, and formation trials.

Docs can clarify role semantics, but source-authored profile and class surfaces still own concrete identity fields.

Keep personhood, self-agency, and formation language bounded, reviewable, evidence-linked, and reversible. Do not make autonomy claims that profiles, evals, memory posture, or runtime seams cannot support.

When docs change handoff, memory, or evaluation posture, re-check the relevant profile, cohort, runtime seam, and downstream proof/memo surfaces.

Verify with:

```bash
python scripts/validate_agents.py
python scripts/validate_semantic_agents.py
```
