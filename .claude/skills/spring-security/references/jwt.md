# JWT Implementation Guide for Spring Security

Comprehensive guide to implementing JWT authentication in Spring Boot applications.

## JWT Structure and Components

JWT (JSON Web Token) consists of three parts separated by dots (.):

1. **Header**: Contains token type and signing algorithm
2. **Payload**: Contains claims (information about entity and metadata)
3. **Signature**: Used to verify token integrity

Example JWT: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c`

## JWT Implementation Patterns

### Enhanced JWT Utility Class
```java
@Component
public class JwtUtil {
    
    private String secret = "${jwt.secret:mySecretKey}"; // Use externalized property
    private int jwtExpiration = Integer.parseInt("${jwt.expiration:86400}"); // 24 hours in seconds
    private int refreshExpiration = Integer.parseInt("${jwt.refreshExpiration:604800}"); // 7 days
    
    public String generateToken(UserDetails userDetails) {
        return generateToken(new HashMap<>(), userDetails);
    }
    
    public String generateToken(Map<String, Object> extraClaims, UserDetails userDetails) {
        return buildToken(extraClaims, userDetails, jwtExpiration);
    }
    
    public String generateRefreshToken(UserDetails userDetails) {
        return buildToken(new HashMap<>(), userDetails, refreshExpiration);
    }
    
    private String buildToken(Map<String, Object> extraClaims, UserDetails userDetails, int expiration) {
        return Jwts.builder()
            .setClaims(extraClaims)
            .setSubject(userDetails.getUsername())
            .setIssuedAt(new Date(System.currentTimeMillis()))
            .setExpiration(new Date(System.currentTimeMillis() + expiration * 1000))
            .signWith(getSignInKey(), SignatureAlgorithm.HS256)
            .compact();
    }
    
    public boolean isTokenValid(String token, UserDetails userDetails) {
        final String username = extractUsername(token);
        return (username.equals(userDetails.getUsername())) && !isTokenExpired(token);
    }
    
    public String extractUsername(String token) {
        return extractClaim(token, Claims::getSubject);
    }
    
    public Date extractExpiration(String token) {
        return extractClaim(token, Claims::getExpiration);
    }
    
    public <T> T extractClaim(String token, Function<Claims, T> claimsResolver) {
        final Claims claims = extractAllClaims(token);
        return claimsResolver.apply(claims);
    }
    
    private Claims extractAllClaims(String token) {
        return Jwts
            .parserBuilder()
            .setSigningKey(getSignInKey())
            .build()
            .parseClaimsJws(token)
            .getBody();
    }
    
    private Boolean isTokenExpired(String token) {
        return extractExpiration(token).before(new Date());
    }
    
    private Key getSignInKey() {
        byte[] keyBytes = Decoders.BASE64.decode(secret);
        return Keys.hmacShaKeyFor(keyBytes);
    }
}
```

### Advanced JWT Authentication Filter
```java
@Component
@RequiredArgsConstructor
public class JwtAuthenticationFilter extends OncePerRequestFilter {
    
    private final JwtUtil jwtUtil;
    private final UserDetailsService userDetailsService;
    
    @Override
    protected void doFilterInternal(
            @NonNull HttpServletRequest request,
            @NonNull HttpServletResponse response,
            @NonNull FilterChain filterChain
    ) throws ServletException, IOException {
        
        final String authHeader = request.getHeader("Authorization");
        final String jwt;
        final String userEmail;
        
        if (authHeader == null || !authHeader.startsWith("Bearer ")) {
            filterChain.doFilter(request, response);
            return;
        }
        
        jwt = authHeader.substring(7);
        userEmail = jwtUtil.extractUsername(jwt);
        
        if (userEmail != null && SecurityContextHolder.getContext().getAuthentication() == null) {
            UserDetails userDetails = this.userDetailsService.loadUserByUsername(userEmail);
            
            if (jwtUtil.isTokenValid(jwt, userDetails)) {
                UsernamePasswordAuthenticationToken authToken = new UsernamePasswordAuthenticationToken(
                        userDetails,
                        null,
                        userDetails.getAuthorities()
                );
                authToken.setDetails(
                        new WebAuthenticationDetailsSource().buildDetails(request)
                );
                SecurityContextHolder.getContext().setAuthentication(authToken);
            }
        }
        filterChain.doFilter(request, response);
    }
}
```

### JWT Authentication Controller
```java
@RestController
@RequestMapping("/api/auth")
@RequiredArgsConstructor
public class AuthenticationController {
    
    private final AuthenticationService authenticationService;
    
    @PostMapping("/authenticate")
    public ResponseEntity<AuthenticationResponse> authenticate(
            @RequestBody AuthenticationRequest request
    ) {
        AuthenticationResponse response = authenticationService.authenticate(request);
        return ResponseEntity.ok(response);
    }
    
    @PostMapping("/refresh-token")
    public ResponseEntity<AuthenticationResponse> refreshToken(
            HttpServletRequest request
    ) {
        String refreshToken = request.getHeader("Authorization");
        if (refreshToken != null && refreshToken.startsWith("Bearer ")) {
            refreshToken = refreshToken.substring(7);
        }
        AuthenticationResponse response = authenticationService.refreshToken(refreshToken);
        return ResponseEntity.ok(response);
    }
}
```

### Authentication Service Implementation
```java
@Service
@RequiredArgsConstructor
public class AuthenticationService {
    
    private final UserRepository repository;
    private final PasswordEncoder passwordEncoder;
    private final JwtUtil jwtUtil;
    private final RefreshTokenService refreshTokenService;
    
    public AuthenticationResponse authenticate(AuthenticationRequest request) {
        authenticationManager.authenticate(
                new UsernamePasswordAuthenticationToken(
                        request.getEmail(),
                        request.getPassword()
                )
        );
        var user = repository.findByEmail(request.getEmail())
                .orElseThrow();
        var jwtToken = jwtUtil.generateToken(user);
        var refreshToken = jwtUtil.generateRefreshToken(user);
        refreshTokenService.saveUserToken(user, refreshToken);
        
        return AuthenticationResponse.builder()
                .token(jwtToken)
                .refreshToken(refreshToken)
                .build();
    }
    
    public AuthenticationResponse refreshToken(String refreshToken) {
        if (jwtUtil.isTokenValid(refreshToken, getUserFromRefreshToken(refreshToken))) {
            var user = getUserFromRefreshToken(refreshToken);
            var accessToken = jwtUtil.generateToken(user);
            return AuthenticationResponse.builder()
                    .token(accessToken)
                    .refreshToken(refreshToken)
                    .build();
        }
        throw new RuntimeException("Invalid refresh token");
    }
    
    private UserDetails getUserFromRefreshToken(String refreshToken) {
        String username = jwtUtil.extractUsername(refreshToken);
        return repository.findByEmail(username)
                .orElseThrow(() -> new UsernameNotFoundException("User not found"));
    }
}
```

## JWT Security Best Practices

### Secure Secret Management
```java
@Configuration
public class JwtSecurityConfig {
    
    @Bean
    public String jwtSecret() {
        // Load from environment variable or external secret manager
        String secret = System.getenv("JWT_SECRET");
        if (secret == null || secret.isEmpty()) {
            throw new IllegalStateException("JWT_SECRET environment variable must be set");
        }
        return secret;
    }
    
    // Or using Spring Cloud Vault
    @Bean
    public String jwtSecretFromVault() {
        // Implementation to retrieve secret from Vault
        return retrieveSecretFromVault("jwt-secret");
    }
    
    private String retrieveSecretFromVault(String key) {
        // Implementation to retrieve secret from vault
        return "secret-from-vault";
    }
}
```

### Token Blacklisting
```java
@Service
public class TokenBlacklistService {
    
    private final Set<String> blacklistedTokens = ConcurrentHashMap.newKeySet();
    
    public void blacklistToken(String token) {
        blacklistedTokens.add(token);
    }
    
    public boolean isTokenBlacklisted(String token) {
        return blacklistedTokens.contains(token);
    }
    
    // Optional: Scheduled cleanup of expired tokens
    @Scheduled(fixedRate = 300000) // Every 5 minutes
    public void cleanupExpiredTokens() {
        blacklistedTokens.removeIf(this::isTokenExpired);
    }
    
    private boolean isTokenExpired(String token) {
        try {
            Claims claims = Jwts.parserBuilder()
                    .setSigningKey(getSignInKey())
                    .build()
                    .parseClaimsJws(token)
                    .getBody();
            return claims.getExpiration().before(new Date());
        } catch (Exception e) {
            // If token is malformed, consider it expired
            return true;
        }
    }
    
    private Key getSignInKey() {
        byte[] keyBytes = Decoders.BASE64.decode(System.getenv("JWT_SECRET"));
        return Keys.hmacShaKeyFor(keyBytes);
    }
}
```

### JWT Claims Validation
```java
@Component
public class JwtValidator {
    
    public boolean validateToken(String token, String expectedAudience, String expectedIssuer) {
        try {
            Claims claims = Jwts.parserBuilder()
                    .setSigningKey(getSignInKey())
                    .build()
                    .parseClaimsJws(token)
                    .getBody();
            
            // Validate expiration
            if (claims.getExpiration().before(new Date())) {
                return false;
            }
            
            // Validate audience
            String audience = claims.getAudience();
            if (!expectedAudience.equals(audience)) {
                return false;
            }
            
            // Validate issuer
            String issuer = claims.getIssuer();
            if (issuer != null && !expectedIssuer.equals(issuer)) {
                return false;
            }
            
            // Validate subject (optional)
            String subject = claims.getSubject();
            if (subject == null || subject.isEmpty()) {
                return false;
            }
            
            return true;
        } catch (JwtException | IllegalArgumentException e) {
            return false;
        }
    }
    
    private Key getSignInKey() {
        byte[] keyBytes = Decoders.BASE64.decode(System.getenv("JWT_SECRET"));
        return Keys.hmacShaKeyFor(keyBytes);
    }
}
```

## JWT with Public/Private Key Pair

### RSA-based JWT Implementation
```java
@Component
public class RsaJwtUtil {
    
    private final RSAPublicKey publicKey;
    private final RSAPrivateKey privateKey;
    
    public RsaJwtUtil() throws NoSuchAlgorithmException, InvalidKeySpecException {
        // Load keys from resources or external source
        this.publicKey = loadPublicKey();
        this.privateKey = loadPrivateKey();
    }
    
    public String generateToken(UserDetails userDetails) {
        Date issuedAt = new Date(System.currentTimeMillis());
        Date expiration = new Date(issuedAt.getTime() + 1000 * 60 * 60); // 1 hour
        
        return Jwts.builder()
                .setSubject(userDetails.getUsername())
                .setIssuedAt(issuedAt)
                .setExpiration(expiration)
                .signWith(privateKey, SignatureAlgorithm.RS256)
                .compact();
    }
    
    public boolean validateToken(String token, UserDetails userDetails) {
        final String username = extractUsername(token);
        return (username.equals(userDetails.getUsername())) && !isTokenExpired(token);
    }
    
    public String extractUsername(String token) {
        return extractClaim(token, Claims::getSubject);
    }
    
    public <T> T extractClaim(String token, Function<Claims, T> claimsResolver) {
        final Claims claims = parseClaims(token);
        return claimsResolver.apply(claims);
    }
    
    private boolean isTokenExpired(String token) {
        return extractExpiration(token).before(new Date());
    }
    
    private Date extractExpiration(String token) {
        return extractClaim(token, Claims::getExpiration);
    }
    
    private Claims parseClaims(String token) {
        return Jwts.parserBuilder()
                .setSigningKey(publicKey)
                .build()
                .parseClaimsJws(token)
                .getBody();
    }
    
    private RSAPublicKey loadPublicKey() throws NoSuchAlgorithmException, InvalidKeySpecException {
        // Load public key from file, environment, or external source
        String publicKeyPEM = System.getenv("RSA_PUBLIC_KEY");
        // Remove header and footer, then decode
        String publicKeyContent = publicKeyPEM
                .replace("-----BEGIN PUBLIC KEY-----", "")
                .replace("-----END PUBLIC KEY-----", "")
                .replaceAll("\\s", "");
        
        byte[] decoded = Base64.getDecoder().decode(publicKeyContent);
        X509EncodedKeySpec spec = new X509EncodedKeySpec(decoded);
        KeyFactory keyFactory = KeyFactory.getInstance("RSA");
        return (RSAPublicKey) keyFactory.generatePublic(spec);
    }
    
    private RSAPrivateKey loadPrivateKey() throws NoSuchAlgorithmException, InvalidKeySpecException {
        // Load private key from file, environment, or external source
        String privateKeyPEM = System.getenv("RSA_PRIVATE_KEY");
        // Remove header and footer, then decode
        String privateKeyContent = privateKeyPEM
                .replace("-----BEGIN PRIVATE KEY-----", "")
                .replace("-----END PRIVATE KEY-----", "")
                .replaceAll("\\s", "");
        
        byte[] decoded = Base64.getDecoder().decode(privateKeyContent);
        PKCS8EncodedKeySpec spec = new PKCS8EncodedKeySpec(decoded);
        KeyFactory keyFactory = KeyFactory.getInstance("RSA");
        return (RSAPrivateKey) keyFactory.generatePrivate(spec);
    }
}
```

## JWT Best Practices Summary

### Security Measures
- Use strong secrets or key pairs (minimum 256-bit for symmetric algorithms)
- Implement token expiration with reasonable lifetimes
- Use HTTPS in production environments
- Consider implementing token blacklisting for logout functionality
- Validate all JWT claims (audience, issuer, expiration, etc.)

### Performance Considerations
- Cache decoded JWT claims to avoid repeated parsing
- Use efficient algorithms (RS256 vs HS256 based on your needs)
- Implement proper error handling for invalid tokens
- Consider using JWK (JSON Web Key) sets for key rotation

### Common Pitfalls to Avoid
- Using weak or predictable secrets
- Not validating token expiration
- Storing sensitive information in JWT payloads
- Not implementing proper error handling
- Using JWT for session management inappropriately