---
name: kubernetes-operations
description: 当用户需要编写或审查 Kubernetes YAML、Deployment、Service、探针、资源 requests/limits、安全上下文、滚动发布、回滚、容量规划或集群故障排查时使用。
---

# Kubernetes 部署与运维

## 开始前

- 阅读根目录 `AGENTS.md` 和目标目录说明。
- 明确 Kubernetes 发行版、版本、Ingress / Load Balancer 实现、镜像来源、命名空间、网络边界和持久化要求；未知时显式列出假设。
- 先区分学习环境、预发和生产环境，不把示例清单直接当作生产模板。

## 清单审查

逐项检查：
- API 版本和字段是否适用于目标集群。
- labels 与 selectors 是否一致。
- 镜像版本是否可重复构建；避免不受控的 `latest`。
- readiness、liveness、startup probe 是否职责清晰，阈值是否合理。
- requests / limits 是否与实际负载相符。
- securityContext、非 root、只读根文件系统、capabilities 和 seccomp 是否适用。
- ConfigMap / Secret 是否正确使用；不把秘密写入 YAML 或 Git。
- Service、Ingress、NetworkPolicy、RBAC 和外部访问范围是否最小化。
- 滚动更新、PodDisruptionBudget、反亲和性和副本数是否符合可用性目标。
- 持久化、备份、恢复、升级和回滚路径是否清晰。

## 操作安全

- 不自动连接或修改真实集群。
- 不执行可能中断生产流量、删除数据或扩大公网暴露的操作，除非用户明确要求并已确认影响。
- 对每条建议说明验证命令、预期结果和失败后的回滚方式。
- 使用 `kubectl diff`、`kubectl apply --dry-run=server` 等适用方法时，明确它们需要的集群权限和连接条件。

## 输出格式

先列出问题及风险等级，再给出修正清单或最小 patch，最后提供验证、发布、观测和回滚步骤。不能声称 YAML 已通过校验，除非确实运行了相应工具。
