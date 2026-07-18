# Progression lift

## Baseline posture

Declare one before movement:

- `baseline_ref` or `prior_delta_ref`
- `first_observed`
- `baseline_missing`
- `baseline_stale`
- `baseline_contested`

Missing, stale, or contested baselines usually support `hold`, `reanchor`, or
first-observed notes, not comparative advance.

## Axes and evidence posture

Assess only supported axes from the owner model:

- `boundary_integrity`
- `execution_reliability`
- `change_legibility`
- `review_sharpness`
- `proof_discipline`
- `provenance_hygiene`
- `deep_readiness`

For each touched axis return `movement` (`up`, `hold`, `reanchor`, `down`, or
`not_assessed`), `evidence_posture` (`confirmed`, `contested`, `provisional`,
`stale`, `not_current_session`, or `no_movement`), refs, attribution limits,
and reason. Do not infer mastery from absence of a visible failure.

## Procedure

1. Confirm one agent, closed review boundary, and source refs.
2. Separate direct current evidence from hints, stale residue, generated
   summaries, tools, environment, prior context, and reviewer inference.
3. Set baseline posture before comparison.
4. Assess supported axes and seek counterevidence. Allow no movement and
   regression.
5. Choose one verdict: `advance`, `hold`, `reanchor`, or `downgrade`.
6. Add only small unlock/rank/quest reflection hints supported by repeated
   evidence; mark every hint `owner_review_required`.
7. Name the rejected nearest route and stop at the owner-review candidate.

The current absolute progression schema is an owner surface, not the output of
this skill. Applying a candidate requires a separate `aoa-agents` owner review
and whatever proof the owner requests.
