# Goal Participant Relations Part

## Applies To

This card applies to `mechanics/boundary-bridge/parts/participant-relations/`.

## Role

This part owns the `aoa-agents` source contract for exact Goal/thread
participant and assignment relations. It publishes an admission-shaped source
feed and a deterministic derived reader for consumers that need the relation
without taking ownership of Goal, model, session, runtime, or acceptance truth.
It also owns the reusable fail-closed intake boundary for an explicit typed
owner publication and its structural admission receipt.
The typed publication is the only admitted upstream input shape.

## Boundaries

- Identity, obligation/role, task assignment, model realization, and runtime
  incarnation remain independent dimensions.
- Each populated dimension requires an exact owner reference, schema version,
  and `sha256:` content digest.
- Consumers join only on the publisher-owned `relation_key`; they must not
  derive joins from names, labels, PIDs, working directories, versions, or a
  bare Goal identifier.
- `aoa-agents` owns the relation contract and publication seam. Goal/thread
  truth belongs to the app-server/session owners, model truth to `aoa-models`,
  and runtime truth to `abyss-stack`.
- A typed `owner_published` publication must name one exact Goal,
  Goal-instance, and master-thread scope, carry producer/publication refs,
  currentness, pagination, privacy omissions, a canonical payload digest, and
  relation records whose publisher-owned key digests are verifiable. The
  intake receipt is structural admission only; it does not create owner facts.
- Empty, absent, stale, deferred, unknown, and invalid evidence stays in that
  state. This part does not fabricate a participant graph or claim activation,
  liveness, wake, acceptance, or Goal completion.

## Validation

```bash
python mechanics/boundary-bridge/parts/participant-relations/scripts/build_goal_participant_graph.py --check
python mechanics/boundary-bridge/parts/participant-relations/scripts/validate_goal_participant_graph.py
python mechanics/boundary-bridge/parts/participant-relations/scripts/admit_goal_participant_publication.py --help
python -m unittest discover -s mechanics/boundary-bridge/parts/participant-relations/tests -p 'test_*.py'
```

Run the parent boundary-bridge and root validators for repository closeout.
