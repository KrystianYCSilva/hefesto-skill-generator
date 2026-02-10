---
name: version-history
description: |
  Documentation file for agent operations and skill usage.
  Use when: you need procedural guidance for agent execution and context management.
---

# Version History and Usage Divergences

| Version Line | Key Change | Practical Divergence |
|---|---|---|
| Security <= 5.6 | `WebSecurityConfigurerAdapter` common | High inheritance coupling and hidden configuration order issues |
| Security 5.7+ | Component-style `SecurityFilterChain` | Clearer composition but migration required for legacy projects |
| Security 6.x | AuthorizationManager-centered model | Method and endpoint authorization rules needed explicit modernization |

## Deep Divergence Notes

- Migration from adapter-based config to `SecurityFilterChain` changes extension points and test strategy.
- OAuth2 resource server defaults differ between major versions; verify claim mapping and authority prefixes.
- Teams that previously used session-first security often need explicit stateless JWT boundaries.

