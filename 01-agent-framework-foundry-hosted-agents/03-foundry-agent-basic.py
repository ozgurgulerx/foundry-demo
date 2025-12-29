"""
Foundry Agent Service (classic) quickstart-style client.

Key point:
- The agent + thread + run live in Foundry Agent Service.
- This script is still the *client/orchestrator* that drives those API calls.
"""

import os
from dotenv import load_dotenv

from azure.ai.agents import AgentsClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import CodeInterpreterTool

load_dotenv()

def main() -> None:
    # Use the *Foundry project endpoint*
    # Format: https://<AIFoundryResourceName>.services.ai.azure.com/api/projects/<ProjectName>
    project_endpoint = os.getenv("PROJECT_ENDPOINT") or os.getenv("AZURE_AI_PROJECT_ENDPOINT")
    if not project_endpoint:
        raise ValueError("Missing PROJECT_ENDPOINT (or AZURE_AI_PROJECT_ENDPOINT).")

    # Use the *project deployment name*
    model_deployment = os.getenv("MODEL_DEPLOYMENT_NAME") or os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
    if not model_deployment:
        raise ValueError("Missing MODEL_DEPLOYMENT_NAME (or AZURE_OPENAI_DEPLOYMENT_NAME).")

    # DefaultAzureCredential will work locally (Azure CLI), and also in Azure (Managed Identity)
    credential = DefaultAzureCredential()

    # Use AgentsClient directly (not AIProjectClient.agents)
    agents_client = AgentsClient(endpoint=project_endpoint, credential=credential)

    with agents_client:
        # Optional: attach built-in tool(s) that execute in the service.
        code_interpreter = CodeInterpreterTool()

        # Create agent in the service
        agent = agents_client.create_agent(
            model=model_deployment,
            name="Quickstart",
            instructions="Be concise.",
            tools=code_interpreter.definitions,
            tool_resources=code_interpreter.resources,
        )
        print(f"Created agent: {agent.id}")

        # Create thread in the service
        thread = agents_client.threads.create()
        print(f"Created thread: {thread.id}")

        # Create message in the service
        agents_client.messages.create(
            thread_id=thread.id,
            role="user",
            content="Write a haiku about Azure AI Foundry.",
        )

        # Create + process run in the service (server-side execution)
        run = agents_client.runs.create_and_process(
            thread_id=thread.id,
            agent_id=agent.id,
        )
        print(f"Run status: {run.status}")

        # Fetch conversation from the service
        messages = agents_client.messages.list(thread_id=thread.id)
        for m in messages:
            # Message content is structured; print the raw for now
            print(f"{m.role}: {m.content}")

        # Cleanup (optional)
        # agents_client.delete_agent(agent.id)
        # agents_client.threads.delete(thread.id)

if __name__ == "__main__":
    main()
