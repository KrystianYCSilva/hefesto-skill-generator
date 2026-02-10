---
name: spring-security
description: |
  Guides secure API design with Spring Security using SecurityFilterChain, JWT, OAuth2/OIDC, method authorization, CORS/CSRF strategy, and password hardening.
  Use when: implementing authentication and authorization in Spring services, integrating identity providers, or auditing security gaps before production.
---

# Spring Security

Spring Security evolved from servlet-era filter controls into a modern security framework covering web, method, and token-based authorization. This skill helps the agent implement secure-by-default Spring APIs without brittle custom auth code.

## How to configure SecurityFilterChain correctly

1. Use explicit `SecurityFilterChain` beans and avoid legacy deprecated patterns.
2. Define endpoint rules from most specific to most general.
3. Keep public endpoints explicit (`/actuator/health`, auth endpoints, docs when required).
4. Deny by default for unknown paths.

## How to implement JWT authentication flow

1. Issue short-lived access tokens and optional refresh tokens.
2. Validate signature, issuer, audience, expiration, and not-before claims.
3. Keep signing keys outside code; rotate keys on schedule.
4. Build authentication filters/providers only when resource-server defaults are insufficient.

## How to integrate OAuth2 and OpenID Connect

1. Use Spring Security OAuth2 Client/Resource Server modules.
2. Prefer OIDC discovery metadata from provider endpoints.
3. Map provider claims to internal authorities consistently.
4. Separate authentication (identity) from authorization (permissions).

## How to apply method-level authorization

1. Enable method security (`@EnableMethodSecurity`).
2. Use `@PreAuthorize` for business-sensitive operations.
3. Keep expressions readable and domain-oriented.
4. Centralize role/authority naming conventions.

## How to handle CORS, CSRF, and session strategy

1. Configure CORS per trusted origins, methods, and headers.
2. For stateless JWT APIs, disable CSRF only when no cookie-based auth is used.
3. For browser sessions/forms, keep CSRF enabled and test token propagation.
4. Set strict session policy for each auth model (`STATELESS`, `IF_REQUIRED`).

## How to harden credentials and user lookup

1. Hash passwords with `BCryptPasswordEncoder` (or stronger adaptive hash).
2. Store only hashed passwords and never log secrets.
3. Implement `UserDetailsService` with locked/disabled account handling.
4. Add brute-force controls (rate limits, lockout windows, step-up auth).

## Common Warnings & Pitfalls

- Building custom JWT parsing instead of using tested library support.
- Granting broad roles (`ADMIN`) where scoped authorities are required.
- Disabling CSRF globally without understanding frontend auth flow.
- Leaking security internals in error payloads.
- Missing tests for authorization boundaries.

## Common Errors and Fixes

| Symptom | Root Cause | Fix |
|---|---|---|
| Every request returns 401 | Missing auth entry point/token parsing | Configure resource server or custom auth filter correctly |
| Authenticated but always 403 | Authorities mapping mismatch | Align token claims to `GrantedAuthority` conventions |
| CORS preflight blocked | OPTIONS not permitted | Add CORS config and allow preflight route handling |
| Invalid signature errors | Wrong key material or algorithm mismatch | Align JWK/secret and signing algorithm on issuer and API |

## Advanced Tips

- Use token introspection or revocation strategy for high-risk domains.
- Prefer authorization policies close to domain services, not only controllers.
- Add structured audit logs for auth success/failure and privileged actions.
- Model security regression tests as part of CI gates.

## How to use extended references

- Read [Version History](references/version-history.md) before upgrades, migrations, or compatibility decisions.
- Read [Java and Kotlin Examples](references/java-kotlin-examples.md) for implementation-ready snippets and language-specific guidance.
- Read [Advanced Techniques](references/advanced-techniques.md) for specialist playbooks, incident tactics, and performance patterns.

