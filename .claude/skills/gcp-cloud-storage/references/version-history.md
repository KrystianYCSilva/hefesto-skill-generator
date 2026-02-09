# Version History and Usage Divergences

| API/Capability Era | Key Change | Practical Divergence |
|---|---|---|
| XML and JSON API coexistence | Broad compatibility surface | Feature parity and tooling behavior varied by interface |
| Signed URL v4 and modern IAM patterns | Stronger auth and governance controls | Legacy ACL-centric usage required migration to IAM-first models |

## Deep Divergence Notes

- Major version transitions usually combine runtime baseline upgrades and compatibility breaks.
- Validate transitive dependencies and integration points before promoting framework upgrades.
- Maintain migration checklists with rollback criteria and contract verification.
