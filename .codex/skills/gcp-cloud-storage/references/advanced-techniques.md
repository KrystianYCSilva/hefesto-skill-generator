# Expert Techniques

- Use generation-match preconditions to guarantee optimistic concurrency on writes.
- Compose smaller uploaded chunks server-side for very large object workflows.
- Separate retention/legal-hold buckets from mutable application buckets.
- Audit signed URL issuance and expiration policy for abuse detection.

## Specialist Playbook

- Define measurable SLOs per critical path and map each technique to a target metric.
- Keep rollback strategies documented before applying high-risk optimizations.
- Run game days to validate failure-path assumptions under realistic load.
- Standardize diagnostics (logs, metrics, traces) before deep tuning.
