# AOA-AG-D-0074 Mechanics Legacy Retirement

## Index Metadata

- Decision ID: AOA-AG-D-0074
- Original date: 2026-09-04
- Surface classes: mechanics/provenance, agent routes, archive retirement
- Agent facets: mechanics atlas, source-first routing
- Mechanic parents: cross-mechanic
- Guard families: active-route authority, historical recovery, generated parity
- Posture: accepted

## Decision

On 2026-09-04, all thirteen archive-only roots below are retired. Active part
routes remain the sole current source. Former content is recoverable from the
baseline commit and immutable Git history; retired roots are not compatibility
routes.

## Baseline historical links

Baseline commit: [`850b86674e77dc741cb53322fb89eaee8bcb1aef`](https://github.com/8Dionysus/aoa-agents/commit/850b86674e77dc741cb53322fb89eaee8bcb1aef).

| Retired root | Baseline tree | Full historical tree link |
| --- | --- | --- |
| `.agents/spark/` | `a60ffedc9132c49b6b829e6e5736f9ba2b9452fd` | [tree](https://github.com/8Dionysus/aoa-agents/tree/850b86674e77dc741cb53322fb89eaee8bcb1aef/.agents/spark) |
| `mechanics/agon/legacy/` | `a4cf2ad61dbae9eb93ebe8324024394b76e25300` | [tree](https://github.com/8Dionysus/aoa-agents/tree/850b86674e77dc741cb53322fb89eaee8bcb1aef/mechanics/agon/legacy) |
| `mechanics/antifragility/legacy/` | `5730b21a29f13250d7b73851f1ba73ab350fa3d3` | [tree](https://github.com/8Dionysus/aoa-agents/tree/850b86674e77dc741cb53322fb89eaee8bcb1aef/mechanics/antifragility/legacy) |
| `mechanics/boundary-bridge/legacy/` | `4d13dfc32046bde70075233374bb986ab3fc6db9` | [tree](https://github.com/8Dionysus/aoa-agents/tree/850b86674e77dc741cb53322fb89eaee8bcb1aef/mechanics/boundary-bridge/legacy) |
| `mechanics/checkpoint/legacy/` | `9a40db99e8c15a7018c6feeb7ef86aaa00b505a3` | [tree](https://github.com/8Dionysus/aoa-agents/tree/850b86674e77dc741cb53322fb89eaee8bcb1aef/mechanics/checkpoint/legacy) |
| `mechanics/codex-projection/legacy/` | `79f47ee09f2d55661ebd5e6e3f1d1d0158b7c847` | [tree](https://github.com/8Dionysus/aoa-agents/tree/850b86674e77dc741cb53322fb89eaee8bcb1aef/mechanics/codex-projection/legacy) |
| `mechanics/experience/legacy/` | `05980eebf80ab5b0c7e42d6e04f9ab8956a0e023` | [tree](https://github.com/8Dionysus/aoa-agents/tree/850b86674e77dc741cb53322fb89eaee8bcb1aef/mechanics/experience/legacy) |
| `mechanics/questbook/legacy/` | `e003705a9532d1995b2d98adff1c724573bd8c8b` | [tree](https://github.com/8Dionysus/aoa-agents/tree/850b86674e77dc741cb53322fb89eaee8bcb1aef/mechanics/questbook/legacy) |
| `mechanics/recurrence/legacy/` | `80703623d4f29f647ce830e3542c5fb7bc3d3164` | [tree](https://github.com/8Dionysus/aoa-agents/tree/850b86674e77dc741cb53322fb89eaee8bcb1aef/mechanics/recurrence/legacy) |
| `mechanics/release-support/legacy/` | `deb7faf8c6bb457041240b8b095dd22f9a8a37e3` | [tree](https://github.com/8Dionysus/aoa-agents/tree/850b86674e77dc741cb53322fb89eaee8bcb1aef/mechanics/release-support/legacy) |
| `mechanics/rpg/legacy/` | `8a17f2ca35d95c449c174cf6cc49ccc06a99f6fa` | [tree](https://github.com/8Dionysus/aoa-agents/tree/850b86674e77dc741cb53322fb89eaee8bcb1aef/mechanics/rpg/legacy) |
| `mechanics/runtime-seam/legacy/` | `2c3a02ec5b15f8e2704507abc21f01ecbede8079` | [tree](https://github.com/8Dionysus/aoa-agents/tree/850b86674e77dc741cb53322fb89eaee8bcb1aef/mechanics/runtime-seam/legacy) |
| `mechanics/titan/legacy/` | `54f8e6b69ccaa9f50d36a258fbd716fd6c0d967c` | [tree](https://github.com/8Dionysus/aoa-agents/tree/850b86674e77dc741cb53322fb89eaee8bcb1aef/mechanics/titan/legacy) |

Each root is retired because it is archive scaffolding with no current owner
route; recovery is by the immutable commit/tree links above or the exact
path/blob inventory in `surface-retirement-20260904/baseline.json`.

## Boundary

This removes archive-only scaffolding and does not change role meaning,
behavioral contracts, source objects, or generated authority. Reviewed memo
candidates retain their historic source references and are not rewritten.

## Recovery

The complete path/blob baseline is recorded in
`surface-retirement-20260904/baseline.json`; every targeted blob was verified
recoverable before removal. No `.aoa`, host, runtime, remote, tag, PR, or merge
surface is part of this decision.
