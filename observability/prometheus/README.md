# Observability learning track

Milestones:

1. Add application metrics with `prometheus-client`.
2. Expose a `/metrics` endpoint and measure request count, latency, and errors.
3. Add scrape configuration and validate target health.
4. Create alert rules for API availability, error ratio, and latency.
5. Build a Grafana dashboard and document alert response steps.

Avoid high-cardinality labels such as request IDs, user IDs, raw prompts, or arbitrary model input. Never put prompt or response content into metric labels.
