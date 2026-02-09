# Version History and Usage Divergences

| Version Line | Key Change | Practical Divergence |
|---|---|---|
| Session 2.x | Mature Redis/JDBC session stores on `javax` stack | Legacy apps relied on container defaults and weak cookie policies |
| Session 3.x | Jakarta + Boot 3 alignment | Required package and dependency updates for security/session modules |

## Deep Divergence Notes

- Major version transitions usually combine runtime baseline upgrades and compatibility breaks.
- Validate transitive dependencies and integration points before promoting framework upgrades.
- Maintain migration checklists with rollback criteria and contract verification.
