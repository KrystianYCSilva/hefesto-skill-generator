$ErrorActionPreference = "Stop"

$skills = @(
  @{
    Name = "gcp-cloud-functions"
    Title = "GCP Cloud Functions"
    Description = "Guides Google Cloud Functions architecture, trigger selection, secure runtime integration, and operational tuning for Java and Kotlin workloads."
    UseWhen = "building event-driven serverless handlers, lightweight HTTP endpoints, or moving JVM integrations to function-based execution on GCP."
    Scope = "Cloud Functions triggers, packaging, IAM, retries, and cold start control"
    Keywords = @("HTTP triggers", "Eventarc", "Pub/Sub events", "IAM service accounts", "cold starts")
    JavaSnippet = "public class Handler implements HttpFunction { public void service(HttpRequest req, HttpResponse res) throws IOException { res.getWriter().write(`"ok`"); } }"
    KotlinSnippet = "class Handler : HttpFunction { override fun service(req: HttpRequest, res: HttpResponse) { res.writer.write(`"ok`") } }"
    Refs = @("https://cloud.google.com/functions/docs", "https://cloud.google.com/functions/docs/concepts/exec", "https://cloud.google.com/functions/docs/samples/functions-helloworld-http")
  },
  @{
    Name = "gcp-cloud-sql"
    Title = "GCP Cloud SQL"
    Description = "Guides Cloud SQL topology, secure connectivity, performance tuning, backup strategy, and production operations for Java and Kotlin services."
    UseWhen = "running transactional relational workloads on GCP and integrating Spring or Ktor services with managed PostgreSQL or MySQL."
    Scope = "Cloud SQL connectivity, pool sizing, failover planning, and restore drills"
    Keywords = @("Cloud SQL connector", "Hikari pool tuning", "read replicas", "PITR backups", "failover")
    JavaSnippet = "HikariConfig cfg = new HikariConfig(); cfg.setJdbcUrl(jdbcUrl); cfg.setMaximumPoolSize(20); DataSource ds = new HikariDataSource(cfg);"
    KotlinSnippet = "val ds = HikariDataSource(HikariConfig().apply { jdbcUrl = url; maximumPoolSize = 20 })"
    Refs = @("https://cloud.google.com/sql/docs", "https://cloud.google.com/sql/docs/postgres/manage-connections", "https://cloud.google.com/sql/docs/postgres/backup-recovery")
  },
  @{
    Name = "gcp-firestore"
    Title = "GCP Firestore"
    Description = "Guides Firestore document modeling, index strategy, transactional patterns, and JVM integration for scalable backend systems."
    UseWhen = "building document-oriented services, read projections, and low-latency event-driven views on GCP."
    Scope = "Collection design, composite indexes, transactions, and consistency windows"
    Keywords = @("document model", "composite indexes", "transaction retries", "hot partitions", "read projections")
    JavaSnippet = "ApiFuture<DocumentSnapshot> snap = db.collection(`"orders`").document(id).get();"
    KotlinSnippet = "val snap = db.collection(`"orders`").document(id).get().get()"
    Refs = @("https://cloud.google.com/firestore/docs", "https://cloud.google.com/firestore/docs/query-data/index-overview", "https://cloud.google.com/firestore/docs/samples")
  },
  @{
    Name = "gcp-secret-manager"
    Title = "GCP Secret Manager"
    Description = "Guides secret lifecycle management with Secret Manager, IAM boundaries, rotation workflows, and secure runtime consumption in Java and Kotlin."
    UseWhen = "managing credentials, API keys, certificates, and rotating sensitive configuration across GCP services."
    Scope = "Secret versioning, IAM least privilege, rotation windows, and auditability"
    Keywords = @("secret versions", "rotation", "least privilege IAM", "runtime secret loading", "audit logs")
    JavaSnippet = "SecretVersionName name = SecretVersionName.of(projectId, `"db-pass`", `"latest`");"
    KotlinSnippet = "val name = SecretVersionName.of(projectId, `"api-key`", `"latest`")"
    Refs = @("https://cloud.google.com/secret-manager/docs", "https://cloud.google.com/secret-manager/docs/best-practices", "https://cloud.google.com/iam/docs/roles-permissions/secretmanager")
  },
  @{
    Name = "gcp-observability"
    Title = "GCP Observability"
    Description = "Guides Cloud Logging, Monitoring, Trace, and SLO-driven alerting for Java and Kotlin distributed systems on GCP."
    UseWhen = "defining production observability baselines, reducing MTTR, and hardening incident response for cloud services."
    Scope = "Metrics, logs, traces, SLO burn-rate alerts, and incident diagnostics"
    Keywords = @("golden signals", "SLO burn rate", "trace context", "structured logging", "runbooks")
    JavaSnippet = "Timer.builder(`"checkout.latency`").tag(`"service`", `"checkout`").register(registry);"
    KotlinSnippet = "val span = tracer.spanBuilder(`"reserve-stock`").startSpan()"
    Refs = @("https://cloud.google.com/stackdriver/docs", "https://cloud.google.com/monitoring/alerts", "https://cloud.google.com/trace/docs")
  },
  @{
    Name = "gcp-cloud-build"
    Title = "GCP Cloud Build"
    Description = "Guides Cloud Build pipeline architecture, secure build identities, artifact promotion, and release orchestration for JVM services."
    UseWhen = "implementing CI/CD on GCP for Java and Kotlin microservices with controlled quality and deployment gates."
    Scope = "Build stages, security controls, cache strategy, and progressive delivery"
    Keywords = @("cloudbuild.yaml", "Artifact Registry", "build service account", "approval gates", "pipeline templates")
    JavaSnippet = "steps: - name: gcr.io/cloud-builders/mvn args: [`"-B`", `"test`"]"
    KotlinSnippet = "steps: - name: gcr.io/cloud-builders/gradle args: [`"test`", `"bootJar`"]"
    Refs = @("https://cloud.google.com/build/docs", "https://cloud.google.com/build/docs/build-config-file-schema", "https://cloud.google.com/build/docs/securing-builds")
  },
  @{
    Name = "gcp-api-gateway"
    Title = "GCP API Gateway"
    Description = "Guides API Gateway contract governance, auth policy, routing controls, and traffic protection for GCP-hosted backends."
    UseWhen = "publishing backend APIs with centralized policy enforcement and OpenAPI-managed ingress on GCP."
    Scope = "OpenAPI governance, JWT validation, quotas, and backend protection"
    Keywords = @("OpenAPI", "JWT auth", "route policies", "quotas", "gateway rollout")
    JavaSnippet = "Use OpenAPI-first contracts and map Spring controllers to stable response schemas."
    KotlinSnippet = "Keep Ktor or Spring Kotlin route contracts aligned with gateway OpenAPI definitions."
    Refs = @("https://cloud.google.com/api-gateway/docs", "https://cloud.google.com/api-gateway/docs/openapi-overview", "https://cloud.google.com/api-gateway/docs/authenticating-users-jwt")
  },
  @{
    Name = "spring-cloud-function"
    Title = "Spring Cloud Function"
    Description = "Guides Spring Cloud Function for transport-agnostic business logic, function composition, and serverless deployment patterns."
    UseWhen = "building reusable Java or Kotlin functions deployable to HTTP, messaging, Cloud Run, and Cloud Functions runtimes."
    Scope = "Function composition, adapter boundaries, and JVM serverless optimization"
    Keywords = @("Function beans", "composition", "HTTP adapter", "messaging adapter", "serverless packaging")
    JavaSnippet = "@Bean Function<OrderEvent, InvoiceEvent> issueInvoice() { return e -> new InvoiceEvent(e.id()); }"
    KotlinSnippet = "@Bean fun issueInvoice(): (OrderEvent) -> InvoiceEvent = { e -> InvoiceEvent(e.id) }"
    Refs = @("https://spring.io/projects/spring-cloud-function", "https://docs.spring.io/spring-cloud-function/reference/", "https://spring.io/blog/2018/10/22/serverless-java-with-spring-cloud-function")
  },
  @{
    Name = "spring-web-services-soap"
    Title = "Spring Web Services SOAP"
    Description = "Guides contract-first SOAP development with Spring Web Services, schema governance, endpoint security, and interoperability testing."
    UseWhen = "implementing or modernizing enterprise SOAP services in Spring with strict WSDL and XSD compatibility."
    Scope = "Spring-WS endpoints, WSDL/XSD governance, WS-Security, and compatibility strategy"
    Keywords = @("contract-first", "WSDL", "XSD", "SOAP faults", "WS-Security")
    JavaSnippet = "@Endpoint class CustomerEndpoint { @PayloadRoot(namespace = NS, localPart = `"GetCustomerRequest`") }"
    KotlinSnippet = "@Endpoint class CustomerEndpoint(private val service: CustomerService)"
    Refs = @("https://spring.io/projects/spring-ws", "https://docs.spring.io/spring-ws/docs/current/reference/", "https://www.w3.org/TR/wsdl20/")
  },
  @{
    Name = "soap-web-services-java"
    Title = "SOAP Web Services Java"
    Description = "Guides SOAP and WS-* integration in Java and Kotlin ecosystems with contract management, interoperability controls, and secure operations."
    UseWhen = "maintaining legacy SOAP integrations, generating client stubs, or evolving enterprise web-service contracts safely."
    Scope = "JAX-WS interoperability, SOAP faults, security policy, and migration seams"
    Keywords = @("JAX-WS", "SOAP 1.2", "WSDL evolution", "fault contracts", "certificate management")
    JavaSnippet = "Service svc = Service.create(wsdlUrl, qname); MyPort port = svc.getPort(MyPort.class);"
    KotlinSnippet = "val port: MyPort = Service.create(wsdlUrl, qname).getPort(MyPort::class.java)"
    Refs = @("https://jakarta.ee/specifications/xml-web-services/", "https://docs.oracle.com/javase/tutorial/webservices/", "https://www.w3.org/TR/soap12-part1/")
  },
  @{
    Name = "servlet-webapp-java"
    Title = "Servlet WebApp Java"
    Description = "Guides servlet web application architecture with layered responsibilities, filter chains, session controls, and performance hardening."
    UseWhen = "building or maintaining Java and Kotlin servlet-based webapps with backend and frontend integration requirements."
    Scope = "Servlet lifecycle, filter order, session strategy, and webapp reliability"
    Keywords = @("filters", "session management", "MVC boundaries", "thread pool", "request lifecycle")
    JavaSnippet = "public class AuthFilter implements Filter { public void doFilter(...) { chain.doFilter(req, res); } }"
    KotlinSnippet = "class AuthFilter : Filter { override fun doFilter(req: ServletRequest, res: ServletResponse, chain: FilterChain) { chain.doFilter(req, res) } }"
    Refs = @("https://jakarta.ee/specifications/servlet/", "https://tomcat.apache.org/tomcat-10.1-doc/", "https://docs.oracle.com/javaee/7/tutorial/servlets.htm")
  },
  @{
    Name = "webapp-backend-frontend-integration"
    Title = "WebApp Backend Frontend Integration"
    Description = "Guides backend-frontend integration with stable contracts, BFF patterns, session and CORS policy, and coordinated release governance."
    UseWhen = "developing web applications where backend and frontend evolve together and require strict API compatibility and release choreography."
    Scope = "BFF design, OpenAPI contracts, browser security, and rollout governance"
    Keywords = @("BFF", "OpenAPI", "CORS", "session cookies", "contract tests")
    JavaSnippet = "record ApiError(String code, String message, String correlationId) {}"
    KotlinSnippet = "data class ApiError(val code: String, val message: String, val correlationId: String)"
    Refs = @("https://openapi.tools/", "https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS", "https://martinfowler.com/articles/micro-frontends.html")
  },
  @{
    Name = "hexagonal-architecture-java-kotlin"
    Title = "Hexagonal Architecture Java Kotlin"
    Description = "Guides hexagonal architecture in Java and Kotlin with ports/adapters, domain isolation, and migration from layered legacy systems."
    UseWhen = "refactoring business-critical services to isolate domain logic from frameworks, transport, persistence, and messaging details."
    Scope = "Ports and adapters, domain purity, boundary tests, and migration sequencing"
    Keywords = @("ports", "adapters", "domain core", "anti-corruption layer", "architecture tests")
    JavaSnippet = "public interface PaymentGatewayPort { PaymentResult authorize(PaymentCommand command); }"
    KotlinSnippet = "interface PaymentGatewayPort { fun authorize(command: PaymentCommand): PaymentResult }"
    Refs = @("https://alistair.cockburn.us/hexagonal-architecture/", "https://martinfowler.com/bliki/ArchitectureTest.html", "https://herbertograca.com/2017/09/14/ports-adapters-architecture/")
  },
  @{
    Name = "domain-driven-design-java-kotlin"
    Title = "Domain Driven Design Java Kotlin"
    Description = "Guides strategic and tactical DDD in Java and Kotlin, including bounded contexts, aggregates, ubiquitous language, and domain events."
    UseWhen = "modeling complex business domains, decomposing services by context, and reducing accidental coupling in evolving systems."
    Scope = "Bounded contexts, aggregates, context maps, domain events, and model evolution"
    Keywords = @("bounded context", "aggregate", "ubiquitous language", "context map", "domain event")
    JavaSnippet = "public final class Money { private final BigDecimal amount; private final Currency currency; }"
    KotlinSnippet = "@JvmInline value class CustomerId(val value: UUID)"
    Refs = @("https://domainlanguage.com/ddd/", "https://martinfowler.com/bliki/BoundedContext.html", "https://dddcommunity.org/")
  },
  @{
    Name = "event-driven-architecture-java-kotlin"
    Title = "Event Driven Architecture Java Kotlin"
    Description = "Guides event-driven architecture with Java and Kotlin using outbox, idempotent consumers, schema evolution, and consistency patterns."
    UseWhen = "building asynchronous microservices with domain events and needing reliable delivery, replay, and compatibility governance."
    Scope = "Event contracts, outbox/inbox, retries, dead-letter handling, and sagas"
    Keywords = @("outbox", "idempotency", "schema versioning", "dead-letter", "saga")
    JavaSnippet = "record OrderCreated(String eventId, String orderId, Instant occurredAt, int schemaVersion) {}"
    KotlinSnippet = "data class OrderCreated(val eventId: String, val orderId: String, val occurredAt: Instant, val schemaVersion: Int)"
    Refs = @("https://microservices.io/patterns/data/transactional-outbox.html", "https://www.enterpriseintegrationpatterns.com/", "https://martinfowler.com/articles/201701-event-driven.html")
  },
  @{
    Name = "layered-architecture-java-kotlin"
    Title = "Layered Architecture Java Kotlin"
    Description = "Guides layered architecture with strict dependency direction, clear service boundaries, and maintainable module structure in Java and Kotlin."
    UseWhen = "building controller-service-repository systems, enforcing architecture constraints, or cleaning boundary violations in legacy codebases."
    Scope = "Layer responsibilities, dependency direction, module boundaries, and architecture fitness checks"
    Keywords = @("controller-service-repository", "dependency rules", "module boundaries", "transaction layer", "architecture lint")
    JavaSnippet = "@Service class OrderApplicationService { /* use-case orchestration */ }"
    KotlinSnippet = "class OrderApplicationService(private val repo: OrderRepository)"
    Refs = @("https://martinfowler.com/bliki/LayeringPrinciples.html", "https://docs.spring.io/spring-framework/reference/", "https://herbertograca.com/2017/07/03/the-software-architecture-chronicles/")
  },
  @{
    Name = "multi-architecture-project-planning"
    Title = "Multi Architecture Project Planning"
    Description = "Guides planning systems that combine layered, hexagonal, microservices, and event-driven patterns with explicit boundary and rollout strategy."
    UseWhen = "designing projects that intentionally mix more than one architecture pattern and need a coherent evolution roadmap."
    Scope = "Pattern composition, boundary governance, phased migration, and architecture decision management"
    Keywords = @("hybrid architecture", "phased roadmap", "ADR", "fitness functions", "architecture governance")
    JavaSnippet = "Use multi-module builds and ADR templates to track boundary and dependency decisions."
    KotlinSnippet = "Use explicit module APIs and versioned contracts for cross-pattern integration points."
    Refs = @("https://martinfowler.com/articles/architectural-fitness-function.html", "https://microservices.io/patterns/", "https://martinfowler.com/articles/evodb.html")
  }
)

function Build-SkillText {
  param([hashtable]$S)
  $kw = ($S.Keywords | ForEach-Object { "`"$_`"" }) -join ", "
  $pit = @(
    "Over-coupling implementation to specific infrastructure details instead of explicit boundaries.",
    "Insufficient contract testing for changes touching $($S.Scope).",
    "Missing observability and rollback strategy for production incidents.",
    "Drift between runtime behavior and documented operational guidelines."
  )
  $err = @(
    "Unexpected behavior after deployment|Configuration and contract mismatch between environments|Add compatibility checks, diff configs, and run canary verification.",
    "Latency and error spikes under load|Missing timeout budgets or retry amplification|Set explicit timeout/retry policy and observe dependency saturation.",
    "Regression in integrations|Schema or interface drift without version guardrails|Adopt versioning policy and contract tests in CI."
  )
  $pitText = ($pit | ForEach-Object { "- $_" }) -join "`n"
  $errRows = ($err | ForEach-Object { $p = $_ -split "\|"; "| $($p[0]) | $($p[1]) | $($p[2]) |" }) -join "`n"
  $refs = ($S.Refs | ForEach-Object { "- [Official Documentation]($_)" }) -join "`n"

  return @"
---
name: $($S.Name)
description: |
  $($S.Description)
  Use when: $($S.UseWhen)
---

# $($S.Title)

$($S.Intro)
The main operating scope is: $($S.Scope). Prioritize stable contracts, operational clarity, and compatibility-first delivery.

## How to design architecture and boundaries

- Use explicit contracts for $($S.Scope).
- Keep ownership clear for each component and avoid implicit shared state.
- Define compatibility policy before introducing breaking changes.
- Keep technology choices aligned with quality attributes and delivery constraints.

## How to implement with Java and Kotlin

- Apply constructor-injected services and explicit DTO contracts.
- Keep framework and transport concerns out of business-core logic.
- Enforce deterministic error mapping and typed responses.
- Use static analysis and tests to prevent boundary regressions.

## How to operate and scale safely

- Define SLOs and alerts for latency, error rate, and saturation.
- Implement rollout plans with canary checks and rollback criteria.
- Keep runbooks updated with known failure modes and mitigations.
- Track dependency risk and budget for resilience patterns.

## How to troubleshoot production incidents

- Start with user-impacting symptoms, then trace to dependencies.
- Correlate logs, metrics, and traces using correlation identifiers.
- Validate recent deployments, config changes, and feature-flag state.
- Capture incident learnings as repeatable diagnostics and tests.

## Common Warnings & Pitfalls

$pitText

## Common Errors and Fixes

| Symptom | Root Cause | Fix |
|---|---|---|
$errRows

## How to use extended references

- Read [Version History](references/version-history.md) before upgrades, migrations, or compatibility decisions.
- Read [Java and Kotlin Examples](references/java-kotlin-examples.md) for implementation-ready snippets and language-specific guidance.
- Read [Advanced Techniques](references/advanced-techniques.md) for specialist playbooks, incident tactics, and performance patterns.

## References

$refs
"@
}

function Build-VersionText {
  param([hashtable]$S)
  return @"
# Version History and Usage Divergences

## Baseline Evolution

- This domain evolved with stronger emphasis on contract-first delivery and controlled rollout strategy.
- Tooling maturity increased observability and automation, but also increased governance requirements.
- Teams commonly diverge in usage due differences in boundary discipline and ownership models.

## Domain-Specific Divergence Notes

- Scope: $($S.Scope).
- Frequent divergence points: $((($S.Keywords | Select-Object -First 3) -join ", ")).
- Migration caution: validate transitive dependencies and runtime compatibility before production upgrades.

## Upgrade Checklist

- Validate compatibility in staging with production-like data and traffic profile.
- Run contract tests and integration tests for all critical boundaries.
- Keep rollback artifacts and clear abort criteria ready.
- Document behavior differences and update operational runbooks.
"@
}

function Build-ExamplesText {
  param([hashtable]$S)
  $keys = ($S.Keywords | ForEach-Object { "- $_" }) -join "`n"
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

## Java and Kotlin Practical Notes

- Keep contracts typed and versioned at module and API boundaries.
- Align nullability, enum names, and date/time formats across both languages.
- Prefer immutable command/event DTOs for transport and integration layers.
- Validate payloads at ingress boundaries before business-core invocation.

## Topic Keywords

$keys
"@
}

function Build-AdvancedText {
  param([hashtable]$S)
  return @"
# Expert Techniques

## Specialist Playbook

- Define architecture fitness checks for key constraints in this domain: $($S.Scope).
- Create synthetic checks for high-risk flows and track regression trends over releases.
- Use staged rollout (canary then progressive traffic shift) tied to SLO gates.
- Build incident playbooks from real outages and validate them in game days.

## Advanced Governance Practices

- Keep Architecture Decision Records (ADR) linked to measurable outcomes.
- Track coupling, latency budget, and deployment lead time as health indicators.
- Maintain a dependency risk register for critical external integrations.
- Revisit operational thresholds after each significant scale or topology change.
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

