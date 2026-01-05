# Azure AI Foundry - Ignite 2025 Demo (Proof Driven)

[![Author](https://img.shields.io/badge/Author-Ozgur%20Guler-orange)](#author)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-in%20progress-blue)](#)
[![Azure](https://img.shields.io/badge/Azure-AI%20Foundry-0078D4)](#)
[![OpenTelemetry](https://img.shields.io/badge/observability-OpenTelemetry-4c4c4c)](#)
[![APIM](https://img.shields.io/badge/governance-API%20Management%20AI%20Gateway-6f42c1)](#)
[![MCP](https://img.shields.io/badge/tools-Model%20Context%20Protocol%20(MCP)-111827)](#)

![Ignite demo storyline](.assets/images/Gemini_Generated_Image_frkx50frkx50frkx.png)

This repo is a hands-on workshop for Microsoft Ignite 2025 announcements around Azure AI Foundry.

### Foundry Hosted Agent Architecture

![Foundry Hosted Agent](.assets/images/foundry_hosted_agent.png)

The hosted agent lifecycle: **Deploy → Govern → Publish → Share** — containerized agents deployed through `azd`, governed by Foundry control plane, and exposed as managed endpoints.

You move from a local Agent Framework script to a governed hosted agent with grounded knowledge, end-to-end tracing, Entra Agent ID Conditional Access, Logic Apps MCP tooling behind APIM AI Gateway, and tool registration in the Foundry control plane.

## What you prove
- Local Agent Framework runs hit your Foundry or Azure OpenAI deployment using `.env` secrets.
- Hosted agent deployed with `azd` exposes a managed endpoint but keeps your code and dependencies.
- OpenTelemetry traces land in Foundry and Application Insights with a stable agent identity.
- Entra Agent ID plus Conditional Access block or allow agent execution in a measurable way.
- Foundry IQ knowledge base backed by Azure AI Search returns grounded answers with citations.
- Logic Apps Standard exposes workflows as MCP tools, including connector-backed actions, fronted by APIM AI Gateway policies.
- Foundry tool catalog registers the APIM-fronted tools, and Logic Apps can invoke the agent (A2A) to close the loop.

## Prerequisites
- Azure subscription with rights to create Foundry resources, Application Insights, Logic Apps Standard, API Management, and Azure AI Search.
- Python 3.10+, Azure CLI (`az`), Azure Developer CLI (`azd`) with the Azure AI Foundry extension.
- Ability to create a local `.env` (gitignored) with: `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_API_KEY`, `AZURE_OPENAI_API_VERSION`, `AZURE_OPENAI_DEPLOYMENT_NAME`, `AZURE_OPENAI_REASONING_DEPLOYMENT_NAME`.

## Quick start
1. Create a virtual environment: `bash 00-environment-setup/scripts/bootstrap_venv.sh` (or `python3 -m venv .venv && source .venv/bin/activate`).
2. Install dependencies: `python -m pip install -r requirements.txt`.
3. Copy the environment template: `cp 00-environment-setup/.env.example .env` and fill in your deployment values.
4. Smoke-test the local agent: `python 01-agent-framework-foundry-hosted-agents/01-af-standard-agent.py` (simple chat) or `python 01-agent-framework-foundry-hosted-agents/02-af-standard-agent-resoning.py` for the reasoning variant.
5. Keep tracing on your radar: `05-observability-otel-to-appinsights/` links Foundry to Application Insights before you add OTel instrumentation.

## Workshop path (folders)
| Order | Folder | Purpose |
| --- | --- | --- |
| 00 | `00-environment-setup/` | Tooling, Python env, `.env` template, verification script |
| 01 | `01-agent-framework-foundry-hosted-agents/` | Local Agent Framework examples and execution model comparison |
| 02 | `05-observability-otel-to-appinsights/` | Attach Application Insights to your Foundry project for tracing |
| 03 | `02-azd-deploy-hosted-agent/` | Deploy the agent as a hosted agent with `azd` |
| 04 | `05-entra-agent-id-ca/` | Entra Agent ID plus Conditional Access enforcement proof |
| 05 | `06-foundry-iq-grounding-with-ai-search/` | Azure AI Search plus Foundry IQ knowledge base grounding |
| 06 | `07-logic-apps-as-mcp-server/` | Logic Apps Standard as a remote MCP server |
| 07 | `08-connectors-as-mcp-tools/` | Connector-backed MCP tools exposed from Logic Apps |
| 08 | `09-apim-ai-gateway-mcp/` | APIM AI Gateway governance in front of MCP |
| 09 | `10-tool-catalog-registration-in-foundry/` | Register APIM-fronted tools in the Foundry catalog |
| 10 | `11-logic-apps-invoke-agent-a2a/` | Logic Apps workflow calls the agent (optionally chaining MCP calls) |
| Ref | `99-reference/` | Supporting PDFs and notes from Ignite and docs |

## How to use this repo
- Each folder README states the goal, prerequisites, and proof checklist; stay sequence-aligned so proofs stay meaningful.
- Keep `.env` local; scripts expect the Azure OpenAI or Foundry values listed above.
- When deploying or invoking hosted agents, align traces, APIM diagnostics, and Conditional Access results with the same `gen_ai.agent.id`.
- For MCP steps, start with `07-logic-apps-as-mcp-server/` before layering connectors and APIM guardrails.

---

## Author

**Ozgur Guler**
AI Solution Leader, AI Innovation Hub
Email: [ozgur.guler1@gmail.com](mailto:ozgur.guler1@gmail.com)

---

## License & Attribution

This repository and its contents are the original work of Ozgur Guler. If you find this material helpful, please provide appropriate credit. For issues, suggestions, or collaboration opportunities, reach out via the email above.

© 2025 Ozgur Guler. All rights reserved.
