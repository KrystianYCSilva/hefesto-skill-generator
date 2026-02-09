# Java and Kotlin Usage Examples

```java
Storage storage = StorageOptions.getDefaultInstance().getService();
BlobInfo blob = BlobInfo.newBuilder(bucket, objectKey)
  .setContentType("application/pdf")
  .build();
storage.create(blob, bytes);
```

```kotlin
val url = storage.signUrl(
  BlobInfo.newBuilder(bucket, objectKey).build(),
  15, TimeUnit.MINUTES,
  Storage.SignUrlOption.withV4Signature()
)
```

## Additional Java and Kotlin Tips

- Java: prefer constructor injection, explicit contracts, and stable package boundaries.
- Kotlin: use null-safety and immutable DTOs to reduce runtime inconsistencies.
- Keep serialization formats and enum naming consistent between Java and Kotlin services.
