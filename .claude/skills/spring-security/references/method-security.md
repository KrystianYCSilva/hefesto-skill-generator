# Method Security Deep Dive

Comprehensive guide to implementing method-level security in Spring applications.

## Method Security Fundamentals

Method security in Spring Security provides authorization at the method level, allowing fine-grained control over which methods can be invoked by which principals.

### Enabling Method Security
```java
@Configuration
@EnableMethodSecurity(
    prePostEnabled = true,     // Enable @PreAuthorize and @PostAuthorize
    securedEnabled = true,     // Enable @Secured
    jsr250Enabled = true       // Enable JSR-250 annotations like @RolesAllowed
)
public class MethodSecurityConfig {
    // Configuration for method-level security
}
```

## @PreAuthorize and @PostAuthorize

### @PreAuthorize - Pre-invocation Authorization

@PreAuthorize evaluates expressions before the method is executed.

```java
@Service
public class UserService {
    
    // Only the user themselves or an admin can access their profile
    @PreAuthorize("#username == authentication.principal.username or hasRole('ROLE_ADMIN')")
    public UserProfile getUserProfile(String username) {
        return userProfileRepository.findByUsername(username);
    }
    
    // Only users with ROLE_ADMIN can access
    @PreAuthorize("hasRole('ROLE_ADMIN')")
    public List<User> getAllUsers() {
        return userRepository.findAll();
    }
    
    // Only the user themselves, an admin, or a manager of the same department can view
    @PreAuthorize("#userId == authentication.principal.id or hasRole('ROLE_ADMIN') or " +
                  "@departmentService.isUserManagerOfDepartment(authentication.principal.id, #userId)")
    public User getUserById(Long userId) {
        return userRepository.findById(userId)
            .orElseThrow(() -> new UserNotFoundException("User not found: " + userId));
    }
    
    // Complex expression with custom method evaluation
    @PreAuthorize("@permissionEvaluator.hasPermission(authentication.principal, #documentId, 'read')")
    public Document getDocument(Long documentId) {
        return documentRepository.findById(documentId)
            .orElseThrow(() -> new DocumentNotFoundException("Document not found: " + documentId));
    }
    
    // Using SpEL with method parameters
    @PreAuthorize("hasRole('ROLE_PREMIUM') or #amount <= 1000")
    public Transaction processTransaction(BigDecimal amount, String currency) {
        // Process transaction logic
        return transactionService.createTransaction(amount, currency);
    }
}
```

### @PostAuthorize - Post-invocation Authorization

@PostAuthorize evaluates expressions after the method executes but before the result is returned.

```java
@Service
public class DocumentService {
    
    // Allow access to document only if user is owner or admin
    // Check happens after method execution
    @PostAuthorize("returnObject.owner == authentication.principal.username or hasRole('ROLE_ADMIN')")
    public Document getDocument(Long documentId) {
        return documentRepository.findById(documentId)
            .orElseThrow(() -> new DocumentNotFoundException("Document not found"));
    }
    
    // Filter results based on user permissions
    @PostAuthorize("hasRole('ROLE_ADMIN') or returnObject.owner == authentication.principal.username")
    public List<Document> getUserDocuments(String username) {
        return documentRepository.findByOwner(username);
    }
    
    // Post-filter collection results
    @PostFilter("filterObject.owner == authentication.principal.username or hasRole('ROLE_ADMIN')")
    public List<Document> getAllDocuments() {
        return documentRepository.findAll();
    }
}
```

## @PreFilter and @PostFilter

### @PreFilter - Pre-invocation Collection Filtering

@PreFilter filters method arguments before the method executes.

```java
@Service
public class DocumentManagementService {
    
    // Filter the documents list to only include documents owned by the current user
    @PreFilter("filterObject.owner == authentication.principal.username")
    public void updateDocuments(List<Document> documents) {
        for (Document doc : documents) {
            documentRepository.save(doc);
        }
    }
    
    // Filter based on multiple conditions
    @PreFilter(value = "filterObject.owner == authentication.principal.username or hasRole('ROLE_ADMIN')", 
               filterTarget = "documents")
    public void processDocuments(List<Document> documents) {
        // Process only documents that passed the filter
        documents.forEach(this::processDocument);
    }
    
    private void processDocument(Document document) {
        // Processing logic
    }
}
```

### @PostFilter - Post-invocation Collection Filtering

@PostFilter filters the method result after execution.

```java
@Service
public class SearchService {
    
    // Filter search results to only include documents accessible to the user
    @PostFilter("filterObject.owner == authentication.principal.username or " +
                "filterObject.visibility == 'PUBLIC' or " +
                "hasRole('ROLE_ADMIN')")
    public List<Document> searchDocuments(String query) {
        List<Document> results = documentRepository.search(query);
        return results;
    }
    
    // Filter based on custom permission evaluator
    @PostFilter("@permissionEvaluator.hasPermission(authentication.principal, filterObject, 'read')")
    public List<Document> getAccessibleDocuments() {
        return documentRepository.findAll();
    }
}
```

## @Secured Annotation

@Secured is simpler than @PreAuthorize but less flexible.

```java
@Service
public class AdminService {
    
    // Only users with ROLE_ADMIN can access
    @Secured("ROLE_ADMIN")
    public void performAdminTask() {
        // Administrative task logic
    }
    
    // Multiple roles allowed
    @Secured({"ROLE_ADMIN", "ROLE_SUPERVISOR"})
    public void performSupervisoryTask() {
        // Supervisory task logic
    }
    
    // Deny access to all (typically overridden by other security mechanisms)
    @Secured("ROLE_DUMMY") // Role that nobody has
    public void restrictedMethod() {
        // This method is effectively denied to all users
    }
}
```

## JSR-250 Annotations

JSR-250 annotations provide standard Java EE security annotations.

```java
@Service
public class AccountService {
    
    @RolesAllowed("ROLE_USER")
    public Account getAccount(Long accountId) {
        return accountRepository.findById(accountId)
            .orElseThrow(() -> new AccountNotFoundException("Account not found"));
    }
    
    @RolesAllowed({"ROLE_USER", "ROLE_ADMIN"})
    public void updateAccount(Account account) {
        accountRepository.save(account);
    }
    
    @PermitAll
    public void publicMethod() {
        // Accessible to all users (authenticated or not)
    }
    
    @DenyAll
    public void denyAllMethod() {
        // Denied to all users
        // This is typically overridden by other security mechanisms
    }
    
    @RunAs("ROLE_ADMIN")
    public void runAsAdmin() {
        // This method runs with ROLE_ADMIN privileges
    }
}
```

## Custom Permission Evaluators

### Implementing Custom PermissionEvaluator

```java
@Component
public class CustomPermissionEvaluator implements PermissionEvaluator {
    
    @Override
    public boolean hasPermission(Authentication authentication, Object targetDomainObject, Object permission) {
        if (targetDomainObject instanceof Document) {
            return hasDocumentPermission(authentication, (Document) targetDomainObject, (String) permission);
        } else if (targetDomainObject instanceof User) {
            return hasUserPermission(authentication, (User) targetDomainObject, (String) permission);
        }
        return false;
    }
    
    @Override
    public boolean hasPermission(Authentication authentication, Serializable targetId, String targetType, Object permission) {
        if ("Document".equals(targetType)) {
            Document document = documentRepository.findById((Long) targetId)
                .orElse(null);
            if (document != null) {
                return hasDocumentPermission(authentication, document, (String) permission);
            }
        }
        return false;
    }
    
    private boolean hasDocumentPermission(Authentication authentication, Document document, String permission) {
        String username = authentication.getName();
        
        switch (permission) {
            case "read":
                return document.isPublic() || 
                       document.getOwner().equals(username) || 
                       hasRole(authentication, "ROLE_ADMIN");
            case "write":
                return document.getOwner().equals(username) || 
                       hasRole(authentication, "ROLE_ADMIN");
            case "delete":
                return document.getOwner().equals(username) || 
                       hasRole(authentication, "ROLE_ADMIN");
            default:
                return false;
        }
    }
    
    private boolean hasUserPermission(Authentication authentication, User user, String permission) {
        String authenticatedUsername = authentication.getName();
        
        switch (permission) {
            case "view":
                return user.getUsername().equals(authenticatedUsername) || 
                       hasRole(authentication, "ROLE_ADMIN");
            case "modify":
                return user.getUsername().equals(authenticatedUsername) || 
                       hasRole(authentication, "ROLE_ADMIN");
            default:
                return false;
        }
    }
    
    private boolean hasRole(Authentication authentication, String roleName) {
        return authentication.getAuthorities().stream()
            .anyMatch(grantedAuthority -> grantedAuthority.getAuthority().equals(roleName));
    }
}
```

### Using Custom Permission Evaluator in Expressions

```java
@Service
public class BusinessService {
    
    // Using custom permission evaluator in @PreAuthorize
    @PreAuthorize("@permissionEvaluator.hasPermission(authentication.principal, #document, 'write')")
    public void updateDocument(Document document) {
        documentRepository.save(document);
    }
    
    // Using custom service method in expression
    @PreAuthorize("@departmentService.isUserInSameDepartment(authentication.principal.username, #username)")
    public UserProfile getUserProfile(String username) {
        return userProfileRepository.findByUsername(username);
    }
    
    // Complex expression combining multiple custom methods
    @PreAuthorize("@permissionEvaluator.hasPermission(authentication.principal, #docId, 'Document', 'read') " +
                  "and @quotaService.hasRemainingQuota(authentication.principal.username)")
    public Document getDocument(Long docId) {
        return documentRepository.findById(docId)
            .orElseThrow(() -> new DocumentNotFoundException("Document not found"));
    }
}
```

## Aspect-Oriented Security Implementation

### Custom Security Aspect

```java
@Aspect
@Component
public class SecurityAspect {
    
    @Around("@annotation(RequiresPrivilege)")
    public Object checkPrivilege(ProceedingJoinPoint joinPoint) throws Throwable {
        MethodSignature signature = (MethodSignature) joinPoint.getSignature();
        RequiresPrivilege annotation = signature.getMethod().getAnnotation(RequiresPrivilege.class);
        
        Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
        
        if (authentication == null || !authentication.isAuthenticated()) {
            throw new AccessDeniedException("User not authenticated");
        }
        
        String requiredPrivilege = annotation.value();
        boolean hasPrivilege = authentication.getAuthorities().stream()
            .anyMatch(auth -> auth.getAuthority().equals("PRIVILEGE_" + requiredPrivilege));
        
        if (!hasPrivilege) {
            throw new AccessDeniedException("User lacks required privilege: " + requiredPrivilege);
        }
        
        return joinPoint.proceed();
    }
}

// Custom annotation
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
public @interface RequiresPrivilege {
    String value();
}
```

### Using Custom Security Annotation

```java
@Service
public class PrivilegedService {
    
    @RequiresPrivilege("DATA_EXPORT")
    public List<DataRecord> exportData() {
        // Export logic that requires DATA_EXPORT privilege
        return dataRepository.findAll();
    }
    
    @RequiresPrivilege("SYSTEM_CONFIG")
    public void updateSystemConfiguration(ConfigUpdateRequest request) {
        // Configuration update logic that requires SYSTEM_CONFIG privilege
        configService.updateConfiguration(request);
    }
}
```

## Method Security with Reactive Programming

### Security in Reactive Streams

```java
@Service
public class ReactiveUserService {
    
    // Using method security with Project Reactor
    @PreAuthorize("hasRole('ROLE_ADMIN')")
    public Mono<User> getUserById(Long userId) {
        return userRepository.findById(userId);
    }
    
    @PreAuthorize("#userId == authentication.principal.id or hasRole('ROLE_ADMIN')")
    public Flux<UserActivity> getUserActivities(Long userId) {
        return activityRepository.findByUserId(userId);
    }
    
    // Using reactive security context
    public Mono<UserProfile> getCurrentUserProfile() {
        return ReactiveSecurityContextHolder.getContext()
            .map(securityContext -> securityContext.getAuthentication().getName())
            .flatMap(username -> userProfileRepository.findByUsername(username));
    }
}
```

## Testing Method Security

### Testing with @WithMockUser

```java
@SpringBootTest
@TestPropertySource(properties = {"spring.security.oauth2.resourceserver.jwt.issuer-uri="})
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
class MethodSecurityTests {
    
    @Autowired
    private UserService userService;
    
    @Test
    @WithMockUser(username = "testuser", roles = {"USER"})
    void shouldAllowUserToAccessOwnProfile() {
        // Given
        String username = "testuser";
        
        // When
        UserProfile profile = userService.getUserProfile(username);
        
        // Then
        assertThat(profile).isNotNull();
        assertThat(profile.getUsername()).isEqualTo(username);
    }
    
    @Test
    @WithMockUser(username = "admin", roles = {"ADMIN"})
    void shouldAllowAdminToAccessAnyProfile() {
        // Given
        String targetUsername = "otheruser";
        
        // When
        UserProfile profile = userService.getUserProfile(targetUsername);
        
        // Then
        assertThat(profile).isNotNull();
        assertThat(profile.getUsername()).isEqualTo(targetUsername);
    }
    
    @Test
    @WithMockUser(username = "testuser", roles = {"USER"})
    @DisplayName("Should deny user access to other user's profile")
    void shouldDenyUserAccessToOtherProfile() {
        // Given
        String otherUsername = "otheruser";
        
        // When & Then
        assertThatThrownBy(() -> userService.getUserProfile(otherUsername))
            .isInstanceOf(AccessDeniedException.class);
    }
}
```

### Testing with Different Security Contexts

```java
@ExtendWith(SpringExtension.class)
@ContextConfiguration(classes = {SecurityConfig.class, MethodSecurityConfig.class})
class AdvancedMethodSecurityTests {
    
    @RegisterExtension
    static SpringMockTestContext spring = new SpringMockTestContext();
    
    @MockBean
    private UserRepository userRepository;
    
    @Autowired
    private UserService userService;
    
    @Test
    void shouldApplyMethodSecurityWithCustomExpression() {
        // Given
        Authentication auth = new TestingAuthenticationToken("testuser", "password", "ROLE_USER");
        SecurityContext securityContext = SecurityContextHolder.createEmptyContext();
        securityContext.setAuthentication(auth);
        SecurityContextHolder.setContext(securityContext);
        
        // And
        User mockUser = new User("testuser", "Test User");
        when(userRepository.findByUsername("testuser")).thenReturn(mockUser);
        
        // When
        User result = userService.getUserById("testuser");
        
        // Then
        assertThat(result).isEqualTo(mockUser);
    }
}
```

## Performance Considerations

### Caching Security Decisions

```java
@Service
public class CachedSecurityService {
    
    @Cacheable(value = "permissions", key = "#authentication.name + '_' + #targetId + '_' + #permission")
    public boolean checkPermission(Authentication authentication, Long targetId, String permission) {
        // Expensive permission checking logic
        return performExpensivePermissionCheck(authentication, targetId, permission);
    }
    
    @PreAuthorize("@cachedSecurityService.checkPermission(authentication, #documentId, 'read')")
    public Document getDocument(Long documentId) {
        return documentRepository.findById(documentId).orElse(null);
    }
    
    private boolean performExpensivePermissionCheck(Authentication authentication, Long targetId, String permission) {
        // Complex permission logic
        return true; // Simplified for example
    }
}
```

## Best Practices

### Security Expression Functions

Create custom security expression functions:

```java
@Component("securityUtils")
public class SecurityExpressionFunctions {
    
    public boolean isOwner(Authentication authentication, String owner) {
        return authentication.getName().equals(owner);
    }
    
    public boolean isInRole(Authentication authentication, String role) {
        return authentication.getAuthorities().stream()
            .anyMatch(auth -> auth.getAuthority().equals("ROLE_" + role));
    }
    
    public boolean hasPermission(Authentication authentication, String resource, String action) {
        // Custom permission logic
        return true; // Simplified
    }
}

// Usage in @PreAuthorize
@Service
public class ResourceService {
    
    @PreAuthorize("@securityUtils.isOwner(authentication, #resource.owner) or " +
                  "@securityUtils.isInRole(authentication, 'ADMIN')")
    public void updateResource(Resource resource) {
        // Update logic
    }
}
```

### Security Documentation

Document security constraints clearly:

```java
/**
 * Updates a user profile.
 * 
 * Security: Only the user themselves or an administrator can update a profile.
 * The authenticated user must have either:
 * - ROLE_USER and be the owner of the profile, OR
 * - ROLE_ADMIN for administrative access
 */
@PreAuthorize("#profile.username == authentication.principal.username or hasRole('ROLE_ADMIN')")
public UserProfile updateProfile(UserProfile profile) {
    return userProfileRepository.save(profile);
}
```

### Common Pitfalls to Avoid

1. **Overly Complex Expressions**: Keep security expressions readable and maintainable
2. **Missing Security Annotations**: Ensure all sensitive methods are properly secured
3. **Insufficient Testing**: Test both positive and negative security scenarios
4. **Performance Issues**: Be mindful of expensive operations in security expressions
5. **Inconsistent Security**: Apply security patterns consistently across the application