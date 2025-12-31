"""Hosted Agent app (Python) - minimal skeleton.

This file is meant to run locally via hosting adapter on localhost:8088.
Later, it gets containerized for Foundry hosted agents.
"""

import os
from dotenv import load_dotenv

# NOTE: The exact import path can vary by package version.
# The hosting adapter concept is: wrap an agent into a Foundry-compatible HTTP service.
from azure.ai.agentserver.agentframework import from_agent_framework

# Your agent logic can be as simple or complex as you want.
# Here we define an ultra-minimal "agent" callable.
def my_agent(user_text: str) -> str:
    return f"You said: {user_text}. (Hosted agent skeleton)"

def main():
    load_dotenv()
    # The adapter will start an HTTP server with Foundry-compatible endpoints.
    # Docs conceptually show one-line hosting like: from_langgraph(my_agent).run()
    # For Agent Framework wrapper we use from_agent_framework.
    server = from_agent_framework(my_agent)
    server.run()  # Hosting adapter handles host/port internally

if __name__ == "__main__":
    main()
    