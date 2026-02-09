# Version History and Usage Divergences

| Version Line | Key Change | Practical Divergence |
|---|---|---|
| JAX-RS 2.x (`javax.ws.rs`) | Legacy Java EE ecosystem | Namespace tied to pre-Jakarta runtimes |
| Jakarta REST 3.x (`jakarta.ws.rs`) | Post-migration API namespace | Code and dependencies required package migration |

## Deep Divergence Notes

- Migration from `javax.ws.rs` to `jakarta.ws.rs` is a package-level break with build/runtime impacts.
- Jersey client/server provider registration differs between older and newer bootstrap styles.
- API governance maturity usually evolves from endpoint correctness to compatibility lifecycle management.
