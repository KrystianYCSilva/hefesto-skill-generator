# Java and Kotlin Usage Examples

```java
@Bean
SecurityFilterChain api(HttpSecurity http) throws Exception {
  http.csrf(csrf -> csrf.disable())
      .authorizeHttpRequests(auth -> auth
        .requestMatchers("/actuator/health", "/auth/**").permitAll()
        .anyRequest().authenticated())
      .oauth2ResourceServer(oauth2 -> oauth2.jwt());
  return http.build();
}
```

```kotlin
@Bean
fun jwtDecoder(): JwtDecoder = NimbusJwtDecoder.withJwkSetUri(jwkSetUri).build()
```

## Additional Java and Kotlin Tips

- Java: keep security config modular by boundary (public API, admin API, internal API).
- Kotlin: prefer explicit bean definitions for security components to improve readability.
- Map claims to authorities in one reusable converter to avoid policy drift.
