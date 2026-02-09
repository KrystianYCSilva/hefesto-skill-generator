# Java and Kotlin Usage Examples

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: orders-api
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: app
        image: REGION-docker.pkg.dev/project/repo/orders:1.0.0
        resources:
          requests:
            cpu: "500m"
            memory: "512Mi"
```

```properties
# JVM hints for containerized Spring workloads
JAVA_TOOL_OPTIONS=-XX:MaxRAMPercentage=75 -XX:+ExitOnOutOfMemoryError
```

## Additional Java and Kotlin Tips

- Java: prefer constructor injection, explicit contracts, and stable package boundaries.
- Kotlin: use null-safety and immutable DTOs to reduce runtime inconsistencies.
- Keep serialization formats and enum naming consistent between Java and Kotlin services.
