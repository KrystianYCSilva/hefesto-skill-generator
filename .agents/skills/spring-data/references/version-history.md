---
name: version-history
description: |
  Documentation file for agent operations and skill usage.
  Use when: you need procedural guidance for agent execution and context management.
---

# Version History and Usage Divergences

| Version Line | Key Change | Practical Divergence |
|---|---|---|
| Spring Data 2.x | JPA repository model stabilized | `javax.persistence` compatibility with older stacks |
| Spring Data 3.x | Jakarta package migration for Boot 3 | Entity imports and custom libs needed namespace migration |

## Deep Divergence Notes

- `javax.persistence` to `jakarta.persistence` migration impacts entities, converters, and metamodel generators.
- Query plan behavior can change after version upgrades due Hibernate and planner improvements.
- Repository customization APIs stayed similar, but compatibility of extension libraries may lag.

