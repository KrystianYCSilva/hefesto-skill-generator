# ZK Framework + Spring Integration

Complete guide to integrating ZK Framework with Spring Framework and Spring Boot.

## Table of Contents

1. [Spring Configuration](#spring-configuration)
2. [Dependency Injection](#dependency-injection)
3. [Spring Security Integration](#spring-security-integration)
4. [Transaction Management](#transaction-management)
5. [Spring Boot Integration](#spring-boot-integration)
6. [Common Pitfalls](#common-pitfalls)

## Spring Configuration

### Maven Dependencies

```xml
<!-- ZK Spring Integration -->
<dependency>
    <groupId>org.zkoss.zk</groupId>
    <artifactId>zkspring-core</artifactId>
    <version>4.0.1</version>
</dependency>

<!-- Spring Framework -->
<dependency>
    <groupId>org.springframework</groupId>
    <artifactId>spring-web</artifactId>
    <version>5.3.30</version>
</dependency>

<dependency>
    <groupId>org.springframework</groupId>
    <artifactId>spring-context</artifactId>
    <version>5.3.30</version>
</dependency>
```

### Web.xml Configuration

```xml
<web-app>
    <!-- Spring Context Loader -->
    <listener>
        <listener-class>
            org.springframework.web.context.ContextLoaderListener
        </listener-class>
    </listener>
    
    <context-param>
        <param-name>contextConfigLocation</param-name>
        <param-value>
            /WEB-INF/applicationContext.xml
        </param-value>
    </context-param>
    
    <!-- ZK Spring Variable Resolver -->
    <listener>
        <listener-class>
            org.zkoss.zkplus.spring.DelegatingVariableResolver
        </listener-class>
    </listener>
    
    <!-- ZK Loader -->
    <servlet>
        <servlet-name>zkLoader</servlet-name>
        <servlet-class>org.zkoss.zk.ui.http.DHtmlLayoutServlet</servlet-class>
        <init-param>
            <param-name>update-uri</param-name>
            <param-value>/zkau</param-value>
        </init-param>
        <load-on-startup>1</load-on-startup>
    </servlet>
    
    <servlet-mapping>
        <servlet-name>zkLoader</servlet-name>
        <url-pattern>*.zul</url-pattern>
    </servlet-mapping>
</web-app>
```

### ApplicationContext.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:context="http://www.springframework.org/schema/context"
       xsi:schemaLocation="
           http://www.springframework.org/schema/beans
           http://www.springframework.org/schema/beans/spring-beans.xsd
           http://www.springframework.org/schema/context
           http://www.springframework.org/schema/context/spring-context.xsd">
    
    <!-- Enable component scanning -->
    <context:component-scan base-package="com.example" />
    
    <!-- Enable annotation-driven configuration -->
    <context:annotation-config />
    
    <!-- Spring bean definitions -->
    <bean id="userService" class="com.example.service.UserServiceImpl" />
    <bean id="productService" class="com.example.service.ProductServiceImpl" />
</beans>
```

## Dependency Injection

### Using @WireVariable in Composers

```java
package com.example.composer;

import org.zkoss.zk.ui.Component;
import org.zkoss.zk.ui.select.SelectorComposer;
import org.zkoss.zk.ui.select.annotation.Wire;
import org.zkoss.zk.ui.select.annotation.Listen;
import org.zkoss.zkplus.spring.DelegatingVariableResolver;
import org.zkoss.zul.*;
import com.example.service.UserService;

public class UserListComposer extends SelectorComposer<Component> {
    
    @Wire
    private Listbox userListbox;
    
    @WireVariable
    private UserService userService;
    
    @Override
    public void doAfterCompose(Component comp) throws Exception {
        super.doAfterCompose(comp);
        loadUsers();
    }
    
    private void loadUsers() {
        List<User> users = userService.findAll();
        ListModelList<User> model = new ListModelList<>(users);
        userListbox.setModel(model);
    }
    
    @Listen("onClick = #addButton")
    public void onAddUser() {
        User user = new User();
        userService.save(user);
        loadUsers();
    }
}
```

### ZUML with Spring Variable Resolver

```xml
<window title="User Management" 
        apply="com.example.composer.UserListComposer"
        viewModel="@id('vm') @init('com.example.viewmodel.UserVM')">
    
    <?variable-resolver class="org.zkoss.zkplus.spring.DelegatingVariableResolver"?>
    
    <listbox id="userListbox" rows="10">
        <listhead>
            <listheader label="ID" />
            <listheader label="Name" />
            <listheader label="Email" />
        </listhead>
        <template name="model">
            <listitem>
                <listcell label="@load(each.id)" />
                <listcell label="@load(each.name)" />
                <listcell label="@load(each.email)" />
            </listitem>
        </template>
    </listbox>
    
    <button id="addButton" label="Add User" />
</window>
```

### Using @WireVariable in ViewModels

```java
package com.example.viewmodel;

import org.zkoss.bind.annotation.*;
import org.zkoss.zk.ui.select.annotation.WireVariable;
import com.example.service.UserService;
import com.example.model.User;

public class UserVM {
    
    @WireVariable
    private UserService userService;
    
    private List<User> users;
    private User selectedUser;
    
    @Init
    public void init() {
        loadUsers();
    }
    
    @Command
    @NotifyChange("users")
    public void loadUsers() {
        users = userService.findAll();
    }
    
    @Command
    @NotifyChange({"users", "selectedUser"})
    public void saveUser() {
        if (selectedUser != null) {
            userService.save(selectedUser);
            selectedUser = new User();
            loadUsers();
        }
    }
    
    @Command
    @NotifyChange({"users", "selectedUser"})
    public void deleteUser(@BindingParam("user") User user) {
        userService.delete(user);
        selectedUser = null;
        loadUsers();
    }
    
    public List<User> getUsers() {
        return users;
    }
    
    public User getSelectedUser() {
        return selectedUser;
    }
    
    public void setSelectedUser(User selectedUser) {
        this.selectedUser = selectedUser;
    }
}
```

## Spring Security Integration

### Security Configuration

```java
package com.example.config;

import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.authentication.builders.AuthenticationManagerBuilder;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.annotation.web.configuration.WebSecurityConfigurerAdapter;

@Configuration
@EnableWebSecurity
public class SecurityConfig extends WebSecurityConfigurerAdapter {
    
    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http
            .csrf().disable()
            .authorizeRequests()
                .antMatchers("/zkau/**").permitAll()
                .antMatchers("/zkres/**").permitAll()
                .antMatchers("/login.zul").permitAll()
                .antMatchers("/admin/**").hasRole("ADMIN")
                .anyRequest().authenticated()
            .and()
            .formLogin()
                .loginPage("/login.zul")
                .defaultSuccessUrl("/index.zul")
                .failureUrl("/login.zul?error=true")
            .and()
            .logout()
                .logoutUrl("/logout")
                .logoutSuccessUrl("/login.zul");
    }
    
    @Override
    protected void configure(AuthenticationManagerBuilder auth) throws Exception {
        auth
            .inMemoryAuthentication()
                .withUser("admin").password("{noop}admin").roles("ADMIN")
                .and()
                .withUser("user").password("{noop}user").roles("USER");
    }
}
```

### Login ViewModel with Spring Security

```java
package com.example.viewmodel;

import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.zkoss.bind.annotation.*;
import org.zkoss.zk.ui.Executions;
import org.zkoss.zk.ui.select.annotation.WireVariable;
import org.zkoss.zul.Messagebox;

public class LoginVM {
    
    @WireVariable
    private AuthenticationManager authenticationManager;
    
    private String username;
    private String password;
    
    @Command
    public void login() {
        try {
            UsernamePasswordAuthenticationToken token = 
                new UsernamePasswordAuthenticationToken(username, password);
            
            Authentication auth = authenticationManager.authenticate(token);
            SecurityContextHolder.getContext().setAuthentication(auth);
            
            Executions.sendRedirect("/index.zul");
        } catch (Exception e) {
            Messagebox.show("Invalid credentials", "Error", 
                Messagebox.OK, Messagebox.ERROR);
        }
    }
    
    public String getUsername() {
        return username;
    }
    
    public void setUsername(String username) {
        this.username = username;
    }
    
    public String getPassword() {
        return password;
    }
    
    public void setPassword(String password) {
        this.password = password;
    }
}
```

### Accessing Security Context

```java
package com.example.util;

import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.core.userdetails.UserDetails;

public class SecurityUtil {
    
    public static String getCurrentUsername() {
        Authentication auth = SecurityContextHolder.getContext().getAuthentication();
        if (auth != null && auth.getPrincipal() instanceof UserDetails) {
            return ((UserDetails) auth.getPrincipal()).getUsername();
        }
        return null;
    }
    
    public static boolean hasRole(String role) {
        Authentication auth = SecurityContextHolder.getContext().getAuthentication();
        return auth != null && 
               auth.getAuthorities().stream()
                   .anyMatch(a -> a.getAuthority().equals("ROLE_" + role));
    }
    
    public static void logout() {
        SecurityContextHolder.clearContext();
    }
}
```

## Transaction Management

### Spring Transaction Configuration

```xml
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:tx="http://www.springframework.org/schema/tx"
       xsi:schemaLocation="
           http://www.springframework.org/schema/tx
           http://www.springframework.org/schema/tx/spring-tx.xsd">
    
    <!-- Enable transaction annotations -->
    <tx:annotation-driven transaction-manager="transactionManager"/>
    
    <!-- Transaction Manager -->
    <bean id="transactionManager" 
          class="org.springframework.orm.jpa.JpaTransactionManager">
        <property name="entityManagerFactory" ref="entityManagerFactory"/>
    </bean>
</beans>
```

### Service with Transactions

```java
package com.example.service;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.transaction.annotation.Propagation;
import com.example.repository.UserRepository;
import com.example.model.User;

@Service
@Transactional(readOnly = true)
public class UserServiceImpl implements UserService {
    
    private final UserRepository userRepository;
    
    public UserServiceImpl(UserRepository userRepository) {
        this.userRepository = userRepository;
    }
    
    @Override
    public List<User> findAll() {
        return userRepository.findAll();
    }
    
    @Override
    public User findById(Long id) {
        return userRepository.findById(id).orElse(null);
    }
    
    @Override
    @Transactional(readOnly = false, propagation = Propagation.REQUIRED)
    public void save(User user) {
        userRepository.save(user);
    }
    
    @Override
    @Transactional(readOnly = false, propagation = Propagation.REQUIRED)
    public void delete(User user) {
        userRepository.delete(user);
    }
    
    @Override
    @Transactional(readOnly = false, propagation = Propagation.REQUIRES_NEW)
    public void saveInNewTransaction(User user) {
        userRepository.save(user);
    }
}
```

## Spring Boot Integration

### Spring Boot Application

```java
package com.example;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.web.servlet.ServletComponentScan;

@SpringBootApplication
@ServletComponentScan
public class ZkSpringBootApplication {
    
    public static void main(String[] args) {
        SpringApplication.run(ZkSpringBootApplication.class, args);
    }
}
```

### ZK Servlet Configuration

```java
package com.example.config;

import org.springframework.boot.web.servlet.ServletRegistrationBean;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.zkoss.zk.ui.http.DHtmlLayoutServlet;

@Configuration
public class ZkConfiguration {
    
    @Bean
    public ServletRegistrationBean<DHtmlLayoutServlet> zkServlet() {
        ServletRegistrationBean<DHtmlLayoutServlet> registration = 
            new ServletRegistrationBean<>(new DHtmlLayoutServlet(), "*.zul");
        registration.setLoadOnStartup(1);
        registration.addInitParameter("update-uri", "/zkau");
        return registration;
    }
}
```

### Application Properties

```properties
# Server Configuration
server.port=8080
server.servlet.context-path=/

# ZK Configuration
zk.homepage=/index.zul
zk.richlet-mapping=/richlet/*

# Spring DataSource
spring.datasource.url=jdbc:mysql://localhost:3306/zkapp
spring.datasource.username=root
spring.datasource.password=password
spring.datasource.driver-class-name=com.mysql.cj.jdbc.Driver

# JPA Configuration
spring.jpa.hibernate.ddl-auto=update
spring.jpa.show-sql=true
spring.jpa.properties.hibernate.format_sql=true
```

### Spring Boot ViewModel

```java
package com.example.viewmodel;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import org.zkoss.bind.annotation.*;
import com.example.service.ProductService;
import com.example.model.Product;

@Component
public class ProductVM {
    
    @Autowired
    private ProductService productService;
    
    private List<Product> products;
    private Product selectedProduct = new Product();
    
    @Init
    public void init() {
        loadProducts();
    }
    
    @Command
    @NotifyChange("products")
    public void loadProducts() {
        products = productService.findAll();
    }
    
    @Command
    @NotifyChange({"products", "selectedProduct"})
    public void save() {
        productService.save(selectedProduct);
        selectedProduct = new Product();
        loadProducts();
    }
    
    public List<Product> getProducts() {
        return products;
    }
    
    public Product getSelectedProduct() {
        return selectedProduct;
    }
    
    public void setSelectedProduct(Product selectedProduct) {
        this.selectedProduct = selectedProduct;
    }
}
```

## Common Pitfalls

### Pitfall 1: Variable Resolver Not Declared

```xml
<!-- WRONG: No variable resolver -->
<window apply="com.example.MyComposer">
    <!-- @WireVariable will fail -->
</window>

<!-- CORRECT: Declare variable resolver -->
<window apply="com.example.MyComposer">
    <?variable-resolver class="org.zkoss.zkplus.spring.DelegatingVariableResolver"?>
</window>
```

### Pitfall 2: Bean Scope Issues

```java
// WRONG: Singleton bean with request-scoped data
@Service
public class UserService {
    private User currentUser; // Shared across all requests!
}

// CORRECT: Use proper scoping
@Service
public class UserService {
    public User getCurrentUser() {
        return SecurityUtil.getCurrentUser(); // Get from context
    }
}
```

### Pitfall 3: Transaction Boundaries

```java
// WRONG: Transaction not propagated
public class MyComposer extends SelectorComposer<Component> {
    
    @WireVariable
    private UserService userService;
    
    @Listen("onClick = #saveButton")
    public void onSave() {
        User user = new User();
        userService.save(user); // Transaction committed here
        user.setName("Changed"); // Change lost!
    }
}

// CORRECT: Keep changes within transaction
public class MyComposer extends SelectorComposer<Component> {
    
    @WireVariable
    private UserService userService;
    
    @Listen("onClick = #saveButton")
    public void onSave() {
        User user = new User();
        user.setName("Initial Name");
        userService.save(user); // All changes saved
    }
}
```

### Pitfall 4: Spring Context Not Available

```java
// WRONG: Trying to wire before context is ready
public class MyComposer extends SelectorComposer<Component> {
    
    @WireVariable
    private UserService userService;
    
    public MyComposer() {
        userService.doSomething(); // NPE - not wired yet!
    }
}

// CORRECT: Use doAfterCompose
public class MyComposer extends SelectorComposer<Component> {
    
    @WireVariable
    private UserService userService;
    
    @Override
    public void doAfterCompose(Component comp) throws Exception {
        super.doAfterCompose(comp);
        userService.doSomething(); // Now it's wired
    }
}
```

### Pitfall 5: Circular Dependencies

```java
// WRONG: Circular dependency
@Service
public class UserService {
    @Autowired
    private OrderService orderService;
}

@Service
public class OrderService {
    @Autowired
    private UserService userService; // Circular!
}

// CORRECT: Use setter injection or refactor
@Service
public class UserService {
    private OrderService orderService;
    
    @Autowired
    public void setOrderService(OrderService orderService) {
        this.orderService = orderService;
    }
}
```
