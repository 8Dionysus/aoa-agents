# Generated Readiness

This directory holds generated read models for the specialization eligibility
queue. Generated files summarize `../records/*.eligibility.json`; they do not
own projection decisions or install authority.

Regenerate with:

```bash
python mechanics/codex-projection/parts/specialization-eligibility/scripts/build_specialization_eligibility_readiness.py
```

Check with:

```bash
python mechanics/codex-projection/parts/specialization-eligibility/scripts/build_specialization_eligibility_readiness.py --check
```
