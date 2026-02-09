# Version History and Usage Divergences

| Go Version | Key Change | Practical Divergence |
|---|---|---|
| 1.18 | Generics introduced | API design shifted from interface-heavy patterns to constrained type params |
| 1.20+ | Runtime/toolchain and stdlib improvements | Error handling and performance tuning practices evolved |

## Deep Divergence Notes

- Generics changed library API design and reduced reliance on empty interface patterns.
- Runtime and toolchain improvements alter benchmark baselines across versions.
- Cross-service contracts should remain explicit regardless of language-level ergonomics.
