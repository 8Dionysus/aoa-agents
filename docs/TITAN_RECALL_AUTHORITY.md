# Titan Recall Authority

Recall is a lantern, not a throne.

A Titan recall answer must expose:

- source kind
- record id
- session id
- titan lane
- confidence
- authority note
- whether the record is candidate, confirmed, redacted, or tombstoned

## Authority notes

Use one of:

- `candidate_only`
- `owner_repo_confirmed`
- `operator_approved`
- `derived_digest`
- `redacted_reference`

`candidate_only` is the default.
