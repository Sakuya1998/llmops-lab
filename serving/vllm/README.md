# vLLM serving track

This directory will hold reproducible model-serving experiments.

Study sequence:

1. Understand GPU memory, model weights, KV cache, batching, and context length.
2. Run a small compatible model in a disposable environment.
3. Record throughput, time to first token, inter-token latency, concurrency, and GPU utilization.
4. Compare safe baseline settings before changing tensor parallelism or batching.
5. Add health checks, resource requests, rollout strategy, and operational runbooks before Kubernetes deployment.

Model availability and hardware requirements vary. Start with a model whose license permits your intended use, and never expose an unauthenticated inference endpoint to the public internet.
