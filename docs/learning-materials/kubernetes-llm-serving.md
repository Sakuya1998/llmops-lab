# Kubernetes 上运行模型服务

## 学习目标

能审查模型服务的 Deployment、Service、探针、资源、存储和网络边界；理解 GPU 调度及上线前风险。

## 1. 先区分控制面与推理数据面

控制面负责模型部署元数据、配置、授权和任务管理；推理数据面负责加载模型并处理 token 请求。它们的资源需求和扩缩容方式不同。把模型权重加载与普通轻量 API 放在同一个扩缩容策略中，往往会导致启动慢、资源争用和不必要的重复加载。

## 2. 工作负载选择

- Deployment：适合无状态 API 或可按副本管理的服务。
- StatefulSet：适用于需要稳定身份或有序管理的场景，但并不自动提供应用级数据一致性。
- Job/CronJob：适合一次性或定时评测任务。
- PVC：为模型缓存或需要持久化的数据提供存储；权重缓存能否共享取决于存储性能、并发访问方式和权限。

模型权重体积大，拉取时间和启动耗时应纳入扩缩容与发布设计。不要假设 Pod 重建后一定能立即获得模型文件。

## 3. GPU 调度

GPU 通常通过设备插件或相应资源插件暴露给 Kubernetes。Pod 请求 GPU 资源的写法取决于集群插件与厂商环境。调度前确认节点标签、驱动、设备插件、CUDA 兼容性、GPU 型号和可用显存。

GPU 数量不是显存容量的全部说明；模型并行、拓扑和跨卡通信也会影响可运行模型与吞吐量。

## 4. 探针和优雅终止

- startupProbe：保护慢启动阶段。
- readinessProbe：模型未加载完成时不接收流量。
- livenessProbe：避免无法自恢复的进程长期卡死。
- terminationGracePeriodSeconds：为请求排空和清理留出时间。

模型加载探针不能只检查 TCP 端口。readiness 应反映实例是否真正可以服务请求。liveness 不宜依赖所有外部依赖，否则短暂故障可能导致重启风暴。

## 5. 资源与扩缩容

CPU、内存、GPU、临时磁盘和 PVC 都需要规划。HPA 的 CPU 指标未必能代表 GPU 推理的真实压力；可结合队列长度、活动序列、请求等待时间等信号设计扩缩容，但自定义指标链路和冷启动成本必须验证。

扩容会带来模型下载、权重加载和显存占用。扩容策略应考虑最小副本、预热、节点容量、缩容排空与成本上限。

## 6. 安全边界

- API 服务默认不应直接暴露到公网。
- 使用 NetworkPolicy 或云网络控制限制调用路径。
- ServiceAccount、RBAC、Secret 和卷权限遵循最小权限。
- 镜像、模型权重和启动参数都应可追踪。
- 限制容器权限，避免 privileged、hostPath 和 hostNetwork，除非有明确需求与安全审查。
- 不要把模型仓库令牌写入 YAML 明文或镜像层。

## 7. 发布与回滚

发布前验证镜像和模型版本、探针、资源配额、GPU 节点容量、模型许可和监控。回滚不仅要恢复旧镜像，也要考虑 API 契约、模型输出格式、提示词版本和缓存兼容性。

## 实验

1. 阅读仓库中的 Kubernetes 示例，不要直接 apply 到生产集群。
2. 标出 image、resources、probes、securityContext、serviceAccount 和 storage 配置。
3. 为模型加载慢、GPU 不足、PVC 挂载失败分别设计诊断步骤。
4. 写出一次滚动更新的成功条件与回滚条件。
5. 如果没有 GPU 集群，只完成 YAML 静态审查和本地模拟，不要为完成课程擅自创建付费资源。

## 验收

- 能解释模型服务与普通 API 在启动、资源和扩缩容方面的差异。
- 能说明探针、GPU 调度和 PVC 的职责。
- 能指出至少五个上线前的安全检查项。
- 能写出可执行的发布验证和回滚清单。

## 参考资料

- [Kubernetes 官方文档](https://kubernetes.io/docs/home/)
- [NVIDIA GPU Operator 文档](https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/latest/)
- [vLLM 文档](https://docs.vllm.ai/)
