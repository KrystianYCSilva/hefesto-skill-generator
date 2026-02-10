---
name: java-kotlin-examples
description: |
  Documentation file for agent operations and skill usage.
  Use when: you need procedural guidance for agent execution and context management.
---

# Java and Kotlin Usage Examples

```java
@Service
class PaymentPublisher {
  private final PubSubTemplate pubSub;
  PaymentPublisher(PubSubTemplate pubSub) { this.pubSub = pubSub; }
  void publish(PaymentEvent event) { pubSub.publish("payments-topic", event); }
}
```

```kotlin
@Service
class ReceiptStorage(private val storage: Storage) {
  fun upload(bucket: String, key: String, bytes: ByteArray) {
    storage.create(BlobInfo.newBuilder(bucket, key).build(), bytes)
  }
}
```

## Additional Java and Kotlin Tips

- Java: prefer constructor injection, explicit contracts, and stable package boundaries.
- Kotlin: use null-safety and immutable DTOs to reduce runtime inconsistencies.
- Keep serialization formats and enum naming consistent between Java and Kotlin services.

