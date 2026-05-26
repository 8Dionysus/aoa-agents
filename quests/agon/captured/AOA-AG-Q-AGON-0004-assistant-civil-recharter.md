# AOA-AG-Q-AGON-0004: Assistant Civil Recharter

## Repository

`aoa-agents`

## Goal

Land assistant civil/service form as an explicit actor kind under Agon.

## Work

- add assistant variant schemas
- add assistant adjunct families for current base roles
- preserve base profiles
- preserve public role catalog
- prohibit hidden contestant authority
- require external revision and certification

## Exit

- `generated/assistant_civil_formation_index.min.json` is current
- `python scripts/validate_assistant_civil_formation.py` passes
- assistant variants cannot claim arena contestant, judge, closer, summoner, scar writer, or ToS promotion authority
