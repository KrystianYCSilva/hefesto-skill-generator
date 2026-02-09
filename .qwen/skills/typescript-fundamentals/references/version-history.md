# Version History and Usage Divergences

| TypeScript Version | Key Change | Practical Divergence |
|---|---|---|
| 4.x | Strong maturity for type narrowing and tooling | Large legacy codebases often stayed with weak strictness settings |
| 5.x | Performance and ergonomics improvements | Build tooling and decorators setup differed across ecosystems |

## Deep Divergence Notes

- Strictness adoption usually lags feature adoption in large legacy repositories.
- ESM/CJS runtime alignment is a recurring source of production-only failures.
- Monorepo scale requires project references and deterministic build graph discipline.
