"""对 OpenAI-compatible /v1/chat/completions 端点做简单并发基准。

仅用于已授权的测试环境。该脚本不创建云资源、不下载模型、不输出提示词内容。
"""

from __future__ import annotations

import argparse
import json
import os
import statistics
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any


def request_once(
    url: str, model: str, prompt: str, token: str | None, timeout: float
) -> dict[str, Any]:
    payload = json.dumps(
        {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 32,
            "temperature": 0,
        }
    ).encode()
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, data=payload, headers=headers, method="POST")
    started = time.perf_counter()
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = json.loads(response.read().decode("utf-8"))
            elapsed = time.perf_counter() - started
            usage = body.get("usage", {})
            return {
                "ok": 200 <= response.status < 300,
                "status": response.status,
                "latency_seconds": elapsed,
                "prompt_tokens": usage.get("prompt_tokens"),
                "completion_tokens": usage.get("completion_tokens"),
            }
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        return {
            "ok": False,
            "status": "error",
            "latency_seconds": time.perf_counter() - started,
            "error_type": type(exc).__name__,
        }


def percentile(values: list[float], p: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    index = min(len(ordered) - 1, max(0, int((len(ordered) - 1) * p)))
    return ordered[index]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default="http://127.0.0.1:8001/v1/chat/completions")
    parser.add_argument("--model", required=True)
    parser.add_argument("--requests", type=int, default=10)
    parser.add_argument("--concurrency", type=int, default=2)
    parser.add_argument("--timeout", type=float, default=60)
    parser.add_argument("--token-env", default="VLLM_API_KEY", help="读取 token 的环境变量名")
    parser.add_argument("--prompt", default="只回答单词 ready。")
    parser.add_argument("--report", help="可选 JSON 报告路径")
    args = parser.parse_args()

    if args.requests < 1 or args.concurrency < 1 or args.timeout <= 0:
        parser.error("requests/concurrency 必须 >= 1，timeout 必须 > 0")
    token = os.environ.get(args.token_env)
    started = time.perf_counter()
    results: list[dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=args.concurrency) as pool:
        futures = [
            pool.submit(request_once, args.url, args.model, args.prompt, token, args.timeout)
            for _ in range(args.requests)
        ]
        for future in as_completed(futures):
            results.append(future.result())

    elapsed = time.perf_counter() - started
    latencies = [item["latency_seconds"] for item in results]
    successful = [item for item in results if item["ok"]]
    report = {
        "url": args.url,
        "model": args.model,
        "requests": args.requests,
        "concurrency": args.concurrency,
        "successes": len(successful),
        "failures": len(results) - len(successful),
        "elapsed_seconds": elapsed,
        "requests_per_second": len(successful) / elapsed if elapsed else 0,
        "latency_seconds": {
            "p50": percentile(latencies, 0.50),
            "p95": percentile(latencies, 0.95),
            "mean": statistics.fmean(latencies) if latencies else None,
        },
        "prompt_tokens": sum(item.get("prompt_tokens") or 0 for item in successful),
        "completion_tokens": sum(item.get("completion_tokens") or 0 for item in successful),
    }
    rendered = json.dumps(report, ensure_ascii=False, indent=2)
    print(rendered)
    if args.report:
        Path(args.report).parent.mkdir(parents=True, exist_ok=True)
        Path(args.report).write_text(rendered + "\n", encoding="utf-8")
    return 0 if report["failures"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
