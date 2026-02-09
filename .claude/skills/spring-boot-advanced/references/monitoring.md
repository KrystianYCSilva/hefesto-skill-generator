# Monitoring & Observability in Spring Boot

Comprehensive guide to monitoring, metrics, and observability in Spring Boot applications.

## Micrometer Metrics Framework

Micrometer is the metrics facade for Spring Boot applications, supporting multiple monitoring systems.

### Core Concepts
- **MeterRegistry**: Central registry for all metrics
- **Counter**: Single monotonic value (e.g., requests served)
- **Gauge**: Single instantaneous value (e.g., active connections)
- **Timer**: Time measurements for short-duration events
- **DistributionSummary**: Measurements of events of finite size
- **LongTaskTimer**: Timers for long-running tasks

### Basic Setup
```java
@Configuration
@EnableConfigurationProperties(MonitoringProperties.class)
public class MonitoringConfiguration {
    
    @Bean
    public MeterRegistryCustomizer<MeterRegistry> metricsCommonTags() {
        return registry -> registry.config()
            .commonTags("application", "myapp")
            .meterFilter(MeterFilter.deny(id -> id.getName().startsWith("unwanted")));
    }
}
```

### Using MeterRegistry
```java
@Service
public class BusinessService {
    
    private final MeterRegistry meterRegistry;
    private final Counter processedOrdersCounter;
    private final Timer businessOperationTimer;
    private final DistributionSummary payloadSizeSummary;
    
    public BusinessService(MeterRegistry meterRegistry) {
        this.meterRegistry = meterRegistry;
        
        // Counter for counting events
        this.processedOrdersCounter = Counter.builder("business.orders.processed")
            .description("Number of orders processed")
            .register(meterRegistry);
        
        // Timer for measuring duration
        this.businessOperationTimer = Timer.builder("business.operation.duration")
            .description("Duration of business operations")
            .register(meterRegistry);
        
        // Distribution summary for measuring sizes
        this.payloadSizeSummary = DistributionSummary.builder("business.payload.size")
            .description("Size of business payloads")
            .baseUnit("bytes")
            .register(meterRegistry);
    }
    
    public void processOrder(Order order) {
        Timer.Sample sample = Timer.start(meterRegistry);
        try {
            // Process the order
            performBusinessLogic(order);
            
            // Record metrics
            processedOrdersCounter.increment();
            payloadSizeSummary.record(order.getSize());
        } finally {
            sample.stop(businessOperationTimer);
        }
    }
    
    private void performBusinessLogic(Order order) {
        // Implementation
    }
}
```

## Prometheus Integration

### Dependencies
```xml
<dependency>
    <groupId>io.micrometer</groupId>
    <artifactId>micrometer-registry-prometheus</artifactId>
</dependency>
```

### Configuration
```yaml
management:
  endpoints:
    web:
      exposure:
        include: health,info,prometheus
  metrics:
    export:
      prometheus:
        enabled: true
        step: 1m
  prometheus:
    metrics:
      export:
        enabled: true
```

### Custom Prometheus Metrics
```java
@Component
public class PrometheusMetricsService {
    
    private final MeterRegistry meterRegistry;
    private final Counter customCounter;
    private final Timer customTimer;
    
    public PrometheusMetricsService(MeterRegistry meterRegistry) {
        this.meterRegistry = meterRegistry;
        
        // Custom counter with labels
        this.customCounter = Counter.builder("custom_requests_total")
            .description("Total custom requests")
            .tag("application", "myapp")
            .register(meterRegistry);
        
        // Custom timer with labels
        this.customTimer = Timer.builder("custom_request_duration_seconds")
            .description("Duration of custom requests")
            .tag("application", "myapp")
            .register(meterRegistry);
    }
    
    public void recordCustomRequest(String endpoint) {
        customCounter.increment(Tags.of("endpoint", endpoint));
        customTimer.record(() -> {
            // Execute custom request
        }, Tags.of("endpoint", endpoint));
    }
}
```

## Distributed Tracing with Spring Cloud Sleuth

### Dependencies
```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-sleuth</artifactId>
</dependency>
```

### Configuration
```yaml
spring:
  sleuth:
    sampler:
      probability: 1.0  # Sample 100% of requests (adjust for production)
    web:
      client:
        enabled: true
      skip-pattern: /actuator/health  # Skip tracing for health checks
```

### Custom Span Creation
```java
@Service
public class TracedBusinessService {
    
    private static final Logger logger = LoggerFactory.getLogger(TracedBusinessService.class);
    private final Tracer tracer;
    
    public TracedBusinessService(Tracer tracer) {
        this.tracer = tracer;
    }
    
    public void performTracedOperation() {
        Span span = tracer.nextSpan().name("perform-business-operation").start();
        
        try (Tracer.SpanInScope ws = tracer.withSpan(span)) {
            // Add tags to the span
            span.tag("operation.type", "business");
            span.tag("user.id", "12345");
            
            // Perform the operation
            performActualOperation();
        } catch (Exception e) {
            // Record the exception in the span
            span.tag("error", e.getMessage());
            throw e;
        } finally {
            // Close the span
            span.end();
        }
    }
    
    private void performActualOperation() {
        // Implementation
    }
}
```

## Custom Metrics Collection

### Gauge for Current Values
```java
@Component
public class ActiveUsersMetrics {
    
    private final MeterRegistry meterRegistry;
    private final AtomicInteger activeUsersCount;
    private final Gauge activeUsersGauge;
    
    public ActiveUsersMetrics(MeterRegistry meterRegistry) {
        this.meterRegistry = meterRegistry;
        this.activeUsersCount = new AtomicInteger(0);
        
        // Gauge that reports current active user count
        this.activeUsersGauge = Gauge.builder("users.active")
            .description("Number of active users")
            .register(meterRegistry, activeUsersCount);
    }
    
    public void incrementActiveUsers() {
        activeUsersCount.incrementAndGet();
    }
    
    public void decrementActiveUsers() {
        activeUsersCount.decrementAndGet();
    }
    
    public int getActiveUsers() {
        return activeUsersCount.get();
    }
}
```

### Long Task Timer for Long-Running Operations
```java
@Service
public class LongRunningTaskService {
    
    private final MeterRegistry meterRegistry;
    private final LongTaskTimer longTaskTimer;
    
    public LongRunningTaskService(MeterRegistry meterRegistry) {
        this.meterRegistry = meterRegistry;
        this.longTaskTimer = LongTaskTimer.builder("long.running.task.duration")
            .description("Duration of long-running tasks")
            .register(meterRegistry);
    }
    
    public void executeLongRunningTask() {
        LongTaskTimer.Sample sample = longTaskTimer.start();
        
        try {
            // Execute long-running task
            performLongRunningOperation();
        } finally {
            sample.stop(); // Stop the timer when task completes
        }
    }
    
    private void performLongRunningOperation() {
        // Implementation of long-running operation
    }
}
```

## Metrics Filtering and Tagging

### Meter Filters
```java
@Configuration
public class MetricsFilterConfiguration {
    
    @Bean
    public MeterFilter denyUnwantedMetrics() {
        return MeterFilter.deny(id -> 
            id.getName().startsWith("unwanted.") || 
            id.getName().equals("jvm.memory.used"));
    }
    
    @Bean
    public MeterFilter addCommonTags() {
        return MeterFilter.commonTags(Tags.of("region", "us-east-1"));
    }
    
    @Bean
    public MeterFilter limitCardinality() {
        return MeterFilter.maximumAllowableTags("http.server.requests", "uri", 100, 
            new MeterFilter.SubstituteFunction() {
                @Override
                public String apply(String value) {
                    return value.length() > 100 ? value.substring(0, 100) + "..." : value;
                }
            });
    }
}
```

### Custom Tag Providers
```java
@Component
public class CustomTagProvider implements MeterFilter {
    
    @Override
    public Meter.Id map(Meter.Id id) {
        if (id.getName().startsWith("http.server.requests")) {
            // Add custom tags based on request attributes
            return id.withTags("tier", "api");
        }
        return id;
    }
}
```

## Health Indicators and Probes

### Custom Health Indicators
```java
@Component
public class DatabaseHealthIndicator implements HealthIndicator {
    
    private final DataSource dataSource;
    
    public DatabaseHealthIndicator(DataSource dataSource) {
        this.dataSource = dataSource;
    }
    
    @Override
    public Health health() {
        try {
            try (Connection connection = dataSource.getConnection()) {
                if (connection.isValid(1)) {
                    return Health.up()
                        .withDetail("database", "Available")
                        .withDetail("validationQuery", "SELECT 1")
                        .build();
                } else {
                    return Health.down()
                        .withDetail("database", "Invalid connection")
                        .build();
                }
            }
        } catch (SQLException e) {
            return Health.down()
                .withDetail("database", "Connection failed")
                .withException(e)
                .build();
        }
    }
}
```

### Reactive Health Indicators
```java
@Component
public class ExternalServiceHealthIndicator implements ReactiveHealthIndicator {
    
    private final WebClient webClient;
    
    public ExternalServiceHealthIndicator(WebClient.Builder webClientBuilder) {
        this.webClient = webClientBuilder.build();
    }
    
    @Override
    public Mono<Health> health() {
        return webClient.get()
            .uri("/health")
            .retrieve()
            .bodyToMono(String.class)
            .map(response -> Health.up()
                .withDetail("externalService", "Available")
                .withDetail("response", response)
                .build())
            .onErrorReturn(Health.down()
                .withDetail("externalService", "Unavailable")
                .build());
    }
}
```

## Application Performance Monitoring (APM)

### Integration with APM Tools
```java
@Configuration
@ConditionalOnProperty(name = "apm.enabled", havingValue = "true", matchIfMissing = false)
public class ApmConfiguration {
    
    @Bean
    @ConditionalOnClass(name = "co.elastic.apm.opentracing.ElasticApmTracer")
    public io.opentracing.Tracer elasticApmTracer() {
        return co.elastic.apm.opentracing.ElasticApmTracer.builder()
            .build();
    }
    
    @Bean
    @ConditionalOnClass(name = "com.newrelic.api.agent.NewRelic")
    public NewRelicService newRelicService() {
        return new NewRelicService();
    }
}
```

## Best Practices

### Metrics Design
- Use consistent naming conventions
- Apply appropriate tags for dimensionality
- Avoid high-cardinality metrics
- Use appropriate metric types for the data being measured

### Performance Considerations
- Keep metric recording operations lightweight
- Use timers appropriately for duration measurements
- Consider sampling for high-frequency events

### Security
- Protect metrics endpoints with authentication
- Avoid exposing sensitive information in metrics
- Regularly review exposed metrics

### Alerting
- Define meaningful alert thresholds
- Monitor for both technical and business metrics
- Set up alerts for degradation patterns