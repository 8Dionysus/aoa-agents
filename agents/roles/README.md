# Role Houses

`agents/roles/` is the role-centered branch of the agent source home.

Each `agents/roles/<role>/` directory is one role house:

- `profile.json` owns the compact base role contract.
- `forms/agonic/` owns Agon-facing companion form inputs.
- `forms/assistant/` owns assistant civil-service companion form inputs.
- `specializations/<slug>/specialization.json` owns a named, role-local
  operating specialization such as `coder.repo-refactor` or
  `reviewer.route-drift-review`.

This shape keeps role pressure attached to the role it changes. It replaces the
old type-first spread where profiles and adjunct families lived apart from the
role houses they modified.

Specializations do not replace roles. They inherit the base role profile and
reference a capability pack under
`agents/operating-model/capabilities/packs/` for permission, tool, skill,
technique, memory, proof, and projection posture.

## Stop Lines

- Do not split one role house across type-first active directories.
- Do not turn role forms into workflows, verdicts, scars, memory truth,
  playbooks, runtime packets, or protocol law.
- Do not flatten specializations into top-level role names unless the base role
  taxonomy changes.
- Use mechanic-local schemas, docs, and validators for mechanic-owned form
  contracts.
