# Expert Techniques

- Add idempotency keys for unsafe retried operations (`POST` create/payment).
- Use conditional requests with ETag/version fields to prevent lost updates.
- Enforce consumer-driven contract tests on public APIs.
- Maintain compatibility policy (sunset headers, deprecation window, migration guide).

## Specialist Playbook

- Define measurable SLOs per critical path and map each technique to a target metric.
- Keep rollback strategies documented before applying high-risk optimizations.
- Run game days to validate failure-path assumptions under realistic load.
- Standardize diagnostics (logs, metrics, traces) before deep tuning.
