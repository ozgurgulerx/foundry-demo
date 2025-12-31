"""
Deploy Chat Agent with Azure OpenAI

This script creates a new hosted agent version with proper environment variables
for Azure OpenAI connectivity.
"""

import subprocess
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    ImageBasedHostedAgentDefinition,
    ProtocolVersionRecord,
    AgentProtocol,
)

# Configuration
PROJECT_ENDPOINT = "https://ozgurguler-7212-resource.services.ai.azure.com/api/projects/ozgurguler-7212"
HOSTED_AGENT_NAME = "my-hosted-agent"
ACR_NAME = "aicontainervault01"
IMAGE_TAG = "chat-v1"  # New tag for chat agent

# Build and push the image first
print("=" * 60)
print("Step 1: Building and pushing container image")
print("=" * 60)

IMAGE_REF = f"{ACR_NAME}.azurecr.io/{HOSTED_AGENT_NAME}:{IMAGE_TAG}"
print(f"Image: {IMAGE_REF}")

# Build the image
print("\nBuilding Docker image...")
subprocess.run([
    "docker", "build",
    "-t", f"{HOSTED_AGENT_NAME}:{IMAGE_TAG}",
    "-t", IMAGE_REF,
    "./src/my-hosted-agent"
], check=True)

# Login to ACR and push
print("\nLogging into ACR...")
subprocess.run(["az", "acr", "login", "--name", ACR_NAME], check=True)

print("\nPushing image to ACR...")
subprocess.run(["docker", "push", IMAGE_REF], check=True)

# Create agent version with SDK
print("\n" + "=" * 60)
print("Step 2: Creating hosted agent version")
print("=" * 60)

credential = DefaultAzureCredential()
client = AIProjectClient(endpoint=PROJECT_ENDPOINT, credential=credential)

# Environment variables for the container
env_vars = {
    "AZURE_AI_PROJECT_ENDPOINT": PROJECT_ENDPOINT,
    "AZURE_OPENAI_ENDPOINT": "https://ozgurguler-7212-resource.openai.azure.com/",
    "MODEL_DEPLOYMENT_NAME": "gpt-5-nano",
}

print(f"\nAgent: {HOSTED_AGENT_NAME}")
print(f"Image: {IMAGE_REF}")
print("Environment variables:")
for k, v in env_vars.items():
    print(f"  {k}: {v}")

# Create new version
agent_version = client.agents.create_version(
    agent_name=HOSTED_AGENT_NAME,
    description="Chat agent with Azure OpenAI (gpt-5-nano)",
    definition=ImageBasedHostedAgentDefinition(
        container_protocol_versions=[
            ProtocolVersionRecord(protocol=AgentProtocol.RESPONSES, version="v1")
        ],
        cpu="1",
        memory="2Gi",
        image=IMAGE_REF,
        environment_variables=env_vars,
    ),
)

version = agent_version.version if hasattr(agent_version, "version") else "?"
print(f"\nCreated version: {version}")
print(f"Status: {agent_version.status if hasattr(agent_version, 'status') else 'unknown'}")

# Start the agent
print("\n" + "=" * 60)
print("Step 3: Starting agent")
print("=" * 60)

client.agents.start(agent_name=HOSTED_AGENT_NAME)
print("Start command sent. Agent is now deploying.")
print(f"\nAgent endpoint: {PROJECT_ENDPOINT}/agents/{HOSTED_AGENT_NAME}/versions/{version}")
