# Task-local actor DAG

The semantic capability tree supports discovery. Typed relations express
cross-tree compatibility. The task-local DAG contains only the lifecycle nodes
needed for one goal and remains ephemeral runtime state.

## Composition law

Use the shared `aoa-task-local-dag-v2` grammar and exact owner capability-graph
hash. Select the smallest valid set from:

```text
detect-obligation
  -> form-actor
  -> bind-incarnation
  -> transfer-responsibility
  -> aoa-summon external execution leaf
  -> receive-return
```

This is a possible chain, not a mandatory workflow. Valid shorter routes
include detection-only, forming a future dormant office, rebinding an existing
role, receiving a return from an already running actor, or waking an existing
role without recreating its identity.

## Planning rules

- During goal planning, add predictable future obligations at the strength
  authorized by their trigger contract.
- During execution, extend the DAG only from new evidence or newly exposed
  obligation pressure.
- During closeout, preserve residual obligations and explicit holders instead
  of hiding them as prose.
- Every edge must carry typed input/output compatibility and responsibility
  movement where applicable.
- Model selection, CLI transport, and domain procedure nodes retain their
  stronger owners.
- Persist neither the concrete DAG nor live runtime state in this bundle.

The DAG is valid planning evidence only. It does not prove an actor was formed,
a model fit was established, a process launched, responsibility accepted, or a
return validated.

