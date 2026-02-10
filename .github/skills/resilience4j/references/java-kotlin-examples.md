# Java and Kotlin Usage Examples

## Java Example

`java
CircuitBreaker cb = CircuitBreaker.ofDefaults("inventory"); Supplier<Stock> d = CircuitBreaker.decorateSupplier(cb, this::callInventory);
`

## Kotlin Example

`kotlin
val cb = CircuitBreaker.ofDefaults("inventory")
`

## Practical Language Tips

- Keep API and event contracts typed and versioned.
- Align nullability, enums, and date/time serialization across Java and Kotlin.
- Use shared contract tests to prevent cross-language regressions.
- Prefer immutable transport models for integration boundaries.
