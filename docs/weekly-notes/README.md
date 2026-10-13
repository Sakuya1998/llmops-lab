# 每周学习记录

路线总表见 [六个月学习路线](../roadmap.md)。第 1 周已有具体任务单：[week-01.md](week-01.md)。

## 周记约定

每周结束时复制下面模板为 week-02.md 等文件。周记应记录实际执行的命令、Git commit、测试输出和个人理解；没有执行的项目保持未勾选，不要把预期结果写成事实。

## 模板

    # 第 N 周：主题

    ## 本周目标
    - [ ] 目标一
    - [ ] 目标二

    ## 对应路线与讲义
    - 路线章节：
    - 讲义：
    - 实验文件：

    ## 实际执行记录
    - 日期 / 环境 / Git commit：
    - 命令：
    - 关键输出：
    - 测试结果：

    ## 故障排查记录
    - 现象：
    - 假设：
    - 验证：
    - 根因（未知时写“待确认”）：
    - 修复：
    - 防止复发：

    ## 验收证据
    - [ ] 验收项一（附命令或证据）
    - [ ] 验收项二（附命令或证据）

    ## 复盘
    - 我能独立解释的概念：
    - 我仍不理解的内容：
    - 下周最小目标：

## 周次映射

| 周次 | 主题 | 讲义 / 实验入口 |
|---|---|---|
| 01 | Python 环境、API、测试 | [week-01](week-01.md) |
| 02 | 服务分层与配置 | [服务工程化](../learning-materials/python-service-engineering.md)、[配置与日志](../learning-materials/config-logging-security.md) |
| 03 | 超时、重试、幂等与日志安全 | [HTTP 可靠性](../learning-materials/http-reliability.md)、[配置与日志](../learning-materials/config-logging-security.md) |
| 04 | Docker 与 CI | [Docker/CI](../learning-materials/docker-ci.md)、[Docker 实验](../../deploy/docker/README.md) |
| 05 | 推理请求生命周期 | [推理基础](../learning-materials/llm-inference-fundamentals.md) |
| 06 | 显存与 KV Cache | [显存讲义](../learning-materials/gpu-memory-kv-cache.md) |
| 07 | vLLM 服务 | [vLLM 讲义](../learning-materials/vllm-serving.md)、[服务目录](../../serving/vllm/README.md) |
| 08 | 基准测试 | [基准脚本](../../serving/vllm/benchmark_openai_compatible.py) |
| 09 | Prometheus 指标 | [指标实验](../../observability/prometheus/README.md) |
| 10 | LLM 延迟与容量 | [SLO 讲义](../learning-materials/llm-observability-slo.md) |
| 11 | 仪表盘与告警 | [Prometheus 配置](../../observability/prometheus/prometheus.yml)、[告警](../../observability/prometheus/alerts.yml) |
| 12 | 故障诊断 | [SLO 讲义](../learning-materials/llm-observability-slo.md) |
| 13 | Kubernetes 网络 | [Kubernetes 讲义](../learning-materials/kubernetes-llm-serving.md)、[Deployment](../../deploy/kubernetes/api-deployment.yaml) |
| 14 | 探针与资源 | [Deployment](../../deploy/kubernetes/api-deployment.yaml) |
| 15 | GPU 调度与缓存 | [Kubernetes 模型服务](../learning-materials/kubernetes-llm-serving.md) |
| 16 | 发布与回滚 | [Kubernetes 模型服务](../learning-materials/kubernetes-llm-serving.md) |
| 17 | 合成评测数据 | [评测数据集](../../pipelines/evaluation/dataset.jsonl) |
| 18 | 评测指标 | [评测脚本](../../pipelines/evaluation/evaluate.py) |
| 19 | 基线与候选比较 | [评测实验](../../pipelines/evaluation/README.md) |
| 20 | 发布质量门禁 | [评测测试](../../tests/test_evaluation.py) |
| 21 | 综合集成 | [综合项目](../learning-materials/integrated-project.md) |
| 22 | 容量与成本 | [显存讲义](../learning-materials/gpu-memory-kv-cache.md)、[SLO 讲义](../learning-materials/llm-observability-slo.md) |
| 23 | 故障注入与恢复 | [可靠性讲义](../learning-materials/http-reliability.md) |
| 24 | 项目验收与展示 | [综合项目](../learning-materials/integrated-project.md) |

此表用于导航；只有提交实际执行证据后，才算完成对应周次。
