// mcp-server-{{SKILL_NAME}}.js
// Generated from Agent Skills template
// MCP Spec: 2024-11-05

const { Server } = require("@modelcontextprotocol/sdk/server/index.js");
const { StdioServerTransport } = require("@modelcontextprotocol/sdk/server/stdio.js");

const server = new Server(
  {
    name: "{{SKILL_NAME}}-server",
    version: "{{VERSION}}",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

server.setRequestHandler("tools/list", async () => {
  return {
    tools: [
      {
        name: "{{SKILL_NAME}}",
        description: "{{SKILL_DESCRIPTION}}",
        inputSchema: {
          type: "object",
          properties: {
            args: {
              type: "string",
              description: "Arguments for the skill"
            }
          },
          required: ["args"]
        }
      }
    ]
  };
});

server.setRequestHandler("tools/call", async (request) => {
  if (request.params.name !== "{{SKILL_NAME}}") {
    throw new Error("Unknown tool");
  }

  // Skill logic placeholder
  // In a real implementation, we would parse and execute the SKILL_BODY logic
  const result = `
Executed skill: {{SKILL_NAME}}
With args: ${request.params.arguments.args}

{{SKILL_BODY}}
  `;

  return {
    content: [{ type: "text", text: result }]
  };
});

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
}

main().catch(console.error);
