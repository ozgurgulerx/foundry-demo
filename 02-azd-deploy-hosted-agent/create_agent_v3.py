import os
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    ImageBasedHostedAgentDefinition,
    ProtocolVersionRecord,
    AgentProtocol,
)

# Load from azd environment
endpoint = "https://ozgurguler-7212-resource.services.ai.azure.com/api/projects/ozgurguler-7212"

# Set up credentials and client
credential = DefaultAzureCredential()
client = AIProjectClient(endpoint=endpoint, credential=credential)

HOSTED_AGENT_NAME = "my-hosted-agent"
IMAGE_REF = "containervault01.azurecr.io/my-hosted-agent:v8"
HOSTED_CPU = "1"
HOSTED_MEMORY = "2Gi"
CONTAINER_PROTOCOL_VERSION = "v1"

env_vars = {
    "AZURE_AI_PROJECT_ENDPOINT": endpoint,
    "AZURE_AI_MODEL_DEPLOYMENT_NAME": "gpt-4o-mini",
}

print(f"Creating agent version for {HOSTED_AGENT_NAME}")
print(f"  Image: {IMAGE_REF}")
print(f"  CPU: {HOSTED_CPU}, Memory: {HOSTED_MEMORY}")

# Create new version with v3 image
agent_version = client.agents.create_version(
    agent_name=HOSTED_AGENT_NAME,
    description="v14: Echo agent with correct protocol version v1, v8 image",
    definition=ImageBasedHostedAgentDefinition(
        container_protocol_versions=[
            ProtocolVersionRecord(protocol=AgentProtocol.RESPONSES, version=CONTAINER_PROTOCOL_VERSION)
        ],
        cpu=HOSTED_CPU,
        memory=HOSTED_MEMORY,
        image=IMAGE_REF,
        environment_variables=env_vars,
    ),
)

CREATED_VERSION = agent_version.version if hasattr(agent_version, "version") else "?"

print(f"\nCreated agent version: {CREATED_VERSION}")
print(f"Status: {agent_version.status if hasattr(agent_version, 'status') else 'unknown'}")

# Start the agent
print("\nStarting agent...")
client.agents.start(agent_name=HOSTED_AGENT_NAME)
print("Start command sent. Agent is now deploying.")
