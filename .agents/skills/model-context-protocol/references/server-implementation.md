---
name: server-implementation
description: |
  Documentation file for agent operations and skill usage.
  Use when: you need procedural guidance for agent execution and context management.
---

# Server Implementation Patterns

## Transport Layers

1.  **Stdio Transport** (Default):
    -   Server runs as a subprocess.
    -   Communication via `stdin`/`stdout`.
    -   *Best for*: Local tools, sensitive data (no network exposure).

2.  **SSE (Server-Sent Events)**:
    -   Server runs as an HTTP service.
    -   *Best for*: Remote tools, distributed agents.

## SDKs

-   **TypeScript SDK**: `@modelcontextprotocol/sdk`
-   **Python SDK**: `mcp`

## Capabilities Negotiation

On handshake (`initialize`), client and server exchange capabilities:

```json
{
  "capabilities": {
    "resources": { "subscribe": true },
    "tools": {},
    "prompts": {},
    "logging": {}
  }
}
```

