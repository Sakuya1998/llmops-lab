# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

这是一个面向运维 / SRE 工程师的 LLMOps 实战学习仓库，目标是通过循序渐进的六个月路线掌握 AI 基础设施与大语言模型运维。项目采用简体中文作为主要交流语言，代码注释和文档均用中文编写。

**重要协作规范：** 根目录的 `AGENTS.md` 定义了完整的项目协作规范，包括任务规划、实现约定、验证流程、学习辅导方式和安全边界。在本仓库工作时必须优先遵守。

## 核心架构

当前为第一阶段的起步项目，使用内存存储的 FastAPI 服务作为学习基础：

```
FastAPI HTTP 层
  ├─ Pydantic 数据校验 (schemas.py)
  ├─ 路由处理器 (main.py)
  └─ 内存字典存储 (_models)
```

**有意保留的限制（教学目的）：**
- 无持久化存储：进程重启后数据丢失
- 无身份认证：仅供本地学习环境使用
- 不调用外部模型：仅登记元数据，不提供推理
- 简单健康检查：`/health` 仅返回存活状态

## 开发环境设置

Python 版本要求：3.11+

安装依赖：
```bash
python -m pip install -e ".[dev]"
```

启动开发服务器：
```bash
uvicorn model_ops_api.main:app --reload --app-dir app
# 或使用 Makefile
make run
```

访问 http://127.0.0.1:8000/docs 查看交互式 API 文档。

## 验证命令

在任何代码修改后，运行以下检查：

```bash
# 运行所有测试
pytest

# 静态代码检查
ruff check .

# 代码格式检查
ruff format --check .

# 类型检查
mypy app

# 或使用 Makefile 一次运行所有检查
make check
```

**自动格式化代码：**
```bash
ruff format .
# 或使用 Makefile
make format
```

**覆盖率测试：**
```bash
pytest --cov=app/model_ops_api --cov-report=term-missing
```

**运行单个测试：**
```bash
pytest tests/test_api.py::test_health_returns_ok
```

**运行单个测试文件：**
```bash
pytest tests/test_api.py
```

## API 接口

当前实现的端点：
- `GET /health` - 基础存活检查
- `POST /api/v1/models` - 登记模型部署元数据（201 Created）
- `GET /api/v1/models` - 列出所有模型
- `GET /api/v1/models/{model_id}` - 按 UUID 查询单个模型（404 if not found）

**数据模型：**
- `ModelCreate`：输入校验模型，包含 name（必填，1-120字符）、provider（枚举类型）、endpoint（可选）、description（可选）
- `ModelRecord`：响应模型，自动生成 id（UUID）和 created_at（UTC 时间戳），frozen=True 确保不可变性

## 代码结构

```
app/model_ops_api/
  ├─ main.py          # FastAPI 应用与路由处理器
  ├─ schemas.py       # Pydantic 数据模型（ModelCreate, ModelRecord）
  └─ __init__.py

tests/
  └─ test_api.py      # API 契约测试（使用 TestClient）

docs/
  ├─ architecture.md           # 当前架构与演进建议
  ├─ roadmap.md               # 六个月学习路线
  ├─ learning-materials/      # 系统化学习讲义
  └─ weekly-notes/            # 每周学习记录

.agents/skills/               # 可复用的 Codex 技能
  ├─ learning-coach/         # 学习规划与复盘
  ├─ python-api-engineering/ # API 实现与测试
  ├─ observability-sre/      # 指标、告警与排障
  ├─ kubernetes-operations/  # K8s 部署与运维
  ├─ vllm-serving/          # vLLM 模型服务
  └─ llm-evaluation/        # 评测数据集与门禁
```

## 测试设计原则

- 每个测试函数使用 `setup_function()` 清空内存存储，避免测试间干扰
- 测试命名遵循 `test_<行为>_<预期结果>` 模式
- 使用 FastAPI 的 `TestClient` 进行端到端接口测试
- 对输入校验、错误处理和成功路径都应有测试覆盖

## 代码质量配置

- **Ruff**: 行长度 100，目标版本 py311，启用规则：E (pycodestyle errors), F (pyflakes), I (isort), UP (pyupgrade), B (flake8-bugbear)
- **mypy**: 启用 strict 模式，类型检查范围为 `app/` 目录
- **pytest**: 测试目录为 `tests/`，使用 `-ra --strict-markers`

**可用的 Makefile 快捷命令：**
```bash
make install      # 安装项目和开发依赖
make run          # 启动开发服务器（带热重载）
make test         # 运行测试
make lint         # 运行 ruff 静态检查
make format       # 自动格式化代码
make typecheck    # 运行 mypy 类型检查
make check        # 运行所有检查（lint + format-check + typecheck + test）
```

## 工作流程

1. **开始任务前：** 检查 Git 状态和当前分支，阅读相关文档和 `AGENTS.md`
2. **实现变更：** 遵守现有代码风格，避免无关重构
3. **补充测试：** 新功能和 bug 修复都应添加测试
4. **本地验证：** 运行 `make check` 或逐个执行验证命令
5. **提交前：** 确认无敏感信息（密钥、令牌、真实数据）

## 学习模式

当用户说"带我学习""继续下一步"或类似表达时：
1. 根据 `docs/roadmap.md` 和 `docs/weekly-notes/` 确认当前阶段
2. 一次聚焦一个核心目标，先讲原理再引导实践
3. 让用户先尝试，需要时再提供提示和参考答案
4. 给出明确验收标准（命令输出、测试结果、接口行为）
5. 完成后建议将实际结果和问题记入周记

## 安全边界

- 不执行破坏性 Git 操作（reset --hard, force push, 删除分支）
- 不提交密钥、私有数据或大型文件
- 不为"修复 CI"而删除测试或降低检查标准
- 对产生费用或影响线上服务的操作，先解释影响并获得确认
- 不能假设依赖已安装、服务已运行或测试已通过，以实际执行结果为准

## CI/CD

GitHub Actions 工作流（`.github/workflows/ci.yml`）在每次推送和 PR 时自动运行：
1. Python 3.12 环境配置
2. 依赖安装
3. ruff 静态检查和格式检查
4. mypy 类型检查
5. pytest 测试（带覆盖率报告）

本地验证通过后再推送，避免浪费 CI 资源。

## 演进方向

参考 `docs/architecture.md` 中的演进建议：
- 分离存储逻辑到 repository 接口
- 增加结构化日志、请求 ID 和 Prometheus 指标
- 集成持久化存储前先明确数据归属和迁移策略
- 对外开放前补齐身份认证和权限校验
- 集成推理服务时明确超时、并发上限和错误处理

每一步都应有对应的验收标准，避免一开始就引入无法解释或验证的组件。
