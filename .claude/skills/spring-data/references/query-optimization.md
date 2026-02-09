# Query Optimization in Spring Data JPA

Comprehensive guide to optimizing database queries in Spring Data JPA applications.

## Query Performance Fundamentals

### Understanding Query Execution Plans
```sql
-- Example of analyzing query performance
EXPLAIN ANALYZE SELECT u.id, u.username, u.email 
FROM users u 
WHERE u.status = 'ACTIVE' 
AND u.created_at > '2023-01-01';

-- Look for:
-- 1. Sequential scans vs Index scans
-- 2. Number of rows examined
-- 3. Actual execution time
```

### Identifying Performance Bottlenecks
```java
// Using Spring Boot Actuator to monitor query performance
@Configuration
public class QueryPerformanceConfig {
    
    @Bean
    @Primary
    public HibernateStatisticsService hibernateStatisticsService(SessionFactory sessionFactory) {
        return new HibernateStatisticsService(sessionFactory);
    }
    
    @EventListener
    public void handleQueryExecution(QueryExecutionEvent event) {
        if (event.getQueryExecutionTime() > 1000) { // More than 1 second
            log.warn("Slow query detected: {} took {} ms", 
                     event.getQueryString(), event.getQueryExecutionTime());
        }
    }
}
```

## Fetch Strategy Optimization

### Solving the N+1 Problem
```java
// Problem: N+1 query issue
@Entity
public class Author {
    @Id
    private Long id;
    private String name;
    
    // LAZY by default, but accessing this causes N+1
    @OneToMany(mappedBy = "author")
    private List<Book> books = new ArrayList<>();
}

// Repository causing N+1
@Repository
public interface AuthorRepository extends JpaRepository<Author, Long> {
    List<Author> findByStatus(String status);
}

// Service causing N+1
@Service
public class AuthorService {
    public List<AuthorDto> getAuthorsWithBooks() {
        List<Author> authors = authorRepository.findByStatus("ACTIVE");
        return authors.stream()
            .map(author -> new AuthorDto(
                author.getId(), 
                author.getName(), 
                author.getBooks().size())) // Triggers N+1
            .collect(Collectors.toList());
    }
}

// Solution 1: JOIN FETCH
@Repository
public interface AuthorRepository extends JpaRepository<Author, Long> {
    @Query("SELECT a FROM Author a LEFT JOIN FETCH a.books WHERE a.status = :status")
    List<Author> findByStatusWithBooks(@Param("status") String status);
}

// Solution 2: EntityGraph
@Entity
@NamedEntityGraph(
    name = "Author.withBooks",
    attributeNodes = @NamedAttributeNode("books")
)
public class Author {
    // ... entity definition
}

@Repository
public interface AuthorRepository extends JpaRepository<Author, Long> {
    @EntityGraph("Author.withBooks")
    List<Author> findByStatus(String status);
}

// Solution 3: Batch fetching
@Entity
public class Author {
    @Id
    private Long id;
    private String name;
    
    @BatchSize(size = 10) // Fetch up to 10 collections at once
    @OneToMany(mappedBy = "author")
    private List<Book> books = new ArrayList<>();
}
```

### Optimizing Fetch Strategies
```java
// Proper use of fetch strategies
@Entity
public class Order {
    @Id
    private Long id;
    
    // EAGER: Small, frequently accessed association
    @OneToOne(fetch = FetchType.EAGER)
    @JoinColumn(name = "order_summary_id")
    private OrderSummary summary;
    
    // LAZY: Large collection, accessed conditionally
    @OneToMany(mappedBy = "order", fetch = FetchType.LAZY)
    private List<OrderItem> items = new ArrayList<>();
    
    // LAZY: Optional association, accessed when needed
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "customer_id")
    private Customer customer;
    
    // LAZY: Large collection, paginated separately
    @OneToMany(mappedBy = "order", fetch = FetchType.LAZY)
    private List<OrderComment> comments = new ArrayList<>();
}

// Repository with optimized queries
@Repository
public interface OrderRepository extends JpaRepository<Order, Long> {
    
    // For order details view - fetch commonly needed associations
    @EntityGraph(attributePaths = {"customer", "summary"})
    @Query("SELECT o FROM Order o WHERE o.id = :id")
    Optional<Order> findByIdWithCustomerAndSummary(@Param("id") Long id);
    
    // For order items view - fetch order with items
    @EntityGraph(attributePaths = {"items", "customer"})
    @Query("SELECT o FROM Order o WHERE o.id = :id")
    Optional<Order> findByIdWithItems(@Param("id") Long id);
    
    // For reporting - fetch aggregated data only
    @Query("SELECT new com.example.dto.OrderReportDto(o.id, o.totalAmount, o.orderDate, c.name) " +
           "FROM Order o JOIN o.customer c WHERE o.orderDate BETWEEN :startDate AND :endDate")
    List<OrderReportDto> findOrderReports(@Param("startDate") LocalDate startDate, 
                                        @Param("endDate") LocalDate endDate);
}
```

## Query Method Optimization

### Efficient Query Methods
```java
@Repository
public interface ProductRepository extends JpaRepository<Product, Long> {
    
    // Efficient: Uses index on category and status
    List<Product> findByCategoryAndStatus(Category category, Status status);
    
    // Inefficient: May not use indexes effectively
    List<Product> findByDescriptionContaining(String description);
    
    // Better: Combine with pagination
    Page<Product> findByDescriptionContaining(String description, Pageable pageable);
    
    // Best: Use full-text search if available
    @Query(value = "SELECT * FROM products WHERE MATCH(description) AGAINST(:description IN NATURAL LANGUAGE MODE)",
           nativeQuery = true)
    List<Product> searchByDescription(@Param("description") String description);
    
    // Efficient: Projection to avoid loading full entities
    @Query("SELECT new com.example.dto.ProductSummary(p.id, p.name, p.price) FROM Product p WHERE p.category = :category")
    List<ProductSummary> findSummariesByCategory(@Param("category") Category category);
    
    // Efficient: Count query without loading entities
    long countByCategoryAndStatus(Category category, Status status);
    
    // Efficient: Exists query without loading entities
    boolean existsByNameAndCategory(String name, Category category);
}
```

### Custom Query Optimization
```java
@Repository
public interface UserRepository extends JpaRepository<User, Long> {
    
    // Optimized with proper indexing hints
    @Query(value = "SELECT u.id, u.username, u.email, u.created_at " +
                   "FROM users u " +
                   "WHERE u.status = :status " +
                   "AND u.created_at >= :sinceDate " +
                   "ORDER BY u.created_at DESC " +
                   "LIMIT :limit",
           nativeQuery = true)
    List<Object[]> findRecentUsers(@Param("status") String status,
                                  @Param("sinceDate") LocalDateTime sinceDate,
                                  @Param("limit") int limit);
    
    // Using window functions for complex aggregations
    @Query(value = "SELECT u.*, " +
                   "ROW_NUMBER() OVER (PARTITION BY u.department_id ORDER BY u.salary DESC) as rank_in_dept " +
                   "FROM users u " +
                   "WHERE u.status = 'ACTIVE'",
           nativeQuery = true)
    List<UserWithRank> findUsersWithRanking();
    
    // Optimized bulk operations
    @Modifying
    @Query("UPDATE User u SET u.status = :newStatus WHERE u.lastLoginDate < :cutoffDate AND u.status = :oldStatus")
    int updateUserStatusBulk(@Param("newStatus") String newStatus,
                            @Param("cutoffDate") LocalDateTime cutoffDate,
                            @Param("oldStatus") String oldStatus);
}
```

## Pagination Optimization

### Efficient Pagination Strategies
```java
@Service
public class ProductService {
    
    // Offset-based pagination (good for small offsets)
    public Page<Product> findProductsOffsetBased(ProductFilter filter, Pageable pageable) {
        // Add index on filtered columns to improve performance
        return productRepository.findByFilters(filter, pageable);
    }
    
    // Cursor-based pagination (better for large datasets)
    public Slice<Product> findProductsCursorBased(Long lastProductId, int pageSize) {
        Pageable pageable = PageRequest.of(0, pageSize, Sort.by("id").ascending());
        return productRepository.findByIdGreaterThan(lastProductId, pageable);
    }
    
    // Keyset pagination implementation
    public Page<Product> findProductsKeyset(Long lastId, String lastCategory, int pageSize) {
        // For keyset pagination, we need to handle the case where multiple records have the same sort value
        Pageable pageable = PageRequest.of(0, pageSize, Sort.by("category", "id").ascending());
        
        if (lastId == null) {
            // First page
            return productRepository.findByCategoryGreaterThanEqual(lastCategory, pageable);
        } else {
            return productRepository.findByCategoryAndIdGreaterThan(lastCategory, lastId, pageable);
        }
    }
}

@Repository
public interface ProductRepository extends JpaRepository<Product, Long> {
    
    // For cursor-based pagination
    @Query("SELECT p FROM Product p WHERE p.id > :lastId ORDER BY p.id ASC")
    Slice<Product> findByIdGreaterThan(@Param("lastId") Long lastId, Pageable pageable);
    
    // For keyset pagination
    @Query("SELECT p FROM Product p WHERE p.category > :category OR (p.category = :category AND p.id > :lastId) ORDER BY p.category ASC, p.id ASC")
    Page<Product> findByCategoryAndIdGreaterThan(@Param("category") String category, 
                                                @Param("lastId") Long lastId, 
                                                Pageable pageable);
}
```

## Indexing Strategies

### Database Index Optimization
```java
// Entity with proper indexing annotations
@Entity
@Table(name = "orders", 
       indexes = {
           @Index(name = "idx_order_status_date", columnList = "status, created_date"),
           @Index(name = "idx_order_customer", columnList = "customer_id"),
           @Index(name = "idx_order_amount", columnList = "total_amount")
       })
public class Order {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(name = "status", nullable = false)
    @Enumerated(EnumType.STRING)
    private OrderStatus status;
    
    @Column(name = "created_date", nullable = false)
    private LocalDateTime createdDate;
    
    @Column(name = "customer_id", nullable = false)
    private Long customerId;
    
    @Column(name = "total_amount", precision = 10, scale = 2)
    private BigDecimal totalAmount;
    
    // Other fields...
}

// Composite index example
@Entity
@Table(name = "user_sessions",
       indexes = @Index(name = "idx_user_session_active", 
                       columnList = "user_id, is_active, expires_at"))
public class UserSession {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(name = "user_id", nullable = false)
    private Long userId;
    
    @Column(name = "is_active", nullable = false)
    private Boolean isActive;
    
    @Column(name = "expires_at")
    private LocalDateTime expiresAt;
    
    // Other fields...
}
```

## Query Caching

### First and Second Level Caching
```java
@Configuration
@EnableJpaRepositories
public class JpaConfig {
    
    @Bean
    public LocalContainerEntityManagerFactoryBean entityManagerFactory() {
        LocalContainerEntityManagerFactoryBean em = new LocalContainerEntityManagerFactoryBean();
        // ... other configuration
        
        Map<String, Object> properties = new HashMap<>();
        // Enable second-level cache
        properties.put("hibernate.cache.use_second_level_cache", true);
        properties.put("hibernate.cache.region.factory_class", "jcache");
        properties.put("hibernate.javax.cache.provider", "org.ehcache.jsr107.EhcacheCachingProvider");
        
        // Enable query cache
        properties.put("hibernate.cache.use_query_cache", true);
        
        em.setJpaPropertyMap(properties);
        return em;
    }
}

// Entity with caching annotations
@Entity
@Cacheable
@org.hibernate.annotations.Cache(usage = CacheConcurrencyStrategy.READ_WRITE)
@Table(name = "categories")
public class Category {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @NaturalId
    @Column(unique = true)
    private String slug;
    
    private String name;
    
    // For frequently accessed, rarely changed data
}

// Repository with query caching
@Repository
public interface CategoryRepository extends JpaRepository<Category, Long> {
    
    @Cacheable("categories")
    List<Category> findAll();
    
    @Cacheable("categories")
    Optional<Category> findBySlug(@Param("slug") String slug);
}
```

## Monitoring and Profiling

### Query Performance Monitoring
```java
@Component
public class QueryPerformanceMonitor {
    
    private static final Logger log = LoggerFactory.getLogger(QueryPerformanceMonitor.class);
    private final MeterRegistry meterRegistry;
    
    public QueryPerformanceMonitor(MeterRegistry meterRegistry) {
        this.meterRegistry = meterRegistry;
    }
    
    @EventListener
    public void handleQueryExecution(QueryExecutionEvent event) {
        Timer.Sample sample = Timer.start(meterRegistry);
        
        // Record query execution time
        sample.stop(Timer.builder("jpa.query.execution.time")
            .tag("entity", event.getEntityName())
            .tag("query_type", event.getQueryType().toString())
            .register(meterRegistry));
        
        // Log slow queries
        if (event.getQueryExecutionTime() > 1000) { // 1 second threshold
            log.warn("Slow query detected: {} took {} ms", 
                     event.getQueryString(), event.getQueryExecutionTime());
            
            // Add to slow query metrics
            Counter.builder("jpa.slow.queries")
                .tag("entity", event.getEntityName())
                .register(meterRegistry)
                .increment();
        }
    }
}

// Configuration for Hibernate statistics
@Configuration
public class HibernateStatisticsConfig {
    
    @Bean
    @Primary
    public HibernateJmxAutoConfiguration hibernateJmxAutoConfiguration() {
        return new HibernateJmxAutoConfiguration();
    }
    
    // Enable Hibernate statistics (use only in development)
    @Bean
    @Profile("dev")
    public BeanPostProcessor hibernateStatisticsEnabler() {
        return new BeanPostProcessor() {
            @Override
            public Object postProcessAfterInitialization(Object bean, String beanName) throws BeansException {
                if (bean instanceof EntityManagerFactory) {
                    SessionFactory sessionFactory = ((EntityManagerFactory) bean).unwrap(SessionFactory.class);
                    sessionFactory.getStatistics().setStatisticsEnabled(true);
                    sessionFactory.getStatistics().setEchoStatistics(true);
                }
                return bean;
            }
        };
    }
}
```

## Best Practices Summary

### Performance Guidelines
1. **Choose the right fetch strategy**: Use LAZY by default, optimize with JOIN FETCH when needed
2. **Implement proper indexing**: Index columns used in WHERE, JOIN, and ORDER BY clauses
3. **Use projections**: Return only the data you need
4. **Optimize pagination**: Use cursor-based pagination for large datasets
5. **Monitor query performance**: Track slow queries and execution times
6. **Use caching appropriately**: Implement first and second-level caching for read-heavy applications
7. **Avoid N+1 problems**: Use JOIN FETCH, EntityGraph, or batch fetching
8. **Consider read replicas**: For read-heavy applications, use separate read databases
9. **Profile regularly**: Use tools like Hibernate Statistics, P6Spy, or database profiling
10. **Optimize bulk operations**: Use native queries or JPA bulk operations for large updates