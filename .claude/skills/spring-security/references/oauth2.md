# OAuth2 & OpenID Connect Integration Guide

Comprehensive guide to implementing OAuth2 and OpenID Connect in Spring Boot applications.

## OAuth2 Fundamentals

OAuth2 is an authorization framework that enables applications to obtain limited access to user accounts on an HTTP service.

### OAuth2 Roles:
- **Resource Owner**: The user who authorizes access to their resources
- **Client**: The application requesting access to the user's resources
- **Resource Server**: The server hosting the user's protected resources
- **Authorization Server**: The server that authenticates the resource owner and issues access tokens

### OAuth2 Grant Types:
- **Authorization Code**: For web applications with server-side components
- **Implicit**: For browser-based or mobile applications (deprecated)
- **Resource Owner Password Credentials**: For trusted applications
- **Client Credentials**: For application-only authentication

## OAuth2 Client Configuration

### Basic OAuth2 Client Setup
```yaml
spring:
  security:
    oauth2:
      client:
        registration:
          google:
            client-id: ${GOOGLE_CLIENT_ID}
            client-secret: ${GOOGLE_CLIENT_SECRET}
            scope: openid, profile, email
            redirect-uri: "{baseUrl}/login/oauth2/code/{registrationId}"
          github:
            client-id: ${GITHUB_CLIENT_ID}
            client-secret: ${GITHUB_CLIENT_SECRET}
            scope: read:user, user:email
            redirect-uri: "{baseUrl}/login/oauth2/code/{registrationId}"
          facebook:
            client-id: ${FACEBOOK_CLIENT_ID}
            client-secret: ${FACEBOOK_CLIENT_SECRET}
            scope: email, public_profile
            redirect-uri: "{baseUrl}/login/oauth2/code/{registrationId}"
        provider:
          github:
            authorization-uri: https://github.com/login/oauth/authorize
            token-uri: https://github.com/login/oauth/access_token
            user-info-uri: https://api.github.com/user
            user-name-attribute: login
          facebook:
            authorization-uri: https://www.facebook.com/v13.0/dialog/oauth
            token-uri: https://graph.facebook.com/v13.0/oauth/access_token
            user-info-uri: https://graph.facebook.com/v13.0/me?fields=id,name,email
            user-name-attribute: id
```

### Custom OAuth2 Client Configuration
```java
@Configuration
@EnableWebSecurity
public class OAuth2ClientConfig {
    
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .authorizeHttpRequests(authz -> authz
                .requestMatchers("/", "/error", "/webjars/**").permitAll()
                .anyRequest().authenticated()
            )
            .oauth2Login(oauth2 -> oauth2
                .defaultSuccessUrl("/dashboard", true)
                .failureUrl("/login?error=true")
                .authorizationEndpoint(endpoint -> endpoint
                    .baseUri("/oauth2/authorize")
                    .authorizationRequestRepository(cookieAuthorizationRequestRepository())
                )
                .redirectionEndpoint(endpoint -> endpoint
                    .baseUri("/oauth2/callback/*")
                )
                .userInfoEndpoint(endpoint -> endpoint
                    .userService(customOAuth2UserService())
                )
                .successHandler(customAuthenticationSuccessHandler())
                .failureHandler(customAuthenticationFailureHandler())
            );
        
        return http.build();
    }
    
    @Bean
    public CookieAuthorizationRequestRepository<OAuth2AuthorizationRequest> 
           cookieAuthorizationRequestRepository() {
        return new CookieAuthorizationRequestRepository<>();
    }
    
    @Bean
    public OAuth2UserService<OAuth2UserRequest, OAuth2User> customOAuth2UserService() {
        return new CustomOAuth2UserService();
    }
    
    @Bean
    public AuthenticationSuccessHandler customAuthenticationSuccessHandler() {
        return new CustomAuthenticationSuccessHandler();
    }
    
    @Bean
    public AuthenticationFailureHandler customAuthenticationFailureHandler() {
        return new CustomAuthenticationFailureHandler();
    }
}
```

### Custom OAuth2 User Service
```java
@Service
public class CustomOAuth2UserService implements OAuth2UserService<OAuth2UserRequest, OAuth2User> {
    
    @Autowired
    private UserRepository userRepository;
    
    @Override
    public OAuth2User loadUser(OAuth2UserRequest userRequest) throws OAuth2AuthenticationException {
        OAuth2User oAuth2User = super.loadUser(userRequest);
        
        try {
            return processOAuth2User(userRequest, oAuth2User);
        } catch (Exception ex) {
            throw new InternalAuthenticationServiceException(ex.getMessage(), ex.getCause());
        }
    }
    
    private OAuth2User processOAuth2User(OAuth2UserRequest userRequest, OAuth2User oAuth2User) {
        OAuth2UserInfo oAuth2UserInfo = OAuth2UserInfoFactory.getOAuth2UserInfo(
            userRequest.getClientRegistration().getRegistrationId(), 
            oAuth2User.getAttributes()
        );
        
        if (oAuth2UserInfo.getEmail().isEmpty()) {
            throw new OAuth2AuthenticationProcessingException("Email not found from OAuth2 provider");
        }
        
        Optional<User> userOptional = userRepository.findByEmail(oAuth2UserInfo.getEmail());
        User user;
        if (userOptional.isPresent()) {
            user = userOptional.get();
            if (!user.getProvider().equals(AuthProvider.valueOf(
                    userRequest.getClientRegistration().getRegistrationId().toUpperCase()))) {
                throw new OAuth2AuthenticationProcessingException("Looks like you're signed up with " +
                        user.getProvider() + " account. Please use your " + user.getProvider() +
                        " account to login.");
            }
            user = updateExistingUser(user, oAuth2UserInfo);
        } else {
            user = registerNewUser(userRequest, oAuth2UserInfo);
        }
        
        return UserPrincipal.create(user, oAuth2User.getAttributes());
    }
    
    private User registerNewUser(OAuth2UserRequest userRequest, OAuth2UserInfo oAuth2UserInfo) {
        User user = new User();
        
        user.setProvider(AuthProvider.valueOf(userRequest.getClientRegistration().getRegistrationId().toUpperCase()));
        user.setProviderId(oAuth2UserInfo.getId());
        user.setName(oAuth2UserInfo.getName());
        user.setEmail(oAuth2UserInfo.getEmail());
        user.setImageUrl(oAuth2UserInfo.getImageUrl());
        
        return userRepository.save(user);
    }
    
    private User updateExistingUser(User existingUser, OAuth2UserInfo oAuth2UserInfo) {
        existingUser.setName(oAuth2UserInfo.getName());
        existingUser.setImageUrl(oAuth2UserInfo.getImageUrl());
        return userRepository.save(existingUser);
    }
}
```

## OpenID Connect (OIDC) Configuration

OpenID Connect is a simple identity layer on top of the OAuth2 protocol.

### OIDC Configuration
```java
@Configuration
@EnableWebSecurity
public class OidcSecurityConfig {
    
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .authorizeHttpRequests(authz -> authz
                .requestMatchers("/public/**").permitAll()
                .anyRequest().authenticated()
            )
            .oauth2Login(oauth2 -> oauth2
                .clientRegistrationRepository(clientRegistrationRepository())
            );
        
        return http.build();
    }
    
    @Bean
    public ClientRegistrationRepository clientRegistrationRepository() {
        return new InMemoryClientRegistrationRepository(this.googleClientRegistration());
    }
    
    private ClientRegistration googleClientRegistration() {
        return ClientRegistration.withRegistrationId("google")
            .clientId("${GOOGLE_CLIENT_ID}")
            .clientSecret("${GOOGLE_CLIENT_SECRET}")
            .clientAuthenticationMethod(ClientAuthenticationMethod.CLIENT_SECRET_BASIC)
            .authorizationGrantType(AuthorizationGrantType.AUTHORIZATION_CODE)
            .redirectUriTemplate("{baseUrl}/login/oauth2/code/{registrationId}")
            .scope("openid", "profile", "email")
            .authorizationUri("https://accounts.google.com/o/oauth2/v2/auth")
            .tokenUri("https://www.googleapis.com/oauth2/v4/token")
            .userInfoUri("https://www.googleapis.com/oauth2/v3/userinfo")
            .userNameAttributeName(IdTokenClaimNames.SUB)
            .jwkSetUri("https://www.googleapis.com/oauth2/v3/certs")
            .clientName("Google")
            .build();
    }
}
```

### OIDC Claims Processing
```java
@Component
public class OidcUserProcessor {
    
    public OidcUser processOidcUser(OidcUserRequest userRequest, OidcUser user) {
        Map<String, Object> attributes = user.getAttributes();
        String registrationId = userRequest.getClientRegistration().getRegistrationId();
        
        // Extract standard OIDC claims
        String email = (String) attributes.get("email");
        Boolean emailVerified = (Boolean) attributes.get("email_verified");
        String name = (String) attributes.get("name");
        String givenName = (String) attributes.get("given_name");
        String familyName = (String) attributes.get("family_name");
        String locale = (String) attributes.get("locale");
        
        // Process provider-specific attributes
        if ("google".equalsIgnoreCase(registrationId)) {
            // Google-specific processing
            String picture = (String) attributes.get("picture");
            // Additional Google-specific attributes
        } else if ("github".equalsIgnoreCase(registrationId)) {
            // GitHub-specific processing
            String avatarUrl = (String) attributes.get("avatar_url");
            // Additional GitHub-specific attributes
        }
        
        // Validate required claims
        if (email == null || email.isEmpty()) {
            throw new OAuth2AuthenticationProcessingException("Email not found in OIDC response");
        }
        
        if (emailVerified != null && !emailVerified) {
            throw new OAuth2AuthenticationProcessingException("Email not verified");
        }
        
        // Create or update user in database
        User dbUser = findOrCreateUser(email, name, registrationId);
        
        // Return custom OidcUser with additional attributes
        return new DefaultOidcUser(dbUser.getAuthorities(), user.getIdToken(), user.getUserInfo());
    }
    
    private User findOrCreateUser(String email, String name, String provider) {
        // Implementation to find or create user
        return new User(); // Placeholder
    }
}
```

## OAuth2 Resource Server Configuration

### JWT-based Resource Server
```java
@Configuration
@EnableWebSecurity
public class JwtResourceServerConfig {
    
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .sessionManagement(session -> session
                .sessionCreationPolicy(SessionCreationPolicy.STATELESS)
            )
            .csrf(csrf -> csrf.disable())
            .authorizeHttpRequests(authz -> authz
                .requestMatchers("/public/**").permitAll()
                .requestMatchers("/api/auth/**").permitAll()
                .requestMatchers("/api/admin/**").hasRole("ADMIN")
                .anyRequest().authenticated()
            )
            .oauth2ResourceServer(oauth2 -> oauth2
                .jwt(jwt -> jwt.jwtDecoder(jwtDecoder()))
            );
        
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

### Custom JWT Authorities Converter
```java
@Component
public class CustomJwtAuthoritiesConverter implements JwtGrantedAuthoritiesConverter {
    
    private static final String AUTHORITIES_CLAIM_NAME = "authorities";
    private static final String ROLES_CLAIM_NAME = "roles";
    
    @Override
    public Collection<GrantedAuthority> convert(Jwt jwt) {
        Collection<GrantedAuthority> authorities = new ArrayList<>();
        
        // Extract authorities from custom claim
        List<String> authoritiesClaim = jwt.getClaimAsStringList(AUTHORITIES_CLAIM_NAME);
        if (authoritiesClaim != null) {
            authorities.addAll(authoritiesClaim.stream()
                .map(SimpleGrantedAuthority::new)
                .collect(Collectors.toList()));
        }
        
        // Extract roles from roles claim and convert to authorities
        List<String> rolesClaim = jwt.getClaimAsStringList(ROLES_CLAIM_NAME);
        if (rolesClaim != null) {
            authorities.addAll(rolesClaim.stream()
                .map(role -> "ROLE_" + role)
                .map(SimpleGrantedAuthority::new)
                .collect(Collectors.toList()));
        }
        
        // Extract scopes as authorities
        List<String> scopes = jwt.getClaimAsStringList("scope");
        if (scopes != null) {
            authorities.addAll(scopes.stream()
                .map(scope -> "SCOPE_" + scope)
                .map(SimpleGrantedAuthority::new)
                .collect(Collectors.toList()));
        }
        
        return authorities;
    }
}
```

## OAuth2 Client Credentials Flow

For machine-to-machine authentication:

```java
@Service
public class OAuth2ClientCredentialsService {
    
    private final WebClient webClient;
    
    public OAuth2ClientCredentialsService(WebClient.Builder webClientBuilder) {
        this.webClient = webClientBuilder
            .filter(new ReactorClientCredentialsExchangeFilter(
                "client_id", 
                "client_secret", 
                "https://auth-server/oauth/token"
            ))
            .build();
    }
    
    public Mono<String> callProtectedResource() {
        return webClient
            .get()
            .uri("https://resource-server/api/data")
            .retrieve()
            .bodyToMono(String.class);
    }
}
```

## OAuth2 Security Best Practices

### Token Validation
```java
@Component
public class TokenValidationService {
    
    private final JwtDecoder jwtDecoder;
    
    public TokenValidationService(JwtDecoder jwtDecoder) {
        this.jwtDecoder = jwtDecoder;
    }
    
    public boolean validateToken(String token) {
        try {
            Jwt decodedToken = jwtDecoder.decode(token);
            
            // Validate expiration
            if (decodedToken.getExpiresAt().isBefore(Instant.now())) {
                return false;
            }
            
            // Validate issuer (if applicable)
            String issuer = decodedToken.getIssuer();
            if (issuer != null && !isValidIssuer(issuer)) {
                return false;
            }
            
            // Validate audience (if applicable)
            List<String> audiences = decodedToken.getAudience();
            if (audiences != null && !isValidAudience(audiences)) {
                return false;
            }
            
            return true;
        } catch (JwtException e) {
            return false;
        }
    }
    
    private boolean isValidIssuer(String issuer) {
        // Validate issuer against expected value
        return "https://your-auth-server".equals(issuer);
    }
    
    private boolean isValidAudience(List<String> audiences) {
        // Validate audience contains expected value
        return audiences.contains("your-app-audience");
    }
}
```

### Security Headers for OAuth2
```java
@Configuration
@EnableWebSecurity
public class OAuth2SecurityHeadersConfig {
    
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .headers(headers -> headers
                .frameOptions(frameOptions -> frameOptions.deny())
                .contentTypeOptions(contentType -> contentType.and())
                .xssProtection(xss -> xss.and())
                .httpStrictTransportSecurity(hsts -> hsts
                    .maxAgeInSeconds(31536000)
                    .includeSubdomains(true)
                    .preload(true)
                )
                .referrerPolicy(referrer -> referrer.policy(ReferrerPolicyHeaderWriter.ReferrerPolicy.STRICT_ORIGIN_WHEN_CROSS_ORIGIN))
            )
            .oauth2Login(oauth2 -> oauth2
                .authorizationEndpoint(endpoint -> endpoint
                    .requireImpliedPkce(true) // Require PKCE for authorization code flow
                )
            );
        
        return http.build();
    }
}
```

## Common OAuth2/OIDC Pitfalls

### Redirect URI Validation
- Always validate redirect URIs to prevent open redirect attacks
- Use exact matching rather than pattern matching when possible
- Don't allow wildcards in production environments

### PKCE Implementation
- Use Proof Key for Code Exchange (PKCE) for public clients
- Generate cryptographically random codes
- Use S256 code challenge method

### Token Storage
- Store refresh tokens securely (preferably in encrypted form)
- Implement proper token rotation
- Don't store access tokens in cookies for SPAs

### Scope Validation
- Validate requested scopes against registered scopes
- Implement minimal necessary scope grants
- Regularly audit granted scopes