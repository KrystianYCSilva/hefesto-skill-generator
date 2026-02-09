# Dependency Injection Patterns in Spring Boot

Comprehensive guide to dependency injection patterns and best practices in Spring Boot applications.

## Constructor Injection (Recommended)

Constructor injection is the recommended approach for mandatory dependencies:

```java
@Service
public class UserService {
    private final UserRepository userRepository;
    private final EmailService emailService;

    public UserService(UserRepository userRepository, EmailService emailService) {
        this.userRepository = userRepository;
        this.emailService = emailService;
    }

    public User createUser(String email) {
        User user = new User(email);
        User savedUser = userRepository.save(user);
        emailService.sendWelcomeEmail(savedUser.getEmail());
        return savedUser;
    }
}
```

**Benefits:**
- Ensures required dependencies are provided
- Makes objects immutable
- Facilitates testing with mock objects
- Prevents circular dependencies

## Setter Injection (Optional Dependencies)

Setter injection is appropriate for optional dependencies:

```java
@Service
public class NotificationService {
    private EmailService emailService;
    private SMSService smsService;

    @Autowired
    public void setEmailService(EmailService emailService) {
        this.emailService = emailService;
    }

    @Autowired(required = false) // Optional dependency
    public void setSmsService(SMSService smsService) {
        this.smsService = smsService;
    }

    public void sendNotification(String message, String recipient, boolean useSMS) {
        if (emailService != null) {
            emailService.send(message, recipient);
        }
        if (useSMS && smsService != null) {
            smsService.send(message, recipient);
        }
    }
}
```

## Field Injection (Not Recommended)

Field injection should be avoided due to tight coupling and testing difficulties:

```java
@Service
public class BadUserService {
    @Autowired
    private UserRepository userRepository; // Avoid this approach
    
    // Methods here
}
```

## Qualifiers and Named Dependencies

When multiple implementations exist, use `@Qualifier` or `@Named`:

```java
// Interface
public interface PaymentProcessor {
    void process(double amount);
}

// Implementations
@Component
@Qualifier("creditCard")
public class CreditCardProcessor implements PaymentProcessor {
    @Override
    public void process(double amount) {
        // Credit card processing logic
    }
}

@Component
@Qualifier("paypal")
public class PayPalProcessor implements PaymentProcessor {
    @Override
    public void process(double amount) {
        // PayPal processing logic
    }
}

// Service using qualified dependencies
@Service
public class OrderService {
    private final PaymentProcessor paymentProcessor;

    public OrderService(@Qualifier("creditCard") PaymentProcessor paymentProcessor) {
        this.paymentProcessor = paymentProcessor;
    }
}
```

## Using @Primary Annotation

Mark one implementation as primary when multiple exist:

```java
@Component
@Primary
public class DefaultPaymentProcessor implements PaymentProcessor {
    @Override
    public void process(double amount) {
        // Default processing logic
    }
}

@Component
public class AlternativePaymentProcessor implements PaymentProcessor {
    @Override
    public void process(double amount) {
        // Alternative processing logic
    }
}

// Service will receive the primary implementation by default
@Service
public class OrderService {
    private final PaymentProcessor paymentProcessor;

    public OrderService(PaymentProcessor paymentProcessor) {
        this.paymentProcessor = paymentProcessor;
    }
}
```

## Conditional Dependencies

Use `@ConditionalOnBean` or `@ConditionalOnMissingBean` for conditional injection:

```java
@Configuration
public class ServiceConfiguration {
    @Bean
    @ConditionalOnMissingBean
    public PaymentProcessor defaultPaymentProcessor() {
        return new DefaultPaymentProcessor();
    }

    @Bean
    @ConditionalOnBean(AdvancedPaymentService.class)
    public PaymentProcessor advancedPaymentProcessor(AdvancedPaymentService service) {
        return new AdvancedPaymentProcessor(service);
    }
}
```

## Lifecycle Management

Understanding bean lifecycle with dependency injection:

```java
@Component
public class LifecycleAwareService implements InitializingBean, DisposableBean {
    private final DatabaseService databaseService;

    public LifecycleAwareService(DatabaseService databaseService) {
        this.databaseService = databaseService;
    }

    @Override
    public void afterPropertiesSet() throws Exception {
        // Called after all properties are set
        databaseService.initializeConnection();
    }

    @PostConstruct
    public void init() {
        // Called after constructor and afterPropertiesSet
        System.out.println("Service initialized");
    }

    @PreDestroy
    public void cleanup() {
        // Called before bean destruction
        System.out.println("Cleaning up resources");
    }

    @Override
    public void destroy() throws Exception {
        // Called after preDestroy
        databaseService.closeConnection();
    }
}
```

## Testing with Dependency Injection

Testing becomes easier with constructor injection:

```java
@Test
public class UserServiceTest {
    private UserRepository mockUserRepository;
    private EmailService mockEmailService;
    private UserService userService;

    @BeforeEach
    public void setUp() {
        mockUserRepository = mock(UserRepository.class);
        mockEmailService = mock(EmailService.class);
        userService = new UserService(mockUserRepository, mockEmailService);
    }

    @Test
    public void shouldCreateUserAndSendWelcomeEmail() {
        // Given
        String email = "test@example.com";
        User newUser = new User(email);
        User savedUser = new User(1L, email);

        when(mockUserRepository.save(newUser)).thenReturn(savedUser);

        // When
        User result = userService.createUser(email);

        // Then
        assertThat(result.getId()).isEqualTo(1L);
        verify(mockUserRepository).save(newUser);
        verify(mockEmailService).sendWelcomeEmail(email);
    }
}
```

## Best Practices

1. **Prefer Constructor Injection**: Use it for mandatory dependencies
2. **Use Setter Injection Sparingly**: Only for optional dependencies
3. **Avoid Field Injection**: It makes testing difficult and creates tight coupling
4. **Be Explicit About Dependencies**: Don't rely on implicit resolution
5. **Use Qualifiers When Needed**: For disambiguation between similar beans
6. **Consider Immutability**: Make injected fields final when possible
7. **Handle Circular Dependencies**: Redesign to eliminate them or use `@Lazy`
8. **Document Dependencies**: Comment on why certain dependencies are needed