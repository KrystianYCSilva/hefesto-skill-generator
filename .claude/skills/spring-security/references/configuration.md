# Security Configuration Patterns in Spring Boot

Comprehensive guide to security configuration patterns and best practices.

## SecurityFilterChain Configuration Patterns

### Multi-Path Security Configuration
```java
@Configuration
@EnableWebSecurity
public class MultiPathSecurityConfig {
    
    @Bean
    @Order(1)
    public SecurityFilterChain apiFilterChain(HttpSecurity http) throws Exception {
        http
            .securityMatcher("/api/**")
            .sessionManagement(session -> session
                .sessionCreationPolicy(SessionCreationPolicy.STATELESS)
            )
            .csrf(csrf -> csrf.disable())
            .authorizeHttpRequests(authz -> authz
                .requestMatchers("/api/public/**").permitAll()
                .anyRequest().authenticated()
            )
            .oauth2ResourceServer(oauth2 -> oauth2.jwt(jwt -> jwt.jwtDecoder(jwtDecoder())));
        
        return http.build();
    }
    
    @Bean
    @Order(2)
    public SecurityFilterChain webFilterChain(HttpSecurity http) throws Exception {
        http
            .securityMatcher("/**")
            .authorizeHttpRequests(authz -> authz
                .requestMatchers("/public/**", "/css/**", "/js/**", "/images/**").permitAll()
                .requestMatchers("/admin/**").hasRole("ADMIN")
                .anyRequest().authenticated()
            )
            .formLogin(form -> form
                .loginPage("/login")
                .permitAll()
            )
            .logout(logout -> logout.permitAll());
        
        return http.build();
    }
    
    @Bean
    public JwtDecoder jwtDecoder() {
        return NimbusJwtDecoder
            .withJwkSetUri("https://your-auth-server/.well-known/jwks.json")
            .build();
    }
}
```

### Conditional Security Configuration
```java
@Configuration
@EnableWebSecurity
@ConditionalOnProperty(name = "app.security.enabled", havingValue = "true", matchIfMissing = true)
public class ConditionalSecurityConfig {
    
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .authorizeHttpRequests(authz -> authz
                .anyRequest().authenticated()
            );
        
        if (isDevelopment()) {
            http.csrf(csrf -> csrf.disable());
        } else {
            http.csrf(csrf -> csrf.enable());
        }
        
        return http.build();
    }
    
    private boolean isDevelopment() {
        return Arrays.asList(environment.getActiveProfiles()).contains("dev");
    }
    
    @Autowired
    private Environment environment;
}
```

## Authentication Configuration Patterns

### Custom Authentication Provider
```java
@Configuration
@EnableWebSecurity
public class CustomAuthProviderSecurityConfig {
    
    @Bean
    public DaoAuthenticationProvider authenticationProvider() {
        DaoAuthenticationProvider authProvider = new DaoAuthenticationProvider();
        authProvider.setUserDetailsService(userDetailsService());
        authProvider.setPasswordEncoder(passwordEncoder());
        return authProvider;
    }
    
    @Bean
    public AuthenticationManager authenticationManager(AuthenticationConfiguration config) throws Exception {
        AuthenticationManagerBuilder authBuilder = config.getAuthenticationManagerBuilder();
        authBuilder.authenticationProvider(authenticationProvider());
        return authBuilder.build();
    }
    
    @Bean
    public UserDetailsService userDetailsService() {
        return new CustomUserDetailsService();
    }
    
    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }
}
```

### LDAP Authentication Configuration
```java
@Configuration
@EnableWebSecurity
public class LdapSecurityConfig {
    
    @Bean
    public LdapAuthenticationProvider authenticationProvider() {
        LdapBindAuthenticationProvider authProvider = 
            new LdapBindAuthenticationProvider("ldap://ldap.example.com:389/dc=example,dc=com");
        authProvider.setUserDetailsContextMapper(userDetailsContextMapper());
        return authProvider;
    }
    
    @Bean
    public UserDetailsContextMapper userDetailsContextMapper() {
        return new PersonContextMapper();
    }
}
```

## Authorization Configuration Patterns

### Role-Based Access Control (RBAC)
```java
@Configuration
@EnableMethodSecurity(prePostEnabled = true)
public class RbacSecurityConfig {
    
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .authorizeHttpRequests(authz -> authz
                .requestMatchers("/admin/**").hasRole("ADMIN")
                .requestMatchers("/manager/**").hasRole("MANAGER")
                .requestMatchers("/user/**").hasRole("USER")
                .requestMatchers("/public/**").permitAll()
                .anyRequest().authenticated()
            );
        
        return http.build();
    }
}
```

### Attribute-Based Access Control (ABAC)
```java
@Configuration
@EnableMethodSecurity(prePostEnabled = true)
public class AbacSecurityConfig {
    
    @Bean
    public SecurityExpressionHandler<FilterInvocation> webExpressionHandler() {
        DefaultWebSecurityExpressionHandler defaultWebSecurityExpressionHandler = 
            new DefaultWebSecurityExpressionHandler();
        defaultWebSecurityExpressionHandler.setPermissionEvaluator(permissionEvaluator());
        return defaultWebSecurityExpressionHandler;
    }
    
    @Bean
    public PermissionEvaluator permissionEvaluator() {
        return new CustomPermissionEvaluator();
    }
    
    // Custom permission evaluator implementation
    public static class CustomPermissionEvaluator implements PermissionEvaluator {
        
        @Override
        public boolean hasPermission(Authentication authentication, Object targetDomainObject, Object permission) {
            // Custom permission logic based on user attributes and resource properties
            return checkPermission(authentication, targetDomainObject, permission);
        }
        
        @Override
        public boolean hasPermission(Authentication authentication, Serializable targetId, 
                                   String targetType, Object permission) {
            // Custom permission logic for object IDs
            return checkPermissionById(authentication, targetId, targetType, permission);
        }
        
        private boolean checkPermission(Authentication authentication, Object targetDomainObject, Object permission) {
            // Implementation logic
            return true;
        }
        
        private boolean checkPermissionById(Authentication authentication, Serializable targetId, 
                                         String targetType, Object permission) {
            // Implementation logic
            return true;
        }
    }
}
```

## Session Management Configuration

### Session Fixation Prevention
```java
@Configuration
@EnableWebSecurity
public class SessionManagementConfig {
    
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .sessionManagement(session -> session
                .sessionCreationPolicy(SessionCreationPolicy.IF_REQUIRED)
                .sessionFixation(sessionFixation -> sessionFixation.changeSessionId())
                .maximumSessions(1)
                .maxSessionsPreventsLogin(false)
            )
            .authorizeHttpRequests(authz -> authz
                .anyRequest().authenticated()
            );
        
        return http.build();
    }
}
```

### Stateless Session Configuration
```java
@Configuration
@EnableWebSecurity
public class StatelessSessionConfig {
    
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .sessionManagement(session -> session
                .sessionCreationPolicy(SessionCreationPolicy.STATELESS)
            )
            .authorizeHttpRequests(authz -> authz
                .anyRequest().authenticated()
            );
        
        return http.build();
    }
}
```

## CORS Configuration Patterns

### Production-Ready CORS Configuration
```java
@Configuration
@EnableWebSecurity
public class ProductionCorsConfig {
    
    @Bean
    public CorsConfigurationSource corsConfigurationSource() {
        CorsConfiguration configuration = new CorsConfiguration();
        
        // Specific allowed origins (not wildcard!)
        configuration.setAllowedOriginPatterns(Arrays.asList(
            "https://app.yourcompany.com",
            "https://admin.yourcompany.com"
        ));
        
        configuration.setAllowedMethods(Arrays.asList(
            HttpMethod.GET.name(),
            HttpMethod.POST.name(),
            HttpMethod.PUT.name(),
            HttpMethod.DELETE.name(),
            HttpMethod.HEAD.name(),
            HttpMethod.OPTIONS.name()
        ));
        
        configuration.setAllowedHeaders(Arrays.asList(
            "Authorization",
            "Cache-Control",
            "Content-Type",
            "X-Requested-With"
        ));
        
        configuration.setAllowCredentials(true);
        configuration.setMaxAge(3600L); // 1 hour
        
        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        source.registerCorsConfiguration("/**", configuration);
        return source;
    }
    
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .cors(cors -> cors.configurationSource(corsConfigurationSource()))
            .authorizeHttpRequests(authz -> authz
                .anyRequest().authenticated()
            );
        
        return http.build();
    }
}
```

## Security Headers Configuration

### Security Headers for Web Applications
```java
@Configuration
@EnableWebSecurity
public class SecurityHeadersConfig {
    
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .headers(headers -> headers
                .frameOptions(frameOptions -> frameOptions.sameOrigin())
                .contentTypeOptions(contentType -> contentType.and())
                .xssProtection(xss -> xss.and())
                .httpStrictTransportSecurity(hsts -> hsts
                    .maxAgeInSeconds(31536000)
                    .includeSubdomains(true)
                )
            )
            .authorizeHttpRequests(authz -> authz
                .anyRequest().authenticated()
            );
        
        return http.build();
    }
}
```

## Best Practices

### Configuration Organization
- Separate security configurations for different application layers
- Use @Order annotation to control filter chain execution order
- Externalize security properties using configuration properties
- Use profiles to differentiate security configurations across environments

### Security Testing
- Test both positive and negative security scenarios
- Verify that unauthorized access is properly blocked
- Test authentication and authorization flows thoroughly
- Include security tests in CI/CD pipelines

### Performance Considerations
- Minimize the number of security filters in the chain
- Cache authentication and authorization decisions when appropriate
- Use efficient data structures for role and permission checks
- Monitor security-related performance metrics