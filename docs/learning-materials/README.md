# 系统化学习资料

本目录提供与仓库代码配套的中文讲义。目标不是一次读完百科，而是每天 1–2 小时，通过“理解概念—检查代码—动手实验—验证结果—复盘”逐步构建 AI Infra / LLMOps 能力。

## 全课程地图

| 阶段 | 资料 | 预计投入 | 主要产出 |
|---|---|---:|---|
| 0. 开发基础 | [Python 环境与依赖](python-environment.md)、[Python 服务工程化](python-service-engineering.md) | 1–2 周 | 可复现的开发环境、清晰的代码分层 |
| 1. API 与测试 | [HTTP、FastAPI、Pydantic](fastapi-and-pydantic.md)、[pytest 测试](pytest-testing.md)、[HTTP 可靠性](http-reliability.md) | 2–3 周 | API 契约、异常处理、测试套件 |
| 2. 配置与交付 | [配置、日志与安全](config-logging-security.md)、[Docker 与健康探针](docker-healthchecks.md)、[Docker 与 CI](docker-ci.md) | 2–3 周 | 安全日志、容器镜像、CI 验证 |
| 3. 推理基础 | [LLM 推理基础](llm-inference-fundamentals.md)、[GPU 显存与 KV Cache](gpu-memory-kv-cache.md)、[vLLM 运维](vllm-serving.md) | 3–4 周 | 推理架构图、容量估算、基准报告 |
| 4. 可观测性 | [LLM 可观测性与 SLO](llm-observability-slo.md) | 2–3 周 | 指标、仪表盘、告警和排障手册 |
| 5. Kubernetes | [Kubernetes 模型服务](kubernetes-llm-serving.md) | 3–4 周 | 部署清单、发布/回滚和资源规划 |
| 6. LLMOps | [评测与发布门禁](llm-evaluation-release.md)、[LLM 安全](llm-security.md) | 3–4 周 | 可重复评测、回归门禁、安全用例 |
| 7. 综合项目 | [综合项目设计](integrated-project.md) | 3–4 周 | 可演示的端到端项目 |

这是一条约六个月的路线，而不是严格的日历承诺。遇到基础薄弱的部分可以延长；阶段验收未通过时，不必为了赶进度跳过。

## 推荐顺序

### 第一阶段：先把服务工程化打牢

1. [Python 开发环境与依赖管理](python-environment.md)
2. [HTTP、FastAPI 与 Pydantic](fastapi-and-pydantic.md)
3. [pytest 与测试设计](pytest-testing.md)
4. [Python 服务工程化](python-service-engineering.md)
5. [配置、结构化日志与服务安全](config-logging-security.md)
6. [HTTP 服务可靠性](http-reliability.md)
7. [Docker、进程与健康探针](docker-healthchecks.md)
8. [Docker 镜像与 CI 流水线](docker-ci.md)

### 第二阶段：理解并运营模型推理

9. [大语言模型推理基础](llm-inference-fundamentals.md)
10. [GPU 显存、模型权重与 KV Cache](gpu-memory-kv-cache.md)
11. [vLLM 模型服务与运维](vllm-serving.md)

### 第三阶段：把推理服务变成可运营系统

12. [LLM 服务可观测性与 SLO](llm-observability-slo.md)
13. [Kubernetes 上运行模型服务](kubernetes-llm-serving.md)
14. [LLM 评测、回归测试与发布门禁](llm-evaluation-release.md)
15. [LLM 应用与模型服务安全](llm-security.md)
16. [综合项目：可观测、可评测的模型服务平台](integrated-project.md)

## 每次学习的固定流程

1. **目标（5 分钟）**：今天要解释或实现什么？
2. **阅读（15–25 分钟）**：读一个小节，不要一次通读整份文档。
3. **动手（25–50 分钟）**：运行命令、检查代码或完成一个小改动。
4. **验证（10–20 分钟）**：执行测试、观察输出、对比预期。
5. **复盘（5–10 分钟）**：记录学会的内容、失败原因和遗留问题。

## 学习原则

- 先用本地 mock、合成数据和免费工具完成工程链路；真实 GPU、云资源和付费 API 都是可选项。
- 先理解故障模式，再添加组件。不要为了“生产级”一开始就引入复杂技术。
- 示例代码是教学材料，不自动等于生产配置。应用前要结合当前版本、环境和安全要求验证。
- 记录真实结果；没有执行的测试不得标记为通过。
- 每个阶段至少交付一个可复现的实验或文档，而不只是读完材料。

## 给 Codex 的提示词

```text
请遵守仓库根目录 AGENTS.md，并使用 $learning-coach。
根据 docs/roadmap.md、当前周记、Git 状态和已有代码，带我完成今天 1–2 小时的学习。
先说清目标、概念、步骤和验收标准；每次只推进一个小任务，先让我尝试，不要直接替我完成全部操作。
所有结论以实际代码和命令输出为准。最后帮助我更新周记，但不要虚构执行结果。
```

## 官方参考入口

- [Python 文档](https://docs.python.org/3/)
- [FastAPI 文档](https://fastapi.tiangolo.com/)
- [pytest 文档](https://docs.pytest.org/en/stable/)
- [Docker 文档](https://docs.docker.com/)
- [Kubernetes 文档](https://kubernetes.io/docs/home/)
- [Prometheus 文档](https://prometheus.io/docs/)
- [vLLM 文档](https://docs.vllm.ai/)
- [OWASP LLM 应用安全项目](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
