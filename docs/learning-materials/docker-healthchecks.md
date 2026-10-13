# Docker、进程与健康探针

> 目标：理解应用进程、容器生命周期和 Kubernetes 探针之间的关系。建议用时 60–90 分钟。

## 1. 容器不是虚拟机

容器通常通过 Linux namespaces、cgroups 等机制隔离进程视图并限制资源；它共享宿主机内核。镜像是构建产物，容器是镜像启动后的运行实例。

对服务运维而言，关键问题不只是“容器是否 Running”，还包括：

- 主进程是否存活；
- 应用是否能够处理请求；
- 应用是否完成启动并准备好接收流量；
- 资源是否被限制；
- 日志和退出码能否帮助定位故障。

## 2. Dockerfile 的核心组成

```dockerfile
FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
WORKDIR /app
COPY pyproject.toml README.md ./
COPY app ./app
RUN python -m pip install --no-cache-dir .
USER 10001:10001
EXPOSE 8000
CMD ["uvicorn", "model_ops_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

这是用于解释概念的示例，不保证与当前仓库的打包配置完全兼容；在使用前应检查实际 Dockerfile、包目录和构建配置。生产镜像还应审查固定版本、构建缓存、镜像来源、依赖漏洞和运行用户。

重点：

- `WORKDIR` 设定后续命令的工作目录。
- `COPY` 将构建上下文中的文件复制进镜像。
- `RUN` 在构建阶段执行命令。
- `CMD` 声明容器默认启动命令。
- `USER` 指定运行身份，减少进程被攻陷后的权限范围。
- `EXPOSE` 是端口元数据，不会自动发布宿主机端口。

非 root 用户运行需要确保应用目录和运行时写入目录具有正确权限。不要用 `chmod -R 777` 作为默认解决办法。

## 3. 为什么主进程很重要

容器通常会在其主进程退出后结束。应用应以前台进程运行，并正确处理 SIGTERM 等终止信号，以便在容器停止或滚动更新时优雅关闭。

避免用 shell 后台化方式启动主服务，例如把服务放到后台后让 shell 继续运行。否则容器生命周期、信号传递和退出状态可能难以预测。

## 4. 存活探针与就绪探针

| 探针 | 要回答的问题 | 失败后的典型行为 |
|---|---|---|
| liveness（存活） | 进程是否陷入无法自行恢复的状态？ | Kubernetes 可重启容器 |
| readiness（就绪） | 当前实例是否应接收业务流量？ | 从 Service 可用端点中移除该实例 |
| startup（启动） | 应用是否完成较慢的初始化？ | 启动探针成功前，其他探针可暂缓执行 |

探针不是越多越好。过于激进的 liveness 检查可能造成重启风暴；readiness 失败通常不应该触发容器重启。

不要把所有依赖检查都塞进 liveness。比如数据库短暂不可用时，如果应用进程仍然健康，重启应用可能只会放大故障。依赖是否应影响 readiness，取决于服务在依赖不可用时能否继续安全地提供功能。

## 5. 一个 Kubernetes 探针示例

```yaml
startupProbe:
  httpGet:
    path: /health
    port: 8000
  periodSeconds: 5
  failureThreshold: 24

readinessProbe:
  httpGet:
    path: /ready
    port: 8000
  periodSeconds: 5
  timeoutSeconds: 2
  failureThreshold: 3

livenessProbe:
  httpGet:
    path: /health
    port: 8000
  periodSeconds: 10
  timeoutSeconds: 2
  failureThreshold: 3
```

这只是探针语义示例：当前仓库是否实现了 `/ready` 必须以实际代码为准。不要直接复制到集群并假设端点已存在。探针的初始延迟、周期、超时和阈值需要结合真实启动时间与恢复行为验证。

## 6. 资源限制与优雅关闭

- CPU limit 可能造成节流；内存超过限制可能触发 OOMKill。
- requests 影响调度器的资源预留判断，不代表应用一定能达到某个性能目标。
- 容器收到终止信号后，应在宽限期内完成请求排空和资源释放。
- 对模型推理服务，还要考虑模型加载时间、显存、并发队列和请求取消行为。

学习阶段先查看当前部署清单的 requests/limits、终止宽限期与探针，再讨论调整，不要凭经验盲目增加资源。

## 7. 动手任务

1. 查看仓库现有 Dockerfile 和部署 YAML。
2. 构建镜像并在本地启动；确认服务能从容器外访问。
3. 查看容器运行用户和日志。
4. 找出 YAML 中的探针配置，并判断失败会触发什么行为。
5. 设计一个“应用启动慢但最终健康”的场景，说明 startupProbe 为什么有帮助。

## 8. 验收标准

- [ ] 能说明镜像、容器与虚拟机的差异。
- [ ] 能解释主进程、SIGTERM 和非 root 运行的意义。
- [ ] 能区分 startup、readiness、liveness 的失败后果。
- [ ] 能指出错误探针配置可能造成的重启风暴或流量黑洞。
- [ ] 不把示例 YAML 当作未经验证即可应用的生产配置。

## 参考资料

- [Docker 官方文档](https://docs.docker.com/)
- [Kubernetes：配置存活、就绪和启动探针](https://kubernetes.io/docs/concepts/configuration/liveness-readiness-startup-probes/)
- [Kubernetes：容器生命周期钩子与终止](https://kubernetes.io/docs/concepts/containers/container-lifecycle-hooks/)
