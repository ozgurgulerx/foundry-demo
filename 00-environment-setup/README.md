# 00 — Environment Setup

## Goal
Establish a repeatable local environment for the workshop (Python runtime, Azure CLIs, and baseline configuration) so every later step is runnable and traceable.

## You will end with
- A working Python environment for local agent runs
- `az` + `azd` installed and authenticated
- A `.env` file populated with the values used in later steps (kept out of git)

## Prerequisites
- Azure subscription with permission to create resources (Foundry, App Insights, APIM, Logic Apps, Search)

## Steps
1. Install tooling: `az`, `azd`, and your preferred Python (3.10+ recommended).
2. Create/activate a virtual environment.
3. Install Python dependencies from the repo root: `pip install -r requirements.txt`.
4. Copy `.env.example` → `.env` (repo root) and populate the values used by the early agent scripts.

## Proof (checklist)
- [ ] `az account show` returns the intended subscription
- [ ] `azd version` prints successfully
- [ ] `python3 --version` is 3.10+
- [ ] `pip install -r requirements.txt` succeeds

## Next
Continue to `../01-foundry-project-and-model-deployment`.
