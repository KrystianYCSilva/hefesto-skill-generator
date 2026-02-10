---
name: spring-cloud-gcp
description: |
  Guides integration between Spring Boot services and Google Cloud managed products such as Pub/Sub, Cloud Storage, Datastore, Firestore, and Cloud SQL.
  Use when: building Spring workloads on GCP, wiring cloud services through starters, or hardening authentication and observability for cloud-native deployments.
---

# Spring Cloud GCP

Spring Cloud GCP emerged to reduce friction between Spring conventions and Google Cloud APIs. It allows teams to keep Spring programming models while integrating managed cloud services with predictable configuration and authentication.

## How to choose starters and dependency strategy

1. Use a single compatible BOM for Spring Boot and Spring Cloud GCP artifacts.
2. Add only the starters required by current use cases.
3. Keep cloud integration modules isolated by capability (messaging, storage, data).
4. Review release compatibility before framework upgrades.

## How to configure authentication and identity

1. Prefer Application Default Credentials (ADC) in GCP runtimes.
2. Use service accounts with least privilege IAM roles.
3. For local development, use dedicated non-production credentials.
4. Avoid static keys in source code or container images.

## How to integrate Pub/Sub safely

1. Use `PubSubTemplate` for publishing and subscription integration.
2. Define ack/nack strategy based on processing guarantees.
3. Design message payloads for idempotent consumers.
4. Configure dead-letter and retry policies for poison messages.

## How to use Cloud Storage and object workflows

1. Use storage templates/clients for upload, download, and metadata operations.
2. Define bucket naming and retention policies by environment.
3. Use signed URLs for controlled client access when needed.
4. Validate content type and size before persistence.

## How to connect Cloud SQL and managed data stores

1. Use Cloud SQL connectors/socket factory with secure connectivity.
2. Configure connection pools for workload profile.
3. Separate transactional data (Cloud SQL) from document/event data stores.
4. Align migration tooling with deployment strategy.

## How to implement observability in GCP

1. Export metrics/traces/logs using Micrometer/OpenTelemetry compatible tooling.
2. Correlate request IDs across HTTP, async events, and DB operations.
3. Define SLO-driven alerts for core business flows.
4. Validate dashboards during load and failure drills.

## Common Warnings & Pitfalls

- Ignoring version compatibility between Spring Boot and cloud libraries.
- Over-privileged service accounts shared across unrelated services.
- Pub/Sub consumers without idempotency protections.
- Running local/test environments with production cloud resources.
- Missing retry/backoff policies for transient cloud failures.

## Common Errors and Fixes

| Symptom | Root Cause | Fix |
|---|---|---|
| Authentication failure on startup | ADC not available or wrong service account | Configure runtime identity and verify IAM permissions |
| Pub/Sub messages reprocessed repeatedly | Ack not issued after success | Ensure ack occurs only after durable processing |
| Cloud SQL connection exhaustion | Pool misconfiguration and slow queries | Tune pool size/timeouts and optimize queries |
| Storage access denied | Missing IAM role on bucket/object | Grant minimal required roles to service account |

## Advanced Tips

- Create internal integration test profiles backed by emulators where possible.
- Standardize cloud resource naming and tagging labels for governance.
- Use contract tests for message schemas and version evolution.
- Add runbooks for quota errors, regional incidents, and rollback paths.

## How to use extended references

- Read [Version History](references/version-history.md) before upgrades, migrations, or compatibility decisions.
- Read [Java and Kotlin Examples](references/java-kotlin-examples.md) for implementation-ready snippets and language-specific guidance.
- Read [Advanced Techniques](references/advanced-techniques.md) for specialist playbooks, incident tactics, and performance patterns.

