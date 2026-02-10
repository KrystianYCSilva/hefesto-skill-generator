# Java and Kotlin Usage Examples

## Java Example

`java
Counter.builder("orders_total").tag("status", "success").register(registry).increment();
`

## Kotlin Example

`kotlin
Timer.builder("checkout_latency").register(registry).record { processCheckout() }
`

## Practical Language Tips

- Keep API and event contracts typed and versioned.
- Align nullability, enums, and date/time serialization across Java and Kotlin.
- Use shared contract tests to prevent cross-language regressions.
- Prefer immutable transport models for integration boundaries.
