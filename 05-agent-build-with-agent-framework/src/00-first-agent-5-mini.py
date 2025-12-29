import os
import asyncio
from agent_framework.azure import AzureOpenAIResponsesClient
from dotenv import load_dotenv

load_dotenv()

async def main():
    # Initialize a chat agent with Azure OpenAI Responses
    # the endpoint, deployment name, and api version can be set via environment variables
    # or they can be passed in directly to the AzureOpenAIResponsesClient constructor
    # make sure you are using "AZURE_OPENAI_VERSION=v1"
    agent = AzureOpenAIResponsesClient(
        endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        deployment_name=os.environ["AZURE_OPENAI_REASONING_DEPLOYMENT_NAME"],
        api_version=os.environ["AZURE_OPENAI_API_VERSION"],
        api_key=os.environ["AZURE_OPENAI_API_KEY"],  # Optional if using AzureCliCredential

    ).create_agent(
        name="physicsbot",
        instructions="You are professor in astrophysics",
	reasoning_effort="minimal", 
    )

    print(await agent.run("Are we in a blackhole?"))

if __name__ == "__main__":
    asyncio.run(main())
