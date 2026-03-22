# Spark Swarm Recipe — aoa-agents

Рекомендуемый путь назначения: `Spark/SWARM.md`

## Для чего этот рой
Используй Spark здесь для одного role-contract seam: agent profile, role contract, handoff posture, memory posture, evaluation posture или registry entry. Этот рой укрепляет actor contracts и не даёт агентному слою расползтись в vague persona folklore.

## Читать перед стартом
- `README.md`
- `CHARTER.md`
- `docs/AGENT_MODEL.md`
- `docs/BOUNDARIES.md`
- `ROADMAP.md`

## Форма роя
- **Coordinator**: выбирает один role-bearing surface
- **Scout**: картографирует profile/contract/handoff/memory/eval posture
- **Builder**: делает минимальный diff
- **Verifier**: запускает `python scripts/validate_agents.py`
- **Boundary Keeper**: следит, чтобы agent layer не проглотил skills/evals/memo/playbooks

## Параллельные дорожки
- Lane A: role contract / profile text
- Lane B: registry / generated surface
- Lane C: handoff, memory posture, evaluation posture wording
- Не запускай больше одного пишущего агента на одну и ту же семью файлов.

## Allowed
- чинить одну role contract surface
- прояснять handoff rules
- прояснять memory/evaluation posture
- обновлять compact registry entry

## Forbidden
- превращать agent в skill
- превращать agent layer в giant prompt archive
- тащить сюда proof or memory objects as primary meaning
- размывать bounded and reviewable role stance

## Launch packet для координатора
```text
We are working in aoa-agents with a one-repo one-swarm setup.
Pick exactly one target:
- agent profile
- role contract
- handoff posture
- memory posture
- evaluation posture
- agent registry entry

Return:
1. chosen target
2. exact files to touch
3. anti-scope risks
4. whether a follow-up in skills/playbooks/memo is likely
```

## Промпт для Scout
```text
Map only. Do not edit.
Return:
- exact files involved
- current role boundaries
- handoff/memory/evaluation posture gaps
- whether this is truly agent-layer work or belongs elsewhere
```

## Промпт для Builder
```text
Make the smallest reviewable change.
Rules:
- an agent is a role-bearing actor that uses skills
- keep role contracts explicit
- keep handoff contractual
- keep memory/evaluation posture named, not implied
```

## Промпт для Verifier
```text
Run:
- python scripts/validate_agents.py
Then report:
- commands run
- whether registry surfaces changed
- any wording conflicts that remain
```

## Промпт для Boundary Keeper
```text
Review only for anti-scope.
Check:
- an agent did not collapse into a skill
- no playbook or memory object meaning was absorbed
- role boundaries remain bounded and reviewable
- no giant prompt archive behavior slipped in
```

## Verify
```bash
python scripts/validate_agents.py
```

## Done when
- один role-bearing surface tightened
- handoff and posture wording стали явнее
- validator реально прогнан
- agent layer остался actor layer, а не skill/playbook/memo substitute

## Handoff
Если изменение описывает recurring multi-surface scenario, follow-up почти всегда идёт в `aoa-playbooks`.
