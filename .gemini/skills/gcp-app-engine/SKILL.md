---
name: gcp-app-engine
description: |
  Guides App Engine architecture, runtime configuration, scaling modes, version routing, scheduled workloads, and safe deployment practices for Java services.
  Use when: deploying backend applications to App Engine Standard or Flexible, planning traffic migration, or operating multi-service App Engine environments.
---

# GCP App Engine

App Engine was one of the first major PaaS offerings and established many modern managed deployment practices. This skill helps the agent choose the right environment, configure deployments safely, and operate services with predictable scaling.

## How to choose Standard vs Flexible

1. Prefer Standard for faster startup, stronger platform constraints, and lower ops overhead.
2. Use Flexible when you need custom runtime/container behavior.
3. Decide based on runtime constraints, scaling profile, and networking requirements.
4. Keep environment choice explicit in architecture docs.

## How to configure `app.yaml` correctly

1. Set runtime (`java17` or supported runtime) and entrypoint strategy.
2. Define instance class and scaling mode (automatic/basic/manual).
3. Keep env vars externalized and secret values managed outside source.
4. Add health check and resource settings aligned with workload characteristics.

## How to manage versions and safe rollouts

1. Deploy each release as a new version.
2. Use traffic splitting for canary and phased rollout.
3. Keep rollback path documented before promotion.
4. Label versions with commit/release metadata.

## How to structure services, routing, and schedules

1. Split bounded services when independent scaling is needed.
2. Use `dispatch.yaml` for centralized route control.
3. Use `cron.yaml` for scheduled jobs and verify idempotency.
4. For queued background workloads, prefer managed task services where appropriate.

## How to operate App Engine in production

1. Monitor latency, error rate, and instance behavior per version.
2. Set alerts for quota, cold starts, and elevated error budgets.
3. Validate IAM/service identity for outbound dependencies.
4. Automate deployment through CI/CD with approval gates.

## Common Warnings & Pitfalls

- Treating App Engine as static infrastructure instead of versioned runtime.
- Deploying without traffic split and rollback strategy.
- Putting long CPU-intensive jobs in request path.
- Hardcoding project IDs and environment-specific URLs.
- Ignoring region and quota constraints during scale events.

## Common Errors and Fixes

| Symptom | Root Cause | Fix |
|---|---|---|
| Deployment succeeds but app fails health checks | Runtime/entrypoint mismatch | Align runtime config and verify startup command |
| Unexpected costs after release | Oversized instance class or scaling policy | Re-tune scaling limits and right-size instances |
| Requests routed to wrong service | Dispatch rules overlap | Review `dispatch.yaml` order and specificity |
| Cron jobs duplicate work | Non-idempotent job logic | Add idempotency key/state guard in scheduled task |

## Advanced Tips

- Use gradual traffic migration with observability checkpoints per step.
- Keep release notes linked to App Engine version labels.
- Build synthetic probes for critical routes before traffic cutover.
- For multi-service systems, define platform SLOs and ownership by service.

## How to use extended references

- Read [Version History](references/version-history.md) before upgrades, migrations, or compatibility decisions.
- Read [Java and Kotlin Examples](references/java-kotlin-examples.md) for implementation-ready snippets and language-specific guidance.
- Read [Advanced Techniques](references/advanced-techniques.md) for specialist playbooks, incident tactics, and performance patterns.

