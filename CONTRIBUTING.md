# Contributing to aoa-agents

Thank you for helping shape the AoA agent layer.

This repository is the role and persona layer of AoA.
Contributions here should improve the clarity, coherence, and usefulness of agent-layer surfaces rather than turning this repository into a prompt graveyard or orchestration dump.

## What belongs here

Good contributions include:
- agent layer definitions
- reusable role profiles
- handoff and posture guidance
- memory and evaluation posture definitions
- compact agent registries, schemas, and validation
- clearer boundaries between actor, workflow, proof, memory, and routing

## What usually does not belong here

Do not use this repository as the default home for:
- new technique bundles
- new skill bundles
- new eval bundles
- routing surfaces
- memory objects
- infrastructure implementation details
- giant prompt payloads with no reusable role contract

If a change mainly defines reusable practice, bounded execution, or bounded proof, prefer the specialized neighboring repository first.

## Source-of-truth discipline

When contributing, preserve this rule:
- `aoa-agents` owns role and persona meaning
- neighboring AoA repositories still own their own meaning

Examples:
- `aoa-techniques` owns practice meaning
- `aoa-skills` owns execution meaning
- `aoa-evals` owns proof meaning
- `aoa-routing` owns navigation surfaces
- `aoa-memo` owns memory meaning

## How to decide where a change belongs

Ask these questions in order:

1. Is this change mainly about role, handoff, memory posture, or evaluation posture?
   - If yes, it may belong here.
2. Is this change mainly about reusable practice?
   - If yes, it probably belongs in `aoa-techniques`.
3. Is this change mainly about bounded execution?
   - If yes, it probably belongs in `aoa-skills`.
4. Is this change mainly about bounded proof?
   - If yes, it probably belongs in `aoa-evals`.
5. Is this change mainly about memory objects or recall truth?
   - If yes, it probably belongs in `aoa-memo`.
6. Is this change mainly about dispatch across repos?
   - If yes, it probably belongs in `aoa-routing`.

## Pull request shape

A strong pull request in this repository should explain:
- what agent-layer surface changed
- why the change belongs in `aoa-agents`
- what neighboring AoA layers are affected
- what was intentionally not absorbed into this repository

## Style guidance

Prefer:
- compactness over role sprawl
- explicit posture over magical behavior
- reviewable profiles over hidden prompt systems
- bounded role contracts over overloaded agent mythology
