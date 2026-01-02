# 05 — Observability: OpenTelemetry to Application Insights

## Goal
Enable end-to-end observability for Azure AI Foundry agents using OpenTelemetry and Application Insights.

## What You'll Learn
- How to connect Application Insights to your Foundry project
- Configure OpenTelemetry for trace collection
- Add custom spans to agent invocations and tools
- View traces in Foundry Portal and Azure Monitor

## You Will End With
- Application Insights resource connected to Foundry project
- OpenTelemetry tracing enabled for agent calls
- Custom spans for tools and functions
- Traces visible in Azure AI Foundry and Application Insights

## Prerequisites
- Completed `../02-azd-deploy-hosted-agent` (working hosted agent)
- Completed `../04-foundry-agent-memory` (agent with memory)
- Azure CLI authenticated (`az login`)

## Key Concepts

| Concept | Description |
|---------|-------------|
| **Span** | A single unit of work (agent call, tool invocation) |
| **Trace** | Collection of spans forming an end-to-end request |
| **Trace ID** | Unique identifier linking all spans |
| **Application Insights** | Azure's APM service for storing traces |
| **OpenTelemetry** | Open standard for observability |

## Proof (Checklist)
- [ ] Application Insights connected to Foundry project
- [ ] OpenTelemetry configured in code
- [ ] Agent invocations create traces
- [ ] Traces visible in Foundry Portal (Tracing section)
- [ ] Traces visible in Application Insights

## Files
- `observability-otel.ipynb` - Main notebook with all steps

## Quick Start

```python
from azure.ai.projects import AIProjectClient
from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry import trace

# Get connection string from Foundry
client = AIProjectClient(endpoint=PROJECT_ENDPOINT, credential=credential)
connection_string = client.telemetry.get_application_insights_connection_string()

# Configure Azure Monitor
configure_azure_monitor(connection_string=connection_string)

# Create tracer
tracer = trace.get_tracer(__name__)

# Trace agent calls
with tracer.start_as_current_span("agent-call") as span:
    span.set_attribute("agent.name", "my-agent")
    response = openai_client.responses.create(...)
```

## Next
Continue to `../06-foundry-iq-grounding-with-ai-search`.
