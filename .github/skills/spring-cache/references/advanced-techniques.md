# Expert Techniques

- Use two-level cache (Caffeine near-cache + Redis distributed) for read-heavy hotspots.
- Add jittered TTL to reduce synchronized expiration waves.
- Use versioned cache keys during schema evolution to avoid mixed payload decoding.
- Create a stale-while-revalidate strategy for low-criticality endpoints.

## Specialist Playbook

- Define measurable SLOs per critical path and map each technique to a target metric.
- Keep rollback strategies documented before applying high-risk optimizations.
- Run game days to validate failure-path assumptions under realistic load.
- Standardize diagnostics (logs, metrics, traces) before deep tuning.
