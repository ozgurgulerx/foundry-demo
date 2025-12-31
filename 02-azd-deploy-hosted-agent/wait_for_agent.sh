#!/bin/bash
echo "Waiting for agent to start..."
for i in {1..30}; do
  status=$(az cognitiveservices agent start \
    --account-name ozgurguler-7212-resource \
    --project-name ozgurguler-7212 \
    --name my-hosted-agent \
    --agent-version 8 \
    -o json 2>/dev/null)

  container_status=$(echo "$status" | jq -r '.container.status')
  overall_status=$(echo "$status" | jq -r '.status')
  error_msg=$(echo "$status" | jq -r '.container.error_message // empty')

  echo "[$i/30] Status: $overall_status, Container: $container_status"

  if [ "$container_status" = "Running" ] || [ "$overall_status" = "Succeeded" ]; then
    echo ""
    echo "Agent is running!"
    echo "$status" | jq
    exit 0
  fi

  if [ -n "$error_msg" ] && [ "$error_msg" != "null" ]; then
    echo ""
    echo "Error: $error_msg"
    echo "$status" | jq
    exit 1
  fi

  sleep 10
done

echo ""
echo "Timeout - agent is still starting. Check again later."
