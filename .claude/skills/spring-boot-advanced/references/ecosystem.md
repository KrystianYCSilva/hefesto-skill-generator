# Spring Boot Advanced Ecosystem & Libraries

Comprehensive toolkit for advanced Spring Boot development.

## Monitoring & Observability
- **Micrometer**: Metrics collection facade supporting multiple monitoring systems
- **Spring Boot Actuator**: Production-ready features for monitoring
- **Spring Cloud Sleuth**: Distributed tracing solution
- **Spring Boot Admin**: Administration UI for Spring Boot applications

## Configuration & Properties
- **@ConfigurationProperties**: Type-safe configuration properties
- **@Validated**: Validation for configuration properties
- **PropertySourcesPlaceholderConfigurer**: Property source handling
- **Environment**: Access to environment properties

## Auto-Configuration & Conditionals
- **@ConditionalOnClass**: Conditional on class presence
- **@ConditionalOnProperty**: Conditional on property value
- **@ConditionalOnMissingBean**: Conditional when bean is missing
- **@ConditionalOnResource**: Conditional on resource existence
- **spring.factories**: Auto-configuration registration

## Application Events & Lifecycle
- **ApplicationEvent**: Base class for application events
- **ApplicationListener**: Interface for listening to events
- **@EventListener**: Annotation for event listener methods
- **ApplicationEventPublisher**: Interface for publishing events

## Testing & Development
- **ApplicationContextRunner**: For testing auto-configuration
- **@SpringBootTest**: Integration testing annotation
- **@TestConfiguration**: Test-specific configuration
- **@ActiveProfiles**: Activate specific profiles for testing

## Security & Management
- **EndpointRequest**: Security matchers for actuator endpoints
- **ManagementWebSecurityConfigurerAdapter**: Security configuration for management endpoints
- **HealthIndicator**: Interface for custom health indicators
- **InfoContributor**: Interface for custom info endpoint contributions

## Custom Starters Components
- **EnableConfigurationProperties**: Enable configuration properties
- **@AutoConfigureAfter**: Order auto-configuration after others
- **@AutoConfigureBefore**: Order auto-configuration before others
- **ImportSelector**: Dynamic import selection