"""
Chatbot Agent - Uses Azure OpenAI gpt-5-nano for responses
"""

import os
from typing import Any, AsyncIterable

from agent_framework import (
    AgentRunResponse,
    AgentRunResponseUpdate,
    AgentThread,
    BaseAgent,
    ChatMessage,
    Role,
    TextContent,
)
from azure.ai.agentserver.agentframework import from_agent_framework
from openai import AzureOpenAI


class ChatbotAgent(BaseAgent):
    """Chatbot agent powered by Azure OpenAI gpt-5-nano."""

    def __init__(self, name: str = "chatbot-agent", description: str = "Chatbot powered by gpt-5-nano", **kwargs):
        super().__init__(name=name, description=description, **kwargs)

        # Get Azure OpenAI configuration from environment
        self.project_endpoint = os.environ.get("AZURE_AI_PROJECT_ENDPOINT", "")
        self.model_deployment = os.environ.get("MODEL_DEPLOYMENT_NAME", "gpt-5-nano")

        # Initialize Azure OpenAI client using the project endpoint
        # The endpoint format is: https://<resource>.services.ai.azure.com/api/projects/<project>
        # We need to extract the base endpoint for Azure OpenAI
        base_endpoint = self.project_endpoint.split("/api/projects")[0] if "/api/projects" in self.project_endpoint else self.project_endpoint

        self.client = AzureOpenAI(
            azure_endpoint=base_endpoint,
            api_version="2024-12-01-preview",
            azure_ad_token_provider=self._get_token,
        )

    def _get_token(self) -> str:
        """Get Azure AD token for authentication."""
        from azure.identity import DefaultAzureCredential
        credential = DefaultAzureCredential()
        token = credential.get_token("https://cognitiveservices.azure.com/.default")
        return token.token

    def _extract_text(self, messages) -> list[dict]:
        """Convert input messages to OpenAI format."""
        openai_messages = []

        if messages is None:
            return openai_messages

        if isinstance(messages, str):
            openai_messages.append({"role": "user", "content": messages})
        elif isinstance(messages, ChatMessage):
            role = "user" if messages.role == Role.USER else "assistant"
            text = ""
            for content in messages.contents:
                if isinstance(content, TextContent):
                    text += content.text or ""
            openai_messages.append({"role": role, "content": text})
        elif isinstance(messages, list):
            for msg in messages:
                if isinstance(msg, str):
                    openai_messages.append({"role": "user", "content": msg})
                elif isinstance(msg, ChatMessage):
                    role = "user" if msg.role == Role.USER else "assistant"
                    text = ""
                    for content in msg.contents:
                        if isinstance(content, TextContent):
                            text += content.text or ""
                    openai_messages.append({"role": role, "content": text})

        return openai_messages

    async def run(
        self,
        messages: str | ChatMessage | list[str] | list[ChatMessage] | None = None,
        *,
        thread: AgentThread | None = None,
        **kwargs: Any,
    ) -> AgentRunResponse:
        # Convert messages to OpenAI format
        openai_messages = self._extract_text(messages)

        # Add system message
        system_message = {"role": "system", "content": "You are a helpful AI assistant."}
        all_messages = [system_message] + openai_messages

        # Call Azure OpenAI
        response = self.client.chat.completions.create(
            model=self.model_deployment,
            messages=all_messages,
        )

        # Extract response text
        response_text = response.choices[0].message.content or "I couldn't generate a response."

        # Build reply
        reply = ChatMessage(role=Role.ASSISTANT, contents=[TextContent(text=response_text)])

        # Persist conversation to the provided AgentThread (if any)
        if thread is not None:
            normalized = self._normalize_messages(messages)
            await self._notify_thread_of_new_messages(thread, normalized, reply)

        return AgentRunResponse(messages=[reply])

    async def run_stream(
        self,
        messages: str | ChatMessage | list[str] | list[ChatMessage] | None = None,
        *,
        thread: AgentThread | None = None,
        **kwargs: Any,
    ) -> AsyncIterable[AgentRunResponseUpdate]:
        # Convert messages to OpenAI format
        openai_messages = self._extract_text(messages)

        # Add system message
        system_message = {"role": "system", "content": "You are a helpful AI assistant."}
        all_messages = [system_message] + openai_messages

        # Call Azure OpenAI with streaming
        stream = self.client.chat.completions.create(
            model=self.model_deployment,
            messages=all_messages,
            stream=True,
        )

        # Collect full response for thread notification
        full_response = ""

        # Stream the response
        for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                full_response += content
                yield AgentRunResponseUpdate(
                    contents=[TextContent(text=content)],
                    role=Role.ASSISTANT
                )

        # Notify thread of input and the complete response once streaming ends
        if thread is not None:
            reply = ChatMessage(role=Role.ASSISTANT, contents=[TextContent(text=full_response)])
            normalized = self._normalize_messages(messages)
            await self._notify_thread_of_new_messages(thread, normalized, reply)


if __name__ == "__main__":
    print("Starting chatbot agent...")
    agent = ChatbotAgent(name="chatbot-agent", description="Chatbot powered by gpt-5-nano")
    from_agent_framework(agent).run()
