# Version History and Usage Divergences

| Version Line | Key Change | Practical Divergence |
|---|---|---|
| Legacy Spring Cloud GCP docs era | Cloud Spring integration under older release trains | Boot 2 and `javax` assumptions in many examples |
| Modern Boot 3 era | Jakarta-compatible ecosystem and updated dependency alignment | Migration required for older starters and package conventions |

## Deep Divergence Notes

- Major version transitions usually combine runtime baseline upgrades and compatibility breaks.
- Validate transitive dependencies and integration points before promoting framework upgrades.
- Maintain migration checklists with rollback criteria and contract verification.
