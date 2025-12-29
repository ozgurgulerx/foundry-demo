import os, asyncio
from dotenv import load_dotenv
from azure.identity.aio import AzureCliCredential
from azure.ai.agents.aio import AgentsClient
from agent_framework.azure import AzureAIAgentClient

load_dotenv()

async def main():
    endpoint = os.environ["AZURE_AI_PROJECT_ENDPOINT"]          # https://<project>.services.ai.azure.com/...
    deployment = os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"]   # Foundry *project* deployment name

    async with AzureCliCredential() as cred:
        async with AgentsClient(endpoint=endpoint, credential=cred) as client:
            async with AzureAIAgentClient(
                agents_client=client,
                model_deployment_name=deployment,
                should_cleanup_agent=True,
            ).create_agent(name="Quickstart", instructions="Be concise.") as agent:
                print(await agent.run("Write a haiku about Azure AI Foundry."))

if __name__ == "__main__":
    asyncio.run(main())
