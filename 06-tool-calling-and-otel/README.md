# 06 — Tool Calling + OpenTelemetry Instrumentation

## Goal
Add tool calling (with at least one deterministic tool) and OpenTelemetry spans, including a stable `gen_ai.agent.id` for correlation and governance.

## You will end with
- Agent tool calling working locally
- OpenTelemetry instrumentation emitting trace spans for: agent run → tool call → tool output/error
- Stable `gen_ai.agent.id` set consistently

## Prerequisites
- Completed `../05-agent-build-with-agent-framework`
- App Insights connected (from `../02-application-insights-tracing`)

## Proof (checklist)
- [ ] At least one deterministic tool call is executed and returns expected output
- [ ] Trace shows a dedicated span for the tool invocation
- [ ] `gen_ai.agent.id` is stable across runs and environments

## Next
Continue to `../07-azd-deploy-hosted-agent`.

