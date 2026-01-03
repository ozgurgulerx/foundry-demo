# Claude Code Instructions for foundry-demo

## Project Overview
This repository contains demos for Microsoft Azure AI Foundry hosted agents using the Microsoft Agent Framework.


##Key Guidance
Check the documentation under /99-reference to double check the correct methods when not clear

## Key Directories
- `01-agent-framework-foundry-hosted-agents/` - Local agent examples using Agent Framework
- `02-azd-deploy-hosted-agent/` - Azure Developer CLI (azd) deployment for hosted agents

## Hosted Agent Deployment (02-azd-deploy-hosted-agent)



### Important Files
- `src/my-hosted-agent/main.py` - Agent code (must extend BaseAgent with `run` and `run_stream` methods)
- `src/my-hosted-agent/agent.yaml` - Agent definition (name, protocols, env vars)
- `src/my-hosted-agent/requirements.txt` - Python dependencies
- `azure.yaml` - azd project configuration
- `.azure/hosted-agent-env/.env` - Environment variables for deployment

### Deployment Commands
```bash
cd 02-azd-deploy-hosted-agent
AZD_EXT_TIMEOUT=120 azd deploy --no-prompt
```

### Agent Code Pattern
Agents MUST:
1. Extend `BaseAgent` from `agent_framework`
2. Implement `async def run(self, messages=None, **kwargs) -> AgentRunResponse`
3. Implement `async def run_stream(self, messages=None, **kwargs)` as an async generator
4. Return `AgentRunResponse(messages=[ChatMessage(Role.ASSISTANT, text="response")])` - use `text=` not `content=`
5. Be wrapped with `from_agent_framework(agent).run()` for hosting

### Common Issues
- **"undefined is not an object (evaluating 't.response.output.find')"** - Wrong response format. Use `ChatMessage(Role.ASSISTANT, text=...)` not `Message(role=, content=...)`
- **"EchoAgent object has no attribute 'run_stream'"** - Must implement `run_stream` method
- **Container stuck in "Starting"** - Check container logs, likely import or runtime error
- **ACR errors** - ACR must be in same resource group as Foundry project

### Environment Variables
Required in `.azure/hosted-agent-env/.env`:
- `AZURE_CONTAINER_REGISTRY_ENDPOINT` - e.g., `aicontainervault01.azurecr.io`
- `AZURE_AI_PROJECT_ENDPOINT` - Foundry project endpoint
- `MODEL_DEPLOYMENT_NAME` - e.g., `gpt-5-nano`

### Region Limitation
Hosted agents only work in **North Central US** region.

## Testing Agents
Agents can be tested in the Azure AI Foundry Portal playground after deployment.
