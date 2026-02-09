# Conditional Configuration in Spring Boot

Comprehensive guide to conditional annotations and configuration in Spring Boot.

## Core Conditional Annotations

### @ConditionalOnClass
Configures beans only if specified classes are present on the classpath:

```java
@Configuration
@ConditionalOnClass(DataSource.class)
public class DataSourceConfiguration {
    
    @Bean
    @ConditionalOnMissingBean
    public DataSource dataSource() {
        // Only created if DataSource class is on classpath
        return new EmbeddedDatabaseBuilder()
            .setType(EmbeddedDatabaseType.H2)
            .build();
    }
}
```

### @ConditionalOnMissingClass
Configures beans only if specified classes are NOT present:

```java
@Configuration
@ConditionalOnMissingClass("javax.sql.DataSource")
public class InMemoryStorageConfiguration {
    
    @Bean
    @ConditionalOnMissingBean
    public StorageService storageService() {
        // Used when no DataSource is available
        return new InMemoryStorageService();
    }
}
```

### @ConditionalOnBean
Configures beans only if specific beans are present:

```java
@Configuration
public class CacheConfiguration {
    
    @Bean
    @ConditionalOnBean(DataSource.class)
    public CacheManager cacheManager() {
        // Only created if DataSource bean exists
        return new JCacheManager();
    }
    
    @Bean
    @ConditionalOnMissingBean
    public CacheManager fallbackCacheManager() {
        // Fallback if no other CacheManager exists
        return new SimpleCacheManager();
    }
}
```

### @ConditionalOnMissingBean
Creates a bean only if no other bean of the same type exists:

```java
@Configuration
public class ServiceConfiguration {
    
    @Bean
    @ConditionalOnMissingBean
    public PaymentService paymentService() {
        return new DefaultPaymentService();
    }
    
    @Bean
    @ConditionalOnMissingBean(PaymentService.class)
    @ConditionalOnProperty(name = "payment.provider", havingValue = "paypal")
    public PaymentService paypalPaymentService() {
        return new PayPalPaymentService();
    }
}
```

## Property-Based Conditions

### @ConditionalOnProperty
Applies configuration based on property values:

```java
@Configuration
public class FeatureToggleConfiguration {
    
    @Bean
    @ConditionalOnProperty(name = "feature.new-ui.enabled", havingValue = "true", matchIfMissing = false)
    public UIService newUIService() {
        return new NewUIService();
    }
    
    @Bean
    @ConditionalOnProperty(name = "feature.new-ui.enabled", havingValue = "false", matchIfMissing = true)
    public UIService legacyUIService() {
        return new LegacyUIService();
    }
}
```

### Complex Property Conditions
```java
@Configuration
@ConditionalOnProperty(prefix = "app.cache", name = "enabled", havingValue = "true", matchIfMissing = true)
public class CacheAutoConfiguration {
    
    @Bean
    @ConditionalOnProperty(prefix = "app.cache", name = "type", havingValue = "redis", matchIfMissing = false)
    public CacheManager redisCacheManager() {
        return new RedisCacheManager();
    }
    
    @Bean
    @ConditionalOnProperty(prefix = "app.cache", name = "type", havingValue = "ehcache", matchIfMissing = false)
    public CacheManager ehCacheManager() {
        return new EhCacheManager();
    }
    
    @Bean
    @ConditionalOnMissingBean(CacheManager.class)
    public CacheManager simpleCacheManager() {
        return new SimpleCacheManager();
    }
}
```

## Resource-Based Conditions

### @ConditionalOnResource
Applies configuration if a specific resource exists:

```java
@Configuration
public class ResourceBasedConfiguration {
    
    @Bean
    @ConditionalOnResource(resources = {"classpath:database.properties", "classpath:application.yml"})
    public DatabaseConfig databaseConfig() {
        // Only created if required resources exist
        return loadDatabaseConfig();
    }
    
    private DatabaseConfig loadDatabaseConfig() {
        // Implementation
        return new DatabaseConfig();
    }
}
```

### @ConditionalOnWebApplication
Applies configuration only in web application contexts:

```java
@Configuration
public class WebConfiguration {
    
    @Bean
    @ConditionalOnWebApplication
    public WebSpecificService webSpecificService() {
        return new WebSpecificService();
    }
    
    @Bean
    @ConditionalOnWebApplication(type = ConditionalOnWebApplication.Type.REACTIVE)
    public ReactiveWebSpecificService reactiveWebSpecificService() {
        return new ReactiveWebSpecificService();
    }
    
    @Bean
    @ConditionalOnWebApplication(type = ConditionalOnWebApplication.Type.SERVLET)
    public ServletWebSpecificService servletWebSpecificService() {
        return new ServletWebSpecificService();
    }
}
```

## Expression-Based Conditions

### @ConditionalOnExpression
Applies configuration based on SpEL expression:

```java
@Configuration
public class ExpressionBasedConfiguration {
    
    @Bean
    @ConditionalOnExpression("${app.feature.enabled:false} and '${app.mode}' == 'production'")
    public ProductionFeatureService productionFeatureService() {
        return new ProductionFeatureService();
    }
    
    @Bean
    @ConditionalOnExpression("#{environment.acceptsProfiles('dev', 'test')}")
    public DevelopmentFeatureService developmentFeatureService() {
        return new DevelopmentFeatureService();
    }
}
```

## Combining Multiple Conditions

### Complex Conditional Logic
```java
@Configuration
@ConditionalOnClass({RedisTemplate.class, LettuceConnectionFactory.class})
@ConditionalOnProperty(name = "app.redis.enabled", havingValue = "true", matchIfMissing = true)
public class RedisAutoConfiguration {
    
    @Bean
    @ConditionalOnMissingBean
    @ConditionalOnProperty(name = "app.redis.cluster", havingValue = "false", matchIfMissing = true)
    public RedisConnectionFactory standaloneRedisConnectionFactory() {
        return new LettuceConnectionFactory(
            new RedisStandaloneConfiguration("localhost", 6379)
        );
    }
    
    @Bean
    @ConditionalOnMissingBean
    @ConditionalOnProperty(name = "app.redis.cluster", havingValue = "true")
    public RedisConnectionFactory clusterRedisConnectionFactory() {
        RedisClusterConfiguration clusterConfig = 
            new RedisClusterConfiguration(Arrays.asList("127.0.0.1:7000", "127.0.0.1:7001"));
        return new LettuceConnectionFactory(clusterConfig);
    }
    
    @Bean
    @ConditionalOnBean(RedisConnectionFactory.class)
    @ConditionalOnMissingBean
    public RedisTemplate<String, Object> redisTemplate(RedisConnectionFactory connectionFactory) {
        RedisTemplate<String, Object> template = new RedisTemplate<>();
        template.setConnectionFactory(connectionFactory);
        template.setDefaultSerializer(new GenericJackson2JsonRedisSerializer());
        return template;
    }
}
```

## Custom Conditional Annotations

### Creating Custom Conditions
```java
@Target({ElementType.TYPE, ElementType.METHOD})
@Retention(RetentionPolicy.RUNTIME)
@Conditional(OnCloudPlatformCondition.class)
public @interface ConditionalOnCloudPlatform {
    CloudPlatform value();
    
    enum CloudPlatform {
        AWS, GCP, AZURE, KUBERNETES
    }
}

public class OnCloudPlatformCondition extends SpringBootCondition {
    
    @Override
    public ConditionOutcome getMatchOutcome(ConditionContext context, AnnotatedTypeMetadata metadata) {
        String platform = (String) metadata.getAnnotationAttributes(ConditionalOnCloudPlatform.class.getName()).get("value");
        
        // Determine if running on specified platform
        boolean isRunningOnPlatform = detectPlatform(platform);
        
        if (isRunningOnPlatform) {
            return ConditionOutcome.match(ConditionMessage.forCondition(ConditionalOnCloudPlatform.class)
                .found("running on platform").items(platform));
        } else {
            return ConditionOutcome.noMatch(ConditionMessage.forCondition(ConditionalOnCloudPlatform.class)
                .didNotFind("running on platform").items(platform));
        }
    }
    
    private boolean detectPlatform(String platform) {
        // Implementation to detect cloud platform
        return false;
    }
}
```

## Auto-Configuration Ordering

### @AutoConfigureBefore and @AutoConfigureAfter
```java
@Configuration
@AutoConfigureAfter(DataSourceAutoConfiguration.class)
@ConditionalOnBean(DataSource.class)
public class JpaAutoConfiguration {
    // Configuration that should run after DataSourceAutoConfiguration
}

@Configuration
@AutoConfigureBefore(WebMvcAutoConfiguration.class)
@ConditionalOnClass(DispatcherServlet.class)
public class SecurityAutoConfiguration {
    // Configuration that should run before WebMvcAutoConfiguration
}
```

## Testing Conditional Configuration

### Using ApplicationContextRunner
```java
class ConditionalConfigurationTests {
    
    private ApplicationContextRunner contextRunner = new ApplicationContextRunner()
        .withConfiguration(AutoConfigurations.of(MyAutoConfiguration.class));
    
    @Test
    void defaultServiceBacksOff() {
        this.contextRunner
            .withPropertyValues("myapp.service.enabled=true")
            .run(context -> {
                assertThat(context).hasSingleBean(MyService.class);
            });
    }
    
    @Test
    void serviceDisabled() {
        this.contextRunner
            .withPropertyValues("myapp.service.enabled=false")
            .run(context -> {
                assertThat(context).doesNotHaveBean(MyService.class);
            });
    }
    
    @Test
    void serviceWhenClassNotPresent() {
        this.contextRunner
            .withClassLoader(new FilteredClassLoader(ServiceClass.class))
            .run(context -> {
                assertThat(context).doesNotHaveBean(MyService.class);
            });
    }
}
```

## Best Practices

### Condition Design
- Use specific conditions rather than generic ones
- Combine conditions logically to achieve the desired behavior
- Document the conditions and their expected behavior

### Performance Considerations
- Keep condition evaluations lightweight
- Avoid expensive operations in condition evaluation
- Cache results when appropriate

### Error Handling
- Provide clear error messages when conditions fail
- Handle missing dependencies gracefully
- Provide fallback configurations when possible

### Testing
- Test all conditional branches
- Use ApplicationContextRunner for testing auto-configuration
- Verify that conditions behave as expected in different scenarios