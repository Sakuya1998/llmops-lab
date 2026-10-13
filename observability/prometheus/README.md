# 可观测性实验：从 API 指标到告警

本目录提供最小可复现的 Prometheus 入门实验。应用指标由 app/model_ops_api/main.py 暴露在 /metrics。

## 本地验证 API 指标

在仓库根目录执行：

    python -m pip install -e ".[dev]"
    uvicorn model_ops_api.main:app --app-dir app --host 127.0.0.1 --port 8000

另开一个终端执行：

    curl -fsS http://127.0.0.1:8000/health
    curl -fsS http://127.0.0.1:8000/metrics | grep '^llmops_http_requests_total'

访问几次 /health 后，llmops_http_requests_total 应出现 method、route、status 标签。/metrics 自身请求被排除，避免抓取流量污染业务请求指标。

## 启动 Prometheus（Docker）

在仓库根目录执行：

    docker run --rm --name llmops-prometheus -p 9090:9090 \
      -v "$PWD/observability/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml:ro" \
      -v "$PWD/observability/prometheus/alerts.yml:/etc/prometheus/alerts.yml:ro" \
      prom/prometheus:latest

配置中的 api:8000 是 Docker 网络内服务名。若 API 直接运行在宿主机，需要把 target 改成 Prometheus 容器可访问的宿主机地址；容器内 localhost 不指向宿主机。API 和 Prometheus 必须处于可互通网络。

检查 http://127.0.0.1:9090/targets，并查询 llmops_http_requests_total。建议先用 Docker Compose 创建同一网络中的 API 与 Prometheus，再做长期实验。

## 指标设计注意事项

- 避免高基数标签，例如 request ID、user ID、原始提示词或任意用户输入。
- 不要把提示词、模型回答或其他敏感内容写入指标标签。
- 当前样例只统计 HTTP 请求量和时延，不代表模型推理时延、token 吞吐或 GPU 指标。
- up 告警代表抓取目标可达性，不等于业务 SLO；后续应基于真实流量补充错误率、延迟和饱和度告警。
- 镜像 tag 仅为教学示例；生产环境应固定已验证版本或 digest。
