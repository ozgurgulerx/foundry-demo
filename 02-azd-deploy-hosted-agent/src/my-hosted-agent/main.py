"""
Minimal Echo Agent - Tests hosting adapter without external API calls
"""

import asyncio
from typing import AsyncIterable

from agent_framework import BaseAgent
from agent_framework.models import (
    AgentRunRequest,
    AgentRunResponse,
    AgentRunResponseUpdate,
    Message,
    MessageDelta,
    Role,
)
from azure.ai.agentserver.agentframework import from_agent_framework


class EchoAgent(BaseAgent):
    """Simple echo agent for testing."""

    def run(self, request: AgentRunRequest) -> AgentRunResponse:
        # Extract last user message
        user_msg = self._get_last_user_message(request)

        # Echo back
        response_text = f"Echo: {user_msg}"
        response_message = Message(role=Role.ASSISTANT, content=response_text)

        # Notify thread if present
        if request.thread:
            self._notify_thread_of_new_messages(request.thread, [response_message])

        return AgentRunResponse(messages=[response_message])

    async def run_stream(self, request: AgentRunRequest) -> AsyncIterable[AgentRunResponseUpdate]:
        # Extract last user message
        user_msg = self._get_last_user_message(request)

        # Echo back
        response_text = f"Echo: {user_msg}"

        # Stream word by word
        words = response_text.split()
        for word in words:
            yield AgentRunResponseUpdate(
                delta=MessageDelta(role=Role.ASSISTANT, content=word + " ")
            )
            await asyncio.sleep(0.02)

        # Notify thread if present
        final_message = Message(role=Role.ASSISTANT, content=response_text)
        if request.thread:
            self._notify_thread_of_new_messages(request.thread, [final_message])

    def _get_last_user_message(self, request: AgentRunRequest) -> str:
        """Extract the last user message from the request."""
        if request.input and request.input.messages:
            for msg in reversed(request.input.messages):
                if msg.role == Role.USER:
                    return msg.content or ""
        return ""


if __name__ == "__main__":
    print("Starting echo agent...")
    agent = EchoAgent(name="echo-agent", description="Simple echo agent")
    from_agent_framework(agent).run()
