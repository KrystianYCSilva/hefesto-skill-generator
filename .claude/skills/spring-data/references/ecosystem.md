# Spring Data JPA Ecosystem & Libraries

Comprehensive toolkit for Spring Data JPA implementation.

## Core Spring Data Modules
- **spring-data-jpa**: Main module for JPA repositories and functionality
- **spring-data-commons**: Shared abstractions across Spring Data modules
- **spring-data-relational**: Support for relational databases (supersedes spring-data-jdbc)

## Repository Interfaces
- **Repository<T, ID>**: Base interface for all repositories
- **CrudRepository<T, ID>**: Provides basic CRUD operations
- **PagingAndSortingRepository<T, ID>**: Extends CrudRepository with pagination and sorting
- **JpaRepository<T, ID>**: Spring Data JPA specific interface with JPA-related features
- **JpaSpecificationExecutor<T>**: Support for Specifications and dynamic queries

## Query Methods Keywords
- **find...By, read...By, query...By, get...By**: Select queries
- **count...By**: Count queries
- **exists...By**: Boolean existence queries
- **delete...By, remove...By**: Delete queries
- **...Distinct...**: Distinct results

## Property Expressions
- **And, Or**: Logical operators
- **Between, LessThan, GreaterThan, Like, IsNull, IsNotNull, In, NotIn**: Comparison operators
- **OrderBy...Asc, OrderBy...Desc**: Sorting
- **IgnoreCase**: Case-insensitive matching

## JPA Implementation Libraries
- **Hibernate**: Default JPA implementation
- **EclipseLink**: Alternative JPA implementation
- **OpenJPA**: Apache's JPA implementation

## Database Drivers
- **PostgreSQL**: PostgreSQL JDBC driver
- **MySQL**: MySQL Connector/J
- **Oracle**: Oracle JDBC driver
- **H2**: In-memory database for testing
- **HSQLDB**: Another in-memory database option

## Connection Pooling
- **HikariCP**: High-performance JDBC connection pool (default in Spring Boot)
- **Tomcat JDBC Pool**: Connection pool from Apache Tomcat
- **C3P0**: Third-party connection pooling library

## Query Building Libraries
- **QueryDSL**: Typesafe query definition
- **JOOQ**: Typesafe SQL building
- **Criteria API**: JPA's built-in programmatic query building

## Testing Libraries
- **TestContainers**: Docker-based integration testing
- **H2 Database**: In-memory database for testing
- **Spring Data Jest**: Elasticsearch integration testing
- **DbUnit**: Database testing framework

## Performance & Monitoring
- **Micrometer**: Metrics collection
- **Spring Boot Actuator**: Production-ready features
- **Hibernate Statistics**: Built-in performance metrics
- **P6Spy**: JDBC statement logging and analysis