# Expert Techniques

- Implement tenant-aware JWT decoders keyed by issuer for multi-tenant APIs.
- Separate authentication errors (401) from authorization errors (403) with explicit handlers.
- Maintain a role-to-authority mapping contract test to prevent silent auth regressions.
- Use short-lived access tokens plus refresh-token rotation for high-risk domains.

## Specialist Playbook

- Define measurable SLOs per critical path and map each technique to a target metric.
- Keep rollback strategies documented before applying high-risk optimizations.
- Run game days to validate failure-path assumptions under realistic load.
- Standardize diagnostics (logs, metrics, traces) before deep tuning.
