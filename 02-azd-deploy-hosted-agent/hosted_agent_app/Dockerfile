FROM python:3.11-slim

WORKDIR /app

# Install runtime deps
COPY . /app

RUN pip install --no-cache-dir -U pip     && pip install --no-cache-dir -U python-dotenv azure-identity azure-ai-projects     && pip install --no-cache-dir -U azure-ai-agentserver-core azure-ai-agentserver-agentframework

EXPOSE 8088

CMD ["python", "agent_app.py"]
