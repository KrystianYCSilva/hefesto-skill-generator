# Java and Kotlin Usage Examples

```java
Publisher publisher = Publisher.newBuilder(topicName).build();
PubsubMessage msg = PubsubMessage.newBuilder()
  .setData(ByteString.copyFromUtf8(payloadJson))
  .putAttributes("eventType", "PAYMENT_CREATED")
  .build();
publisher.publish(msg).get();
```

```kotlin
subscriber = Subscriber.newBuilder(subscriptionName) { message, consumer ->
  process(message)
  consumer.ack()
}.build()
subscriber.startAsync().awaitRunning()
```

## Additional Java and Kotlin Tips

- Java: prefer constructor injection, explicit contracts, and stable package boundaries.
- Kotlin: use null-safety and immutable DTOs to reduce runtime inconsistencies.
- Keep serialization formats and enum naming consistent between Java and Kotlin services.
