# Version History and Usage Divergences

| Version Line | Key Change | Practical Divergence |
|---|---|---|
| Spring 5.x | WebFlux and MVC coexisted with legacy matcher defaults | Mixed reactive/blocking stacks often caused thread model confusion |
| Spring 6.x | Jakarta migration + modern path matching defaults | Legacy path patterns and exception contracts needed migration |

## Deep Divergence Notes

- Major version transitions usually combine runtime baseline upgrades and compatibility breaks.
- Validate transitive dependencies and integration points before promoting framework upgrades.
- Maintain migration checklists with rollback criteria and contract verification.
