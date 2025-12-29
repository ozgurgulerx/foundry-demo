# 01 — Agent Framework Agent (Local “Hello Agent”)

If you’ve built “agents” before, this step will feel familiar: it’s an application you run (laptop/VM/container/CI) that calls Azure-hosted models over HTTPS. That familiarity is the point. Before we introduce any platform abstraction, we want a baseline where behavior, tool calling, and trace signals are attributable to *your code*, running in *your runtime*.

## Agents in Azure AI Foundry: execution models (the platform shift)

![Foundry Agent Service overview diagram](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/media/agent-service-the-glue.png?view=foundry-classic)


Azure AI Foundry currently supports multiple “agent” execution models that coexist. They’re not just feature variations; they are different **execution substrates**. The substrate determines what can be governed, what can be observed end-to-end, and what can be made operationally deterministic.

### Substrate comparison (what really changes)

| Execution model | Where code runs | Deployment artifact | Dependency control | Identity & governance | Best for |
| --- | --- | --- | --- | --- | --- |
| Agent Framework agent | Your compute | Your repo/build | Full control | Optional/indirect | Proving logic, tools, and signals early |
| Foundry Agent Service (non-hosted) | Foundry-managed runtime | Configuration | Limited | Partial/limited boundaries | Zero-ops experimentation and UX-first agents |
| Foundry Hosted Agents | Containerized runtime | Versioned deployable | Full (within your container) | Strong (Agent ID, policies, lifecycle) | Enterprise workflows, MCP, A2A, governed tool access |

## 1) Agent Framework agent (local compute, API-driven)

In this model, an agent is simply software you run. You own the process lifecycle, the runtime, and the dependencies; Azure provides the model endpoint and (when you wire it in) the tracing backend. The agent calls Azure OpenAI / Foundry models over HTTPS and behaves like any other application that depends on a cloud API.

The mental model is: *an agent is an application that happens to call Azure-hosted models.* This repo starts here because it lets you validate reasoning and tool-calling semantics before any managed runtime enters the picture.

**Where this is in the repo:** `01-agent-framework-agent/`

## 2) Foundry Agent Service (managed runtime, non-containerized)

This is the configuration-first model: you define the agent’s identity, instructions, tools, and grounding, but execution happens inside a shared managed runtime. You don’t deploy software, and you can’t bring arbitrary dependencies. That’s an intentional trade: speed and UX abstraction over runtime control.

For serious enterprise composition (agent-to-agent flows, MCP tool servers, strict operational boundaries), that opacity becomes a constraint. It’s not “worse”, it’s a different substrate with different guarantees.

## 3) Foundry Hosted Agents (containerized, code-first)

Hosted Agents are the real shift. Once the agent becomes a containerized, versioned workload, Foundry can act as a control plane rather than a black-box runtime: deploy/version/rollback, correlate traces consistently, and enforce identity-based governance. This is the substrate that makes stable Agent IDs, Conditional Access, deterministic observability boundaries, and “enterprise-safe MCP” practical.

**Where this shows up next:** `04-azd-deploy-hosted-agent/`

## Why this step comes first

The workshop is linear because the platform evolution is linear: prove behavior first (agent logic), then prove signals (observability and wiring), then cross the container boundary (hosted agents), then prove governance (Agent ID/CA, MCP/APIM policies, workflows). Each step answers: *what becomes possible only after this execution model exists?*

## Run locally

After completing `00-environment-setup/` and creating `.env` from `00-environment-setup/.env.example`, run:

```bash
python3 01-agent-framework-agent/agent/hello_agent.py
python3 01-agent-framework-agent/agent/hello_agent_reasoning_min.py
```

## Proof

You’re done with this step when the agent returns a model response using values loaded from `.env`.

## Next

Continue to `../02-observability-otel-to-appinsights`.

