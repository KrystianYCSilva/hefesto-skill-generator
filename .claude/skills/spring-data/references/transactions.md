# Transaction Management in Spring Data JPA

Comprehensive guide to transaction management in Spring Data JPA applications.

## Transaction Fundamentals

### ACID Properties
- **Atomicity**: All operations in a transaction succeed or fail as a single unit
- **Consistency**: Transactions bring the database from one valid state to another
- **Isolation**: Concurrent transactions don't interfere with each other
- **Durability**: Once committed, changes are permanent

### Transaction Boundaries
```java
@Service
@Transactional
public class OrderService {
    
    @Autowired
    private OrderRepository orderRepository;
    
    @Autowired
    private PaymentService paymentService;
    
    @Autowired
    private InventoryService inventoryService;
    
    // Method runs in a new transaction
    @Transactional
    public Order createOrder(OrderRequest request) {
        Order order = new Order();
        order.setStatus(OrderStatus.PENDING);
        order.setItems(request.getItems());
        order.setTotalAmount(calculateTotal(request.getItems()));
        
        // Save order - transaction begins here
        Order savedOrder = orderRepository.save(order);
        
        try {
            // Process payment - same transaction
            paymentService.processPayment(savedOrder, request.getPaymentInfo());
            
            // Update inventory - same transaction
            inventoryService.reserveInventory(request.getItems());
            
            // Update order status - same transaction
            savedOrder.setStatus(OrderStatus.CONFIRMED);
            orderRepository.save(savedOrder);
            
            // Transaction commits when method completes successfully
            return savedOrder;
        } catch (Exception e) {
            // Transaction will rollback due to exception
            throw new OrderProcessingException("Failed to process order", e);
        }
    }
}
```

## Transaction Propagation

### Propagation Types
```java
@Service
public class UserService {
    
    @Autowired
    private UserRepository userRepository;
    
    @Autowired
    private AuditService auditService;
    
    // REQUIRES_NEW: Always runs in a new transaction
    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public void logUserAction(Long userId, String action) {
        AuditLog log = new AuditLog();
        log.setUserId(userId);
        log.setAction(action);
        log.setTimestamp(LocalDateTime.now());
        
        auditService.saveAuditLog(log);
        // This transaction commits independently of the calling method
    }
    
    // NESTED: Runs in a nested transaction
    @Transactional(propagation = Propagation.NESTED)
    public void updateUserProfile(Long userId, UserProfileUpdateRequest request) {
        User user = userRepository.findById(userId)
            .orElseThrow(() -> new UserNotFoundException("User not found"));
        
        user.setProfile(request.getProfile());
        
        try {
            userRepository.save(user);
            // Nested transaction can be rolled back independently
        } catch (Exception e) {
            // This nested transaction rolls back, but outer transaction continues
            log.warn("Failed to update user profile", e);
        }
    }
    
    // SUPPORTS: Runs in existing transaction if available
    @Transactional(propagation = Propagation.SUPPORTS)
    public boolean validateUser(Long userId) {
        // Uses existing transaction if called from @Transactional method
        // Otherwise runs without a transaction
        return userRepository.existsById(userId);
    }
    
    // NOT_SUPPORTED: Runs without a transaction
    @Transactional(propagation = Propagation.NOT_SUPPORTED)
    public void runWithoutTransaction() {
        // This method runs without a transaction
        // Any existing transaction is suspended
    }
    
    // NEVER: Must not run in a transaction
    @Transactional(propagation = Propagation.NEVER)
    public void runWithoutTransactionRequired() {
        // Throws an exception if called from within a transaction
    }
    
    // MANDATORY: Must run in an existing transaction
    @Transactional(propagation = Propagation.MANDATORY)
    public void runInExistingTransaction() {
        // Throws an exception if not called from within a transaction
    }
}
```

## Transaction Isolation Levels

### Isolation Configuration
```java
@Service
public class BankingService {
    
    @Autowired
    private AccountRepository accountRepository;
    
    // READ_COMMITTED: Default isolation level
    @Transactional(isolation = Isolation.READ_COMMITTED)
    public void transferFunds(Long fromAccountId, Long toAccountId, BigDecimal amount) {
        Account fromAccount = accountRepository.findById(fromAccountId)
            .orElseThrow(() -> new AccountNotFoundException("From account not found"));
        
        Account toAccount = accountRepository.findById(toAccountId)
            .orElseThrow(() -> new AccountNotFoundException("To account not found"));
        
        if (fromAccount.getBalance().compareTo(amount) < 0) {
            throw new InsufficientFundsException("Insufficient funds");
        }
        
        fromAccount.setBalance(fromAccount.getBalance().subtract(amount));
        toAccount.setBalance(toAccount.getBalance().add(amount));
        
        accountRepository.save(fromAccount);
        accountRepository.save(toAccount);
    }
    
    // SERIALIZABLE: Highest isolation level
    @Transactional(isolation = Isolation.SERIALIZABLE)
    public void updateHighlyContendedResource() {
        // Use for operations that must be completely isolated
        // Warning: May cause performance issues due to locking
    }
    
    // READ_UNCOMMITTED: Lowest isolation level
    @Transactional(isolation = Isolation.READ_UNCOMMITTED)
    public List<Account> getAccountSnapshot() {
        // May read uncommitted changes from other transactions
        // Generally not recommended
        return accountRepository.findAll();
    }
}
```

## Transaction Rollback Configuration

### Rollback Rules
```java
@Service
@Transactional
public class OrderProcessingService {
    
    @Autowired
    private OrderRepository orderRepository;
    
    // Rollback on specific exceptions
    @Transactional(rollbackFor = {OrderProcessingException.class}, 
                   noRollbackFor = {ValidationException.class})
    public void processOrder(OrderRequest request) throws OrderProcessingException, ValidationException {
        try {
            // Business logic here
            Order order = createOrder(request);
            
            // If ValidationException is thrown, transaction commits
            validateOrder(order);
            
            // If OrderProcessingException is thrown, transaction rolls back
            chargePayment(order);
            
        } catch (ValidationException e) {
            // Log validation error but don't rollback transaction
            log.warn("Validation error: {}", e.getMessage());
            throw e;
        } catch (OrderProcessingException e) {
            // This will trigger a rollback
            log.error("Order processing failed: {}", e.getMessage());
            throw e;
        }
    }
    
    // Read-only transactions
    @Transactional(readOnly = true)
    public Order getOrder(Long orderId) {
        // Optimizes for read operations
        // May use read replicas
        // Prevents accidental modifications
        return orderRepository.findById(orderId)
            .orElseThrow(() -> new OrderNotFoundException("Order not found"));
    }
    
    // Write transaction
    @Transactional(readOnly = false)
    public Order updateOrder(Long orderId, OrderUpdateRequest request) {
        Order order = orderRepository.findById(orderId)
            .orElseThrow(() -> new OrderNotFoundException("Order not found"));
        
        // Update order properties
        order.setStatus(request.getStatus());
        order.setNotes(request.getNotes());
        
        return orderRepository.save(order);
    }
}
```

## Advanced Transaction Patterns

### Programmatic Transaction Management
```java
@Service
public class ComplexTransactionService {
    
    @Autowired
    private TransactionTemplate transactionTemplate;
    
    @Autowired
    private OrderRepository orderRepository;
    
    @Autowired
    private PaymentRepository paymentRepository;
    
    // Programmatic transaction management
    public Order processOrderWithManualTx(OrderRequest request) {
        return transactionTemplate.execute(status -> {
            try {
                Order order = new Order();
                order.setItems(request.getItems());
                order.setTotalAmount(calculateTotal(request.getItems()));
                
                Order savedOrder = orderRepository.save(order);
                
                Payment payment = new Payment();
                payment.setOrderId(savedOrder.getId());
                payment.setAmount(savedOrder.getTotalAmount());
                payment.setStatus(PaymentStatus.PENDING);
                
                Payment savedPayment = paymentRepository.save(payment);
                
                // Simulate payment processing
                if (!processPayment(savedPayment)) {
                    status.setRollbackOnly(); // Mark for rollback
                    throw new PaymentFailedException("Payment processing failed");
                }
                
                savedOrder.setStatus(OrderStatus.CONFIRMED);
                return orderRepository.save(savedOrder);
                
            } catch (Exception e) {
                status.setRollbackOnly();
                throw new RuntimeException("Transaction failed", e);
            }
        });
    }
    
    // Custom transaction configuration
    public void executeWithCustomConfig(Runnable operation) {
        TransactionDefinition def = new DefaultTransactionDefinition();
        def.setIsolationLevel(TransactionDefinition.ISOLATION_SERIALIZABLE);
        def.setPropagationBehavior(TransactionDefinition.PROPAGATION_REQUIRES_NEW);
        def.setTimeout(30); // 30 seconds timeout
        
        TransactionStatus status = transactionTemplate.getTransactionManager().getTransaction(def);
        
        try {
            operation.run();
            transactionTemplate.getTransactionManager().commit(status);
        } catch (Exception e) {
            transactionTemplate.getTransactionManager().rollback(status);
            throw new RuntimeException("Transaction failed", e);
        }
    }
}
```

### Transaction Synchronization
```java
@Service
public class TransactionSynchronizationService {
    
    // Execute after transaction completion
    public void performActionAfterCommit(Runnable action) {
        TransactionSynchronizationManager.registerSynchronization(
            new TransactionSynchronization() {
                @Override
                public void afterCommit() {
                    // This runs after the transaction commits successfully
                    action.run();
                }
                
                @Override
                public void afterCompletion(int status) {
                    if (status == TransactionSynchronization.STATUS_ROLLED_BACK) {
                        // Handle rollback scenario
                        log.warn("Transaction was rolled back");
                    }
                }
            }
        );
    }
    
    // Example usage
    @Transactional
    public void createUserWithNotifications(User user) {
        userRepository.save(user);
        
        // Send notification after successful commit
        performActionAfterCommit(() -> {
            notificationService.sendWelcomeEmail(user.getEmail());
            auditService.logUserCreation(user.getId());
        });
    }
}
```

## Transaction Performance Considerations

### Optimizing Transaction Scope
```java
@Service
public class OptimizedTransactionService {
    
    // Bad: Long-running transaction holding locks
    @Transactional
    public void badLongRunningOperation() {
        // This transaction holds locks for a long time
        List<Order> orders = orderRepository.findAll();
        
        for (Order order : orders) {
            // Simulate long-running external operation
            externalService.processOrder(order);
            order.setStatus(OrderStatus.PROCESSED);
            orderRepository.save(order); // Keeps transaction open
        }
    }
    
    // Good: Short transactions with bulk operations
    @Transactional
    public void goodBatchProcessing() {
        // Fetch only what we need
        List<Order> orders = orderRepository.findPendingOrders();
        
        // Process outside of transaction
        List<Order> processedOrders = orders.stream()
            .map(this::processOrderExternally)
            .collect(Collectors.toList());
        
        // Update in a short transaction
        orderRepository.saveAll(processedOrders);
    }
    
    private Order processOrderExternally(Order order) {
        // Process order without transaction
        externalService.processOrder(order);
        order.setStatus(OrderStatus.PROCESSED);
        return order;
    }
    
    // Using REQUIRES_NEW for independent operations
    @Transactional
    public void processOrdersIndependently(List<OrderRequest> requests) {
        for (OrderRequest request : requests) {
            // Each order is processed in its own transaction
            processSingleOrderInNewTransaction(request);
        }
    }
    
    @Transactional(propagation = Propagation.REQUIRES_NEW)
    protected void processSingleOrderInNewTransaction(OrderRequest request) {
        // If one order fails, others are not affected
        Order order = createOrder(request);
        chargePayment(order);
        updateInventory(order);
    }
}
```

## Transaction Best Practices

### Configuration Best Practices
```java
@Configuration
@EnableTransactionManagement
public class TransactionConfig {
    
    @Bean
    public PlatformTransactionManager transactionManager(EntityManagerFactory entityManagerFactory) {
        JpaTransactionManager transactionManager = new JpaTransactionManager();
        transactionManager.setEntityManagerFactory(entityManagerFactory);
        
        // Set default rollback rules
        transactionManager.setDefaultTimeout(30); // 30 second timeout
        transactionManager.setGlobalRollbackOnParticipationFailure(true);
        
        return transactionManager;
    }
    
    @Bean
    public TransactionTemplate transactionTemplate(PlatformTransactionManager transactionManager) {
        TransactionTemplate template = new TransactionTemplate(transactionManager);
        template.setIsolationLevel(TransactionDefinition.ISOLATION_READ_COMMITTED);
        template.setTimeout(30);
        return template;
    }
}

// Service with proper transaction design
@Service
@Transactional(readOnly = true) // Default for read operations
public class WellDesignedService {
    
    @Autowired
    private UserRepository userRepository;
    
    // Read operation inherits readOnly = true
    public User findById(Long id) {
        return userRepository.findById(id)
            .orElseThrow(() -> new UserNotFoundException("User not found: " + id));
    }
    
    // Write operation overrides to allow modifications
    @Transactional(readOnly = false) // Allow writes
    public User save(User user) {
        return userRepository.save(user);
    }
    
    // Complex operation with specific requirements
    @Transactional(
        readOnly = false,
        isolation = Isolation.READ_COMMITTED,
        propagation = Propagation.REQUIRED,
        rollbackFor = {BusinessException.class},
        timeout = 60
    )
    public void complexBusinessOperation(OperationRequest request) throws BusinessException {
        // Implementation
    }
}
```

### Error Handling in Transactions
```java
@Service
public class ErrorHandlingService {
    
    // Proper exception hierarchy
    @Transactional(rollbackFor = {BusinessException.class})
    public void businessOperation() throws BusinessException {
        try {
            // Business logic
            performBusinessLogic();
        } catch (ValidationException e) {
            // Validation errors shouldn't cause rollback
            log.warn("Validation error: {}", e.getMessage());
            throw new BusinessException("Validation failed", e);
        } catch (TechnicalException e) {
            // Technical errors should cause rollback
            log.error("Technical error: {}", e.getMessage(), e);
            throw new BusinessException("Technical error occurred", e);
        }
    }
    
    // Handling checked exceptions
    @Transactional(rollbackFor = Exception.class)
    public void operationWithCheckedExceptions() throws IOException, SQLException {
        // Even checked exceptions will cause rollback
        performIoOperation();
        performDatabaseOperation();
    }
}
```

## Common Transaction Pitfalls

### Avoiding Common Mistakes
```java
// Pitfall 1: Exception handling that prevents rollback
@Service
public class BadExceptionHandling {
    
    @Transactional
    public void badExceptionHandling() {
        try {
            // This operation fails
            riskyOperation();
        } catch (Exception e) {
            // The exception is caught and swallowed
            // Transaction still commits! This is wrong!
            log.error("Error occurred but transaction will commit", e);
        }
    }
    
    // Correct approach
    @Transactional(rollbackFor = Exception.class)
    public void goodExceptionHandling() throws Exception {
        try {
            riskyOperation();
        } catch (Exception e) {
            log.error("Error occurred, transaction will rollback", e);
            throw e; // Re-throw to trigger rollback
        }
    }
}

// Pitfall 2: Calling @Transactional methods from within the same class
@Service
public class SelfInvocationProblem {
    
    @Transactional
    public void methodA() {
        // Transactional behavior works here
        methodB(); // This call won't be transactional!
    }
    
    @Transactional
    public void methodB() {
        // This won't run in a separate transaction when called from methodA
        // because Spring's proxy mechanism doesn't apply to self-invocations
    }
    
    // Solution: Inject self-reference or restructure
    @Autowired
    private SelfInvocationProblem self;
    
    @Transactional
    public void methodA_fixed() {
        // Now this will work as expected
        self.methodB();
    }
    
    @Transactional
    public void methodB_fixed() {
        // This will now run in its own transaction
    }
}
```

## Testing Transactions

### Transaction Testing Strategies
```java
@SpringBootTest
@Transactional
@Rollback // Rollback transactions after each test
class TransactionServiceTest {
    
    @Autowired
    private OrderService orderService;
    
    @Autowired
    private TestEntityManager entityManager;
    
    @Test
    void testSuccessfulTransaction() {
        // Given
        OrderRequest request = createValidOrderRequest();
        
        // When
        Order result = orderService.createOrder(request);
        
        // Then
        assertThat(result).isNotNull();
        assertThat(result.getStatus()).isEqualTo(OrderStatus.CONFIRMED);
        
        // Verify in database
        entityManager.flush();
        Order savedOrder = entityManager.find(Order.class, result.getId());
        assertThat(savedOrder).isNotNull();
    }
    
    @Test
    void testTransactionRollbackOnException() {
        // Given
        OrderRequest request = createInvalidOrderRequest();
        
        // When/Then
        assertThatThrownBy(() -> orderService.createOrder(request))
            .isInstanceOf(OrderProcessingException.class);
        
        // Transaction is automatically rolled back
        entityManager.flush();
        List<Order> orders = entityManager.getEntityManager()
            .createQuery("SELECT o FROM Order o", Order.class)
            .getResultList();
        assertThat(orders).isEmpty();
    }
}
```

This comprehensive guide covers transaction management in Spring Data JPA, including propagation, isolation, rollback rules, performance considerations, and best practices.