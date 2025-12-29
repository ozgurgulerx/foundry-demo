# 13 — APIM AI Gateway in Front of MCP (“Enterprise-Safe MCP”)

## Goal
Put the Logic Apps MCP endpoint behind APIM AI Gateway and prove governance with rate limiting + injection/safety guardrails + diagnostics.

## You will end with
- APIM routing to the Logic Apps MCP server
- Policies:
  - Rate limiting (burst demo)
  - Prompt-injection/content-safety guardrail (block/rewrite/allowlist args)
- Diagnostics enabled (App Insights recommended)

## Prerequisites
- Completed `../12-logic-apps-connectors-as-mcp-tools`

## Proof (checklist)
- [ ] Burst requests yield `429` with rate-limit headers and logs
- [ ] Injection attempt is blocked/rewritten and decision is logged
- [ ] APIM diagnostics correlate to agent runs (via trace IDs / `gen_ai.agent.id`)

## Next
Continue to `../14-foundry-tool-catalog-registration`.

