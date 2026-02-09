# JPA Mapping Strategies

Comprehensive guide to JPA entity mapping strategies and best practices.

## Entity Mapping Fundamentals

### Basic Entity Mapping
```java
@Entity
@Table(name = "users")
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(name = "username", nullable = false, unique = true, length = 50)
    private String username;
    
    @Column(name = "email", nullable = false, length = 100)
    private String email;
    
    @Column(name = "created_at", nullable = false, updatable = false)
    private LocalDateTime createdAt;
    
    @Column(name = "updated_at")
    private LocalDateTime updatedAt;
    
    // Constructors, getters, setters
}
```

### Composite Primary Keys
```java
// Using @EmbeddedId
@Embeddable
public class UserRoleKey implements Serializable {
    @Column(name = "user_id")
    private Long userId;
    
    @Column(name = "role_id")
    private Long roleId;
    
    // Constructors, equals, hashCode
}

@Entity
@Table(name = "user_roles")
public class UserRole {
    @EmbeddedId
    private UserRoleKey id;
    
    @ManyToOne
    @MapsId("userId") // Maps to userId in UserRoleKey
    @JoinColumn(name = "user_id")
    private User user;
    
    @ManyToOne
    @MapsId("roleId") // Maps to roleId in UserRoleKey
    @JoinColumn(name = "role_id")
    private Role role;
    
    @Column(name = "assigned_at")
    private LocalDateTime assignedAt;
    
    // Constructors, getters, setters
}

// Using @IdClass
@IdClass(OrderItemKey.class)
@Entity
@Table(name = "order_items")
public class OrderItem {
    @Id
    @Column(name = "order_id")
    private Long orderId;
    
    @Id
    @Column(name = "product_id")
    private Long productId;
    
    @ManyToOne
    @JoinColumn(name = "order_id", insertable = false, updatable = false)
    private Order order;
    
    @ManyToOne
    @JoinColumn(name = "product_id", insertable = false, updatable = false)
    private Product product;
    
    @Column(name = "quantity")
    private Integer quantity;
    
    // Constructors, getters, setters
}

public class OrderItemKey implements Serializable {
    private Long orderId;
    private Long productId;
    
    // Constructors, equals, hashCode
}
```

## Inheritance Strategies

### Single Table Strategy (Default)
```java
@Entity
@Inheritance(strategy = InheritanceType.SINGLE_TABLE)
@DiscriminatorColumn(name = "employee_type", discriminatorType = DiscriminatorType.STRING)
public abstract class Employee {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    private String name;
    private String email;
    
    // Common fields and methods
}

@Entity
@DiscriminatorValue("FT")
public class FullTimeEmployee extends Employee {
    private BigDecimal salary;
    private BigDecimal annualBonus;
    
    // Full-time specific fields and methods
}

@Entity
@DiscriminatorValue("PT")
public class PartTimeEmployee extends Employee {
    private BigDecimal hourlyRate;
    private Integer hoursPerWeek;
    
    // Part-time specific fields and methods
}
```

### Table Per Class Strategy
```java
@Entity
@Inheritance(strategy = InheritanceType.TABLE_PER_CLASS)
public abstract class Vehicle {
    @Id
    @GeneratedValue(strategy = GenerationType.TABLE) // Must use TABLE strategy
    private Long id;
    
    private String brand;
    private String model;
    
    // Common fields and methods
}

@Entity
public class Car extends Vehicle {
    private Integer numberOfDoors;
    private String fuelType;
    
    // Car specific fields and methods
}

@Entity
public class Motorcycle extends Vehicle {
    private Boolean hasSidecar;
    private String engineCapacity;
    
    // Motorcycle specific fields and methods
}
```

### Joined Strategy
```java
@Entity
@Inheritance(strategy = InheritanceType.JOINED)
public abstract class Animal {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    private String name;
    private Integer age;
    
    // Common fields and methods
}

@Entity
@Table(name = "dogs")
public class Dog extends Animal {
    private String breed;
    private Boolean isTrained;
    
    // Dog specific fields and methods
}

@Entity
@Table(name = "cats")
public class Cat extends Animal {
    private String furColor;
    private Boolean isIndoor;
    
    // Cat specific fields and methods
}
```

## Advanced Mapping Techniques

### Embeddable Objects
```java
@Embeddable
public class Address {
    @Column(name = "street")
    private String street;
    
    @Column(name = "city")
    private String city;
    
    @Column(name = "state")
    private String state;
    
    @Column(name = "zip_code")
    private String zipCode;
    
    @Enumerated(EnumType.STRING)
    @Column(name = "country")
    private Country country;
    
    // Constructors, getters, setters
}

@Entity
@Table(name = "employees")
public class Employee {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    private String name;
    
    @Embedded
    @AttributeOverrides({
        @AttributeOverride(name = "street", column = @Column(name = "home_street")),
        @AttributeOverride(name = "city", column = @Column(name = "home_city")),
        @AttributeOverride(name = "state", column = @Column(name = "home_state")),
        @AttributeOverride(name = "zipCode", column = @Column(name = "home_zip_code"))
    })
    private Address homeAddress;
    
    @Embedded
    private Address workAddress; // Uses default column names
    
    // Constructors, getters, setters
}
```

### Element Collections
```java
@Entity
@Table(name = "users")
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    private String username;
    
    // Store as JSON in a single column
    @ElementCollection
    @CollectionTable(name = "user_phones", joinColumns = @JoinColumn(name = "user_id"))
    @Column(name = "phone_number")
    private List<String> phoneNumbers = new ArrayList<>();
    
    // Store as separate columns with additional attributes
    @ElementCollection
    @CollectionTable(name = "user_skills", joinColumns = @JoinColumn(name = "user_id"))
    @MapKeyColumn(name = "skill_name")
    @Column(name = "proficiency_level")
    @Enumerated(EnumType.STRING)
    private Map<String, ProficiencyLevel> skills = new HashMap<>();
    
    // Custom embeddable element
    @ElementCollection
    @CollectionTable(name = "user_hobbies", joinColumns = @JoinColumn(name = "user_id"))
    private Set<Hobby> hobbies = new HashSet<>();
    
    // Constructors, getters, setters
}

@Embeddable
public class Hobby {
    private String name;
    private Integer yearsOfExperience;
    
    // Constructors, getters, setters, equals, hashCode
}

public enum ProficiencyLevel {
    BEGINNER, INTERMEDIATE, ADVANCED, EXPERT
}
```

### Value Conversions
```java
@Entity
@Table(name = "products")
public class Product {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    private String name;
    
    // Convert BigDecimal to/from database representation
    @Convert(converter = MoneyAttributeConverter.class)
    private Money price;
    
    // Convert enum to string with custom converter
    @Convert(converter = StatusConverter.class)
    private ProductStatus status;
    
    // Constructors, getters, setters
}

@Converter(autoApply = true)
public class MoneyAttributeConverter implements AttributeConverter<Money, String> {
    
    @Override
    public String convertToDatabaseColumn(Money money) {
        return money != null ? money.getAmount().toString() : null;
    }
    
    @Override
    public Money convertToEntityAttribute(String dbData) {
        return dbData != null ? new Money(new BigDecimal(dbData)) : null;
    }
}

@Converter
public class StatusConverter implements AttributeConverter<ProductStatus, String> {
    
    @Override
    public String convertToDatabaseColumn(ProductStatus status) {
        return status != null ? status.getCode() : null;
    }
    
    @Override
    public ProductStatus convertToEntityAttribute(String dbData) {
        return dbData != null ? ProductStatus.fromCode(dbData) : null;
    }
}
```

## Relationship Mapping Strategies

### Bidirectional Relationships with Proper Equals/HashCode
```java
@Entity
@Table(name = "authors")
public class Author {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    private String name;
    
    @OneToMany(mappedBy = "author", cascade = CascadeType.ALL, 
               fetch = FetchType.LAZY, orphanRemoval = true)
    private List<Book> books = new ArrayList<>();
    
    // Helper methods to maintain bidirectional relationship
    public void addBook(Book book) {
        books.add(book);
        book.setAuthor(this);
    }
    
    public void removeBook(Book book) {
        books.remove(book);
        book.setAuthor(null);
    }
    
    // Proper equals/hashCode implementation
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Author)) return false;
        Author author = (Author) o;
        return Objects.equals(id, author.id);
    }
    
    @Override
    public int hashCode() {
        return getClass().hashCode();
    }
    
    // Constructors, getters, setters
}

@Entity
@Table(name = "books")
public class Book {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    private String title;
    private String isbn;
    
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "author_id")
    private Author author;
    
    // Proper equals/hashCode implementation
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Book)) return false;
        Book book = (Book) o;
        return Objects.equals(id, book.id);
    }
    
    @Override
    public int hashCode() {
        return getClass().hashCode();
    }
    
    // Constructors, getters, setters
}
```

## Best Practices

### Performance Considerations
- Use `@BatchSize` to optimize lazy loading
- Consider `@Fetch(FetchMode.SUBSELECT)` for collections
- Use `@Formula` for computed properties
- Implement proper indexing strategies

### Design Patterns
- Use DTOs/projections for read operations
- Apply the Repository pattern consistently
- Use Specification pattern for dynamic queries
- Implement proper auditing with `@CreatedDate`, `@LastModifiedDate`

### Common Pitfalls to Avoid
- Don't use `EAGER` fetch type unnecessarily
- Avoid circular dependencies in entity relationships
- Don't modify collections directly without helper methods
- Be careful with `equals`/`hashCode` implementations when using JPA proxies