---
name: advanced-techniques
description: |
  Documentation file for agent operations and skill usage.
  Use when: you need procedural guidance for agent execution and context management.
---

# Expert Techniques

- Use `EXPLAIN (ANALYZE, BUFFERS, WAL)` for write-heavy troubleshooting, not only read plans.
- Combine partial indexes with predicate-stable query contracts.
- Track bloat trend and autovacuum lag as first-class SLO signals.
- Use lock graph analysis (`pg_locks`) during deadlock/perf incidents.

## Specialist Playbook

- Build plan-regression gates for top queries using sampled production statistics.
- Track vacuum lag and bloat budgets per high-write table as operational SLOs.
- Use controlled failover drills to validate RPO/RTO and connection recovery behavior.
- Maintain lock-contention dashboards and deadlock triage runbooks.

