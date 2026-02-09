# Expert Techniques

- Run race detector in CI for all concurrency-heavy packages.
- Use `pprof` before tuning allocations; avoid blind `sync.Pool` usage.
- Keep goroutine ownership explicit and test cancellation propagation paths.
- Use backpressure-aware worker pools instead of unbounded goroutine fan-out.

## Specialist Playbook

- Gate concurrency-heavy paths with race detector and load-test coverage.
- Profile allocation and lock contention before applying low-level optimizations.
- Keep cancellation propagation checks in integration tests.
- Instrument worker pools with backlog and saturation metrics.
