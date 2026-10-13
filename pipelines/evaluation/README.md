# LLM evaluation pipeline (planned)

The first evaluation milestone should be deterministic and inexpensive:

- Keep a small, versioned, synthetic dataset in the repository.
- Define task-specific checks before selecting a model.
- Record model identifier, model revision, prompt version, parameters, latency, and token usage.
- Separate hard correctness checks from human preference review.
- Compare candidate and baseline results before a release.
- Set explicit thresholds and fail the pipeline when regression limits are exceeded.

Never commit private production prompts, customer data, credentials, or licensed datasets without permission.
