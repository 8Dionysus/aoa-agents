# AoA Agents Charter

## Purpose

`aoa-agents` is the role and persona layer of the AoA ecosystem.

Its purpose is to make agents explicit as reusable role-bearing actors with clear contracts rather than leaving them implicit inside prompts, ad hoc workflow code, or orchestration folklore.

## Mission

This repository exists to support agent-layer work such as:
- defining reusable agent profiles
- naming role boundaries and handoff rules
- clarifying preferred skill families
- naming memory posture and evaluation posture
- making agent composition more legible
- keeping the distinction between actor, workflow, proof, memory, and routing explicit

## What this repository owns

This repository owns agent-layer truth about:
- agent profiles
- role contracts
- handoff posture
- memory posture
- evaluation posture
- compact agent registries
- agent-layer schemas and validation rules

## What this repository does not own

This repository does not own the primary meaning of:
- reusable techniques
- bounded execution workflows
- bounded proof surfaces
- memory objects
- routing surfaces
- infrastructure implementation

## Core principles

- agent roles should be explicit rather than magical
- handoff must be legible and reviewable
- memory posture should be named, not assumed
- evaluation posture should be named, not improvised later
- agent profiles should stay compact enough to inspect
- the agent layer should not quietly absorb skills, memory, proof, or routing

## Source-of-truth rule

Neighboring AoA repositories still own their own meaning.

Examples:
- `aoa-techniques` owns practice meaning
- `aoa-skills` owns execution meaning
- `aoa-evals` owns proof meaning
- `aoa-routing` owns navigation and dispatch surfaces
- `aoa-memo` owns memory and recall meaning
- `aoa-agents` owns role and persona meaning

## Role in the federation

Treat `aoa-agents` as:
- the role and persona layer of AoA
- the canonical home of reusable agent profiles and role contracts
- the place where agent posture becomes explicit and reviewable

## Long-term direction

If `aoa-agents` matures well, it should help AoA move from anonymous agent behavior toward legible cohorts of roles that can coordinate without collapsing the distinction between:
- who acts
- how action is carried out
- how the action is judged
- what memory is available
