# 使用 Codex 持续学习本仓库

本仓库通过根目录的 `AGENTS.md` 保存长期协作规则，并通过 `.agents/skills/` 提供可复用的学习与工程工作流。

## 推荐使用方式

在 Codex Desktop 中打开本仓库目录，然后在任务提示中描述目标。也可以用 `$技能名称` 显式指定技能；技能是否出现在列表中取决于当前 Codex 版本和工作区加载状态。

### 每天开始学习

可以直接发送：

> 请根据 AGENTS.md、docs/roadmap.md 和当前周记，带我完成今天的一个学习任务。每天投入约 1–2 小时。先说明目标、背景知识、步骤和验收标准，不要一次性替我完成整个月的内容。

### 解释现有代码

> 请使用 $python-api-engineering 技能，用简体中文逐段解释相关代码。说明执行流程、类型与框架机制、异常路径、测试方法和生产环境风险。先不要修改代码。

### 实现一个小功能

> 请使用 $python-api-engineering 技能，为当前 API 增加一个小功能。先检查现有实现和测试，提出最小变更方案，然后编码、补测试并运行相关检查。最后解释关键设计选择。

### 学习可观测性

> 请使用 $observability-sre 技能，为当前服务设计最小可用的 Prometheus 指标和告警。注意指标基数、敏感数据、告警噪声，并提供验证步骤。

### 学习 Kubernetes

> 请使用 $kubernetes-operations 技能，审查当前 Kubernetes 清单。逐项解释安全上下文、探针、资源 requests/limits、发布与回滚风险，并给出可验证的改进。

### 学习模型推理或评测

> 请根据当前学习路线，使用 $vllm-serving 或 $llm-evaluation 中最相关的技能，给我一个可以在有限资源下完成的实验。先确认硬件与预算假设，不要默认启动付费云资源或下载大型模型。

## 每次任务的结束标准

要求 Codex 在结束前给出：

1. **变更摘要**：修改了哪些文件。
2. **原理说明**：核心设计与关键权衡。
3. **验证结果**：执行过的命令及真实结果；未执行的检查要明确标出。
4. **风险与限制**：演示代码与生产环境之间还缺什么。
5. **下一步任务**：一个 1–2 小时内可以完成的具体目标。
6. **学习记录**：建议写入周记的要点，未经要求不要覆盖用户已有记录。

## 技能目录

- `.agents/skills/learning-coach/SKILL.md`：规划与引导学习。
- `.agents/skills/python-api-engineering/SKILL.md`：Python、FastAPI、测试与代码质量。
- `.agents/skills/observability-sre/SKILL.md`：指标、告警、仪表盘和故障排查。
- `.agents/skills/kubernetes-operations/SKILL.md`：Kubernetes 部署、安全与运维。
- `.agents/skills/vllm-serving/SKILL.md`：模型推理、资源规划和基准测试。
- `.agents/skills/llm-evaluation/SKILL.md`：评测集、指标和发布门禁。

技能是工作流说明，不会自动安装软件、连接云账号或替你运行生产操作。对高影响操作仍应先审查具体计划。
