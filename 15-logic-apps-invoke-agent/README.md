# 15 — Logic Apps “Use the Agent”

## Goal
Create a Logic Apps workflow that invokes the agent using the Agent Service connector / supported pattern, optionally chaining workflow → agent → MCP tool → 3P connector.

## You will end with
- A Logic Apps workflow that calls the agent endpoint
- An observable chain (workflow run history + traces)

## Prerequisites
- Completed `../14-foundry-tool-catalog-registration`

## Proof (checklist)
- [ ] One workflow run triggers an agent execution
- [ ] (Optional) agent calls an MCP tool through APIM and triggers a 3P connector
- [ ] Traces show the full chain and correlate via `gen_ai.agent.id`

## Next
Continue to `../16-optional-a2a-agent-api-in-apim`.

