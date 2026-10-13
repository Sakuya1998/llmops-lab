# Week 1 — Build a service, not just a script

## Goals
- [ ] Create and activate a Python virtual environment.
- [ ] Install the project in editable mode.
- [ ] Run the API and inspect `/docs`.
- [ ] Run the test suite.
- [ ] Run Ruff and mypy; fix any issues rather than suppressing them blindly.
- [ ] Explain the difference between liveness and readiness.
- [ ] Write down why in-memory state disappears on restart and is not shared between replicas.

## Daily plan
- Day 1: local environment, run the API, explore the endpoints.
- Day 2: read `main.py` and `schemas.py`; explain each type and decorator.
- Day 3: add a delete endpoint with a 204 response and tests.
- Day 4: add structured request logging without logging prompts or secrets.
- Day 5: run checks, update this note, and summarize what failed and why.

## Questions to answer
1. What happens when Pydantic rejects an invalid request?
2. Why should an API return a stable error contract?
3. What does the container's non-root user protect against?
4. Which data must not be included in logs or metric labels?

## Notes
Add your own commands, errors, fixes, and observations here. Prefer real debugging notes over copied theory.
