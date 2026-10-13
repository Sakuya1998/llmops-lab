# LLMOps 实验室

这是一个帮助运维 / SRE 工程师转向 **AI Infra（AI 基础设施）与 LLMOps（大语言模型运维）** 的实战学习仓库。

项目按照循序渐进的六个月路线组织：先构建并测试 API，再完成容器化、可观测性和 Kubernetes 部署，最后加入模型服务与评测流水线。

## 学习背景与节奏

- 适合人群：具备 Linux、Shell/Python 自动化、云平台、Kubernetes、监控等运维经验的工程师。
- 每日投入：建议每天 1–2 小时。
- 学习原则：每个主题都尽量产出可运行的代码、自动化测试或运维手册。

## 学习路线

| 阶段 | 学习重点 | 阶段产出 |
|---|---|---|
| 第 1 阶段 | Python 服务工程化 | FastAPI 模型登记 API、自动化测试、代码检查 |
| 第 2 阶段 | 模型推理基础 | vLLM 部署笔记、基准测试方案、资源规划 |
| 第 3 阶段 | 可观测性 | Prometheus 指标、告警规则、Grafana 仪表盘设计 |
| 第 4 阶段 | Kubernetes 运维 | 部署清单、探针、资源限制、发布与回滚手册 |
| 第 5 阶段 | LLMOps | 评测数据集、可重复评测任务、发布门禁 |
| 第 6 阶段 | 项目整合与可靠性 | 端到端演示、故障演练、架构与事故文档 |

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

也可以使用 Makefile 中的快捷命令，例如 `make install`、`make run`、`make test`。

## 当前 API

- `GET /health`：返回基础存活状态。
- `POST /api/v1/models`：登记一条模型部署元数据。
- `GET /api/v1/models`：列出已登记的模型。
- `GET /api/v1/models/{model_id}`：按 ID 查询模型记录。

第一版故意使用内存存储，便于学习 API 设计。**它不是持久化的生产级模型注册中心**：进程重启后数据会丢失，多副本之间也不会共享数据。

## 目录说明

- `app/model_ops_api/`：API 接口与领域数据结构。
- `tests/`：自动化测试。
- `serving/vllm/`：模型服务学习笔记与示例。
- `observability/`：Prometheus 告警和指标设计。
- `deploy/`：Docker 与 Kubernetes 示例。
- `pipelines/evaluation/`：模型评测流水线起步说明。
- `docs/learning-materials/`：按主题组织的中文学习讲义。
- `docs/`：学习路线、每周记录、架构说明和运维手册。
- `scripts/`：本地开发辅助脚本。

## 中文学习资料

从 [系统化学习资料目录](docs/learning-materials/README.md) 开始。目前第一批资料覆盖：

- [Python 开发环境与依赖管理](docs/learning-materials/python-environment.md)
- [HTTP、FastAPI 与 Pydantic](docs/learning-materials/fastapi-and-pydantic.md)
- [pytest 与测试设计](docs/learning-materials/pytest-testing.md)
- [Docker、进程与健康探针](docs/learning-materials/docker-healthchecks.md)

讲义配合当前仓库代码与每周任务使用。每次学习一个主题，亲自执行命令、修改代码、运行测试并记录真实结果，不要把示例配置未经验证地直接用于生产环境。

## 安全与使用边界

- 不要提交密码、API Key、访问令牌、私有数据集或生产环境配置。
- 本地实验可以复制 `.env.example` 为 `.env`；真实的 `.env` 文件已加入 Git 忽略规则。
- Kubernetes 与模型服务示例仅供学习。用于真实环境前，必须审查资源限制、访问控制、镜像版本和持久化方案。
- 未经授权，不要把公司机密、用户数据或生产提示词发送给第三方模型服务。

## 使用 Codex 持续学习

仓库根目录的 [`AGENTS.md`](AGENTS.md) 定义了长期协作规范；`.agents/skills/` 提供面向不同任务的可复用技能。建议在 Codex Desktop 中打开仓库根目录使用。

- [Codex 使用指南](docs/codex-workflow.md)：常用提示词、任务流程与验收要求。
- [学习教练技能](.agents/skills/learning-coach/SKILL.md)：按每天 1–2 小时规划学习与复盘。
- [Python API 工程化技能](.agents/skills/python-api-engineering/SKILL.md)：接口实现、代码讲解与测试。
- [可观测性与 SRE 技能](.agents/skills/observability-sre/SKILL.md)：指标、告警、仪表盘和排障。
- [Kubernetes 运维技能](.agents/skills/kubernetes-operations/SKILL.md)：部署清单、安全、发布和回滚。
- [vLLM 模型服务技能](.agents/skills/vllm-serving/SKILL.md)：推理资源规划与性能实验。
- [LLM 评测技能](.agents/skills/llm-evaluation/SKILL.md)：评测数据集、质量门禁与版本比较。

示例提示词：

> 请遵守 `AGENTS.md`，根据学习路线和当前周记，带我完成今天 1–2 小时的任务。先给出目标、步骤和验收标准，再循序渐进地指导我；不要假设测试已通过。

技能放在仓库的 `.agents/skills/` 中，可随项目版本管理，方便在不同开发环境中复用。如果 Codex 没有显示新技能，尝试重新加载工作区或重启 Codex。

## 每周学习循环

1. 学习一个核心概念。
2. 实现一个小功能。
3. 为功能补充或更新测试。
4. 在本地运行所有检查。
5. 记录一个可能的故障场景，以及如何发现和恢复。

从 [六个月学习路线](docs/roadmap.md)、[系统化学习资料](docs/learning-materials/README.md) 和 [第 1 周任务清单](docs/weekly-notes/week-01.md) 开始。
