# 03 — Entra Agent ID + Conditional Access (Preview)

## Goal
Attach an Entra "Agent ID" Conditional Access policy to the hosted agent identity and demonstrate measurable enforcement.

An agent identity is a specialized identity in Microsoft Entra ID for AI agents. Hosted agents in Foundry use the project's managed identity by default.

## You will end with
- Understanding of how hosted agents use managed identities
- A Conditional Access policy targeting the agent identity
- A triggerable allow/deny condition to demonstrate enforcement
- Visibility into CA evaluation via sign-in logs

## Prerequisites
- Completed `../02-azd-deploy-hosted-agent` (working hosted agent)
- Microsoft Entra ID P1 or P2 license (for Conditional Access)
- Conditional Access Administrator role

## Demo Approach
The simplest demonstration:
1. Find the hosted agent's principal ID
2. Create a CA policy that blocks the agent from accessing Azure Cognitive Services
3. Enable the policy and observe the agent fail
4. Check sign-in logs for CA evaluation
5. Disable the policy to restore functionality

## Proof (checklist)
- [ ] Agent's principal ID identified
- [ ] CA policy exists targeting the agent identity
- [ ] Policy blocks agent when enabled (agent invocation fails)
- [ ] Entra sign-in logs show CA result (blocked/allowed)

## Next
Continue to `../04-foundry-agent-memory`.
