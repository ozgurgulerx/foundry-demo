# 09 — Observability Proof (Foundry Tracing + App Insights Agents View)

## Goal
Run multiple agent executions and validate trace continuity across successes, tool calls, and failures.

## You will end with
- End-to-end traces visible in Foundry tracing timeline
- Runs visible in Application Insights “Agents view” with latency, errors, and token/cost breakdown

## Prerequisites
- Completed `../08-entra-agent-id-conditional-access`
- OTel instrumentation from `../06-tool-calling-and-otel`

## Proof (checklist)
- [ ] At least one successful run, one tool call, and one failure run are captured
- [ ] Trace spans connect agent run → tool invocation → tool output/error
- [ ] App Insights shows runs with latency + error details

## Next
Continue to `../10-iq-grounding-proof`.

