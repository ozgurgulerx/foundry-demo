"""
Hosted Agent - Microsoft Agent Framework Implementation

This agent can be deployed to Azure AI Foundry using:
  1. Azure Developer CLI (azd): azd up
  2. Manual SDK/CLI approach (see notebook)

Uses AzureAIClient for simplified Azure AI integration.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Agent Framework imports
from agent_framework.azure import AzureAIClient

# Hosting adapter
from azure.ai.agentserver.agentframework import from_agent_framework


def create_agent():
    """Create and configure the hosted agent using AzureAIClient."""

    # Get configuration from environment (set by hosted agent platform)
    model_deployment = os.getenv("MODEL_DEPLOYMENT_NAME", "gpt-4o-mini")

    print(f"Creating agent with model deployment: {model_deployment}")
    print(f"Project endpoint: {os.getenv('AZURE_AI_PROJECT_ENDPOINT', 'not set')}")

    # Use DefaultAzureCredential (works with managed identity in Azure)
    from azure.identity import DefaultAzureCredential
    credential = DefaultAzureCredential()

    # Create AzureAIClient - uses AZURE_AI_PROJECT_ENDPOINT env var automatically
    client = AzureAIClient(credential=credential)

    # Create agent with instructions
    agent = client.create_agent(
        instructions="""You are a helpful AI assistant running as a hosted agent on Azure AI Foundry.

You can help users with:
- Answering questions
- Providing explanations
- Having conversations

Be concise but helpful in your responses.""",
    )

    return agent


if __name__ == "__main__":
    # Create the agent
    print("Initializing hosted agent...")
    agent = create_agent()

    # Wrap with hosting adapter and start server
    # This exposes the agent as a Foundry-compatible HTTP service on port 8088
    print("Starting hosted agent server...")
    from_agent_framework(agent).run()
