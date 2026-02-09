# Expert Techniques

- Roll traffic in explicit waves (1% -> 5% -> 25% -> 100%) with SLO checkpoints.
- Keep per-version dashboards to compare latency/error regressions before promotion.
- Use idempotent cron job design because retries and replays are operationally real.
- Encode release metadata into version labels for fast incident rollback.

## Specialist Playbook

- Define measurable SLOs per critical path and map each technique to a target metric.
- Keep rollback strategies documented before applying high-risk optimizations.
- Run game days to validate failure-path assumptions under realistic load.
- Standardize diagnostics (logs, metrics, traces) before deep tuning.
