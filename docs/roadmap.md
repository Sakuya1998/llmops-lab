# Six-month roadmap

## Month 1 — Python service engineering
- Week 1: virtual environments, packaging, type hints, API basics, pytest.
- Week 2: validation, error handling, structured logging, configuration.
- Week 3: Docker image, non-root user, health probes.
- Week 4: CI, code quality, test coverage, API contract documentation.

**Exit criteria:** a reproducible API that passes tests and CI from a clean checkout.

## Month 2 — Model serving
- Learn inference lifecycle, GPU memory, quantization, batching, and KV cache.
- Run a compatible model locally or in a disposable GPU environment.
- Benchmark latency and throughput with a documented methodology.

**Exit criteria:** a repeatable benchmark report and a model-serving runbook.

## Month 3 — Observability
- Instrument request count, latency, errors, queue depth, and model-specific metrics.
- Build Prometheus alerts and a Grafana dashboard.
- Practice diagnosing availability, latency, and saturation symptoms.

**Exit criteria:** dashboard, alerts, and a short incident playbook.

## Month 4 — Kubernetes
- Package the API and inference service for Kubernetes.
- Add probes, requests/limits, security context, rollout and rollback.
- Study GPU scheduling and node capacity if GPU infrastructure is available.

**Exit criteria:** reproducible deployment manifests and tested rollback steps.

## Month 5 — LLMOps
- Build a small synthetic evaluation dataset.
- Version prompts and evaluation configuration.
- Add baseline/candidate comparisons and a release gate.

**Exit criteria:** evaluation results are repeatable and can block a regressed release.

## Month 6 — Portfolio and reliability
- Connect API, serving, observability, and evaluation into one demonstrable workflow.
- Perform failure drills: model unavailable, slow inference, bad release, exhausted capacity.
- Document architecture, trade-offs, known limitations, and recovery procedures.

**Exit criteria:** a clean demo, operational docs, and a portfolio README.

## Weekly cadence (1–2 hours/day)
- 3 days: learn and implement.
- 1 day: tests and debugging.
- 1 day: docs and operational notes.
- Weekend: review progress and choose one small next milestone.
