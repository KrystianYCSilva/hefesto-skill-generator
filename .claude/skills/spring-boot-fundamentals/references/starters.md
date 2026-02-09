# Spring Boot Starters & Auto-configuration

Comprehensive guide to Spring Boot starters and auto-configuration mechanisms.

## Understanding Starters

Spring Boot starters are a set of convenient dependency descriptors that you can include in your application to get up and running quickly.

### Core Starters

#### spring-boot-starter
- Base starter, including auto-configuration support, logging, and YAML
- Includes: spring-boot, spring-boot-autoconfigure, spring-boot-starter-logging
- Foundation for all other starters

#### spring-boot-starter-web
- Starter for web applications including RESTful services
- Includes: spring-webmvc, spring-web, Jackson, Tomcat
- For reactive applications, use `spring-boot-starter-webflux`

#### spring-boot-starter-data-jpa
- Starter for using Spring Data JPA with Hibernate
- Includes: spring-data-jpa, spring-orm, Hibernate, JPA API
- Automatically configures DataSource, EntityManagerFactory, TransactionManager

#### spring-boot-starter-security
- Starter for using Spring Security
- Includes: spring-security-core, spring-security-web, spring-security-config
- Provides authentication and authorization support

#### spring-boot-starter-test
- Starter for testing with JUnit, Mockito, Hamcrest, and other libraries
- Includes: JUnit, Spring Test, AssertJ, Hamcrest, Mockito, JSONassert, JsonPath
- Essential for comprehensive testing

#### spring-boot-starter-actuator
- Starter for using Spring Boot's Actuator functionality
- Includes: spring-boot-starter, spring-boot-actuator
- Provides production-ready features like health, metrics, info endpoints

## Creating Custom Starters

### Structure of a Custom Starter
```
my-custom-starter/
├── pom.xml (or build.gradle)
├── src/main/java/com/example/autoconfigure/
│   └── MyServiceAutoConfiguration.java
├── src/main/resources/
    └── META-INF/
        └── spring.factories
```

### Example Custom Starter

#### Auto-Configuration Class
```java
@Configuration
@ConditionalOnClass(MyService.class)
@EnableConfigurationProperties(MyServiceProperties.class)
public class MyServiceAutoConfiguration {

    @Autowired
    private MyServiceProperties properties;

    @Bean
    @ConditionalOnMissingBean
    public MyService myService() {
        return new MyService(properties.getHost(), properties.getPort());
    }

    @Bean
    @ConditionalOnMissingBean
    public MyServiceRunner myServiceRunner(MyService myService) {
        return new MyServiceRunner(myService);
    }
}
```

#### Properties Class
```java
@ConfigurationProperties(prefix = "myservice")
public class MyServiceProperties {
    private String host = "localhost";
    private int port = 8080;
    private boolean enabled = true;

    // Getters and setters
    public String getHost() { return host; }
    public void setHost(String host) { this.host = host; }
    
    public int getPort() { return port; }
    public void setPort(int port) { this.port = port; }
    
    public boolean isEnabled() { return enabled; }
    public void setEnabled(boolean enabled) { this.enabled = enabled; }
}
```

#### Registering Auto-Configuration
In `META-INF/spring.factories`:
```properties
org.springframework.boot.autoconfigure.EnableAutoConfiguration=\
com.example.autoconfigure.MyServiceAutoConfiguration
```

## Auto-Configuration Mechanics

### Conditional Annotations

#### @ConditionalOnClass
Configures beans only if specified classes are present on the classpath:
```java
@ConditionalOnClass(DataSource.class)
public class DataSourceAutoConfiguration {
    // Configuration only applied if DataSource is on classpath
}
```

#### @ConditionalOnMissingBean
Creates a bean only if no other bean of the same type exists:
```java
@Bean
@ConditionalOnMissingBean
public MyService myService() {
    return new MyServiceImpl();
}
```

#### @ConditionalOnProperty
Applies configuration based on property values:
```java
@ConditionalOnProperty(name = "myservice.enabled", havingValue = "true", matchIfMissing = true)
public class MyServiceConfiguration {
    // Configuration applied based on property value
}
```

#### @ConditionalOnExpression
Applies configuration based on SpEL expression:
```java
@ConditionalOnExpression("${myservice.condition:true}")
public class ConditionalConfiguration {
    // Configuration based on expression evaluation
}
```

#### @ConditionalOnResource
Applies configuration if a specific resource exists:
```java
@ConditionalOnResource(resources = "classpath:myconfig.xml")
public class ResourceBasedConfiguration {
    // Configuration applied if resource exists
}
```

## Excluding Auto-Configuration

### At Application Level
```java
@SpringBootApplication(exclude = {DataSourceAutoConfiguration.class})
public class MyApplication {
    public static void main(String[] args) {
        SpringApplication.run(MyApplication.class, args);
    }
}
```

### Using Properties
In `application.properties`:
```properties
spring.autoconfigure.exclude=org.springframework.boot.autoconfigure.jdbc.DataSourceAutoConfiguration
```

In `application.yml`:
```yaml
spring:
  autoconfigure:
    exclude:
      - org.springframework.boot.autoconfigure.jdbc.DataSourceAutoConfiguration
```

### Multiple Exclusions
```java
@SpringBootApplication(exclude = {
    DataSourceAutoConfiguration.class,
    HibernateJpaAutoConfiguration.class,
    SecurityAutoConfiguration.class
})
public class MyApplication {
    // Application configuration
}
```

## Writing Robust Auto-Configuration

### Proper Ordering
```java
@Configuration
@AutoConfigureAfter(DataSourceAutoConfiguration.class)
@ConditionalOnBean(DataSource.class)
public class MyServiceAutoConfiguration {
    // Configuration that depends on DataSource being configured first
}
```

### Using @AutoConfigureBefore and @AutoConfigureAfter
```java
@Configuration
@AutoConfigureBefore(WebMvcAutoConfiguration.class)
public class MyWebConfiguration {
    // Configuration that should run before WebMvcAutoConfiguration
}
```

### Handling Optional Dependencies
```java
@Configuration
@ConditionalOnClass({RedisTemplate.class, RedisConnectionFactory.class})
@ConditionalOnProperty(name = "myapp.redis.enabled", havingValue = "true", matchIfMissing = true)
public class RedisAutoConfiguration {
    
    @Bean
    @ConditionalOnMissingBean
    public RedisTemplate<String, Object> redisTemplate(RedisConnectionFactory connectionFactory) {
        RedisTemplate<String, Object> template = new RedisTemplate<>();
        template.setConnectionFactory(connectionFactory);
        // Configure template
        return template;
    }
}
```

## Starter Best Practices

### Naming Conventions
- Use `spring-boot-starter-{name}` for official starters
- Use `{name}-spring-boot-starter` for third-party starters
- Example: `mybatis-spring-boot-starter`

### Dependency Management
```xml
<dependencies>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter</artifactId>
    </dependency>
    <dependency>
        <groupId>com.example</groupId>
        <artifactId>my-library</artifactId>
        <version>${my-library.version}</version>
    </dependency>
    <!-- Test dependencies -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-test</artifactId>
        <scope>test</scope>
    </dependency>
</dependencies>
```

### Properties Documentation
Create `additional-spring-configuration-metadata.json`:
```json
{
  "properties": [
    {
      "name": "myservice.host",
      "type": "java.lang.String",
      "description": "The host for the service.",
      "defaultValue": "localhost"
    },
    {
      "name": "myservice.port",
      "type": "java.lang.Integer",
      "description": "The port for the service.",
      "defaultValue": 8080
    }
  ]
}
```

## Troubleshooting Auto-Configuration

### Enable Debug Logging
```properties
debug=true
```
Or:
```bash
java -jar myapp.jar --debug
```

### Check Auto-Configuration Report
Look for "AUTO-CONFIGURATION REPORT" in logs to see which configurations were applied and which were excluded.

### Common Issues and Solutions

#### Issue: Bean Creation Failure
- **Cause**: Missing dependencies or misconfigured properties
- **Solution**: Check conditional annotations and ensure all prerequisites are met

#### Issue: Conflicting Beans
- **Cause**: Multiple beans of the same type
- **Solution**: Use `@ConditionalOnMissingBean` or `@Primary` annotation

#### Issue: Auto-Configuration Not Applied
- **Cause**: Conditional annotations not satisfied
- **Solution**: Verify conditions and provide required dependencies

## Advanced Auto-Configuration Techniques

### Import Selectors
```java
@Configuration
@Import(MyServiceImportSelector.class)
public class MyServiceConfiguration {
    // Configuration using import selector
}

public class MyServiceImportSelector implements ImportSelector {
    @Override
    public String[] selectImports(AnnotationMetadata importingClassMetadata) {
        // Dynamic selection of configurations
        return new String[]{"com.example.config.ServiceAConfig", "com.example.config.ServiceBConfig"};
    }
}
```

### Import Beans
```java
@Configuration
@Import({ServiceA.class, ServiceB.class})
public class MyServiceConfiguration {
    // Imports specific beans
}
```

### Conditional on Bean Type
```java
@ConditionalOnBean(annotation = Service.class)
public class ServiceAutoConfiguration {
    // Applied when beans annotated with @Service exist
}
```

This comprehensive guide covers the essential aspects of Spring Boot starters and auto-configuration, providing the foundation for understanding and creating custom starters.