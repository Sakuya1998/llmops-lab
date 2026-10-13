# LLMOps Lab

A hands-on learning lab for moving from Site Reliability / Operations Engineering into **AI Infrastructure and LLMOps**.

The repository is organized as a progressive, six-month portfolio. Start small: build and test an API, containerize it, observe it, deploy it, then add model serving and evaluation workflows.

## Learning profile

- Background: operations engineering, Linux, shell/Python automation, cloud, Kubernetes, monitoring.
- Pace: 1–2 hours per day.
- Approach: every topic should produce a runnable artifact, a test, or an operational runbook.

## Roadmap

| Phase | Focus | Deliverable |
|---|---|---|
| 1 | Python service engineering | FastAPI model registry API, tests, lint/type checks |
| 2 | Model serving fundamentals | vLLM deployment notes, benchmark plan, resource considerations |
| 3 | Observability | Prometheus metrics, alert rules, Grafana dashboard plan |
| 4 | Kubernetes operations | manifests, probes, resources, rollout and rollback runbooks |
| 5 | LLMOps | evaluation dataset, repeatable evaluation job, release gates |
| 6 | Portfolio & reliability | end-to-end demo, failure drills, architecture and incident docs |

## Quick start

Requires Python 3.11+.

```bash
git clone https://github.com/Sakuya1998/llmops-lab.git
cd llmops-lab
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
uvicorn model_ops_api.main:app --reload --app-dir app
```

Open the interactive API docs at http://127.0.0.1:8000/docs.

Run checks:

```bash
pytest
ruff check .
ruff format --check .
mypy app
```

## API endpoints

- `GET /health` — liveness-style health response.
- `POST /api/v1/models` — register a model deployment record.
- `GET /api/v1/models` — list registered model records.
- `GET /api/v1/models/{model_id}` — retrieve one record.

The first version uses in-memory storage intentionally. It is a learning exercise, **not** durable storage or a production model registry.

## Repository map

- `app/model_ops_api/` — API and domain schemas.
- `tests/` — automated tests.
- `serving/vllm/` — model-serving notes and examples.
- `observability/` — Prometheus rules and metrics design.
- `deploy/` — Docker and Kubernetes examples.
- `pipelines/evaluation/` — evaluation workflow starter.
- `docs/` — roadmap, weekly notes, architecture, runbooks.
- `scripts/` — local developer helpers.

## Safety and scope

- Never commit credentials, API keys, private datasets, or production configuration.
- Copy `.env.example` to `.env` for local experiments; `.env` is git-ignored.
- Kubernetes and model-serving examples are educational; review resource limits, access controls, image versions, and storage before any real deployment.
- Do not send confidential company data to third-party model APIs.

## Weekly learning loop

1. Read one concept.
2. Implement a small change.
3. Add or update a test.
4. Run checks locally.
5. Write down one operational failure mode and how to detect/recover from it.

See [the roadmap](docs/roadmap.md) and [week 1 plan](docs/weekly-notes/week-01.md).
