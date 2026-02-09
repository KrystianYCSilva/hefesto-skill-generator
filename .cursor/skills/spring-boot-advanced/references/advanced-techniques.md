# Expert Techniques

- Model auto-config with a condition matrix test suite (class-path, property, bean-presence dimensions).
- Keep optional integrations isolated behind `@ConditionalOnClass` and explicit feature flags.
- Use low-cardinality metric tags from domain vocabulary, not request payloads.
- Add synthetic health checks for critical dependency paths, not only TCP reachability.

## Specialist Playbook

- Define measurable SLOs per critical path and map each technique to a target metric.
- Keep rollback strategies documented before applying high-risk optimizations.
- Run game days to validate failure-path assumptions under realistic load.
- Standardize diagnostics (logs, metrics, traces) before deep tuning.
