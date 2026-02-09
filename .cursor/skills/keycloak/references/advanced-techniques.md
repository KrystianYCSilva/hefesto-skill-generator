# Expert Techniques

- Use client scopes as reusable claim contracts across products.
- Keep realm migration scripts versioned and rehearse rollback on staging.
- Isolate admin plane from public traffic with strict network boundaries.
- Model token exchange and service account flows explicitly for machine actors.

## Specialist Playbook

- Version realm/client configuration as code and promote through environments.
- Implement token-claim contract tests for every API relying on custom claims.
- Keep admin plane isolated and enforce MFA + short-lived elevated privileges.
- Rehearse key rotation and issuer migration with staged validation.
