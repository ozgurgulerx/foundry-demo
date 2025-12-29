"""
Simplest Azure AI Foundry agent using Agent Framework.

Prerequisites:
- Install deps: `pip install -r requirements.txt`
- Auth: `az login` (AAD token required for Azure AI Agents API)
- Set env vars (any of the compatible names will work, project endpoint preferred):
  - Project endpoint: `AZURE_OPENAI_PROJECT_ENDPOINT` or `AZURE_AI_PROJECT_ENDPOINT` or `PROJECT_ENDPOINT` (optionally `AZURE_OPENAI_ENDPOINT`)
  - Model deployment: `AZURE_AI_MODEL_DEPLOYMENT_NAME`, `FOUNDRY_MODEL_DEPLOYMENT_NAME`,
    `MODEL_DEPLOYMENT_NAME`, or `AZURE_OPENAI_DEPLOYMENT_NAME`

Usage:
    python src/quickstart_agent.py "Write a haiku about Azure AI Foundry."
"""

import asyncio
import os
import sys
from typing import Optional

from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import AzureCliCredential, DefaultAzureCredential
from azure.ai.agents.aio import AgentsClient
from azure.core.exceptions import ResourceNotFoundError
from dotenv import load_dotenv


def _env_first(*names: str) -> str:
    """Return the first non-empty environment value for the given names."""
    for name in names:
        value = os.getenv(name)
        if value:
            return value
    raise RuntimeError(f"Missing required environment variable. Tried: {', '.join(names)}")


async def main(prompt: Optional[str] = None) -> None:
    load_dotenv()

    project_endpoint = _env_first(
        # Prefer explicit project endpoint if available
        "AZURE_OPENAI_PROJECT_ENDPOINT",
        "AZURE_AI_PROJECT_ENDPOINT",
        "PROJECT_ENDPOINT",
        "AZURE_OPENAI_ENDPOINT",
    )
    # Hardcode model to gpt-4.1 for reliability (ignore deployment env vars).
    model_deployment = "gpt-5-mini"
    # Ensure downstream libraries also see the normalized names
    os.environ.setdefault("AZURE_AI_PROJECT_ENDPOINT", project_endpoint)
    os.environ.setdefault("AZURE_AI_MODEL_DEPLOYMENT_NAME", model_deployment)

    message = prompt or "Give me one tip for getting started with Azure AI Foundry agents."

    print(f"Using endpoint: {project_endpoint}")
    print(f"Using model: {model_deployment}")

    if "services.ai.azure.com" not in project_endpoint:
        print("The endpoint must be the Project endpoint (e.g., https://<project>.services.ai.azure.com).")
        print("Current endpoint looks like an Azure OpenAI resource endpoint. Please update "
              "AZURE_AI_PROJECT_ENDPOINT / PROJECT_ENDPOINT / AZURE_OPENAI_PROJECT_ENDPOINT accordingly.")
        return

    async with DefaultAzureCredential() as credential:
        try:
            async with AgentsClient(
                endpoint=project_endpoint,
                credential=credential,
                api_version="2025-05-01",
            ) as agents_client:
                async with AzureAIAgentClient(
                    agents_client=agents_client,
                    model_deployment_name=model_deployment,
                    should_cleanup_agent=True,
                ).create_agent(
                    name="FoundryQuickstart",
                    instructions="You are a concise assistant that helps me try Azure AI Foundry quickly.",
                ) as agent:
                    response = await agent.run(message)
                    print(response)
        except ResourceNotFoundError as ex:
            async with AzureAIAgentClient(
                project_endpoint=project_endpoint,
                model_deployment_name=model_deployment,
                async_credential=credential,
            ).create_agent(
                name="FoundryQuickstart",
                instructions="You are a concise assistant that helps me try Azure AI Foundry quickly.",
            ) as agent:
                try:
                    response = await agent.run(message)
                    print(response)
                except ResourceNotFoundError as inner_ex:
                    print("Resource not found when creating or running the agent.")
                    print("Check that:")
                    print(" - The endpoint is the project endpoint (e.g., https://<project>.services.ai.azure.com)")
                    print(" - The model deployment 'gpt-4.1' exists in that project")
                    print(f"Details: {inner_ex.message or inner_ex}")
        except Exception as ex:  # best-effort diagnostics
            print(f"Unexpected error: {ex}")


if __name__ == "__main__":
    user_prompt = " ".join(sys.argv[1:]).strip() or None
    asyncio.run(main(user_prompt))
