# 07 — Logic Apps as MCP Server

## Goal
Connect a Foundry agent to Logic Apps Standard workflows exposed as MCP (Model Context Protocol) tools.

## What is MCP?

MCP is an open standard that lets AI agents discover and invoke external tools - like **"USB-C for AI agents"**. Logic Apps exposes 1,400+ connectors as MCP tools.

## Architecture

```
┌─────────────────┐     MCP Protocol      ┌──────────────────┐
│  Foundry Agent  │ ◄──────────────────► │  Logic Apps MCP  │
│   (MCP Client)  │                       │     Server       │
└─────────────────┘                       └────────┬─────────┘
                                                   │
                                          ┌────────▼─────────┐
                                          │  1,400+ Connectors│
                                          │  (SAP, Salesforce,│
                                          │   SharePoint...)  │
                                          └──────────────────┘
```

## Quick Start

```python
from azure.ai.agents.models import McpTool

# 1. Configure MCP tool
mcp_tool = McpTool(
    server_label="logic-apps",
    server_url="https://<app>.azurewebsites.net/api/mcpservers/<name>/mcp",
)

# 2. Create agent with tool
agent = client.agents.create_agent(
    model="gpt-5-nano",
    tools=mcp_tool.definitions,
)

# 3. Run with tool resources
run = client.agents.runs.create(
    thread_id=thread.id,
    agent_id=agent.id,
    tool_resources=mcp_tool.resources,
)
```

## Logic Apps Setup

1. **Enable MCP** in `host.json`:
```json
{ "extensions": { "workflow": { "McpServerEndpoints": { "enable": true } } } }
```

2. **Define tools** in `mcpservers.json`:
```json
{ "mcpServers": [{ "name": "ticketing", "tools": [{ "name": "CreateTicket" }] }] }
```

## Proof (Checklist)
- [ ] MCP endpoint is reachable
- [ ] Tool listing works
- [ ] Tool invocation triggers Logic Apps workflow

## Files
- `logic-apps-mcp.ipynb` - Minimal example notebook

## Sources
- [Logic Apps as MCP Servers](https://learn.microsoft.com/en-us/azure/logic-apps/set-up-model-context-protocol-server-standard)
- [MCP Tool in Foundry](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/how-to/tools/model-context-protocol)

## Next
Continue to `../08-connectors-as-mcp-tools`.
