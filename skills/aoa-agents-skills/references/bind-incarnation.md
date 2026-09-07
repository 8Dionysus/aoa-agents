### Mode: bind-incarnation

Bind the holder-selected physical realization of a complete actor mandate.
The role remains unchanged when the realization is substituted.

## Input

Require one complete `actor-mandate-v1`, current `aoa-models` fit evidence,
an `aoa-sdk` incarnation-binding-v2 contract, and an `abyss-stack` external CLI
runtime profile compatible with the mandate's environment and permissions.

## Procedure

For an existing actor, first inspect its obligation, mandate, holder, binding,
and runtime continuation refs. Keep a valid incarnation and continue through
its supported runtime interface. Session resumption is not a reason to query
fit or reconstruct the binding. Run the steps below only for formation or an
actual binding change; verify authority/currentness at that boundary.

1. Send required executor properties, domain posture, environment, authority,
   continuity, and evidence threshold to `aoa-models`. Preserve an explicit
   operator model/effort choice, checking its fit rather than silently
   substituting a different model. Otherwise the current holder selects from
   the returned candidates.
2. Require a current fit response identifying one model realization and mode,
   evidence refs, known failure modes, expiry/recheck conditions, and viable
   alternatives. A catalog entry is not fit evidence.
3. Give the exact obligation, mandate, role resolution, model-fit query and
   selected fit projection, realization ref, runtime profile, workspace,
   permissions, usage-metering, continuation, and wake policy to the
   `aoa-sdk` incarnation binding.
4. Require `abyss-stack` to support a separate OS process, separate CLI
   session, explicit state root, resume handle, event surface, and the exact
   effect class required by the mandate. Built-in Codex subagents are not an
   acceptable binding for this path.
5. Verify the binding is content-addressed to the exact mandate and owner
   inputs. Record usage counting, never a pre-emptive token budget.
6. Return the binding ref and evidence; do not launch from this mode.

An unavailable start, resume, or wake interface is a runtime integration gap.
Keep the existing obligation and report that gap without forging a lifecycle
transition or creating a replacement scheduler.

## Output

Return `agent-incarnation-binding-ref-v2` with obligation, mandate, role
resolution, model-fit query and selected projection, model realization,
mode, fit evidence, specialized environment, runtime profile, workspace,
permission/effect envelope, state and continuation posture, usage metering,
wake policy, content digest, recheck conditions, alternatives, uncertainty,
and exact stronger-owner refs.
