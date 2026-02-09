# Spring Boot Configuration Deep Dive

Advanced configuration techniques and best practices for Spring Boot applications.

## Externalized Configuration Sources

Spring Boot supports various configuration sources with the following precedence (highest first):

1. Devtools global settings properties on your home directory when devtools is active (`~/.spring-boot-devtools.properties`)
2. Test properties (`@TestPropertySource`)
3. Command line arguments
4. Properties from SPRING_APPLICATION_JSON
5. ServletConfig init parameters
6. ServletContext init parameters
7. JNDI attributes from java:comp/env
8. Java System properties (`System.getProperties()`)
9. OS environment variables
10. Random properties (`random.*`)
11. Profile-specific application properties
12. Application properties (`application.properties` or `application.yml`)
13. Default properties (by setting `SpringApplication.setDefaultProperties`)

## Property Placeholders

### Basic Placeholder Resolution
```properties
app.name=MyApp
app.description=${app.name} is a Spring Boot application
```

### Default Values
```properties
app.database.url=${DATABASE_URL:jdbc:h2:mem:testdb}
app.max-connections=${MAX_CONNECTIONS:10}
```

### Cross-Reference Between Properties
```properties
app.base-url=https://example.com
app.api-url=${app.base-url}/api
```

## Type-Safe Configuration Properties

Using `@ConfigurationProperties` for type-safe binding:

```java
@Component
@ConfigurationProperties(prefix = "mail")
public class MailProperties {
    private String host;
    private int port = 25;
    private String from;

    // Standard getters and setters
}
```

With corresponding configuration:
```yaml
mail:
  host: smtp.example.com
  port: 587
  from: contact@example.com
```

## Relaxed Binding Rules

Spring Boot follows relaxed rules for binding properties to configuration objects:

| Property Name | Note |
|---------------|------|
| `person.first-name` | Kebab case (recommended) |
| `person.firstName` | Standard camel case |
| `PERSON_FIRSTNAME` | UPPER_CASE format |

## Configuration Validation

Using Bean Validation with `@Validated`:

```java
@Component
@ConfigurationProperties(prefix = "connection")
@Validated
public class ConnectionProperties {
    @NotBlank
    private String url;
    
    @Min(1)
    @Max(65535)
    private int port = 8080;
    
    @Email
    private String adminEmail;
    
    // Getters and setters
}
```

## Custom Converters

For complex type conversion:

```java
@Configuration
public class ConversionServiceConfig {
    @Bean
    public ApplicationConversionService applicationConversionService() {
        return new ApplicationConversionService();
    }
    
    public static class ApplicationConversionService extends DefaultConversionService {
        public ApplicationConversionService() {
            addConverter(new StringToFileConverter());
        }
    }
}
```

## Loading Properties from External Locations

```java
@SpringBootApplication
@PropertySource("classpath:custom.properties")
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
```

## Configuration Properties Best Practices

1. **Group Related Properties**: Use prefixes to group related properties
2. **Use Descriptive Names**: Choose clear, meaningful property names
3. **Provide Defaults**: Always provide sensible default values
4. **Validate Input**: Use Bean Validation annotations
5. **Document Properties**: Add documentation for custom properties
6. **Avoid Hardcoded Values**: Externalize all environment-specific values