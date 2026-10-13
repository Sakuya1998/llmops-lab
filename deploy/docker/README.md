# Docker

Build and run from the repository root:

```bash
docker build -t llmops-lab-api:dev .
docker run --rm -p 8000:8000 llmops-lab-api:dev
curl -fsS http://127.0.0.1:8000/health
```

The image runs as UID/GID 10001 and contains only the application runtime dependencies. For production, pin the base image by digest, scan the image, define resource limits, and run behind an authenticated ingress if the API is exposed beyond a trusted local environment.
