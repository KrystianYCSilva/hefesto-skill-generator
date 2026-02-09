---
name: gcp-cloud-storage
description: |
  Guides Google Cloud Storage architecture, bucket/object governance, upload/download patterns, signed URL access, lifecycle management, and security controls.
  Use when: building file and object workflows on GCP, integrating backend services with Cloud Storage, or hardening storage operations for production.
---

# GCP Cloud Storage

Cloud Storage is Google Cloud's object storage foundation for durable and scalable file workflows. This skill helps the agent design secure bucket strategies, efficient object access, and operationally safe lifecycle controls.

## How to design bucket strategy

1. Create buckets per environment and data classification boundary.
2. Choose region/multi-region based on latency and compliance needs.
3. Define naming conventions that reflect domain and ownership.
4. Separate public, private, and archival use cases.

## How to upload and download objects safely

1. Validate content type, size limits, and checksum handling.
2. Use resumable uploads for large files.
3. Set metadata explicitly (cache headers, content disposition, retention tags).
4. Prefer server-side generation workflows for trusted uploads.

## How to secure object access

1. Use IAM and least privilege for service accounts.
2. Prefer Uniform bucket-level access unless object ACLs are required.
3. Use signed URLs for controlled temporary client access.
4. Rotate credentials and audit storage access logs.

## How to control retention and lifecycle

1. Define lifecycle rules for transition and deletion policies.
2. Use object versioning where recovery requirements demand it.
3. Apply retention policies and legal holds when needed.
4. Test lifecycle impact before production rollout.

## How to integrate event-driven workflows

1. Emit object events to Pub/Sub/Eventarc for downstream processing.
2. Make processors idempotent for duplicate event tolerance.
3. Track object processing status in durable metadata store.
4. Add dead-letter handling for failed processors.

## Common Warnings & Pitfalls

- Mixing unrelated data domains in the same bucket.
- Public access exposure by policy misconfiguration.
- Missing lifecycle controls causing cost growth.
- Overwriting objects unintentionally without generation checks.
- Assuming object events are exactly-once.

## Common Errors and Fixes

| Symptom | Root Cause | Fix |
|---|---|---|
| `403 AccessDenied` on read/write | IAM role missing or wrong principal | Grant required role to correct identity and verify project/bucket scope |
| Unexpected overwrite | No object precondition checks | Use generation-match preconditions for safe writes |
| Download URL expires too soon | Signed URL TTL too short | Tune expiration window by client workflow |
| Storage cost spikes | No retention/lifecycle governance | Add lifecycle policies and monitor bucket growth trends |

## Advanced Tips

- Use checksum validation for critical data integrity workflows.
- Keep object keys partition-friendly for large-scale listing patterns.
- Add object-level business metadata for downstream indexing/search.
- Combine Cloud Storage with CDN for high-volume public delivery.

## How to use extended references

- Read [Version History](references/version-history.md) before upgrades, migrations, or compatibility decisions.
- Read [Java and Kotlin Examples](references/java-kotlin-examples.md) for implementation-ready snippets and language-specific guidance.
- Read [Advanced Techniques](references/advanced-techniques.md) for specialist playbooks, incident tactics, and performance patterns.

