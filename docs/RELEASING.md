# Releasing

This document keeps the `aoa-agents` release route discoverable without
duplicating executable validation commands from root `VALIDATION.md`.

Use it when preparing a public release, checking release-readiness posture, or
recovering the next honest step after a release preflight failure.

## Operating Card

| Field | Route |
| --- | --- |
| role | release-readiness route card for public `aoa-agents` releases |
| input | version target, changelog entry, release audit result, PR validation, tag or publication state |
| output | release-ready branch, landed main, tag, GitHub Release, or explicit blocker |
| owner | root `VALIDATION.md` maps executable release/validation commands; root `AGENTS.md` owns landing stop-lines; this file owns release-readiness shape |
| next route | `CHANGELOG.md`, `README.md`, `ROADMAP.md`, `docs/CURRENT_CONTOUR.md`, GitHub PR, tag, GitHub Release |
| validation | root `VALIDATION.md`, release audit, GitHub Repo Validation, and post-merge release gate |

## Release Shape

A release is ready only after all of these are true:

- the changelog has a dated release section with Summary, Validation, and Notes;
- active release markers agree across the public front door and current contour;
- version-alignment tests move with the public markers;
- the release branch lands through PR and GitHub Repo Validation;
- landed `main` is fast-forwarded locally and checked again before tagging;
- the tag points at landed `main`, not at an unmerged branch commit;
- the GitHub Release body is derived from the canonical changelog section;
- post-publication verification confirms the tag, release, branch, and clean
  worktree state.

## Changelog Completeness

Do not trust `[Unreleased]` alone when preparing a release. Reconstruct the
release note from the full previous-tag-to-HEAD history, current source tree,
decision records, generated readers, local memo candidates, and recent PR
route. The changelog should name the durable surface changes, not every file.

Keep release validation prose in the changelog concise. Command examples belong
in root `VALIDATION.md`, not in the release note.

## Branch and PR Landing

When the operator authorizes commit, push, and merge for this repository:

1. Start from a branch based on current `origin/main`. If the worktree is
   already dirty, inventory it and carry forward only the intended diff.
2. Commit the intended change with a message naming the changed surface.
3. Push the branch and open a pull request that states changed surfaces,
   validation run, skipped checks, and remaining risk.
4. Observe GitHub `Repo Validation` and every required check. Fix failures on
   the branch and observe the replacement result.
5. Merge through GitHub only after green validation and confirmed authority;
   use the repository-required method and report what landed.
6. Return to `main`, fast-forward from `origin/main`, and confirm the worktree
   is clean before closeout.

If GitHub status or merge permission cannot be observed, stop and report the
exact blocker instead of guessing.

## Public-Share Review

Before publishing a release, treat the changelog and GitHub Release as
public-share surfaces:

- keep raw logs, secrets, tokens, and private operational material out of the
  release body;
- prefer summarized validation results over raw transcript excerpts;
- name sensitive boundaries only at the level already present in public repo
  surfaces;
- preserve enough detail for future contributors to recover why the release
  exists.

## Version Surfaces

When the release marker moves, check the public marker surfaces together:

- `README.md`;
- `CHANGELOG.md`;
- `ROADMAP.md`;
- `docs/CURRENT_CONTOUR.md`;
- tests that assert public release-line alignment.

Generated surfaces should change only when their source builders require it.
The OS Abyss artifact envelope for `generated/agent_registry.min.json` lives in
`manifests/artifact_bundles/role_contract_registry.bundle.json`; verify it with
`scripts/validate_abyss_machine_role_registry_bundle.py` before treating
the generated role registry as a release/export handoff. That validator builds
the bundle, promotes durable evidence, materializes the subject store, and
requires an OS Abyss consumer trust-gate allow/warn verdict.

## Closeout

After publication, verify the tag and GitHub Release, confirm local `main`
matches `origin/main`, and report any skipped checks or release-audit blockers.

If the release changes owner boundaries, workflow law, or route posture, add or
update the owning decision surface. If it only publishes already-documented
changes, the changelog and existing decisions can be enough.
