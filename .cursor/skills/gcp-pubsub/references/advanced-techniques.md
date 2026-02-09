# Expert Techniques

- Use deduplication keys persisted in a fast store for side-effecting consumers.
- Cap outstanding bytes/messages aggressively during incident backpressure.
- Segment high-priority events into dedicated topics/subscriptions.
- Use replay runbooks with bounded time windows and compensating logic.

## Specialist Playbook

- Define measurable SLOs per critical path and map each technique to a target metric.
- Keep rollback strategies documented before applying high-risk optimizations.
- Run game days to validate failure-path assumptions under realistic load.
- Standardize diagnostics (logs, metrics, traces) before deep tuning.
