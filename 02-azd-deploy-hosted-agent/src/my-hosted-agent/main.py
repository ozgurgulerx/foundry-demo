"""
Minimal Echo Agent - Tests hosting adapter without external API calls
"""

import os
from agent_framework import BaseAgent, AgentRunResponse, AgentRunResponseUpdate, ChatMessage, Role
from azure.ai.agentserver.agentframework import from_agent_framework


class EchoAgent(BaseAgent):
    """Simple echo agent for testing."""

    async def run(self, messages=None, **kwargs):
        # Extract user message
        user_msg = ""
        if isinstance(messages, str):
            user_msg = messages
        elif isinstance(messages, ChatMessage):
            user_msg = messages.text or ""
        elif isinstance(messages, list) and messages:
            last = messages[-1]
            user_msg = last if isinstance(last, str) else (last.text or "")

        # Echo back
        response_text = f"Echo: {user_msg}"
        return AgentRunResponse(messages=[ChatMessage(Role.ASSISTANT, text=response_text)])

    async def run_stream(self, messages=None, **kwargs):
        # Extract user message
        user_msg = ""
        if isinstance(messages, str):
            user_msg = messages
        elif isinstance(messages, ChatMessage):
            user_msg = messages.text or ""
        elif isinstance(messages, list) and messages:
            last = messages[-1]
            user_msg = last if isinstance(last, str) else (last.text or "")

        # Echo back as streaming update
        response_text = f"Echo: {user_msg}"
        yield AgentRunResponseUpdate(messages=[ChatMessage(Role.ASSISTANT, text=response_text)])


if __name__ == "__main__":
    print("Starting echo agent...")
    agent = EchoAgent(name="echo-agent", description="Simple echo agent")
    from_agent_framework(agent).run()
