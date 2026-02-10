---
name: spring-web
description: |
  Guides Spring MVC and REST endpoint implementation with request mapping, validation, exception handling, content negotiation, and async response patterns.
  Use when: building or refactoring Spring HTTP APIs, enforcing response contracts, or improving error handling and controller-level robustness.
---

# Spring Web

Spring Web evolved from classic MVC into a mature API stack used across monoliths and microservices. This skill helps the agent structure HTTP layers clearly, with predictable contracts and operationally safe error handling.

## How to design controllers and mappings

1. Use `@RestController` for JSON APIs and `@Controller` for server-rendered views.
2. Keep route design resource-oriented and stable.
3. Use explicit method mappings (`@GetMapping`, `@PostMapping`, `@PutMapping`, `@PatchMapping`, `@DeleteMapping`).
4. Keep controller logic focused on transport concerns.

## How to bind and validate request data

1. Use DTOs for input/output instead of exposing entities.
2. Bind input with `@RequestBody`, `@PathVariable`, `@RequestParam`, and `@RequestHeader`.
3. Apply Bean Validation with `@Valid` and custom constraints where needed.
4. Return consistent validation error payloads.

## How to model HTTP responses correctly

1. Use `ResponseEntity` for explicit status/header/body control.
2. Use semantic status codes (`201` create, `204` no content, `409` conflict, `422` validation semantic error).
3. Include resource location headers on create operations.
4. Keep response envelope strategy consistent across the API.

## How to centralize exception handling

1. Use `@ControllerAdvice` with targeted `@ExceptionHandler` methods.
2. Map domain exceptions to stable API error contracts.
3. Avoid leaking stack traces and framework internals.
4. Add correlation IDs to error responses/logs for traceability.

## How to handle content negotiation and converters

1. Define supported media types explicitly when needed.
2. Keep JSON as default unless XML or others are required by clients.
3. Configure message converters only when default behavior is insufficient.
4. Version content contracts deliberately to avoid silent client breakage.

## How to apply async controller patterns

1. Use `CompletableFuture`, `DeferredResult`, or reactive stack when latency hiding is needed.
2. Configure timeouts and fallback behavior for async endpoints.
3. Preserve tracing/security context in async execution.
4. Prefer async only for real I/O wait advantages.

## Common Warnings & Pitfalls

- Fat controllers mixing business logic and transport concerns.
- Inconsistent error schema across endpoints.
- Missing validation on query params/path params.
- Returning `200 OK` for failed operations with error messages in body.
- Async endpoints without timeout/exception strategy.

## Common Errors and Fixes

| Symptom | Root Cause | Fix |
|---|---|---|
| `415 Unsupported Media Type` | Client content type not accepted | Configure `consumes` correctly and document required media type |
| `400 Bad Request` on valid payload | DTO binding/validation mismatch | Align JSON field names, constraints, and deserialization settings |
| Global handler not triggered | Exception type not mapped | Add specific handler and verify advice scanning |
| CORS errors in browser | Missing origin/method/header policy | Configure CORS centrally and include preflight support |

## Advanced Tips

- Use RFC 7807 style problem details for standardized errors.
- Add request/response contract tests for external API consumers.
- Separate internal and public API controller modules when possible.
- Keep OpenAPI generation aligned with runtime behavior.

## How to use extended references

- Read [Version History](references/version-history.md) before upgrades, migrations, or compatibility decisions.
- Read [Java and Kotlin Examples](references/java-kotlin-examples.md) for implementation-ready snippets and language-specific guidance.
- Read [Advanced Techniques](references/advanced-techniques.md) for specialist playbooks, incident tactics, and performance patterns.

