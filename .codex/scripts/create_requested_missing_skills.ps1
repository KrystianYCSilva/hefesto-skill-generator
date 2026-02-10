$ErrorActionPreference = "Stop"

$skills = @(
  @{
    Name = "gcp-datastore"
    Title = "GCP Datastore"
    Description = "Guides Firestore in Datastore mode for schema modeling, query patterns, consistency, and backend integration."
    UseWhen = "building key-value and entity workloads on GCP where Datastore mode fits access patterns and operational constraints."
    Scope = "entity modeling, index planning, and consistency in Datastore mode"
    Keywords = @("Datastore mode", "kind and entity", "ancestor query", "indexes", "eventual consistency")
    JavaSnippet = "Entity task = Entity.newBuilder(keyFactory.newKey(`"t1`")).set(`"status`", `"OPEN`").build(); datastore.put(task);"
    KotlinSnippet = "val task = Entity.newBuilder(keyFactory.newKey(`"t1`")).set(`"status`", `"OPEN`").build(); datastore.put(task)"
    Refs = @("https://cloud.google.com/datastore/docs", "https://cloud.google.com/datastore/docs/concepts/overview", "https://cloud.google.com/datastore/docs/concepts/queries")
  },
  @{
    Name = "gcp-bigquery"
    Title = "GCP BigQuery"
    Description = "Guides BigQuery data modeling, SQL performance optimization, cost controls, and JVM integration patterns."
    UseWhen = "building analytics pipelines, reporting workloads, and event-driven data marts on GCP."
    Scope = "dataset design, partitioning and clustering, query optimization, and governance"
    Keywords = @("partitioned tables", "clustering", "slot usage", "cost controls", "materialized views")
    JavaSnippet = "TableResult result = bigquery.query(QueryJobConfiguration.of(`"SELECT COUNT(*) c FROM ds.orders`"));"
    KotlinSnippet = "val result = bigquery.query(QueryJobConfiguration.of(`"SELECT COUNT(*) c FROM ds.orders`"))"
    Refs = @("https://cloud.google.com/bigquery/docs", "https://cloud.google.com/bigquery/docs/best-practices-performance-overview", "https://cloud.google.com/bigquery/docs/samples")
  },
  @{
    Name = "gcp-cloud-tasks"
    Title = "GCP Cloud Tasks"
    Description = "Guides Cloud Tasks queue architecture, retry policy design, idempotent handlers, and secure HTTP dispatch workflows."
    UseWhen = "orchestrating deferred work, background jobs, and resilient task execution in GCP microservices."
    Scope = "queue design, retry/backoff strategy, task routing, and operational safeguards"
    Keywords = @("queue and task", "idempotency key", "retry config", "dead-letter", "rate limits")
    JavaSnippet = "Task task = Task.newBuilder().setHttpRequest(HttpRequest.newBuilder().setUrl(url).build()).build(); client.createTask(queuePath, task);"
    KotlinSnippet = "val task = Task.newBuilder().setHttpRequest(HttpRequest.newBuilder().setUrl(url).build()).build(); client.createTask(queuePath, task)"
    Refs = @("https://cloud.google.com/tasks/docs", "https://cloud.google.com/tasks/docs/creating-http-target-tasks", "https://cloud.google.com/tasks/docs/configuring-queues")
  },
  @{
    Name = "docker"
    Title = "Docker"
    Description = "Guides Docker image design, container runtime hardening, build optimization, and developer workflow integration."
    UseWhen = "packaging Java and Kotlin services for reproducible local development, CI pipelines, and cloud deployment."
    Scope = "Dockerfile design, image security, runtime settings, and build performance"
    Keywords = @("multi-stage builds", "slim images", "non-root", "layer cache", "runtime env")
    JavaSnippet = "FROM eclipse-temurin:21-jre\nWORKDIR /app\nCOPY build/libs/app.jar app.jar\nENTRYPOINT [`"java`",`"-jar`",`"/app/app.jar`"]"
    KotlinSnippet = "Use the same JVM image strategy for Kotlin Spring/Ktor services with deterministic jar naming."
    Refs = @("https://docs.docker.com/", "https://docs.docker.com/build/", "https://docs.docker.com/engine/security/")
  },
  @{
    Name = "kubernetes"
    Title = "Kubernetes"
    Description = "Guides Kubernetes workload design, service networking, security policy, and production operations for distributed applications."
    UseWhen = "running containerized services at scale with declarative deployment, autoscaling, and resilience controls."
    Scope = "workload manifests, networking, autoscaling, and operational governance"
    Keywords = @("deployment", "service", "ingress", "HPA", "pod disruption budget")
    JavaSnippet = "apiVersion: apps/v1\nkind: Deployment\nmetadata:\n  name: orders-api"
    KotlinSnippet = "Use readiness and liveness probes with Kotlin services to avoid restart storms under startup load."
    Refs = @("https://kubernetes.io/docs/home/", "https://kubernetes.io/docs/concepts/", "https://kubernetes.io/docs/tasks/")
  },
  @{
    Name = "resilience4j"
    Title = "Resilience4j"
    Description = "Guides resilience patterns with Resilience4j including circuit breaker, retry, bulkhead, and rate limiter design."
    UseWhen = "hardening Java and Kotlin microservices against dependency instability and cascading failures."
    Scope = "fault-tolerance policies, timeout budgets, and safe degradation patterns"
    Keywords = @("circuit breaker", "retry", "bulkhead", "rate limiter", "time limiter")
    JavaSnippet = "CircuitBreaker cb = CircuitBreaker.ofDefaults(`"inventory`"); Supplier<Stock> d = CircuitBreaker.decorateSupplier(cb, this::callInventory);"
    KotlinSnippet = "val cb = CircuitBreaker.ofDefaults(`"inventory`")"
    Refs = @("https://resilience4j.readme.io/", "https://resilience4j.readme.io/docs/getting-started-3", "https://docs.spring.io/spring-cloud-circuitbreaker/reference/")
  },
  @{
    Name = "logger"
    Title = "Logger"
    Description = "Guides logging architecture for Java and Kotlin services with structured logs, correlation IDs, and production-safe verbosity."
    UseWhen = "designing or refactoring logging strategy for microservices, webapps, and asynchronous pipelines."
    Scope = "structured logging, log levels, trace correlation, and operational diagnostics"
    Keywords = @("SLF4J", "Logback", "JSON logs", "correlation id", "log governance")
    JavaSnippet = "log.info(`"order_created orderId={} customerId={}`", orderId, customerId);"
    KotlinSnippet = "logger.info(`"order_created orderId={} customerId={}`", orderId, customerId)"
    Refs = @("https://www.slf4j.org/manual.html", "https://logback.qos.ch/documentation.html", "https://docs.spring.io/spring-boot/reference/features/logging.html")
  },
  @{
    Name = "prometheus"
    Title = "Prometheus"
    Description = "Guides Prometheus metric modeling, scrape architecture, alert strategy, and JVM observability integration."
    UseWhen = "building metrics-driven monitoring for Java and Kotlin services and creating actionable alerting signals."
    Scope = "metric naming, label cardinality, scraping, recording rules, and alert design"
    Keywords = @("PromQL", "metric labels", "scrape configs", "recording rules", "alerts")
    JavaSnippet = "Counter.builder(`"orders_total`").tag(`"status`", `"success`").register(registry).increment();"
    KotlinSnippet = "Timer.builder(`"checkout_latency`").register(registry).record { processCheckout() }"
    Refs = @("https://prometheus.io/docs/introduction/overview/", "https://prometheus.io/docs/practices/naming/", "https://prometheus.io/docs/prometheus/latest/querying/basics/")
  },
  @{
    Name = "gcp-logger"
    Title = "GCP Logger"
    Description = "Guides Cloud Logging usage with structured payloads, sinks, retention, and production diagnostics workflows."
    UseWhen = "operating GCP workloads that need centralized logs, compliance retention, and low-noise incident triage."
    Scope = "Cloud Logging ingestion, structured fields, sinks, and retention policies"
    Keywords = @("Cloud Logging", "log sinks", "retention", "structured payload", "log-based metrics")
    JavaSnippet = "logger.atInfo().log(`"event=payment_approved orderId=%s`", orderId);"
    KotlinSnippet = "logger.info(`"event=payment_approved orderId={}`", orderId)"
    Refs = @("https://cloud.google.com/logging/docs", "https://cloud.google.com/logging/docs/structured-logging", "https://cloud.google.com/logging/docs/log-based-metrics")
  },
  @{
    Name = "gcp-trace"
    Title = "GCP Trace"
    Description = "Guides distributed tracing on GCP with Cloud Trace, context propagation, latency analysis, and JVM instrumentation."
    UseWhen = "diagnosing latency and dependency issues across distributed Java and Kotlin systems on GCP."
    Scope = "trace instrumentation, context propagation, and cross-service latency analysis"
    Keywords = @("Cloud Trace", "OpenTelemetry", "trace context", "span tags", "critical path")
    JavaSnippet = "Span span = tracer.spanBuilder(`"reserve-stock`").startSpan();"
    KotlinSnippet = "val span = tracer.spanBuilder(`"reserve-stock`").startSpan()"
    Refs = @("https://cloud.google.com/trace/docs", "https://cloud.google.com/trace/docs/trace-overview", "https://cloud.google.com/trace/docs/setup/java-ot")
  },
  @{
    Name = "software-design"
    Title = "Software Design"
    Description = "Guides software design decisions across modularity, cohesion, coupling, and pattern selection for maintainable systems."
    UseWhen = "planning or reviewing architecture and design tradeoffs in Java and Kotlin backend projects."
    Scope = "design principles, pattern fit, quality attributes, and tradeoff reasoning"
    Keywords = @("SOLID", "cohesion", "coupling", "design patterns", "architecture decisions")
    JavaSnippet = "Prefer composition over inheritance when evolving domain behavior boundaries."
    KotlinSnippet = "Use sealed hierarchies and value classes to model constrained domain concepts."
    Refs = @("https://martinfowler.com/architecture/", "https://refactoring.guru/design-patterns", "https://c4model.com/")
  },
  @{
    Name = "software-testing"
    Title = "Software Testing"
    Description = "Guides software testing strategy from unit to integration and contract tests with reliability-focused quality gates."
    UseWhen = "defining test architecture for backend systems and preventing regressions in evolving services."
    Scope = "test pyramid, contract testing, deterministic fixtures, and CI quality gates"
    Keywords = @("unit tests", "integration tests", "contract tests", "test data", "CI gates")
    JavaSnippet = "@Test void shouldCreateOrder() { assertEquals(`"CREATED`", service.create(cmd).status()); }"
    KotlinSnippet = "@Test fun shouldCreateOrder() { assertEquals(`"CREATED`", service.create(cmd).status) }"
    Refs = @("https://martinfowler.com/testing/", "https://junit.org/junit5/docs/current/user-guide/", "https://testcontainers.com/guides/")
  },
  @{
    Name = "software-quality"
    Title = "Software Quality"
    Description = "Guides software quality management using measurable attributes, quality gates, and continuous improvement loops."
    UseWhen = "defining engineering standards, quality metrics, and release criteria for software products."
    Scope = "quality attributes, defect prevention, and measurable engineering outcomes"
    Keywords = @("ISO 25010", "defect leakage", "technical debt", "quality gates", "continuous improvement")
    JavaSnippet = "Track quality metrics per module and enforce fail thresholds in CI."
    KotlinSnippet = "Combine static analysis and mutation testing to track quality trend over time."
    Refs = @("https://iso25000.com/index.php/en/iso-25000-standards/iso-25010", "https://martinfowler.com/bliki/TechnicalDebt.html", "https://sre.google/sre-book/table-of-contents/")
  },
  @{
    Name = "quality-assurance"
    Title = "Quality Assurance"
    Description = "Guides QA practices for process quality, release readiness, risk-based validation, and defect prevention in software delivery."
    UseWhen = "setting QA governance, release criteria, and cross-team validation workflows."
    Scope = "QA process design, risk-based testing, and release confidence management"
    Keywords = @("QA strategy", "risk-based testing", "release criteria", "defect prevention", "auditability")
    JavaSnippet = "Use release checklists tied to automated verification and risk gates."
    KotlinSnippet = "Keep QA signals visible in pipelines and deployment dashboards."
    Refs = @("https://www.istqb.org/", "https://www.iso.org/iso-9001-quality-management.html", "https://sre.google/workbook/table-of-contents/")
  },
  @{
    Name = "software-project-manager"
    Title = "Software Project Manager"
    Description = "Guides software project management for planning, risk control, execution tracking, and stakeholder alignment."
    UseWhen = "leading engineering delivery with multiple teams, dependencies, and architectural workstreams."
    Scope = "planning, risk management, execution control, and communication cadence"
    Keywords = @("scope", "schedule", "risk register", "stakeholder map", "delivery governance")
    JavaSnippet = "Break architecture epics into measurable increments with clear acceptance criteria."
    KotlinSnippet = "Use roadmap checkpoints tied to technical risk reduction and integration milestones."
    Refs = @("https://www.pmi.org/pmbok-guide-standards", "https://www.atlassian.com/agile/project-management", "https://www.scrum.org/resources/what-is-scrum")
  },
  @{
    Name = "software-construction"
    Title = "Software Construction"
    Description = "Guides software construction practices for code organization, build reliability, maintainability, and technical execution quality."
    UseWhen = "improving coding standards, build discipline, and implementation consistency in software teams."
    Scope = "implementation practices, build discipline, and maintainable construction workflows"
    Keywords = @("coding standards", "build reproducibility", "modularity", "refactoring", "continuous integration")
    JavaSnippet = "Use incremental refactoring and small commits to reduce integration risk."
    KotlinSnippet = "Prefer explicit APIs and immutable DTOs to reduce construction defects."
    Refs = @("https://www.computer.org/education/bodies-of-knowledge/software-engineering", "https://martinfowler.com/bliki/ContinuousIntegration.html", "https://12factor.net/")
  },
  @{
    Name = "requirements-engineering"
    Title = "Requirements Engineering"
    Description = "Guides requirements engineering from elicitation to specification, validation, and traceability for software projects."
    UseWhen = "defining clear, testable requirements and controlling scope change across engineering delivery."
    Scope = "requirement elicitation, specification quality, validation, and traceability"
    Keywords = @("functional requirements", "non-functional requirements", "acceptance criteria", "traceability", "change control")
    JavaSnippet = "Convert each requirement into executable acceptance tests where possible."
    KotlinSnippet = "Map requirements to domain capabilities and testable user outcomes."
    Refs = @("https://www.iiba.org/standards-and-resources/babok/", "https://www.ireb.org/en/", "https://www.volere.org/")
  },
  @{
    Name = "api-design"
    Title = "API Design"
    Description = "Guides API design for REST and service interfaces with versioning, compatibility, observability, and consumer-centric governance."
    UseWhen = "defining or evolving APIs for backend services used by webapps, mobile, or partner integrations."
    Scope = "contract design, compatibility policy, versioning, and API governance"
    Keywords = @("OpenAPI", "versioning", "error model", "idempotency", "consumer contracts")
    JavaSnippet = "Use explicit DTO schemas and stable error contract for all public endpoints."
    KotlinSnippet = "Enforce API compatibility checks in CI before publishing new versions."
    Refs = @("https://cloud.google.com/apis/design", "https://spec.openapis.org/oas/latest.html", "https://opensource.zalando.com/restful-api-guidelines/")
  },
  @{
    Name = "project-manager"
    Title = "Project Manager"
    Description = "Guides project management fundamentals for software initiatives including scope control, delivery planning, and communication governance."
    UseWhen = "coordinating execution across product, engineering, QA, and platform stakeholders."
    Scope = "project lifecycle control, stakeholder communication, and delivery assurance"
    Keywords = @("milestones", "dependencies", "risk management", "status reporting", "governance")
    JavaSnippet = "Plan technical milestones with explicit dependency and risk mitigation strategy."
    KotlinSnippet = "Keep team dashboards aligned with engineering and product outcomes."
    Refs = @("https://www.pmi.org/pmbok-guide-standards", "https://www.prince2.com/", "https://www.scrum.org/resources/scrum-guide")
  },
  @{
    Name = "agile-methodologies"
    Title = "Agile Methodologies"
    Description = "Guides agile methodologies for iterative delivery, feedback loops, and adaptive planning in software engineering teams."
    UseWhen = "running Scrum, Kanban, or hybrid agile practices in engineering organizations."
    Scope = "iterative planning, flow optimization, and empirical delivery management"
    Keywords = @("Scrum", "Kanban", "backlog", "iteration", "retrospective")
    JavaSnippet = "Link technical debt backlog items to sprint goals and quality metrics."
    KotlinSnippet = "Use lightweight architecture spikes to reduce uncertainty before implementation."
    Refs = @("https://agilemanifesto.org/", "https://www.scrum.org/resources/scrum-guide", "https://kanban.university/kanban-guide/")
  },
  @{
    Name = "parallel-computing"
    Title = "Parallel Computing"
    Description = "Guides parallel computing patterns, workload partitioning, synchronization controls, and performance tuning for JVM systems."
    UseWhen = "optimizing CPU-bound workloads and designing concurrent processing in Java and Kotlin applications."
    Scope = "parallelization strategy, synchronization, and performance measurement"
    Keywords = @("thread pools", "fork-join", "coroutines", "contention", "throughput")
    JavaSnippet = "ForkJoinPool.commonPool().submit(() -> processChunk(chunk));"
    KotlinSnippet = "withContext(Dispatchers.Default) { chunks.map { async { process(it) } }.awaitAll() }"
    Refs = @("https://docs.oracle.com/javase/tutorial/essential/concurrency/", "https://kotlinlang.org/docs/coroutines-overview.html", "https://www.openmp.org/resources/refguides/")
  },
  @{
    Name = "distributed-systems"
    Title = "Distributed Systems"
    Description = "Guides distributed systems design with consistency models, failure handling, coordination, and scalable service interactions."
    UseWhen = "building microservices and event-driven systems that must handle network partitions, retries, and partial failures."
    Scope = "consistency tradeoffs, coordination patterns, and failure-aware architecture"
    Keywords = @("CAP tradeoffs", "consensus", "eventual consistency", "timeouts", "idempotency")
    JavaSnippet = "Implement idempotency and timeout budgets in every remote call path."
    KotlinSnippet = "Model retries and circuit-breakers explicitly for remote dependency boundaries."
    Refs = @("https://martinfowler.com/articles/patterns-of-distributed-systems/", "https://microservices.io/", "https://sre.google/sre-book/distributed-periodic-scheduling/")
  },
  @{
    Name = "cloud-computing"
    Title = "Cloud Computing"
    Description = "Guides cloud computing principles, service model tradeoffs, reliability engineering, and cost-aware architecture decisions."
    UseWhen = "designing, migrating, or operating applications across cloud platforms with scalable and resilient architectures."
    Scope = "IaaS/PaaS/serverless tradeoffs, reliability, security, and cost governance"
    Keywords = @("IaaS", "PaaS", "serverless", "cloud architecture", "cost optimization")
    JavaSnippet = "Select runtime model based on latency, scaling, operational burden, and compliance requirements."
    KotlinSnippet = "Design cloud-native modules with explicit failure handling and observability contracts."
    Refs = @("https://csrc.nist.gov/pubs/sp/800/145/final", "https://cloud.google.com/architecture", "https://learn.microsoft.com/en-us/azure/architecture/")
  },
  @{
    Name = "database-design"
    Title = "Database Design"
    Description = "Guides relational database design with normalization, denormalization tradeoffs, indexing strategy, and query-driven schema evolution."
    UseWhen = "modeling transactional data domains and optimizing long-term maintainability and query performance."
    Scope = "schema modeling, constraints, indexing, and evolution strategy"
    Keywords = @("normalization", "indexes", "constraints", "ER modeling", "query plans")
    JavaSnippet = "Model aggregate boundaries before table decomposition to avoid accidental coupling."
    KotlinSnippet = "Keep schema migrations aligned with domain versioning and API compatibility."
    Refs = @("https://www.oracle.com/database/what-is-database-design/", "https://www.postgresql.org/docs/current/ddl.html", "https://learn.microsoft.com/en-us/sql/relational-databases/databases/database-design?view=sql-server-ver16")
  },
  @{
    Name = "hibernate-jpa"
    Title = "Hibernate JPA"
    Description = "Guides Hibernate and JPA usage with entity modeling, transaction boundaries, query optimization, and migration-safe mapping strategies."
    UseWhen = "building Java and Kotlin persistence layers with Hibernate/JPA and needing performance-aware ORM patterns."
    Scope = "entity mapping, fetch strategy, transaction design, and query performance"
    Keywords = @("entity mapping", "lazy loading", "N+1", "entity graph", "transaction boundaries")
    JavaSnippet = "@Entity class OrderEntity { @Id Long id; @ManyToOne(fetch = FetchType.LAZY) CustomerEntity customer; }"
    KotlinSnippet = "@Entity class OrderEntity(@Id var id: Long? = null)"
    Refs = @("https://hibernate.org/orm/documentation/", "https://docs.jboss.org/hibernate/orm/current/userguide/html_single/Hibernate_User_Guide.html", "https://jakarta.ee/specifications/persistence/")
  },
  @{
    Name = "database-migrations"
    Title = "Database Migrations"
    Description = "Guides database migration strategy with versioned scripts, backward compatibility, rollout safety, and rollback planning."
    UseWhen = "evolving database schemas in production systems without downtime or data integrity regressions."
    Scope = "schema migration lifecycle, rollout sequencing, and data safety controls"
    Keywords = @("Flyway", "Liquibase", "expand-contract", "backward compatibility", "rollback")
    JavaSnippet = "Use expand-and-contract migrations for zero-downtime releases across multiple services."
    KotlinSnippet = "Gate deployment on migration status checks and compatibility tests."
    Refs = @("https://flywaydb.org/documentation/", "https://www.liquibase.com/documentation", "https://martinfowler.com/articles/evodb.html")
  }
)

function Build-SkillText {
  param([hashtable]$S)

  $pit = @(
    "Architecture decisions are implicit and undocumented, causing long-term drift.",
    "Operational controls are added late, increasing incident recovery time.",
    "Compatibility strategy is missing for evolving integrations and schemas.",
    "Quality gates are inconsistent across environments and release stages."
  )
  $errs = @(
    "Production regression after deployment|Configuration or contract drift across environments|Add compatibility checks, staged rollout, and rollback criteria.",
    "Latency spikes under load|Missing timeout and backpressure policies|Define budgets, tune pools, and monitor saturation indicators.",
    "Integration failures after change|Versioning and contract tests not enforced|Apply contract governance and CI compatibility gates."
  )

  $pitText = ($pit | ForEach-Object { "- $_" }) -join "`n"
  $errRows = ($errs | ForEach-Object { $p = $_ -split "\|"; "| $($p[0]) | $($p[1]) | $($p[2]) |" }) -join "`n"
  $refs = ($S.Refs | ForEach-Object { "- [Official Documentation]($_)" }) -join "`n"
  $keywords = ($S.Keywords | ForEach-Object { "- $_" }) -join "`n"

  return @"
---
name: $($S.Name)
description: |
  $($S.Description)
  Use when: $($S.UseWhen)
---

# $($S.Title)

This skill supports professional execution in: $($S.Scope).
Use it to keep architecture decisions explicit, implementation consistent, and operations reliable.

## How to define architecture and boundaries

- Establish explicit contracts for core interfaces, data flows, and ownership.
- Keep domain behavior separate from infrastructure details and framework glue.
- Define compatibility policy before introducing schema or contract changes.
- Document tradeoffs and decisions in architecture records.

## How to implement with Java and Kotlin

- Prefer constructor injection and explicit DTOs in service boundaries.
- Enforce nullability and serialization consistency between Java and Kotlin modules.
- Keep cross-module interfaces small, typed, and version-aware.
- Add contract tests for external integrations and critical internal boundaries.

## How to operate and harden in production

- Define SLOs and alert thresholds tied to user-facing outcomes.
- Implement staged rollout and rollback strategy for every critical change.
- Track dependency saturation, retries, and failure amplification indicators.
- Keep runbooks updated with tested mitigation steps.

## How to use extended references

- Read [Version History](references/version-history.md) before upgrades, migrations, or compatibility decisions.
- Read [Java and Kotlin Examples](references/java-kotlin-examples.md) for implementation-ready snippets and language-specific guidance.
- Read [Advanced Techniques](references/advanced-techniques.md) for specialist playbooks, incident tactics, and performance patterns.

## Common Warnings & Pitfalls

$pitText

## Common Errors and Fixes

| Symptom | Root Cause | Fix |
|---|---|---|
$errRows

## Keywords

$keywords

## References

$refs
"@
}

function Build-VersionText {
  param([hashtable]$S)
  return @"
# Version History and Usage Divergences

## Evolution Notes

- Domain: $($S.Scope).
- Common divergence areas: $(($S.Keywords | Select-Object -First 4) -join ", ").
- Teams with explicit governance and compatibility tests tend to scale safer.
- Teams without rollout discipline usually see integration regressions and unstable operations.

## Upgrade and Migration Checklist

- Validate dependencies and runtime compatibility in staging.
- Execute contract and integration test suites before release.
- Keep rollback artifacts, migration notes, and abort criteria available.
- Capture observed divergences and feed them into architecture runbooks.
"@
}

function Build-ExamplesText {
  param([hashtable]$S)
  return @"
# Java and Kotlin Usage Examples

## Java Example

```java
$($S.JavaSnippet)
```

## Kotlin Example

```kotlin
$($S.KotlinSnippet)
```

## Practical Language Tips

- Keep API and event contracts typed and versioned.
- Align nullability, enums, and date/time serialization across Java and Kotlin.
- Use shared contract tests to prevent cross-language regressions.
- Prefer immutable transport models for integration boundaries.
"@
}

function Build-AdvancedText {
  param([hashtable]$S)
  return @"
# Expert Techniques

## Specialist Playbook

- Build architecture fitness checks for constraints in: $($S.Scope).
- Track leading indicators: latency budget drift, retry amplification, and dependency saturation.
- Run canary validations before broad rollout for high-risk changes.
- Convert incident findings into deterministic tests and operational runbooks.

## Advanced Governance

- Use ADRs tied to measurable outcomes, not only descriptive documentation.
- Maintain a risk register for critical dependencies and upgrade paths.
- Review architectural debt periodically with business impact context.
- Keep quality gates stable across local, CI, and production release flows.
"@
}

foreach ($s in $skills) {
  $dir = ".codex/skills/$($s.Name)"
  $refDir = "$dir/references"
  New-Item -ItemType Directory -Force $dir, $refDir | Out-Null

  Set-Content -Path "$dir/SKILL.md" -Value (Build-SkillText -S $s)
  Set-Content -Path "$refDir/version-history.md" -Value (Build-VersionText -S $s)
  Set-Content -Path "$refDir/java-kotlin-examples.md" -Value (Build-ExamplesText -S $s)
  Set-Content -Path "$refDir/advanced-techniques.md" -Value (Build-AdvancedText -S $s)
}

Write-Output ("created_skills=" + $skills.Count)

