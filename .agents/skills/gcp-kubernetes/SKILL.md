---
name: gcp-kubernetes
description: |
  Guides Google Kubernetes Engine architecture, workload deployment patterns, networking, identity, autoscaling, and production operations.
  Use when: deploying or operating containerized microservices on GKE, choosing Autopilot vs Standard, or improving reliability and platform governance.
---

# GCP Kubernetes

GKE packages upstream Kubernetes with managed control plane operations, enabling teams to run complex container platforms with reduced operational burden. This skill helps the agent apply Kubernetes patterns in a production-safe way on Google Cloud.

## How to choose GKE mode and cluster topology

1. Use Autopilot for reduced platform operations and opinionated defaults.
2. Use Standard for advanced node/policy/network control.
3. Design clusters by environment and blast-radius boundaries.
4. Define multi-zone/regional strategy for availability targets.

## How to deploy workloads correctly

1. Use `Deployment` for stateless services and `StatefulSet` when identity/storage are required.
2. Add readiness/liveness probes for safe rollout and recovery.
3. Set CPU/memory requests and limits explicitly.
4. Use rolling updates with surge/unavailable thresholds aligned to SLO.

## How to manage networking and traffic ingress

1. Use `Service` abstraction for stable discovery.
2. Use Ingress/Gateway for external routing and TLS termination.
3. Segment workloads with namespaces and network policies.
4. Keep internal-only services private by default.

## How to secure identity and secrets

1. Use Workload Identity for pod-to-GCP access.
2. Avoid static service account keys inside pods.
3. Manage secrets with Secret Manager integrations when possible.
4. Apply RBAC with least privilege for platform and app teams.

## How to implement autoscaling and resilience

1. Use HPA for workload scaling by CPU/custom metrics.
2. Use cluster autoscaling policies aligned with workload peaks.
3. Add PodDisruptionBudgets for controlled maintenance events.
4. Validate graceful shutdown and retry behavior across dependencies.

## Common Warnings & Pitfalls

- Missing resource requests leading to noisy-neighbor instability.
- Over-privileged service accounts in workload namespaces.
- Ingress and service rules drifting from intended architecture.
- No budget controls for cluster growth.
- Deploying without rollout and rollback guardrails.

## Common Errors and Fixes

| Symptom | Root Cause | Fix |
|---|---|---|
| Pods restart repeatedly | Probe misconfiguration or insufficient resources | Fix probe endpoints/timeouts and tune requests/limits |
| Pending pods during scale-out | Node capacity or quota limits | Enable autoscaling and validate regional quota headroom |
| Service inaccessible externally | Ingress misrouting/TLS config issue | Review Ingress/Gateway rules and certificate bindings |
| `403` when accessing GCP APIs | Workload identity mapping missing | Bind Kubernetes SA to correct GCP service account |

## Advanced Tips

- Standardize Helm/Kustomize templates with guardrails per workload class.
- Use GitOps flow for auditable cluster changes.
- Define SRE runbooks for incident classes (network, quota, rollout, node failures).
- Use policy-as-code for security and compliance baselines.

## How to use extended references

- Read [Version History](references/version-history.md) before upgrades, migrations, or compatibility decisions.
- Read [Java and Kotlin Examples](references/java-kotlin-examples.md) for implementation-ready snippets and language-specific guidance.
- Read [Advanced Techniques](references/advanced-techniques.md) for specialist playbooks, incident tactics, and performance patterns.

