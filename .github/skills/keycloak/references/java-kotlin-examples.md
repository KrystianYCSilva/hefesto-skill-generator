# Java and Kotlin Usage Examples

```java
@Bean
JwtAuthenticationConverter jwtAuthConverter() {
  JwtGrantedAuthoritiesConverter scopes = new JwtGrantedAuthoritiesConverter();
  scopes.setAuthorityPrefix("SCOPE_");
  JwtAuthenticationConverter converter = new JwtAuthenticationConverter();
  converter.setJwtGrantedAuthoritiesConverter(scopes);
  return converter;
}
```

```kotlin
@Bean
fun authManagerResolver(): AuthenticationManagerResolver<HttpServletRequest> {
  return JwtIssuerAuthenticationManagerResolver(issuerUri)
}
```

## Additional Java and Kotlin Tips

- Java: prefer constructor injection, explicit contracts, and stable package boundaries.
- Kotlin: use null-safety and immutable DTOs to reduce runtime inconsistencies.
- Keep serialization formats and enum naming consistent between Java and Kotlin services.
