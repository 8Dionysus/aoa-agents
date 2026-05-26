# Agon Parts

`mechanics/agon/parts/` is the lower index for active Agon operation parts.
Use it after the parent route has selected Agon as the owning mechanic.

## Active Parts

| Part | Operation | Current route |
| --- | --- | --- |
| `formation/` | agonic actor recharter, assistant civil posture, and formation trial | `formation/README.md` |
| `pre-protocol-boundary/` | bounded pre-protocol posture before role promotion | `pre-protocol-boundary/README.md` |
| `arena-rank-school/` | rank jurisdiction, school affiliation, campaign posture, arena limits | `arena-rank-school/README.md` |
| `epistemic-actor/` | concept, model-of-other, and epistemic actor limits | `epistemic-actor/README.md` |
| `adoption-retention/` | pattern adoption, shared scars, retention readiness | `adoption-retention/README.md` |
| `recursor-boundary/` | Agon-facing recursor and recurrence limits | `recursor-boundary/README.md` |

## Admission Rule

Create a child part directory only when the part gains package-local docs,
schemas, examples, builders, validators, or generated outputs. Until then,
`../PARTS.md` owns the payload anchor map.
