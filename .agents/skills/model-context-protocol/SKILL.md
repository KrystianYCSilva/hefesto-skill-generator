---
name: model-context-protocol
description: |
  Connect AI agents to external data sources using the standardized Model Context Protocol (MCP).
  Use when: integrating agents with databases, file systems, APIs, or building custom MCP servers.
---

# Model Context Protocol (MCP)

MCP is an open standard that decouples AI models from data sources. Instead of building specific connectors for every service (Linear, GitHub, Postgres), developers build *one* MCP Server that any MCP Client (Claude, Cursor, etc.) can use.

## How to implement an MCP Server

An MCP Server exposes three primary capabilities:

1.  **Resources**: Passive data sources (File-like).
    -   *Use for*: Reading files, database rows, API logs.
    -   *URI Scheme*: `postgres://`, `file:///`, `linear://`.
2.  **Tools**: Executable functions (Function-calling).
    -   *Use for*: `insert_row`, `send_email`, `analyze_image`.
3.  **Prompts**: Pre-defined templates (slash commands).
    -   *Use for*: `summarize_bugs`, `explain_schema`.

> See [Server Implementation Guide](references/server-implementation.md) for TypeScript/Python examples.

## How to configure MCP Clients

Different CLIs ingest MCP servers differently:

-   **Claude Desktop**: Configured in `claude_desktop_config.json`.
-   **Cursor**: Configured in Settings > Features > MCP.
-   **Gemini/Qwen**: Often require a bridge or a local proxy if not natively supported.

## How to optimize Performance

-   **Resource Subscription**: Instead of polling, clients can *subscribe* to resource updates. Implement `notifications/resources/updated`.
-   **Pagination**: For large resources (DB tables), implement pagination tokens to avoid context flooding.
-   **sampling**: Use the `sampling/createMessage` capability to let the Server ask the Client (LLM) for help during complex tasks (Agentic loop).

## Common Pitfalls

| Issue | Cause | Fix |
|-------|-------|-----|
| **Connection Refused** | Server crashes or stdio pipe broken. | Use `mcp-inspector` to debug JSON-RPC traffic. Ensure stderr is used for logs, stdout ONLY for protocol. |
| **Context Overflow** | Sending entire DB tables as resources. | Use `read_resource` with slice/filter parameters, or expose as a Tool instead. |
| **Security Risks** | Exposing `rm -rf` as a Tool. | Implement "Human in the Loop" approval for destructive tools. |

## Examples

### Example: Defining a Resource (TypeScript)

**Input:** A list of users in a database.
**Output:** An MCP Resource definition.

```typescript
// Server side
server.resource(
  "user-list",
  "users://list",
  async (uri) => {
    const users = await db.users.findMany();
    return {
      contents: [{
        uri: uri.href,
        text: JSON.stringify(users)
      }]
    };
  }
);
```

### Example: Client Configuration (JSON)

**Input:** Enabling a local SQLite server.
**Output:** `claude_desktop_config.json` entry.

```json
{
  "mcpServers": {
    "sqlite": {
      "command": "uvx",
      "args": ["mcp-server-sqlite", "--db-path", "test.db"]
    }
  }
}
```

## References

-   [Official MCP Documentation](https://modelcontextprotocol.io/)
-   [MCP Protocol Specification](https://spec.modelcontextprotocol.io/)
-   [Server Implementation Guide](references/server-implementation.md)
