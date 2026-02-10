---
name: version-history
description: |
  Documentation file for agent operations and skill usage.
  Use when: you need procedural guidance for agent execution and context management.
---

# Version History and Usage Divergences

| Version Line | Key Change | Practical Divergence |
|---|---|---|
| Boot 1.x | Early auto-config and embedded containers | Heavy XML migration and weaker modern observability defaults |
| Boot 2.x | Strong Actuator/Micrometer integration | `javax.*` ecosystem and Java 8/11 migration complexity |
| Boot 3.x | Jakarta namespace + Java 17 baseline + AOT/native maturity | Breaking package migration (`javax` -> `jakarta`) and stricter upgrade path |

## Deep Divergence Notes

- Major version transitions usually combine runtime baseline upgrades and compatibility breaks.
- Validate transitive dependencies and integration points before promoting framework upgrades.
- Maintain migration checklists with rollback criteria and contract verification.

