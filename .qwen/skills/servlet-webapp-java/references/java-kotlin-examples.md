# Java and Kotlin Usage Examples

## Java Example

`java
public class AuthFilter implements Filter { public void doFilter(...) { chain.doFilter(req, res); } }
`

## Kotlin Example

`kotlin
class AuthFilter : Filter { override fun doFilter(req: ServletRequest, res: ServletResponse, chain: FilterChain) { chain.doFilter(req, res) } }
`

## Java and Kotlin Practical Notes

- Keep contracts typed and versioned at module and API boundaries.
- Align nullability, enum names, and date/time formats across both languages.
- Prefer immutable command/event DTOs for transport and integration layers.
- Validate payloads at ingress boundaries before business-core invocation.

## Topic Keywords

- filters
- session management
- MVC boundaries
- thread pool
- request lifecycle
