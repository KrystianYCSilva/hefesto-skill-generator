# Spring Boot Actuator Deep Dive

Comprehensive guide to Spring Boot Actuator for monitoring and managing applications.

## Essential Endpoints

### Health Endpoint
The `/actuator/health` endpoint provides information about the application's health status.

```yaml
management:
  endpoint:
    health:
      show-details: when-authorized  # never, when-authorized, always
  health:
    diskspace:
      enabled: true
    db:
      enabled: true
    redis:
      enabled: true
```

### Info Endpoint
The `/actuator/info` endpoint displays arbitrary application information.

```yaml
info:
  app:
    name: MyApp
    description: Sample application
    version: 1.0.0
  build:
    artifact: myapp
    name: MyApp
    version: 1.0.0
  git:
    mode: full
```

### Metrics Endpoint
The `/actuator/metrics` endpoint provides access to collected metrics.

```yaml
management:
  metrics:
    export:
      prometheus:
        enabled: true
        step: 1m
    distribution:
      percentiles-histogram:
        all: true
      sla:
        http.server.requests: 1ms, 10ms, 100ms, 1000ms
```

## Custom Endpoints

### Creating Custom Endpoint
```java
@Component
@Endpoint(id = "custom", enableByDefault = true)
public class CustomEndpoint {
    
    @ReadOperation
    public Map<String, Object> customInfo() {
        Map<String, Object> info = new HashMap<>();
        info.put("status", "running");
        info.put("timestamp", Instant.now());
        return info;
    }
    
    @WriteOperation
    public String updateCustomInfo(@Selector String key, String value) {
        // Update logic here
        return "Updated " + key + " to " + value;
    }
    
    @DeleteOperation
    public String removeCustomInfo(@Selector String key) {
        // Remove logic here
        return "Removed " + key;
    }
}
```

### Web-Specific Endpoint
```java
@RestController
@RequestMapping("/actuator/custom")
public class CustomWebEndpoint {
    
    @GetMapping("/status")
    public ResponseEntity<Map<String, Object>> getStatus() {
        Map<String, Object> status = new HashMap<>();
        status.put("status", "healthy");
        status.put("timestamp", Instant.now());
        return ResponseEntity.ok(status);
    }
    
    @PostMapping("/action")
    public ResponseEntity<String> performAction(@RequestBody Map<String, Object> params) {
        // Action logic here
        return ResponseEntity.ok("Action performed");
    }
}
```

## Security Configuration

### Securing Actuator Endpoints
```java
@Configuration
@EnableWebSecurity
public class ActuatorSecurityConfig {
    
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http.requestMatcher(EndpointRequest.toAnyEndpoint())
            .authorizeHttpRequests(authz -> authz
                .requestMatchers(EndpointRequest.to("health", "info")).permitAll()
                .requestMatchers(EndpointRequest.to("shutdown")).hasRole("ADMIN")
                .anyRequest().authenticated()
            )
            .httpBasic(); // Basic auth for secured endpoints
        return http.build();
    }
}
```

### Role-Based Access
```yaml
management:
  endpoints:
    web:
      exposure:
        include: "*"
  endpoint:
    shutdown:
      enabled: true
    health:
      show-details: when-authorized
  roles:
    - ACTUATOR
    - ADMIN
```

## Custom Health Indicators

### Simple Health Indicator
```java
@Component
public class DatabaseHealthIndicator implements HealthIndicator {
    
    @Override
    public Health health() {
        // Perform health check
        boolean isHealthy = checkDatabaseConnection();
        
        if (isHealthy) {
            return Health.up()
                .withDetail("database", "Available")
                .withDetail("version", getDatabaseVersion())
                .build();
        } else {
            return Health.down()
                .withDetail("database", "Unavailable")
                .withDetail("error", "Connection failed")
                .build();
        }
    }
    
    private boolean checkDatabaseConnection() {
        // Implementation
        return true;
    }
    
    private String getDatabaseVersion() {
        // Implementation
        return "1.0.0";
    }
}
```

### Reactive Health Indicator
```java
@Component
public class ExternalServiceHealthIndicator implements ReactiveHealthIndicator {
    
    @Override
    public Mono<Health> health() {
        return checkExternalService()
            .map(response -> Health.up()
                .withDetail("externalService", "Available")
                .withDetail("responseTime", response.getTime())
                .build())
            .onErrorReturn(Health.down()
                .withDetail("externalService", "Unavailable")
                .withDetail("error", "Service timeout")
                .build());
    }
    
    private Mono<ServiceResponse> checkExternalService() {
        // Implementation returning Mono
        return Mono.just(new ServiceResponse());
    }
}
```

## Metrics Collection

### Custom Metrics
```java
@Service
public class BusinessMetricsService {
    
    private final MeterRegistry meterRegistry;
    private final Counter processedOrdersCounter;
    private final Timer businessOperationTimer;
    private final Gauge activeUsersGauge;
    private final AtomicInteger activeUsersCount;
    
    public BusinessMetricsService(MeterRegistry meterRegistry) {
        this.meterRegistry = meterRegistry;
        
        // Counter for counting events
        this.processedOrdersCounter = Counter.builder("orders.processed")
            .description("Number of orders processed")
            .tag("application", "myapp")
            .register(meterRegistry);
        
        // Timer for measuring duration
        this.businessOperationTimer = Timer.builder("business.operation.duration")
            .description("Duration of business operations")
            .register(meterRegistry);
        
        // Gauge for current values
        this.activeUsersCount = new AtomicInteger(0);
        this.activeUsersGauge = Gauge.builder("users.active")
            .description("Number of active users")
            .register(meterRegistry, activeUsersCount);
    }
    
    public void recordOrderProcessed() {
        processedOrdersCounter.increment();
    }
    
    public void measureBusinessOperation(Runnable operation) {
        businessOperationTimer.record(operation);
    }
    
    public void incrementActiveUsers() {
        activeUsersCount.incrementAndGet();
    }
    
    public void decrementActiveUsers() {
        activeUsersCount.decrementAndGet();
    }
}
```

### Tagging Strategy
```java
@Service
public class RequestMetricsService {
    
    private final MeterRegistry meterRegistry;
    
    public RequestMetricsService(MeterRegistry meterRegistry) {
        this.meterRegistry = meterRegistry;
    }
    
    public void recordRequest(String method, String uri, int status) {
        Timer.builder("http.requests")
            .description("HTTP request duration")
            .tag("method", method)
            .tag("uri", uri)
            .tag("status", String.valueOf(status))
            .register(meterRegistry)
            .record(() -> {
                // Execute request
            });
    }
}
```

## Custom Info Contributors

### Info Contributor Implementation
```java
@Component
public class BuildInfoContributor implements InfoContributor {
    
    @Override
    public void contribute(Info.Builder builder) {
        builder.withDetail("build", Map.of(
            "artifact", "myapp",
            "name", "My Application",
            "version", getVersionFromBuild(),
            "timestamp", Instant.now()
        ));
    }
    
    private String getVersionFromBuild() {
        // Retrieve version from build system
        return "1.0.0";
    }
}
```

## Best Practices

### Endpoint Exposure
- Only expose necessary endpoints in production
- Use security to protect sensitive endpoints
- Regularly review exposed endpoints

### Health Checks
- Keep health checks lightweight
- Avoid external dependencies in health checks when possible
- Use reactive health indicators for non-blocking checks

### Metrics
- Use appropriate metric types (counters, gauges, timers, distributions)
- Apply consistent tagging strategy
- Avoid high-cardinality tags

### Security
- Secure sensitive endpoints with authentication
- Use role-based access control
- Regularly audit endpoint access