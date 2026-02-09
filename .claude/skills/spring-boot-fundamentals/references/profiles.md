# Spring Boot Profiles & Environment Configuration

Complete guide to managing different environments using Spring Boot profiles.

## Profile Basics

Profiles provide a way to register different beans in different environments:

```java
@Configuration
@Profile("dev")
public class DevDatabaseConfig {
    @Bean
    public DataSource dataSource() {
        return new EmbeddedDatabaseBuilder()
            .setType(EmbeddedDatabaseType.H2)
            .addScript("schema.sql")
            .addScript("test-data.sql")
            .build();
    }
}
```

## Activating Profiles

### Programmatic Activation
```java
@SpringBootApplication
public class Application {
    public static void main(String[] args) {
        SpringApplication app = new SpringApplication(Application.class);
        app.setAdditionalProfiles("dev", "local");
        app.run(args);
    }
}
```

### Configuration File Activation
In `application.properties`:
```properties
spring.profiles.active=dev,test
```

In `application.yml`:
```yaml
spring:
  profiles:
    active: dev,test
```

### Command Line Activation
```bash
java -jar myapp.jar --spring.profiles.active=prod
```

### Environment Variable Activation
```bash
export SPRING_PROFILES_ACTIVE=prod
java -jar myapp.jar
```

## Profile-Specific Properties Files

Spring Boot loads profile-specific properties files:
- `application.properties` (default)
- `application-{profile}.properties` (profile-specific)
- `application-{profile}.yml` (profile-specific)

Example file structure:
```
src/main/resources/
├── application.properties
├── application-dev.properties
├── application-prod.properties
└── application-test.properties
```

## Profile Groups

Group multiple profiles together:

In `application.properties`:
```properties
spring.profiles.group.production=proddb,prodmq,prodservices
```

In `application.yml`:
```yaml
spring:
  profiles:
    group:
      production:
        - proddb
        - prodmq
        - prodservices
```

Then activate the group:
```bash
java -jar myapp.jar --spring.profiles.active=production
```

## Conditional Annotations with Profiles

### @Profile with Logical Operators
```java
@Configuration
@Profile("!production") // Not production
public class DevConfiguration {
    // Configuration for non-production environments
}

@Configuration
@Profile("production & !test") // Production but not test
public class ProductionConfiguration {
    // Production-specific configuration
}

@Configuration
@Profile("dev | test") // Dev or test
public class DevTestConfiguration {
    // Configuration for dev or test environments
}
```

## Profile-Specific Beans

Define beans that only exist in specific profiles:

```java
@Component
@Profile("development")
public class DevelopmentOnlyService {
    public void doDevelopmentSpecificTask() {
        // Development-specific implementation
    }
}

@Component
@Profile("production")
public class ProductionReadyService {
    public void doProductionTask() {
        // Production-specific implementation
    }
}
```

## Profile-Specific Configuration Classes

Create configuration classes for different environments:

```java
@Configuration
@Profile("production")
public class ProductionConfiguration {
    @Bean
    @Primary
    public DatabaseConfig databaseConfig() {
        return new ProductionDatabaseConfig();
    }
    
    @Bean
    public CacheManager cacheManager() {
        // Production cache configuration
        return new RedisCacheManager();
    }
}

@Configuration
@Profile({"dev", "test"})
public class DevelopmentConfiguration {
    @Bean
    @Primary
    public DatabaseConfig databaseConfig() {
        return new InMemoryDatabaseConfig();
    }
    
    @Bean
    public CacheManager cacheManager() {
        // Development cache configuration
        return new SimpleCacheManager();
    }
}
```

## Profile-Specific Application Properties

### application-dev.properties
```properties
# Development-specific settings
logging.level.com.example=DEBUG
spring.datasource.url=jdbc:h2:mem:devdb
spring.jpa.show-sql=true
server.error.include-message=always
```

### application-prod.properties
```properties
# Production-specific settings
logging.level.com.example=WARN
spring.datasource.url=jdbc:mysql://prod-db:3306/myapp
spring.jpa.show-sql=false
server.error.include-message=never
management.endpoints.enabled-by-default=true
```

### application-test.properties
```properties
# Test-specific settings
logging.level.com.example=INFO
spring.datasource.url=jdbc:h2:mem:testdb
spring.jpa.hibernate.ddl-auto=create-drop
```

## Profile-Specific YAML Configuration

### application-dev.yml
```yaml
spring:
  datasource:
    url: jdbc:h2:mem:devdb
    username: sa
    password: 
  jpa:
    show-sql: true
    hibernate:
      ddl-auto: create-drop

logging:
  level:
    com.example: DEBUG

app:
  debug: true
  features:
    - debug-mode
    - enhanced-logging
```

### application-prod.yml
```yaml
spring:
  datasource:
    url: ${DATABASE_URL}
    username: ${DATABASE_USERNAME}
    password: ${DATABASE_PASSWORD}
  jpa:
    show-sql: false
    hibernate:
      ddl-auto: validate

logging:
  level:
    com.example: WARN

app:
  debug: false
  features:
    - caching
    - compression
```

## Testing with Profiles

### @ActiveProfiles for Testing
```java
@SpringBootTest
@ActiveProfiles("test")
class UserServiceTest {
    @Autowired
    private UserService userService;
    
    @Test
    void shouldCreateUser() {
        // Test implementation
    }
}
```

### Profile-Specific Test Configuration
```java
@TestConfiguration
@Profile("test")
public class TestConfig {
    @Bean
    @Primary
    public EmailService mockEmailService() {
        return Mockito.mock(EmailService.class);
    }
}
```

## Profile Hierarchy and Inheritance

Profiles can be inherited and combined:

```java
@Configuration
@Profile("database")
public class DatabaseConfiguration {
    // Common database configuration
}

@Configuration
@Profile("mysql")
public class MySQLConfiguration extends DatabaseConfiguration {
    // MySQL-specific configuration
}
```

## Best Practices

1. **Use Meaningful Profile Names**: Choose clear, descriptive names like `dev`, `test`, `staging`, `prod`
2. **Externalize Sensitive Information**: Never hardcode passwords or API keys in profile files
3. **Keep Common Configuration in Default**: Put shared configuration in the default `application.properties`
4. **Document Profile Differences**: Maintain documentation about what changes between profiles
5. **Use Profile Groups**: Group related profiles to simplify activation
6. **Test Profile-Specific Code**: Ensure profile-specific configurations are tested
7. **Avoid Profile-Specific Logic in Code**: Keep environment differences in configuration, not in code
8. **Use Environment Variables**: For production deployments, prefer environment variables over properties files
9. **Secure Profile Files**: Treat profile files as sensitive configuration documents
10. **Monitor Profile Activation**: Log which profiles are active in your application startup