# LLMOps 实验室

这是一个帮助运维 / SRE 工程师转向 **AI Infra（AI 基础设施）与 LLMOps（大语言模型运维）** 的实战学习仓库。

目标是用约六个月、每天 1–2 小时的节奏，完成从 Python 服务工程化、模型推理、可观测性、Kubernetes 到 LLMOps 评测的系统学习。课程材料、实验、测试和复盘记录都放在同一仓库中。

## 学习背景与节奏

- 适合人群：具备 Linux、Shell/Python 自动化、云平台、Kubernetes、监控等运维经验的工程师。
- 每日投入：建议每天 1–2 小时。
- 学习原则：每个主题都尽量产出可运行代码、自动化测试、基准报告或运维手册。
- 成本原则：优先用本地 mock、合成数据和免费工具完成工程链路；GPU、云资源和付费 API 都是可选项。

## 学习路线

| 阶段 | 学习重点 | 阶段产出 |
|---|---|---|
| 第 1 个月 | Python 服务工程化、API、测试、配置、日志、Docker、CI | 可复现的服务与自动化测试 |
| 第 2 个月 | LLM 推理、GPU 显存、KV Cache、vLLM | 推理架构说明与基准报告 |
| 第 3 个月 | Prometheus、Grafana、LLM 指标、SLO | 仪表盘、告警和排障手册 |
| 第 4 个月 | Kubernetes、GPU 调度、发布与回滚 | 部署清单和回滚演练 |
| 第 5 个月 | 评测数据集、基线比较、质量门禁、LLM 安全 | 可重复评测流水线 |
| 第 6 个月 | 综合项目、故障演练、容量与可靠性 | 端到端演示项目 |

## 中文课程资料

从 [系统化学习资料目录](docs/learning-materials/README.md) 开始，里面包含课程顺序、预计投入、验收标准和官方参考入口。

### 基础工程能力

- [Python 开发环境与依赖管理](docs/learning-materials/python-environment.md)
- [HTTP、FastAPI 与 Pydantic](docs/learning-materials/fastapi-and-pydantic.md)
- [pytest 与测试设计](docs/learning-materials/pytest-testing.md)
- [Python 服务工程化](docs/learning-materials/python-service-engineering.md)
- [配置、结构化日志与服务安全](docs/learning-materials/config-logging-security.md)
- [HTTP 服务可靠性：超时、重试、幂等与限流](docs/learning-materials/http-reliability.md)
- [Docker、进程与健康探针](docs/learning-materials/docker-healthchecks.md)
- [Docker 镜像与 CI 流水线](docs/learning-materials/docker-ci.md)

### 模型推理与基础设施

- [大语言模型推理基础](docs/learning-materials/llm-inference-fundamentals.md)
- [GPU 显存、模型权重与 KV Cache](docs/learning-materials/gpu-memory-kv-cache.md)
- [vLLM 模型服务与运维](docs/learning-materials/vllm-serving.md)
- [LLM 服务可观测性与 SLO](docs/learning-materials/llm-observability-slo.md)
- [Kubernetes 上运行模型服务](docs/learning-materials/kubernetes-llm-serving.md)

### LLMOps 与综合实践

- [LLM 评测、回归测试与发布门禁](docs/learning-materials/llm-evaluation-release.md)
- [LLM 应用与模型服务安全](docs/learning-materials/llm-security.md)
- [综合项目：可观测、可评测的模型服务平台](docs/learning-materials/integrated-project.md)

## 快速开始

环境要求：Python 3.11 或更高版本。

```bash
git clone https://github.com/Sakuya1998/llmops-lab.git
cd llmops-lab
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
uvicorn model_ops_api.main:app --reload --app-dir app
```

启动后访问 http://127.0.0.1:8000/docs 查看交互式 API 文档。

运行代码检查与测试：

```bash
pytest
ruff check .
ruff format --check .
mypy app
```

也可以使用 Makefile 中的快捷命令，例如 `make install`、`make run`、`make test`。\n\n运行确定性评测门禁：\n\n```bash\npython pipelines/evaluation/evaluate.py\npytest -q tests/test_evaluation.py\n```\n\n启动本地 API + Prometheus 组合实验（需要 Docker Compose）：\n\n```bash\ndocker compose -f compose.yaml up --build\n```\n\nAPI 文档位于 http://127.0.0.1:8000/docs，Prometheus 位于 http://127.0.0.1:9090。停止实验使用 `docker compose -f compose.yaml down`。

## 当前起步 API

- `GET /health`：返回基础健康状态。\n- `GET /metrics`：导出 Prometheus HTTP 请求量与时延指标。
- `POST /api/v1/models`：登记模型部署元数据。
- `GET /api/v1/models`：列出已登记的模型。
- `GET /api/v1/models/{model_id}`：按 ID 查询模型记录。

第一版使用内存存储，便于学习 API 设计。**它不是生产级模型注册中心**：进程重启后数据会丢失，多副本之间也不会共享数据。

## 目录说明

- `app/model_ops_api/`：API 接口与领域数据结构。
- `tests/`：自动化测试。
- `serving/vllm/`：模型服务学习笔记与示例。
- `observability/`：Prometheus 指标、抓取配置和告警。\n- `compose.yaml`：本地 API + Prometheus 实验环境。
- `deploy/`：Docker 与 Kubernetes 示例。
- `pipelines/evaluation/`：可运行的合成数据评测与回归门禁。\n- `serving/vllm/benchmark_openai_compatible.py`：OpenAI-compatible 推理端点并发基准脚本。
- `docs/learning-materials/`：系统化中文课程讲义。
- `docs/weekly-notes/`：每周任务和真实学习记录。
- `docs/`：路线、架构、Codex 工作流和运维手册。
- `.agents/skills/`：可复用的 Codex 学习与工程技能。

## 使用 Codex 持续学习

仓库根目录的 [`AGENTS.md`](AGENTS.md) 定义长期协作规范，`.agents/skills/` 提供可复用技能。

- [Codex 使用指南](docs/codex-workflow.md)
- [学习教练技能](.agents/skills/learning-coach/SKILL.md)
- [Python API 工程化技能](.agents/skills/python-api-engineering/SKILL.md)
- [可观测性与 SRE 技能](.agents/skills/observability-sre/SKILL.md)
- [Kubernetes 运维技能](.agents/skills/kubernetes-operations/SKILL.md)
- [vLLM 模型服务技能](.agents/skills/vllm-serving/SKILL.md)
- [LLM 评测技能](.agents/skills/llm-evaluation/SKILL.md)

推荐提示词：

> 请遵守 `AGENTS.md`，根据学习路线、学习资料目录、当前周记和实际代码，带我完成今天 1–2 小时的任务。先给目标、步骤和验收标准，再循序渐进指导我；不要假设测试已通过。

## 学习循环

1. 学习一个核心概念。
2. 阅读仓库对应代码。
3. 完成一个小实验或代码改动。
4. 运行测试和检查，记录真实结果。
5. 写下一个故障场景、观测方法和恢复步骤。

从 [六个月学习路线](docs/roadmap.md)、[系统化学习资料](docs/learning-materials/README.md) 和 [第 1 周任务清单](docs/weekly-notes/week-01.md) 开始。

## 安全边界

- 不要提交密码、API Key、访问令牌、私有数据集或生产配置。
- 未经授权，不要将公司机密、用户数据或生产提示词发送给第三方模型服务。
- 云资源、GPU 和付费 API 实验必须先明确预算、权限与销毁步骤。
- 部署 YAML 和命令示例是教学材料，应用于真实环境前必须审查并验证。
