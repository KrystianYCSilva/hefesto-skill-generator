# Spring Security Ecosystem & Libraries

Comprehensive toolkit for Spring Security implementation.

## Core Security Components
- **spring-security-core**: Core authentication and authorization infrastructure
- **spring-security-web**: Web security support including filters and URL-based access control
- **spring-security-config**: XML configuration support
- **spring-security-oauth2-client**: OAuth2 client support
- **spring-security-oauth2-resource-server**: OAuth2 resource server support

## Authentication Providers
- **DaoAuthenticationProvider**: Authenticates users against a UserDetailsService
- **LdapAuthenticationProvider**: LDAP authentication support
- **OAuth2AuthenticationProvider**: OAuth2 authentication support
- **AnonymousAuthenticationProvider**: Anonymous authentication support

## Authorization Components
- **Method Security**: @PreAuthorize, @PostAuthorize, @Secured annotations
- **Expression-based Access Control**: SpEL expressions for authorization
- **AccessDecisionManager**: Manages access decisions
- **FilterSecurityInterceptor**: Intercepts HTTP requests for authorization

## JWT & Token Handling
- **Nimbus JOSE+JWT**: Library for JWT handling
- **spring-security-oauth2-jose**: JOSE support for OAuth2
- **Jwts**: JWT builder/parser from Java JWT library
- **JwtDecoder/JwtEncoder**: Interfaces for JWT decoding/encoding

## Password Encoding
- **BCryptPasswordEncoder**: BCrypt password encoder
- **DelegatingPasswordEncoder**: Delegates to other encoders based on ID
- **Pbkdf2PasswordEncoder**: PBKDF2 password encoder
- **SCryptPasswordEncoder**: SCrypt password encoder

## Testing Components
- **spring-security-test**: Testing support for Spring Security
- **@WithMockUser**: Annotation for mocking authenticated users in tests
- **SecurityMockMvcRequestPostProcessors**: Security-related request post-processors
- **TestSecurityContextHolder**: Test holder for security context

## Integration Libraries
- **spring-security-ldap**: LDAP integration
- **spring-security-saml2-service-provider**: SAML 2.0 support
- **spring-security-rsocket**: RSocket security support
- **spring-security-messaging**: Messaging security support