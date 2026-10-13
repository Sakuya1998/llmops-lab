# Starter architecture

```text
Developer
   |
   v
FastAPI HTTP layer
   |
   +--> Pydantic request validation
   |
   +--> In-memory model metadata store (temporary learning implementation)
```

## Intentional limitations

- No authentication or authorization: run locally only.
- No persistent database: restart clears records and replicas do not share state.
- No external model invocation: records describe deployments; they do not serve inference.
- The `/health` endpoint is a simple liveness response, not a dependency readiness check.
- No production SLO or load-test claim has been made.

## Evolution path

1. Separate API/domain logic from storage behind a repository interface.
2. Add structured logs, request IDs, and Prometheus metrics.
3. Add persistence only after defining ownership, migrations, and failure behavior.
4. Add authn/authz before exposing control endpoints.
5. Integrate inference through explicit timeouts, bounded concurrency, retries only where safe, and clear error mapping.
