# 16 (Optional) — A2A Agent API in APIM AI Gateway

## Goal
If you want A2A as a first-class capability, publish an A2A agent endpoint + agent card JSON and import it into APIM as an A2A Agent API with policies applied.

## You will end with
- An A2A agent endpoint + agent card JSON
- APIM A2A Agent API import with governance policies

## Prerequisites
- Completed `../13-apim-ai-gateway-enterprise-safe-mcp`
- Stable `gen_ai.agent.id` (from `../06-tool-calling-and-otel`)

## Proof (checklist)
- [ ] APIM shows the A2A API tile/config
- [ ] Calls flow through APIM and are governed
- [ ] Traces correlate to agent runs using `gen_ai.agent.id`

