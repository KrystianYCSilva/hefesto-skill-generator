# Version History and Usage Divergences

| PostgreSQL Version | Key Change | Practical Divergence |
|---|---|---|
| 12 | CTE inlining behavior changed | Previously optimization-fenced queries became planner-optimized |
| 13 | Better btree dedup and planner improvements | Different index/storage behavior under heavy duplicate keys |
| 14-16 | Performance, logical replication, and SQL feature evolution | Upgrade planning required for extension compatibility and tuning defaults |

## Deep Divergence Notes

- Major version transitions usually combine runtime baseline upgrades and compatibility breaks.
- Validate transitive dependencies and integration points before promoting framework upgrades.
- Maintain migration checklists with rollback criteria and contract verification.
