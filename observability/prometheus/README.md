# 可观测性实验：从 API 指标到告警

本目录提供最小可复现的 Prometheus 入门实验。应用指标由 app/model_ops_api/main.py 暴露在 /metrics。

## 1. 启动完整实验栈

在仓库根目录执行（需要 Docker Compose）：

    docker compose -f compose.yaml up --build

访问 API 文档 http://127.0.0.1:8000/docs，Prometheus http://127.0.0.1:9090。查看 Prometheus 的 Status -> Targets 页面，确认 llmops-lab-api 抓取目标为 UP。停止并清理容器：

    docker compose -f compose.yaml down

## 2. 观察指标

另开终端，多次请求 API：

    curl -fsS http://127.0.0.1:8000/health
    curl -fsS http://127.0.0.1:8000/metrics | grep '^llmops_http_requests_total'

访问几次 /health 后，llmops_http_requests_total 应出现 method、route、status 标签。/metrics 自身请求被排除，避免抓取流量污染业务请求指标。也可在 Prometheus 查询页运行 llmops_http_requests_total。

## 3. 理解指标和告警

prometheus.yml 将 API 配置为 api:8000，这是 Compose 网络内的服务名。若独立运行 Prometheus，必须按实际网络修改 target；容器内 localhost 不指向宿主机。

当前应用只记录 HTTP 请求量和时延，不包含真实模型推理时延、token 吞吐或 GPU 指标。up 告警只表示抓取目标可达性，不等于业务 SLO。后续可按真实流量补充错误率、延迟、饱和度和模型推理指标。

## 指标设计注意事项

- 避免高基数标签，例如 request ID、user ID、原始提示词或任意用户输入。
- 不要把提示词、模型回答或其他敏感内容写入指标标签。
- 指标用于聚合和趋势分析；排查单次请求时，应使用经过脱敏的日志和追踪信息。
- 告警阈值应结合服务 SLO、流量基线和实际故障演练逐步确定。
- Compose 使用的 Prometheus 版本固定为教学版本；生产环境应按组织流程升级和验证镜像。
