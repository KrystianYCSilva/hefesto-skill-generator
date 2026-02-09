# Version History and Usage Divergences

| Feature Era | Key Change | Practical Divergence |
|---|---|---|
| Basic pull/push subscriptions | Standard at-least-once semantics | Idempotency required in all consumers |
| Advanced delivery controls | Exactly-once and refined retry/dead-letter controls | Higher reliability options with cost/latency trade-offs |

## Deep Divergence Notes

- Major version transitions usually combine runtime baseline upgrades and compatibility breaks.
- Validate transitive dependencies and integration points before promoting framework upgrades.
- Maintain migration checklists with rollback criteria and contract verification.
