"""
Foundry Agent Service (classic) client — rewritten using Microsoft Agent Framework (Python).

Key point:
- The agent + thread + run live in Foundry Agent Service.
- This script is still the *client/orchestrator* that drives those API calls.

Prereqs (roughly):
- pip install agent-framework --pre
- pip install azure-ai-agents azure-identity python-dotenv
- Env vars:
  - PROJECT_ENDPOINT (or AZURE_AI_PROJECT_ENDPOINT)
  - MODEL_DEPLOYMENT_NAME (or AZURE_OPENAI_DEPLOYMENT_NAME)
"""

import os
import asyncio
from dotenv import load_dotenv

from azure.identity.aio import DefaultAzureCredential
from azure.ai.agents.aio import AgentsClient

# Agent Framework adapter that wraps Foundry Agent Service as an "agent" you can run
from agent_framework.azure import AzureAIAgentClient


load_dotenv()


async def main() -> None:
    # Use the *Foundry project endpoint*
    # Format: https://<AIFoundryResourceName>.services.ai.azure.com/api/projects/<ProjectName>
    project_endpoint = os.getenv("PROJECT_ENDPOINT") or os.getenv("AZURE_AI_PROJECT_ENDPOINT")
    if not project_endpoint:
        raise ValueError("Missing PROJECT_ENDPOINT (or AZURE_AI_PROJECT_ENDPOINT).")

    # Use the *project deployment name*
    model_deployment = os.getenv("MODEL_DEPLOYMENT_NAME") or os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
    if not model_deployment:
        raise ValueError("Missing MODEL_DEPLOYMENT_NAME (or AZURE_OPENAI_DEPLOYMENT_NAME).")

    # DefaultAzureCredential works locally (Azure CLI / VS Code / etc.) and in Azure (Managed Identity)
    async with DefaultAzureCredential() as credential:
        # AgentsClient talks to Foundry Agent Service (classic) at the *project endpoint*
        async with AgentsClient(endpoint=project_endpoint, credential=credential) as agents_client:
            # AzureAIAgentClient is the Agent Framework wrapper around the Foundry Agent Service agent lifecycle
            #
            # should_cleanup_agent=True:
            #   - creates an agent in the service
            #   - creates/uses a thread in the service
            #   - deletes the created agent when the context exits
            async with AzureAIAgentClient(
                agents_client=agents_client,
                model_deployment_name=model_deployment,
                should_cleanup_agent=True,
            ).create_agent(
                name="Quickstart",
                instructions="Be concise.",
            ) as agent:
                # Run executes server-side in Foundry Agent Service
                result = await agent.run("Write a haiku about Azure AI Foundry.")
                print(result)

                # Optional: if your AF version exposes thread/messages helpers, this is where you'd fetch them.
                # (Different preview builds expose slightly different helpers.)
                # Example patterns you might have available:
                #   msgs = await agent.get_messages()
                #   print(msgs)
                #
                # If not, you can always drop down to agents_client.messages.list(thread_id=...) if you have thread_id.


if __name__ == "__main__":
    asyncio.run(main())
