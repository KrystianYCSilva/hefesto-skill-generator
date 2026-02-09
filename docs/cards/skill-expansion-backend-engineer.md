# 🎯 Skill Expansion Card - Backend Engineer Stack

**Criado:** 2026-02-09  
**Owner:** Krystian Silva (Senior Software Engineer)  
**Objetivo:** Transformar o coding agent no parceiro inseparável do engenheiro backend  
**Status:** 📋 Planejado

---

## 📊 Resumo Executivo

| Métrica | Valor |
|---------|-------|
| **Skills Totais** | 59 (consolidadas de 68) |
| **Agents Totais** | 9 |
| **Tempo Total** | ~23.5 horas |
| **Skills Consolidadas** | 9 merges realizados |
| **Redução** | -13% skills (maior eficiência) |

---

## 🎯 Estratégias de Execução

### 🥇 Estratégia 1: MVP Essencial (RECOMENDADO)
```yaml
Skills: 10 (TIER S)
Agents: 4 (essenciais)
Tempo: ~5 horas
Valor: 80% das necessidades diárias
ROI: 16% de valor por hora
```

**Resultado:** Stack funcional para backend Java/Kotlin + GCP + REST APIs

---

### 🥈 Estratégia 2: Completo Crítico
```yaml
Skills: 20 (TIER S + A)
Agents: 7
Tempo: ~10 horas
Valor: 95% das necessidades
ROI: 9.5% de valor por hora
```

**Resultado:** Stack completo incluindo microservices, Kubernetes, Keycloak

---

### 🥉 Estratégia 3: JIT (Just-In-Time)
```yaml
Skills inicial: 10 (TIER S)
Agents inicial: 4
Tempo inicial: ~5 horas
Expansão: sob demanda (20-30min por skill)
Valor: 80% + expansão gradual
```

**Resultado:** MVP + criação sob demanda quando necessário

---

## ⭐ TIER S: DIÁRIO - MVP ESSENCIAL

**Target:** 10 skills + 4 agents  
**Tempo:** ~4h skills + ~1h agents = 5h total  
**Valor:** 80% das necessidades diárias

---

### 🍃 Spring Ecosystem (6 skills)

#### Card S1: spring-boot-fundamentals
```yaml
ID: S1
Nome: spring-boot-fundamentals
Categoria: Spring
Prioridade: CRÍTICA
Tempo: ~25 min
Status: ⬜ Não iniciado
```

**Escopo:**
- Spring Boot starters e auto-configuration
- application.properties e application.yaml
- @SpringBootApplication anatomy
- Dependency injection (@Autowired, constructor injection)
- Component scanning (@Component, @Service, @Repository)
- Profiles (dev, test, prod)
- Banner customization
- Command-line runners

**Comando:**
```bash
/hefesto.create spring-boot-fundamentals
```

**Referências:**
- https://spring.io/projects/spring-boot
- https://docs.spring.io/spring-boot/docs/current/reference/html/
- https://spring.io/guides/gs/spring-boot/

**Checklist:**
- [ ] Skill gerada
- [ ] Auto-crítica (13 pontos) PASS
- [ ] Distribuída (7 CLIs)
- [ ] Testada com prompt: "Create a Spring Boot application with REST API"

---

#### Card S2: spring-boot-advanced
```yaml
ID: S2
Nome: spring-boot-advanced
Categoria: Spring
Prioridade: CRÍTICA
Tempo: ~25 min
Complexidade: ⚡ Alta
Status: ⬜ Não iniciado
Depende: S1 (spring-boot-fundamentals)
```

**Escopo:**
- Spring Boot Actuator (endpoints: /health, /metrics, /info)
- Custom health indicators
- Creating custom starters
- @Conditional annotations (@ConditionalOnClass, @ConditionalOnProperty)
- External configuration (env vars, command-line args)
- @ConfigurationProperties
- Custom auto-configuration
- Application events (@EventListener)
- Custom metrics with Micrometer

**Comando:**
```bash
/hefesto.create spring-boot-advanced
```

**Referências:**
- https://docs.spring.io/spring-boot/docs/current/reference/html/actuator.html
- https://docs.spring.io/spring-boot/docs/current/reference/html/features.html#features.developing-auto-configuration

**Checklist:**
- [ ] Skill gerada
- [ ] Auto-crítica PASS
- [ ] Distribuída (7 CLIs)
- [ ] Testada com prompt: "Add Actuator with custom health check"

---

#### Card S3: spring-security
```yaml
ID: S3
Nome: spring-security
Categoria: Spring
Prioridade: CRÍTICA
Tempo: ~30 min
Complexidade: ⚡ Alta
Status: ⬜ Não iniciado
```

**Escopo:**
- SecurityFilterChain configuration
- JWT authentication (token generation, validation)
- OAuth2 / OpenID Connect integration
- @PreAuthorize, @Secured, @RolesAllowed
- CORS configuration
- CSRF protection
- Password encoding (BCryptPasswordEncoder)
- Method security (@EnableGlobalMethodSecurity)
- UserDetailsService implementation
- Authentication providers
- Remember-me functionality

**Comando:**
```bash
/hefesto.create spring-security
```

**Referências:**
- https://spring.io/projects/spring-security
- https://docs.spring.io/spring-security/reference/index.html
- https://www.baeldung.com/spring-security-jwt

**Checklist:**
- [ ] Skill gerada
- [ ] Auto-crítica PASS
- [ ] Distribuída (7 CLIs)
- [ ] Testada com prompt: "Add JWT authentication to REST API"

---

#### Card S4: spring-data
```yaml
ID: S4
Nome: spring-data
Categoria: Spring
Prioridade: CRÍTICA
Tempo: ~30 min
Complexidade: ⚡ Alta
Status: ⬜ Não iniciado
```

**Escopo:**
- Repository interfaces (CrudRepository, JpaRepository, PagingAndSortingRepository)
- Query methods (findBy, countBy, deleteBy, existsBy)
- @Query annotation (JPQL, native SQL)
- @Transactional (propagation, isolation, rollback)
- Entity relationships (@OneToMany, @ManyToMany, @ManyToOne, @OneToOne)
- Cascade types and orphan removal
- Fetch strategies (LAZY, EAGER)
- @EntityGraph for solving N+1 problems
- Specifications for dynamic queries
- Pagination and Sorting (Pageable, Sort)
- Auditing (@CreatedDate, @LastModifiedDate)

**Comando:**
```bash
/hefesto.create spring-data
```

**Referências:**
- https://spring.io/projects/spring-data-jpa
- https://docs.spring.io/spring-data/jpa/docs/current/reference/html/
- https://www.baeldung.com/spring-data-jpa-query

**Checklist:**
- [ ] Skill gerada
- [ ] Auto-crítica PASS
- [ ] Distribuída (7 CLIs)
- [ ] Testada com prompt: "Create JPA repository with custom query methods"

---

#### Card S5: spring-web
```yaml
ID: S5
Nome: spring-web
Categoria: Spring
Prioridade: CRÍTICA
Tempo: ~25 min
Status: ⬜ Não iniciado
```

**Escopo:**
- @RestController vs @Controller
- @RequestMapping, @GetMapping, @PostMapping, @PutMapping, @DeleteMapping, @PatchMapping
- @RequestBody, @PathVariable, @RequestParam, @RequestHeader
- ResponseEntity<T> (status codes, headers, body)
- @Valid and @Validated (Bean Validation)
- @ControllerAdvice for global exception handling
- @ExceptionHandler
- Content negotiation (JSON, XML)
- HTTP message converters
- CORS @CrossOrigin
- Async controllers (@Async, DeferredResult, CompletableFuture)

**Comando:**
```bash
/hefesto.create spring-web
```

**Referências:**
- https://docs.spring.io/spring-framework/docs/current/reference/html/web.html
- https://spring.io/guides/gs/rest-service/
- https://www.baeldung.com/spring-controller-vs-restcontroller

**Checklist:**
- [ ] Skill gerada
- [ ] Auto-crítica PASS
- [ ] Distribuída (7 CLIs)
- [ ] Testada com prompt: "Create REST controller with exception handling"

---

#### Card S6: spring-cloud-gcp
```yaml
ID: S6
Nome: spring-cloud-gcp
Categoria: Spring
Prioridade: CRÍTICA
Tempo: ~30 min
Complexidade: ⚡ Alta
Status: ⬜ Não iniciado
```

**Escopo:**
- Spring Boot starters for GCP (spring-cloud-gcp-starter-*)
- Pub/Sub integration (@EnableGcpPubSub, PubSubTemplate)
- Cloud Storage (spring-cloud-gcp-storage, GcsTemplate)
- Datastore integration (spring-cloud-gcp-datastore)
- Cloud Trace for distributed tracing
- Cloud SQL integration
- Firestore integration
- Auto-configuration for GCP services
- Service authentication (default credentials, service accounts)

**Comando:**
```bash
/hefesto.create spring-cloud-gcp
```

**Referências:**
- https://spring.io/projects/spring-cloud-gcp
- https://cloud.spring.io/spring-cloud-gcp/reference/html/
- https://github.com/GoogleCloudPlatform/spring-cloud-gcp

**Checklist:**
- [ ] Skill gerada
- [ ] Auto-crítica PASS
- [ ] Distribuída (7 CLIs)
- [ ] Testada com prompt: "Integrate Spring Boot with GCP Pub/Sub"

---

### ☁️ GCP Core Services (3 skills)

#### Card S7: gcp-app-engine
```yaml
ID: S7
Nome: gcp-app-engine
Categoria: GCP
Prioridade: CRÍTICA
Tempo: ~25 min
Status: ⬜ Não iniciado
```

**Escopo:**
- app.yaml structure (Standard vs Flexible environments)
- Runtime configuration (Java 11, Java 17)
- Scaling configuration (automatic, basic, manual)
- Version management (gcloud app deploy)
- Traffic splitting between versions
- Services (microservices on App Engine)
- dispatch.yaml for routing
- cron.yaml for scheduled tasks
- queue.yaml for task queues
- Environment variables and secrets
- Instance classes and resources

**Comando:**
```bash
/hefesto.create gcp-app-engine
```

**Referências:**
- https://cloud.google.com/appengine/docs
- https://cloud.google.com/appengine/docs/standard/java11
- https://cloud.google.com/appengine/docs/standard/java11/config/appref

**Checklist:**
- [ ] Skill gerada
- [ ] Auto-crítica PASS
- [ ] Distribuída (7 CLIs)
- [ ] Testada com prompt: "Deploy Java app to App Engine with autoscaling"

---

#### Card S8: gcp-cloud-run
```yaml
ID: S8
Nome: gcp-cloud-run
Categoria: GCP
Prioridade: CRÍTICA
Tempo: ~25 min
Status: ⬜ Não iniciado
```

**Escopo:**
- Container deployment (from Artifact Registry/Container Registry)
- Dockerfile best practices for Cloud Run
- Revision management
- Traffic splitting between revisions
- Concurrency settings (requests per instance)
- Serverless architecture patterns
- Cold start optimization
- CPU allocation (always allocated vs request-only)
- Memory limits
- Service-to-service authentication
- Custom domains and SSL
- Cloud Run vs Cloud Run for Anthos

**Comando:**
```bash
/hefesto.create gcp-cloud-run
```

**Referências:**
- https://cloud.google.com/run/docs
- https://cloud.google.com/run/docs/deploying
- https://cloud.google.com/run/docs/configuring/containers

**Checklist:**
- [ ] Skill gerada
- [ ] Auto-crítica PASS
- [ ] Distribuída (7 CLIs)
- [ ] Testada com prompt: "Deploy containerized app to Cloud Run"

---

#### Card S9: gcp-pubsub
```yaml
ID: S9
Nome: gcp-pubsub
Categoria: GCP
Prioridade: CRÍTICA
Tempo: ~30 min
Complexidade: ⚡ Alta
Status: ⬜ Não iniciado
```

**Escopo:**
- Topics creation and management
- Subscriptions (push vs pull)
- Message publishing and consumption
- Message ordering (ordering keys)
- Dead letter topics
- Retry policies and exponential backoff
- Message filtering
- Exactly-once delivery
- Acknowledging and nacking messages
- Batching and flow control
- Message attributes
- Pub/Sub vs Kafka comparison

**Comando:**
```bash
/hefesto.create gcp-pubsub
```

**Referências:**
- https://cloud.google.com/pubsub/docs
- https://cloud.google.com/pubsub/docs/overview
- https://cloud.google.com/pubsub/docs/publisher

**Checklist:**
- [ ] Skill gerada
- [ ] Auto-crítica PASS
- [ ] Distribuída (7 CLIs)
- [ ] Testada com prompt: "Implement async messaging with Pub/Sub"

---

### 🌐 Web & APIs (1 skill consolidada)

#### Card S10: rest-api-development
```yaml
ID: S10
Nome: rest-api-development
Categoria: Web/APIs
Prioridade: CRÍTICA
Tempo: ~30 min
Tipo: CONSOLIDADO (api-rest + jersey + HTTP)
Complexidade: ⚡ Alta
Status: ⬜ Não iniciado
```

**Escopo (consolida 3 skills):**

**REST Principles:**
- Resources and resource identifiers (URIs)
- Representations (JSON, XML)
- Stateless communication
- HTTP methods semantic (GET, POST, PUT, PATCH, DELETE, OPTIONS)
- HTTP status codes (2xx success, 3xx redirect, 4xx client error, 5xx server error)
- HATEOAS (Hypermedia as the Engine of Application State)
- Richardson Maturity Model (Level 0-3)

**Jersey (JAX-RS):**
- @Path, @GET, @POST, @PUT, @DELETE
- @Produces, @Consumes (media types)
- @PathParam, @QueryParam, @HeaderParam, @FormParam
- Resources and sub-resources
- Response and Response.ResponseBuilder
- ExceptionMapper for error handling
- MessageBodyReader and MessageBodyWriter (custom providers)
- Filters and Interceptors (request/response)
- Client API for consuming REST services

**API Best Practices:**
- Content negotiation
- API versioning (URI, header, query param)
- Pagination and filtering
- Rate limiting
- API documentation (OpenAPI/Swagger)
- CORS handling
- Authentication (Bearer tokens)

**Comando:**
```bash
/hefesto.create rest-api-development
```

**Referências:**
- https://restfulapi.net/
- https://eclipse-ee4j.github.io/jersey/
- https://jcp.org/en/jsr/detail?id=370
- https://martinfowler.com/articles/richardsonMaturityModel.html

**Checklist:**
- [ ] Skill gerada
- [ ] Auto-crítica PASS
- [ ] Distribuída (7 CLIs)
- [ ] Testada com prompt: "Design RESTful API with Jersey"

---

## 🤖 AGENTS ESSENCIAIS

### Agent A1: backend-engineer
```yaml
ID: A1
Nome: backend-engineer
Fase: Coding
Prioridade: ESSENCIAL
Tempo: ~15 min
Status: ⬜ Não iniciado
Depende: S1-S6, existing skills (java-*, kotlin-*, sql/nosql-specialist)
```

**Skills Compostas:**
- java-advanced, kotlin-advanced, java-kotlin-interop ✅ (já existem)
- spring-boot-fundamentals, spring-boot-advanced
- spring-security, spring-data, spring-web
- spring-cloud-gcp
- sql-specialist, nosql-specialist, postgres-expert ✅ (já existem)

**Workflow:**
```
1. Análise de requisitos
   └─ Identifica: entities, endpoints, security, database

2. Setup do projeto
   └─ Spring Boot initialization, dependencies

3. Implementação de camadas
   ├─ Entities (@Entity, relationships)
   ├─ Repositories (JpaRepository, custom queries)
   ├─ Services (@Service, business logic, @Transactional)
   └─ Controllers (@RestController, endpoints)

4. Segurança
   ├─ SecurityFilterChain configuration
   ├─ JWT authentication
   └─ Method security (@PreAuthorize)

5. Integração GCP
   ├─ Pub/Sub messaging
   ├─ Cloud Storage
   └─ Datastore/Firestore

6. Testes
   ├─ Unit tests (Mockito)
   ├─ Integration tests (@SpringBootTest)
   └─ API tests (MockMvc, RestAssured)
```

**Comando:**
```bash
/hefesto.agent backend-engineer
```

**Exemplo de uso:**
```
Prompt: "Create a backend API for user management with JWT authentication and Postgres"

Agent workflow:
1. Creates User entity with JPA annotations
2. Creates UserRepository with custom query methods
3. Creates UserService with business logic
4. Creates UserController with REST endpoints
5. Configures Spring Security with JWT
6. Adds integration tests
```

**Checklist:**
- [ ] Agent criado
- [ ] Validado (workflow completo)
- [ ] Distribuído (7 CLIs)
- [ ] Testado com exemplo real

---

### Agent A2: cloud-engineer
```yaml
ID: A2
Nome: cloud-engineer
Fase: Coding
Prioridade: ESSENCIAL
Tempo: ~15 min
Status: ⬜ Não iniciado
Depende: S7-S9, TIER A GCP skills
```

**Skills Compostas:**
- gcp-app-engine, gcp-cloud-run, gcp-kubernetes
- gcp-pubsub, gcp-cloud-storage
- gcp-datastore, gcp-firestore
- gcp-observability
- spring-cloud-gcp

**Workflow:**
```
1. Análise de deployment target
   └─ Identifica: App Engine vs Cloud Run vs GKE

2. Configuração de deployment
   ├─ app.yaml (App Engine)
   ├─ Dockerfile (Cloud Run)
   └─ k8s manifests (GKE)

3. Setup de databases
   ├─ Cloud SQL (Postgres/MySQL)
   ├─ Datastore (NoSQL)
   └─ Firestore (real-time)

4. Configuração de messaging
   ├─ Pub/Sub topics/subscriptions
   └─ Cloud Tasks queues

5. Observability
   ├─ Cloud Logging
   ├─ Cloud Monitoring (metrics, alerts)
   └─ Cloud Trace (distributed tracing)

6. CI/CD
   ├─ Cloud Build configuration
   └─ Deployment automation
```

**Comando:**
```bash
/hefesto.agent cloud-engineer
```

**Exemplo de uso:**
```
Prompt: "Deploy Spring Boot app to Cloud Run with Pub/Sub and monitoring"

Agent workflow:
1. Creates optimized Dockerfile for Cloud Run
2. Configures Pub/Sub topic and subscription
3. Adds Cloud Logging/Monitoring
4. Creates cloudbuild.yaml for CI/CD
5. Deploys with traffic splitting
```

**Checklist:**
- [ ] Agent criado
- [ ] Validado
- [ ] Distribuído (7 CLIs)
- [ ] Testado com exemplo real

---

### Agent A3: senior-reviewer
```yaml
ID: A3
Nome: senior-reviewer
Fase: Review
Prioridade: ESSENCIAL
Tempo: ~15 min
Status: ⬜ Não iniciado
Depende: existing skills (code-reviewer, software-architect, design-patterns)
```

**Skills Compostas:**
- code-reviewer ✅ (já existe)
- software-architect ✅ (já existe)
- design-patterns ✅ (já existe)
- spring-security (foco em segurança)

**Workflow:**
```
1. Análise de mudanças
   └─ git diff, arquivos modificados

2. Code quality
   ├─ Anti-patterns (God Class, Spaghetti Code)
   ├─ Code smells
   ├─ SOLID violations
   └─ DRY violations

3. Security audit
   ├─ SQL injection risks
   ├─ XSS vulnerabilities
   ├─ Secrets in code
   ├─ Authentication/Authorization flaws
   └─ OWASP Top 10

4. Performance
   ├─ N+1 query problems
   ├─ Memory leaks
   ├─ Inefficient algorithms
   └─ Database index usage

5. Architecture
   ├─ Layering violations
   ├─ Dependency direction
   └─ Coupling vs cohesion

6. Tests
   ├─ Test coverage
   ├─ Test quality
   └─ Missing edge cases
```

**Comando:**
```bash
/hefesto.agent senior-reviewer
```

**Exemplo de uso:**
```
Prompt: "Review this Spring Boot controller code for issues"

Agent workflow:
1. Identifies missing input validation
2. Points out SQL injection risk in custom query
3. Suggests using @Transactional on service method
4. Recommends adding exception handling
5. Notes missing unit tests
```

**Checklist:**
- [ ] Agent criado
- [ ] Validado
- [ ] Distribuído (7 CLIs)
- [ ] Testado com código real

---

### Agent A4: speckit-planner
```yaml
ID: A4
Nome: speckit-planner
Fase: Planning
Prioridade: ESSENCIAL
Tempo: ~15 min
Status: ⬜ Não iniciado
Depende: existing skills (spec-kit-fundamentals, software-architect, software-documentation)
```

**Skills Compostas:**
- spec-kit-fundamentals ✅ (já existe)
- software-architect ✅ (já existe)
- software-documentation ✅ (já existe)

**Workflow:**
```
1. Análise de requisitos
   └─ Extrai: funcionalidades, restrições, dependências

2. Geração de spec.md
   ├─ Problema e contexto
   ├─ Solução proposta
   ├─ Critérios de aceitação
   └─ Riscos e mitigações

3. Conversão para plan.md
   ├─ Passos de implementação
   ├─ Dependências entre passos
   ├─ Estimativas de tempo
   └─ Pontos de decisão

4. Sugestão de tasks
   ├─ Tasks atômicas
   ├─ Ordem de execução
   └─ Blockers e dependências

5. Identificação de gaps
   └─ Skills ou conhecimento faltante
```

**Comando:**
```bash
/hefesto.agent speckit-planner
```

**Exemplo de uso:**
```
Prompt: "Plan implementation of user authentication feature"

Agent workflow:
1. Generates spec.md with:
   - Problem: need secure user authentication
   - Solution: JWT-based auth with refresh tokens
   - Acceptance criteria: login, logout, token refresh
2. Converts to plan.md with:
   - Setup Spring Security
   - Implement JWT generation/validation
   - Create login/logout endpoints
   - Add refresh token mechanism
3. Suggests tasks in execution order
```

**Checklist:**
- [ ] Agent criado
- [ ] Validado
- [ ] Distribuído (7 CLIs)
- [ ] Testado com requisito real

---

## 📊 PROGRESS TRACKER - TIER S

### Skills (10 total)
- [ ] S1 - spring-boot-fundamentals
- [ ] S2 - spring-boot-advanced
- [ ] S3 - spring-security
- [ ] S4 - spring-data
- [ ] S5 - spring-web
- [ ] S6 - spring-cloud-gcp
- [ ] S7 - gcp-app-engine
- [ ] S8 - gcp-cloud-run
- [ ] S9 - gcp-pubsub
- [ ] S10 - rest-api-development

**Progresso:** 0/10 (0%)

### Agents (4 total)
- [ ] A1 - backend-engineer
- [ ] A2 - cloud-engineer
- [ ] A3 - senior-reviewer
- [ ] A4 - speckit-planner

**Progresso:** 0/4 (0%)

---

## 🎯 MILESTONES

### Milestone M1: MVP Backend Stack ✅
**Target:** 10 skills + 4 agents  
**Tempo:** ~5 horas  
**Valor:** 80% das necessidades  
**Status:** ⬜ Não iniciado

**Critérios de conclusão:**
- [ ] Todas as 10 skills TIER S criadas e validadas
- [ ] Todos os 4 agents essenciais criados e validados
- [ ] Todas distribuídas para 7 CLIs
- [ ] Testadas com prompts reais
- [ ] Documentação de uso criada

**Resultado esperado:**
Capaz de criar, deployar e manter aplicações backend Java/Kotlin com Spring Boot no GCP, com segurança (JWT), banco de dados (JPA), APIs REST, e messaging (Pub/Sub).

---

## 🔥 TIER A: SEMANAL (Próxima Fase)

**Target:** 10 skills + 3 agents  
**Tempo:** ~4 horas  
**Valor:** +15% (95% acumulado)  
**Pré-requisito:** Milestone M1 completo

### Skills Quick Reference:
- A1-A3: spring-cloud, spring-session, spring-cache
- A4-A5: gcp-cloud-storage, gcp-kubernetes
- A6: postgres-expert
- A7-A8: typescript-fundamentals, go-fundamentals
- A9: microservicos
- A10: keycloak

### Agents Quick Reference:
- A5: frontend-engineer
- A6: architecture-advisor
- A7: test-engineer

---

## 📝 NOTAS DE IMPLEMENTAÇÃO

### Ordem Recomendada de Execução:

**Fase 1: Spring Foundation (2h)**
```
S1 → S2 → S5
(boot-fundamentals → boot-advanced → spring-web)
```
✅ Resultado: Capaz de criar APIs REST básicas

**Fase 2: Data & Security (1.5h)**
```
S4 → S3
(spring-data → spring-security)
```
✅ Resultado: APIs com banco de dados e autenticação

**Fase 3: GCP Integration (1.5h)**
```
S6 → S7 → S8 → S9 → S10
(spring-cloud-gcp → app-engine → cloud-run → pubsub → rest-api)
```
✅ Resultado: Deploy no GCP com messaging

**Fase 4: Agents (1h)**
```
A1 → A2 → A3 → A4
(backend-engineer → cloud-engineer → senior-reviewer → speckit-planner)
```
✅ Resultado: Workflow completo automatizado

---

## 🚀 QUICK START

### Para começar AGORA:

```bash
# 1. Criar primeira skill
/hefesto.create spring-boot-fundamentals

# 2. Após aprovação, criar próxima
/hefesto.create spring-boot-advanced

# 3. Continue seguindo a ordem recomendada...
```

### Para criar todas de uma vez (avançado):
```bash
# Não recomendado - melhor criar em fases
# Mas se quiser, pode executar em batch
```

---

## 🔗 Arquivos Relacionados

- **Plano Completo:** `~/.copilot/session-state/.../files/skill-creation-plan.md`
- **Gap Analysis:** Executado em 2026-02-09
- **Skills Existentes:** `.claude/skills/` (38 skills já prontas)
- **Agents Existentes:** `.claude/commands/software-engineer.md`

---

## 📞 Suporte

**Issues comuns:**

1. **"Skill muito grande (>500 linhas)"**
   - Solução: Mover conteúdo detalhado para `references/`
   - Skill principal < 500 linhas
   - Detalhes em arquivos separados

2. **"Auto-crítica falhou"**
   - Solução: Verificar checklist de 13 pontos
   - Ajustar frontmatter
   - Revisar description (deve ter "Use when:")

3. **"Distribuição falhou"**
   - Solução: Verificar se todos os 7 CLI dirs existem
   - Criar diretórios faltantes
   - Re-executar distribuição

---

**Criado por:** Hefesto Framework  
**Data:** 2026-02-09  
**Versão:** 1.0

---

**FIM DO CARD**
