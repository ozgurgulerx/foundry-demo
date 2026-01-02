# 09 — APIM AI Gateway for MCP

## Goal
Put MCP servers behind Azure API Management for enterprise governance: rate limiting, authentication, content safety, and monitoring.

## Architecture

```
┌──────────┐      ┌─────────────────┐      ┌─────────────────┐
│  Agent   │ ──► │  APIM Gateway   │ ──► │  MCP Server     │
│          │      │  • Rate Limit   │      │  (Logic Apps)   │
│          │      │  • Auth         │      │                 │
│          │      │  • Safety       │      │                 │
└──────────┘      └─────────────────┘      └─────────────────┘
```

## Key Policies

| Policy | Purpose |
|--------|---------|
| `rate-limit-by-key` | Limit requests per consumer |
| `llm-token-limit` | Limit tokens per minute |
| `validate-jwt` | OAuth/JWT authentication |
| `llm-content-safety` | Block prompt injection |
| `llm-emit-token-metric` | Track token usage |

## Quick Start

```python
from azure.ai.agents.models import McpTool

# Point to APIM gateway (not directly to backend)
mcp_tool = McpTool(
    server_label="apim-mcp",
    server_url="https://your-apim.azure-api.net/mcp/ticketing/mcp",
)

# Add subscription key if required
mcp_tool.update_headers("Ocp-Apim-Subscription-Key", "your-key")

# Create agent
agent = client.agents.create_agent(tools=mcp_tool.definitions)
```

## Sample Policy

```xml
<inbound>
    <validate-jwt header-name="Authorization" />
    <rate-limit-by-key calls="10" renewal-period="60" />
    <llm-content-safety backend-id="content-safety" />
</inbound>
<outbound>
    <llm-emit-token-metric namespace="mcp-gateway" />
</outbound>
```

## Proof (Checklist)
- [ ] Burst requests return `429` (rate limited)
- [ ] Injection attempts blocked
- [ ] Metrics visible in App Insights

## Files
- `apim-ai-gateway.ipynb` - Minimal example

## Sources
- [AI Gateway Capabilities](https://learn.microsoft.com/en-us/azure/api-management/genai-gateway-capabilities)
- [MCP Server Overview](https://learn.microsoft.com/en-us/azure/api-management/mcp-server-overview)
- [AI Gateway in Foundry](https://techcommunity.microsoft.com/blog/integrationsonazureblog/ai-gateway-in-azure-api-management-is-now-available-in-microsoft-foundry-preview/4470676)

## Next
Continue to `../10-tool-catalog-registration-in-foundry`.
