FROM python:3.11-slim

WORKDIR /app

# Copy application code
COPY . /app

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -U pip \
    && pip install --no-cache-dir -r requirements.txt

# Expose the hosting adapter port
EXPOSE 8088

# Run the agent (main.py uses BaseAgent pattern)
CMD ["python", "main.py"]
