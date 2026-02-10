---
name: keycloak
description: |
  Guides Keycloak identity and access management with realms, clients, roles, OAuth2/OIDC flows, token customization, and Spring integration patterns.
  Use when: implementing centralized authentication/authorization, integrating backend APIs with OIDC, or operating Keycloak securely in production.
---

# Keycloak

Keycloak is a widely used open-source IAM platform for OAuth2 and OpenID Connect. This skill helps the agent configure identity flows, map authorization correctly, and integrate Keycloak with backend services such as Spring Security.

## How to model realms, clients, roles, and groups

1. Use realms as strong isolation boundaries (env or tenant strategy).
2. Configure clients by application type (public, confidential, machine-to-machine).
3. Model permissions through realm/client roles and groups.
4. Keep role taxonomy stable and domain-oriented.

## How to choose OAuth2/OIDC flows

1. Use authorization code flow (with PKCE) for user-facing applications.
2. Use client credentials flow for service-to-service auth.
3. Keep implicit flow disabled unless legacy constraints require it.
4. Validate issuer, audience, and token lifetime policies.

## How to integrate Keycloak with Spring services

1. Configure Spring Resource Server JWT validation against realm metadata.
2. Map token claims to Spring authorities consistently.
3. Use method security for domain-sensitive operations.
4. Keep auth concerns centralized in security configuration.

## How to customize tokens and user federation

1. Use protocol mappers for controlled custom claims.
2. Keep token payload minimal to avoid oversized headers.
3. Integrate external identity stores only with clear ownership model.
4. Version claim contracts used by downstream services.

## How to secure operations and lifecycle management

1. Harden admin access with MFA and restricted network paths.
2. Separate admin, automation, and runtime identities.
3. Rotate secrets/keys and monitor auth events.
4. Plan backup, migration, and upgrade paths explicitly.

## Common Warnings & Pitfalls

- Overloading tokens with excessive claims.
- Role explosion without governance conventions.
- Sharing clients/secrets across unrelated services.
- Inconsistent clock settings causing token validation errors.
- Skipping compatibility testing during Keycloak upgrades.

## Common Errors and Fixes

| Symptom | Root Cause | Fix |
|---|---|---|
| API returns `invalid_token` | Issuer/audience mismatch or expired token | Align resource server config with realm metadata and token policy |
| User authenticates but gets 403 | Claim-to-role mapping mismatch | Normalize role mapping and authority prefix strategy |
| Frequent login loops | Redirect URI misconfiguration | Correct client redirect URIs and frontend callback handling |
| Admin console exposed riskily | Weak network/admin policy | Restrict admin endpoints and enforce MFA/least privilege |

## Advanced Tips

- Separate realm-per-environment for safer lifecycle management.
- Use client scopes to standardize claim sets across apps.
- Add contract tests for token claims consumed by APIs.
- Treat identity configuration as code with review and promotion flow.

## How to use extended references

- Read [Version History](references/version-history.md) before upgrades, migrations, or compatibility decisions.
- Read [Java and Kotlin Examples](references/java-kotlin-examples.md) for implementation-ready snippets and language-specific guidance.
- Read [Advanced Techniques](references/advanced-techniques.md) for specialist playbooks, incident tactics, and performance patterns.

