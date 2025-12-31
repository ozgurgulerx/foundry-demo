"""
Hosted Agent - Azure OpenAI Chat

Uses gpt-5-nano for intelligent conversations.
"""

import os
from typing import Any
from collections.abc import AsyncIterable

# Agent Framework imports
from agent_framework import BaseAgent, AgentRunResponse, AgentRunResponseUpdate, AgentThread, ChatMessage

# Hosting adapter
from azure.ai.agentserver.agentframework import from_agent_framework


class ChatAgent(BaseAgent):
    """A chat agent powered by Azure OpenAI."""

    def __init__(self):
        super().__init__(
            name="chat-agent",
            description="A helpful AI assistant powered by Azure OpenAI"
        )
        self._client = None

    def _get_client(self):
        """Lazy initialization of OpenAI client."""
        if self._client is None:
            from openai import AzureOpenAI
            from azure.identity import DefaultAzureCredential, get_bearer_token_provider

            token_provider = get_bearer_token_provider(
                DefaultAzureCredential(),
                "https://cognitiveservices.azure.com/.default"
            )
            self._client = AzureOpenAI(
                azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT", "https://ozgurguler-7212-resource.openai.azure.com/"),
                azure_ad_token_provider=token_provider,
                api_version="2024-02-15-preview",
            )
        return self._client

    def _get_user_message(self, messages) -> str:
        """Extract user message text."""
        if messages is None:
            return ""
        if isinstance(messages, str):
            return messages
        if isinstance(messages, ChatMessage):
            return messages.text or ""
        if isinstance(messages, list) and len(messages) > 0:
            last = messages[-1]
            return last if isinstance(last, str) else (last.text or "")
        return str(messages)

    async def run(
        self,
        messages: str | ChatMessage | list[str] | list[ChatMessage] | None = None,
        *,
        thread: AgentThread | None = None,
        **kwargs: Any,
    ) -> AgentRunResponse:
        """Get a response from Azure OpenAI."""
        user_msg = self._get_user_message(messages)
        client = self._get_client()
        deployment = os.getenv("MODEL_DEPLOYMENT_NAME", "gpt-5-nano")

        response = client.chat.completions.create(
            model=deployment,
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": user_msg}
            ]
        )

        return AgentRunResponse(text=response.choices[0].message.content)

    async def run_stream(
        self,
        messages: str | ChatMessage | list[str] | list[ChatMessage] | None = None,
        *,
        thread: AgentThread | None = None,
        **kwargs: Any,
    ) -> AsyncIterable[AgentRunResponseUpdate]:
        """Stream response from Azure OpenAI."""
        user_msg = self._get_user_message(messages)
        client = self._get_client()
        deployment = os.getenv("MODEL_DEPLOYMENT_NAME", "gpt-5-nano")

        stream = client.chat.completions.create(
            model=deployment,
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": user_msg}
            ],
            stream=True
        )

        for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                yield AgentRunResponseUpdate(text=chunk.choices[0].delta.content)


if __name__ == "__main__":
    print("Initializing chat agent...")
    print(f"Project endpoint: {os.getenv('AZURE_AI_PROJECT_ENDPOINT', 'not set')}")

    agent = ChatAgent()

    print("Starting hosted agent server on port 8088...")
    from_agent_framework(agent).run()
