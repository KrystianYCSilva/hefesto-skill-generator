# Java and Kotlin Usage Examples

## Java Example

`java
@Bean Function<OrderEvent, InvoiceEvent> issueInvoice() { return e -> new InvoiceEvent(e.id()); }
`

## Kotlin Example

`kotlin
@Bean fun issueInvoice(): (OrderEvent) -> InvoiceEvent = { e -> InvoiceEvent(e.id) }
`

## Java and Kotlin Practical Notes

- Keep contracts typed and versioned at module and API boundaries.
- Align nullability, enum names, and date/time formats across both languages.
- Prefer immutable command/event DTOs for transport and integration layers.
- Validate payloads at ingress boundaries before business-core invocation.

## Topic Keywords

- Function beans
- composition
- HTTP adapter
- messaging adapter
- serverless packaging
