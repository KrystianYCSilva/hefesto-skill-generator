# Expert Techniques

- Use `ETag` and conditional requests (`If-None-Match`) to reduce payload transfer.
- Normalize error output with RFC 7807-compatible payloads.
- Enforce contract tests for serialization edge cases (nulls, enums, date formats).
- Propagate correlation IDs through async boundaries for trace consistency.

## Specialist Playbook

- Define measurable SLOs per critical path and map each technique to a target metric.
- Keep rollback strategies documented before applying high-risk optimizations.
- Run game days to validate failure-path assumptions under realistic load.
- Standardize diagnostics (logs, metrics, traces) before deep tuning.
