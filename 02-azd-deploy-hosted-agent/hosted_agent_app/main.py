"""
Hosted Agent - Microsoft Agent Framework Implementation

This agent can be deployed to Azure AI Foundry using:
  1. Azure Developer CLI (azd): azd up
  2. Manual SDK/CLI approach (see notebook)

The agent extends BaseAgent for proper streaming support and
thread management integration with Foundry.
"""

import os
import asyncio
from typing import AsyncIterable

from dotenv import load_dotenv

# Agent Framework imports
from agent_framework import BaseAgent
from agent_framework.models import (
    AgentRunRequest,
    AgentRunResponse,
    AgentRunResponseUpdate,
    Message,
    MessageDelta,
    Role,
)

# Hosting adapter
from azure.ai.agentserver.agentframework import from_agent_framework


class MyHostedAgent(BaseAgent):
    """
    A hosted agent that demonstrates the BaseAgent pattern.

    This pattern provides:
    - Synchronous and streaming response modes
    - Thread integration for conversation persistence
    - Proper message handling for Foundry compatibility
    """

    def __init__(
        self,
        name: str = "my-hosted-agent",
        description: str = "A hosted agent running on Azure AI Foundry",
        **kwargs
    ):
        super().__init__(name=name, description=description, **kwargs)
        self.model_deployment = os.getenv("MODEL_DEPLOYMENT_NAME", "gpt-4o")
        self.project_endpoint = os.getenv("AZURE_AI_PROJECT_ENDPOINT", "")

    def run(self, request: AgentRunRequest) -> AgentRunResponse:
        """
        Synchronous execution - returns complete response at once.

        Use this for simple request/response patterns.
        """
        # Extract the last user message
        user_message = self._get_last_user_message(request)

        # Generate response (replace with your actual agent logic)
        response_text = self._generate_response(user_message)

        # Create response message
        response_message = Message(
            role=Role.ASSISTANT,
            content=response_text
        )

        # Notify thread if present (for conversation persistence)
        if request.thread:
            self._notify_thread_of_new_messages(request.thread, [response_message])

        return AgentRunResponse(
            messages=[response_message]
        )

    async def run_stream(
        self, request: AgentRunRequest
    ) -> AsyncIterable[AgentRunResponseUpdate]:
        """
        Streaming execution - yields response chunks progressively.

        Use this for real-time response display and better UX.
        """
        # Extract the last user message
        user_message = self._get_last_user_message(request)

        # Generate response
        response_text = self._generate_response(user_message)

        # Stream response word by word for demonstration
        words = response_text.split()
        accumulated = []

        for i, word in enumerate(words):
            accumulated.append(word)

            # Yield partial update
            yield AgentRunResponseUpdate(
                delta=MessageDelta(
                    role=Role.ASSISTANT,
                    content=word + " "
                )
            )

            # Small delay to simulate streaming
            await asyncio.sleep(0.05)

        # Final message for thread notification
        final_message = Message(
            role=Role.ASSISTANT,
            content=" ".join(accumulated)
        )

        # Notify thread if present
        if request.thread:
            self._notify_thread_of_new_messages(request.thread, [final_message])

    def _get_last_user_message(self, request: AgentRunRequest) -> str:
        """Extract the last user message from the request."""
        if request.input and request.input.messages:
            for msg in reversed(request.input.messages):
                if msg.role == Role.USER:
                    return msg.content or ""
        return ""

    def _generate_response(self, user_message: str) -> str:
        """
        Generate a response to the user message.

        TODO: Replace this with your actual agent logic:
        - Call Azure OpenAI
        - Use LangChain/LangGraph
        - Implement custom business logic
        - Call external APIs
        """
        # Simple echo response for demonstration
        # In a real agent, you would:
        # 1. Call your LLM (Azure OpenAI, etc.)
        # 2. Use tools (code interpreter, web search, etc.)
        # 3. Implement your business logic

        return (
            f"You said: '{user_message}'\n\n"
            f"This is a hosted agent running on Azure AI Foundry. "
            f"Replace this response logic with your actual agent implementation."
        )


def get_agent() -> MyHostedAgent:
    """Factory function to create the agent instance."""
    load_dotenv()

    return MyHostedAgent(
        name=os.getenv("AGENT_NAME", "my-hosted-agent"),
        description="Hosted agent deployed via azd"
    )


if __name__ == "__main__":
    # Start the hosting adapter server
    # This exposes the agent as a Foundry-compatible HTTP service
    from_agent_framework(get_agent()).run()
