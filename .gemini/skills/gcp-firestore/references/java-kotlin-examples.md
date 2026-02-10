# Java and Kotlin Usage Examples

## Java Example

`java
ApiFuture<DocumentSnapshot> snap = db.collection("orders").document(id).get();
`

## Kotlin Example

`kotlin
val snap = db.collection("orders").document(id).get().get()
`

## Java and Kotlin Practical Notes

- Keep contracts typed and versioned at module and API boundaries.
- Align nullability, enum names, and date/time formats across both languages.
- Prefer immutable command/event DTOs for transport and integration layers.
- Validate payloads at ingress boundaries before business-core invocation.

## Topic Keywords

- document model
- composite indexes
- transaction retries
- hot partitions
- read projections
