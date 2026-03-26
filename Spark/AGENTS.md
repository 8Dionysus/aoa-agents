# Spark lane for aoa-agents

This file only governs work started from `Spark/`.

The root `AGENTS.md` remains authoritative for repository identity, ownership boundaries, reading order, and validation commands. This local file only narrows how GPT-5.3-Codex-Spark should behave when used as the fast-loop lane.

If `SWARM.md` exists in this directory, treat it as queue / swarm context. This `AGENTS.md` is the operating policy for Spark work.

## Default Spark posture

- Use Spark for short-loop work where a small diff is enough.
- Start with a map: task, files, risks, and validation path.
- Prefer one bounded patch per loop.
- Read the nearest source docs before editing.
- Use the narrowest relevant validation already documented by the repo.
- Report exactly what was and was not checked.
- Escalate instead of widening into a broad architectural rewrite.

## Spark is strongest here for

- profile and role-contract wording cleanup
- handoff, memory-posture, or evaluation-posture refinement
- schema, example, and generated-surface alignment
- small cohort-composition hint repairs
- tight audits of boundary language around who acts and when to hand off

## Do not widen Spark here into

- turning profiles into skills or playbooks
- rewriting memory-object meaning or eval doctrine here
- inventing hidden orchestration logic in the role layer
- inflating role identity into vague total authority

## Local done signal

A Spark task is done here when:

- the role is clearer and more bounded
- handoff posture is explicit
- memory posture stays distinct from memory objects
- evaluation posture stays distinct from eval doctrine
- the documented validation path ran when relevant

## Local note

Spark should act like a contract editor here: sharpen the role, tighten the handoff, stop before the profile becomes a whole operating system.

## Reporting contract

Always report:

- the restated task and touched scope
- which files or surfaces changed
- whether the change was semantic, structural, or clarity-only
- what validation actually ran
- what still needs a slower model or human review
