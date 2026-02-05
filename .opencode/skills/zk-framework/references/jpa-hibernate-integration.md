# ZK Framework + JPA/Hibernate Integration

Complete guide to integrating ZK with JPA and Hibernate for database persistence.

## Table of Contents

1. [Configuration](#configuration)
2. [Entity Management](#entity-management)
3. [LazyInitializationException](#lazyinitializationexception)
4. [N+1 Query Problem](#n1-query-problem)
5. [Detached Entities](#detached-entities)
6. [Best Practices](#best-practices)

## Configuration

### Maven Dependencies

```xml
<!-- JPA/Hibernate -->
<dependency>
    <groupId>org.hibernate</groupId>
    <artifactId>hibernate-core</artifactId>
    <version>5.6.15.Final</version>
</dependency>

<dependency>
    <groupId>org.hibernate</groupId>
    <artifactId>hibernate-entitymanager</artifactId>
    <version>5.6.15.Final</version>
</dependency>

<!-- Database Driver -->
<dependency>
    <groupId>mysql</groupId>
    <artifactId>mysql-connector-java</artifactId>
    <version>8.0.33</version>
</dependency>

<!-- Connection Pool -->
<dependency>
    <groupId>com.zaxxer</groupId>
    <artifactId>HikariCP</artifactId>
    <version>5.0.1</version>
</dependency>
```

### persistence.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<persistence xmlns="http://xmlns.jcp.org/xml/ns/persistence" version="2.2">
    <persistence-unit name="zkAppPU" transaction-type="RESOURCE_LOCAL">
        <provider>org.hibernate.jpa.HibernatePersistenceProvider</provider>
        
        <class>com.example.model.User</class>
        <class>com.example.model.Order</class>
        <class>com.example.model.Product</class>
        
        <properties>
            <!-- Database connection -->
            <property name="javax.persistence.jdbc.driver" 
                      value="com.mysql.cj.jdbc.Driver"/>
            <property name="javax.persistence.jdbc.url" 
                      value="jdbc:mysql://localhost:3306/zkapp"/>
            <property name="javax.persistence.jdbc.user" value="root"/>
            <property name="javax.persistence.jdbc.password" value="password"/>
            
            <!-- Hibernate settings -->
            <property name="hibernate.dialect" 
                      value="org.hibernate.dialect.MySQL8Dialect"/>
            <property name="hibernate.hbm2ddl.auto" value="update"/>
            <property name="hibernate.show_sql" value="true"/>
            <property name="hibernate.format_sql" value="true"/>
            
            <!-- Connection pool -->
            <property name="hibernate.hikari.maximumPoolSize" value="10"/>
            <property name="hibernate.hikari.minimumIdle" value="5"/>
        </properties>
    </persistence-unit>
</persistence>
```

### Entity Manager Factory

```java
package com.example.persistence;

import javax.persistence.EntityManagerFactory;
import javax.persistence.Persistence;

public class JPAUtil {
    
    private static final EntityManagerFactory emf;
    
    static {
        try {
            emf = Persistence.createEntityManagerFactory("zkAppPU");
        } catch (Throwable ex) {
            throw new ExceptionInInitializerError(ex);
        }
    }
    
    public static EntityManagerFactory getEntityManagerFactory() {
        return emf;
    }
    
    public static void shutdown() {
        if (emf != null) {
            emf.close();
        }
    }
}
```

## Entity Management

### Entity Examples

```java
package com.example.model;

import javax.persistence.*;
import java.util.Date;
import java.util.List;

@Entity
@Table(name = "users")
public class User {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(nullable = false, unique = true, length = 100)
    private String email;
    
    @Column(nullable = false, length = 100)
    private String name;
    
    @Temporal(TemporalType.TIMESTAMP)
    @Column(name = "created_at")
    private Date createdAt;
    
    @OneToMany(mappedBy = "user", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private List<Order> orders;
    
    @PrePersist
    protected void onCreate() {
        createdAt = new Date();
    }
    
    // Getters and setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    
    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }
    
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    
    public Date getCreatedAt() { return createdAt; }
    
    public List<Order> getOrders() { return orders; }
    public void setOrders(List<Order> orders) { this.orders = orders; }
}
```

```java
package com.example.model;

import javax.persistence.*;
import java.math.BigDecimal;
import java.util.Date;

@Entity
@Table(name = "orders")
public class Order {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id", nullable = false)
    private User user;
    
    @Column(nullable = false, precision = 10, scale = 2)
    private BigDecimal total;
    
    @Temporal(TemporalType.TIMESTAMP)
    @Column(name = "order_date")
    private Date orderDate;
    
    @Enumerated(EnumType.STRING)
    @Column(length = 20)
    private OrderStatus status;
    
    @PrePersist
    protected void onCreate() {
        orderDate = new Date();
        status = OrderStatus.PENDING;
    }
    
    public enum OrderStatus {
        PENDING, CONFIRMED, SHIPPED, DELIVERED, CANCELLED
    }
    
    // Getters and setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    
    public User getUser() { return user; }
    public void setUser(User user) { this.user = user; }
    
    public BigDecimal getTotal() { return total; }
    public void setTotal(BigDecimal total) { this.total = total; }
    
    public Date getOrderDate() { return orderDate; }
    
    public OrderStatus getStatus() { return status; }
    public void setStatus(OrderStatus status) { this.status = status; }
}
```

### DAO Pattern

```java
package com.example.dao;

import javax.persistence.EntityManager;
import javax.persistence.EntityTransaction;
import java.util.List;

public abstract class GenericDAO<T, ID> {
    
    private final Class<T> entityClass;
    
    public GenericDAO(Class<T> entityClass) {
        this.entityClass = entityClass;
    }
    
    protected EntityManager getEntityManager() {
        return JPAUtil.getEntityManagerFactory().createEntityManager();
    }
    
    public T findById(ID id) {
        EntityManager em = getEntityManager();
        try {
            return em.find(entityClass, id);
        } finally {
            em.close();
        }
    }
    
    public List<T> findAll() {
        EntityManager em = getEntityManager();
        try {
            return em.createQuery("FROM " + entityClass.getSimpleName(), entityClass)
                     .getResultList();
        } finally {
            em.close();
        }
    }
    
    public T save(T entity) {
        EntityManager em = getEntityManager();
        EntityTransaction tx = null;
        try {
            tx = em.getTransaction();
            tx.begin();
            
            if (em.contains(entity)) {
                entity = em.merge(entity);
            } else {
                em.persist(entity);
            }
            
            tx.commit();
            return entity;
        } catch (Exception e) {
            if (tx != null && tx.isActive()) {
                tx.rollback();
            }
            throw e;
        } finally {
            em.close();
        }
    }
    
    public void delete(ID id) {
        EntityManager em = getEntityManager();
        EntityTransaction tx = null;
        try {
            tx = em.getTransaction();
            tx.begin();
            
            T entity = em.find(entityClass, id);
            if (entity != null) {
                em.remove(entity);
            }
            
            tx.commit();
        } catch (Exception e) {
            if (tx != null && tx.isActive()) {
                tx.rollback();
            }
            throw e;
        } finally {
            em.close();
        }
    }
}
```

```java
package com.example.dao;

import com.example.model.User;

public class UserDAO extends GenericDAO<User, Long> {
    
    public UserDAO() {
        super(User.class);
    }
    
    public User findByEmail(String email) {
        EntityManager em = getEntityManager();
        try {
            return em.createQuery(
                "SELECT u FROM User u WHERE u.email = :email", User.class)
                .setParameter("email", email)
                .getSingleResult();
        } catch (NoResultException e) {
            return null;
        } finally {
            em.close();
        }
    }
    
    public List<User> findByNameContaining(String name) {
        EntityManager em = getEntityManager();
        try {
            return em.createQuery(
                "SELECT u FROM User u WHERE u.name LIKE :name", User.class)
                .setParameter("name", "%" + name + "%")
                .getResultList();
        } finally {
            em.close();
        }
    }
}
```

## LazyInitializationException

### Problem: Accessing Lazy Collections

```java
// WRONG: LazyInitializationException
public class UserVM {
    
    private UserDAO userDAO = new UserDAO();
    private List<User> users;
    
    @Init
    public void init() {
        users = userDAO.findAll(); // EntityManager closed after this
    }
    
    public List<Order> getUserOrders(User user) {
        // LazyInitializationException: EntityManager is closed!
        return user.getOrders();
    }
}
```

### Solution 1: Eager Fetching with JOIN FETCH

```java
package com.example.dao;

public class UserDAO extends GenericDAO<User, Long> {
    
    public List<User> findAllWithOrders() {
        EntityManager em = getEntityManager();
        try {
            return em.createQuery(
                "SELECT DISTINCT u FROM User u LEFT JOIN FETCH u.orders", 
                User.class)
                .getResultList();
        } finally {
            em.close();
        }
    }
    
    public User findByIdWithOrders(Long id) {
        EntityManager em = getEntityManager();
        try {
            return em.createQuery(
                "SELECT u FROM User u LEFT JOIN FETCH u.orders WHERE u.id = :id", 
                User.class)
                .setParameter("id", id)
                .getSingleResult();
        } catch (NoResultException e) {
            return null;
        } finally {
            em.close();
        }
    }
}
```

### Solution 2: Open Session in View Pattern

```java
package com.example.filter;

import javax.persistence.EntityManager;
import javax.servlet.*;
import java.io.IOException;

public class OpenEntityManagerInViewFilter implements Filter {
    
    @Override
    public void doFilter(ServletRequest request, ServletResponse response, 
                        FilterChain chain) throws IOException, ServletException {
        EntityManager em = JPAUtil.getEntityManagerFactory().createEntityManager();
        EntityManagerHolder.set(em);
        
        try {
            chain.doFilter(request, response);
        } finally {
            EntityManagerHolder.remove();
            em.close();
        }
    }
    
    @Override
    public void init(FilterConfig filterConfig) {}
    
    @Override
    public void destroy() {}
}

class EntityManagerHolder {
    private static ThreadLocal<EntityManager> holder = new ThreadLocal<>();
    
    public static void set(EntityManager em) {
        holder.set(em);
    }
    
    public static EntityManager get() {
        return holder.get();
    }
    
    public static void remove() {
        holder.remove();
    }
}
```

```xml
<!-- web.xml -->
<filter>
    <filter-name>OpenEntityManagerInViewFilter</filter-name>
    <filter-class>com.example.filter.OpenEntityManagerInViewFilter</filter-class>
</filter>

<filter-mapping>
    <filter-name>OpenEntityManagerInViewFilter</filter-name>
    <url-pattern>*.zul</url-pattern>
</filter-mapping>
```

### Solution 3: Initialize Collections Manually

```java
public class UserDAO extends GenericDAO<User, Long> {
    
    public List<User> findAllWithOrdersInitialized() {
        EntityManager em = getEntityManager();
        try {
            List<User> users = em.createQuery("FROM User", User.class)
                                 .getResultList();
            
            // Force initialization
            for (User user : users) {
                user.getOrders().size();
            }
            
            return users;
        } finally {
            em.close();
        }
    }
}
```

## N+1 Query Problem

### Problem: Multiple Queries for Lazy Collections

```java
// WRONG: Generates N+1 queries
public class OrderListVM {
    
    private OrderDAO orderDAO = new OrderDAO();
    
    @Init
    public void init() {
        List<Order> orders = orderDAO.findAll(); // 1 query
        
        for (Order order : orders) {
            // N queries (one per order)
            User user = order.getUser();
            String userName = user.getName();
        }
    }
}
```

### Solution 1: JOIN FETCH

```java
public class OrderDAO extends GenericDAO<Order, Long> {
    
    public List<Order> findAllWithUsers() {
        EntityManager em = getEntityManager();
        try {
            // Single query with JOIN
            return em.createQuery(
                "SELECT o FROM Order o JOIN FETCH o.user", 
                Order.class)
                .getResultList();
        } finally {
            em.close();
        }
    }
}
```

### Solution 2: Entity Graph

```java
public class OrderDAO extends GenericDAO<Order, Long> {
    
    public List<Order> findAllWithEntityGraph() {
        EntityManager em = getEntityManager();
        try {
            EntityGraph<Order> graph = em.createEntityGraph(Order.class);
            graph.addAttributeNodes("user");
            
            return em.createQuery("FROM Order", Order.class)
                     .setHint("javax.persistence.fetchgraph", graph)
                     .getResultList();
        } finally {
            em.close();
        }
    }
}
```

### Solution 3: Batch Fetching

```java
@Entity
@Table(name = "orders")
@BatchSize(size = 10)
public class Order {
    
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id")
    @BatchSize(size = 10)
    private User user;
    
    // Rest of entity
}
```

## Detached Entities

### Problem: Modifying Detached Entities

```java
// WRONG: Changes lost
public class UserEditVM {
    
    private UserDAO userDAO = new UserDAO();
    private User user;
    
    @Init
    public void init(@ExecutionArgParam("userId") Long userId) {
        user = userDAO.findById(userId); // Entity becomes detached
    }
    
    @Command
    public void save() {
        // user is detached, changes not saved!
        userDAO.save(user);
    }
}
```

### Solution 1: Merge Detached Entities

```java
public class GenericDAO<T, ID> {
    
    public T update(T entity) {
        EntityManager em = getEntityManager();
        EntityTransaction tx = null;
        try {
            tx = em.getTransaction();
            tx.begin();
            
            // Merge detached entity
            T merged = em.merge(entity);
            
            tx.commit();
            return merged;
        } catch (Exception e) {
            if (tx != null && tx.isActive()) {
                tx.rollback();
            }
            throw e;
        } finally {
            em.close();
        }
    }
}
```

### Solution 2: Reattach Within Transaction

```java
public class UserEditVM {
    
    private UserDAO userDAO = new UserDAO();
    private User user;
    
    @Command
    public void save() {
        EntityManager em = JPAUtil.getEntityManagerFactory().createEntityManager();
        EntityTransaction tx = null;
        
        try {
            tx = em.getTransaction();
            tx.begin();
            
            // Reattach
            User managed = em.find(User.class, user.getId());
            managed.setName(user.getName());
            managed.setEmail(user.getEmail());
            
            tx.commit();
            
            Clients.showNotification("User saved successfully");
        } catch (Exception e) {
            if (tx != null && tx.isActive()) {
                tx.rollback();
            }
            Clients.showNotification("Error: " + e.getMessage(), "error", null, null, 0);
        } finally {
            em.close();
        }
    }
}
```

### Solution 3: DTO Pattern

```java
package com.example.dto;

public class UserDTO {
    private Long id;
    private String name;
    private String email;
    
    public UserDTO() {}
    
    public UserDTO(User user) {
        this.id = user.getId();
        this.name = user.getName();
        this.email = user.getEmail();
    }
    
    public User toEntity() {
        User user = new User();
        user.setId(this.id);
        user.setName(this.name);
        user.setEmail(this.email);
        return user;
    }
    
    // Getters and setters
}
```

```java
public class UserEditVM {
    
    private UserDAO userDAO = new UserDAO();
    private UserDTO userDTO;
    
    @Init
    public void init(@ExecutionArgParam("userId") Long userId) {
        User user = userDAO.findById(userId);
        userDTO = new UserDTO(user);
    }
    
    @Command
    @NotifyChange("userDTO")
    public void save() {
        User user = userDTO.toEntity();
        userDAO.update(user);
        Clients.showNotification("User saved successfully");
    }
    
    public UserDTO getUserDTO() {
        return userDTO;
    }
}
```

## Best Practices

### Practice 1: Close EntityManager Properly

```java
// Use try-with-resources (JPA 2.1+)
public List<User> findAll() {
    try (EntityManager em = JPAUtil.getEntityManagerFactory().createEntityManager()) {
        return em.createQuery("FROM User", User.class).getResultList();
    }
}
```

### Practice 2: Use Query Pagination

```java
public class UserDAO extends GenericDAO<User, Long> {
    
    public List<User> findPaginated(int page, int pageSize) {
        EntityManager em = getEntityManager();
        try {
            return em.createQuery("FROM User ORDER BY name", User.class)
                     .setFirstResult(page * pageSize)
                     .setMaxResults(pageSize)
                     .getResultList();
        } finally {
            em.close();
        }
    }
    
    public long count() {
        EntityManager em = getEntityManager();
        try {
            return em.createQuery("SELECT COUNT(u) FROM User u", Long.class)
                     .getSingleResult();
        } finally {
            em.close();
        }
    }
}
```

### Practice 3: Use Named Queries

```java
@Entity
@Table(name = "users")
@NamedQueries({
    @NamedQuery(
        name = "User.findAll",
        query = "SELECT u FROM User u ORDER BY u.name"
    ),
    @NamedQuery(
        name = "User.findByEmail",
        query = "SELECT u FROM User u WHERE u.email = :email"
    ),
    @NamedQuery(
        name = "User.countAll",
        query = "SELECT COUNT(u) FROM User u"
    )
})
public class User {
    // Entity definition
}
```

```java
public class UserDAO extends GenericDAO<User, Long> {
    
    public List<User> findAll() {
        EntityManager em = getEntityManager();
        try {
            return em.createNamedQuery("User.findAll", User.class)
                     .getResultList();
        } finally {
            em.close();
        }
    }
}
```

### Practice 4: Handle Optimistic Locking

```java
@Entity
@Table(name = "users")
public class User {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Version
    private Long version;
    
    // Other fields
}
```

```java
public T update(T entity) {
    EntityManager em = getEntityManager();
    EntityTransaction tx = null;
    try {
        tx = em.getTransaction();
        tx.begin();
        
        T merged = em.merge(entity);
        
        tx.commit();
        return merged;
    } catch (OptimisticLockException e) {
        if (tx != null && tx.isActive()) {
            tx.rollback();
        }
        throw new RuntimeException("Entity was modified by another user");
    } catch (Exception e) {
        if (tx != null && tx.isActive()) {
            tx.rollback();
        }
        throw e;
    } finally {
        em.close();
    }
}
```

### Practice 5: Use Criteria API for Dynamic Queries

```java
public class UserDAO extends GenericDAO<User, Long> {
    
    public List<User> findByDynamicCriteria(String name, String email) {
        EntityManager em = getEntityManager();
        try {
            CriteriaBuilder cb = em.getCriteriaBuilder();
            CriteriaQuery<User> cq = cb.createQuery(User.class);
            Root<User> root = cq.from(User.class);
            
            List<Predicate> predicates = new ArrayList<>();
            
            if (name != null && !name.isEmpty()) {
                predicates.add(cb.like(root.get("name"), "%" + name + "%"));
            }
            
            if (email != null && !email.isEmpty()) {
                predicates.add(cb.equal(root.get("email"), email));
            }
            
            cq.where(predicates.toArray(new Predicate[0]));
            
            return em.createQuery(cq).getResultList();
        } finally {
            em.close();
        }
    }
}
```
