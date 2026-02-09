---
name: rest-api-development
description: |
  Guides REST API design and implementation with HTTP semantics, Jersey (JAX-RS), versioning, pagination, error contracts, and documentation standards.
  Use when: designing or reviewing backend APIs, implementing JAX-RS/Jersey endpoints, or improving API consistency, compatibility, and operational quality.
---

# REST API Development

REST became the dominant web API style by standardizing resource-oriented design over HTTP, while JAX-RS/Jersey provided a robust Java implementation model. This skill helps the agent deliver APIs that are predictable, evolvable, and production-ready.

## How to model resources and URI design

1. Model URIs by business resources (`/users`, `/orders/{id}`), not actions.
2. Keep naming consistent, pluralized, and stable.
3. Represent relationships with sub-resources only when ownership is clear.
4. Avoid deep nesting that harms readability and caching behavior.

## How to apply HTTP method and status semantics

1. Use method intent correctly (`GET`, `POST`, `PUT`, `PATCH`, `DELETE`).
2. Return precise status codes (`201`, `204`, `400`, `401`, `403`, `404`, `409`, `422`, `500`).
3. Include `Location` header after resource creation.
4. Keep idempotency guarantees explicit for retries and clients.

## How to implement APIs with Jersey (JAX-RS)

1. Use core annotations: `@Path`, `@GET`, `@POST`, `@PUT`, `@DELETE`.
2. Define media types with `@Produces` and `@Consumes`.
3. Use parameter annotations (`@PathParam`, `@QueryParam`, `@HeaderParam`).
4. Centralize exception mapping with `ExceptionMapper` for consistent errors.

## How to design pagination, filtering, and versioning

1. Implement pagination with explicit `page`, `size`, and deterministic `sort`.
2. Allow filter fields with validated operators.
3. Choose versioning strategy (URI/header/media type) and keep it consistent.
4. Document backward-compatibility guarantees for clients.

## How to define error contracts and API documentation

1. Use a stable error schema with code, message, details, and trace/correlation ID.
2. Avoid leaking stack traces or internal implementation details.
3. Publish OpenAPI specs and keep them synchronized with runtime behavior.
4. Add examples for success and error responses in docs.

## How to enforce cross-cutting concerns

1. Add CORS policy explicitly by client trust boundaries.
2. Apply authentication and authorization consistently.
3. Use rate limiting and quotas for abuse protection.
4. Add request logging and metrics aligned with SLOs.

## Common Warnings & Pitfalls

- RPC-style endpoints disguised as REST.
- Inconsistent status codes for similar outcomes.
- Pagination without stable ordering.
- Silent breaking changes in response shape.
- Missing idempotency strategy for client retries.

## Common Errors and Fixes

| Symptom | Root Cause | Fix |
|---|---|---|
| Clients break after minor release | Backward-incompatible contract change | Introduce versioning policy and compatibility tests |
| API returns 200 for failures | Error mapping missing/incorrect | Standardize exception handling and status mapping |
| Duplicate resource creation on retry | Non-idempotent create flow | Add idempotency key or conflict detection strategy |
| Slow list endpoints | Missing pagination/index strategy | Add bounded page size and indexed sort fields |

## Advanced Tips

- Define API governance rules (naming, status codes, version lifecycle).
- Use consumer-driven contract tests for external integrations.
- Prefer additive changes over breaking schema rewrites.
- Track deprecation windows and communicate end-of-life dates.

## How to use extended references

- Read [Version History](references/version-history.md) before upgrades, migrations, or compatibility decisions.
- Read [Java and Kotlin Examples](references/java-kotlin-examples.md) for implementation-ready snippets and language-specific guidance.
- Read [Advanced Techniques](references/advanced-techniques.md) for specialist playbooks, incident tactics, and performance patterns.

