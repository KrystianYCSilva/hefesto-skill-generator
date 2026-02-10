---
name: gcp-cloud-run
description: |
  Guides Cloud Run service deployment, container hardening, revision traffic control, concurrency tuning, identity-based communication, and cold-start optimization.
  Use when: running containerized backend workloads on Cloud Run, optimizing cost and latency, or implementing secure service-to-service communication on GCP.
---

# GCP Cloud Run

Cloud Run brought serverless execution to container workflows, combining Knative principles with managed operations. This skill helps the agent deploy secure and efficient services with clear revision control and production tuning.

## How to prepare containers for Cloud Run

1. Build small, reproducible images with multi-stage Docker builds.
2. Ensure app listens on `$PORT` and exits gracefully on shutdown signals.
3. Run as non-root and avoid unnecessary OS packages.
4. Externalize all config through env vars and secret bindings.

## How to deploy and manage revisions

1. Treat each deployment as immutable revision.
2. Use tagged revisions for canary tests.
3. Route traffic gradually for risk control.
4. Keep rollback command path documented.

## How to tune concurrency, CPU, and memory

1. Set concurrency based on app threading model and downstream limits.
2. Choose CPU allocation mode according to latency goals.
3. Configure memory to avoid OOM while controlling cost.
4. Use min instances for low-latency critical paths.

## How to secure service-to-service communication

1. Use IAM-based identity between Cloud Run services.
2. Require authenticated invocations for internal APIs.
3. Validate audience and token issuer in downstream services.
4. Separate identities by service responsibility.

## How to integrate networking, domains, and secrets

1. Configure VPC connectors only when private resources require it.
2. Bind custom domains with managed certificates for public endpoints.
3. Use Secret Manager integrations for sensitive values.
4. Keep egress rules explicit for compliance requirements.

## Common Warnings & Pitfalls

- Deploying heavy images that increase startup latency.
- Concurrency too high for non-thread-safe frameworks.
- Publicly exposed internal services due missing auth policy.
- Ignoring container startup probe behavior under load.
- Overusing VPC connectors and increasing latency/cost unnecessarily.

## Common Errors and Fixes

| Symptom | Root Cause | Fix |
|---|---|---|
| Service never becomes ready | App not listening on `$PORT` | Update runtime config and container entrypoint |
| Frequent 503 during spikes | Insufficient scaling/concurrency settings | Tune max instances, concurrency, and downstream pool limits |
| `403 Forbidden` between services | Missing invoker IAM role or token audience mismatch | Grant correct role and validate ID token audience |
| Unexpected cold-start latency | Large image or no warm capacity | Reduce image size and configure min instances |

## Advanced Tips

- Build load profiles per endpoint and tune concurrency per service type.
- Use revision tags to run shadow/canary validation before full cutover.
- Add structured logs with trace context for each request.
- Define separate Cloud Run services for latency-critical and batch traffic.

## How to use extended references

- Read [Version History](references/version-history.md) before upgrades, migrations, or compatibility decisions.
- Read [Java and Kotlin Examples](references/java-kotlin-examples.md) for implementation-ready snippets and language-specific guidance.
- Read [Advanced Techniques](references/advanced-techniques.md) for specialist playbooks, incident tactics, and performance patterns.

