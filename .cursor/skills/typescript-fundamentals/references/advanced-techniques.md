# Expert Techniques

- Use branded types for domain IDs to prevent cross-entity misuse.
- Enforce exhaustive switches in CI with `noFallthroughCasesInSwitch` and lint rules.
- Keep `unknown` at system boundaries and parse to trusted domain types.
- Use project references and incremental builds for large monorepos.

## Specialist Playbook

- Add API-surface type tests for generated clients and public SDKs.
- Enforce strict lint + type gates in CI for changed packages only.
- Track compile-time budget and incremental build health in monorepos.
- Keep migration codemods versioned and reversible.
