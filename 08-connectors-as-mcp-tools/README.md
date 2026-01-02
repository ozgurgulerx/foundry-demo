# 08 — Logic Apps Connectors as MCP Tools

## Goal
Use 1,400+ Logic Apps connectors (Salesforce, ServiceNow, SAP, etc.) as AI agent tools via MCP.

## Supported Connectors

| Connector | Use Cases |
|-----------|----------|
| **Salesforce** | Query contacts, create opportunities, update accounts |
| **ServiceNow** | Create incidents, update tickets, assign tasks |
| **SAP** | Read business data, trigger workflows |
| **Dynamics 365** | CRM operations, sales pipeline |
| **SQL/Dataverse** | Database queries, record updates |

## Quick Start

```python
from azure.ai.agents.models import McpTool

# ServiceNow connector as MCP tool
servicenow_tool = McpTool(
    server_label="servicenow",
    server_url="https://<logic-app>.azurewebsites.net/api/mcpservers/servicenow/mcp",
    allowed_tools=["CreateIncident", "UpdateIncident"],
)

# Create agent with connector
agent = client.agents.create_agent(
    model="gpt-5-nano",
    name="it-support-agent",
    tools=servicenow_tool.definitions,
)
```

## Setup via Foundry Portal

1. Go to **Agent Tools** catalog
2. Search for connector (e.g., "Salesforce")
3. Select Logic App resource
4. Choose operations to expose
5. Configure parameters
6. Register in Foundry

## Proof (Checklist)
- [ ] MCP tool call triggers Logic Apps run
- [ ] Connector action executes successfully
- [ ] Third-party system shows activity

## Files
- `connectors-mcp.ipynb` - Examples for ServiceNow, Salesforce

## Sources
- [Logic Apps Connectors as MCP Tools](https://techcommunity.microsoft.com/blog/integrationsonazureblog/🎙️public-preview-azure-logic-apps-connectors-as-mcp-tools-in-microsoft-foundry/4473062)
- [Agentic Integration with SAP, ServiceNow, Salesforce](https://techcommunity.microsoft.com/blog/azurearchitectureblog/agentic-integration-with-sap-servicenow-and-salesforce/4466049)

## Next
Continue to `../09-apim-ai-gateway-mcp`.
