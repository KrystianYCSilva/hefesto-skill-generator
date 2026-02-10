---
name: version-history
description: |
  Documentation file for agent operations and skill usage.
  Use when: you need procedural guidance for agent execution and context management.
---

# Version History and Usage Divergences

| Version Line | Key Change | Practical Divergence |
|---|---|---|
| Boot 2.2-2.7 | Actuator and metrics became default production baseline | Endpoint exposure defaults often surprised legacy teams |
| Boot 3.0+ | Observation API and Jakarta alignment | Instrumentation and old custom auto-config modules required adaptation |

## Deep Divergence Notes

- Major version transitions usually combine runtime baseline upgrades and compatibility breaks.
- Validate transitive dependencies and integration points before promoting framework upgrades.
- Maintain migration checklists with rollback criteria and contract verification.

