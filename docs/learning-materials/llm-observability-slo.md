# LLM 服务可观测性与 SLO

## 学习目标

将传统 SRE 的 RED/USE 思路应用到推理服务，能设计指标、告警和仪表盘，并识别高基数风险。

## 1. 三类基础视角

- RED：Rate（请求速率）、Errors（错误率）、Duration（延迟）。
- USE：Utilization（利用率）、Saturation（饱和度）、Errors（错误）。
- LLM 专属：输入/输出 token 速率、TTFT、TPOT、队列等待、活动序列、模型加载时间、GPU 显存和 KV Cache 使用率（如果可获得）。

指标必须对应明确的单位和定义。不要将不同系统中同名但口径不同的指标直接比较。

## 2. 指标命名和标签

指标应包含单位或在名称/文档中清楚说明单位。延迟通常用 histogram 记录，以便计算分位数和不同区间分布。

适合的低基数标签示例：service、environment、model_family、route 模板、status_class。要谨慎使用 provider/model 名称，因为动态模型名可能带来基数增长。

不适合的标签：user_id、request_id、原始 URL、prompt、任意错误消息、每次请求生成的任务 ID。

## 3. Prometheus 示例

以下示例表达计数器与直方图的常见形态，具体代码需根据项目使用的客户端库调整：

```python
from prometheus_client import Counter, Histogram

REQUESTS = Counter(
    "llm_requests_total",
    "Total number of LLM requests",
    ["route", "status_class"],
)
LATENCY = Histogram(
    "llm_request_duration_seconds",
    "LLM request duration in seconds",
    ["route"],
)
```

不要在每次请求中动态创建新的 metric 对象。标签值应来自受控的有限集合，且要对指标暴露端点设置合适的网络访问边界。

## 4. 延迟分解

总耗时可拆成排队、tokenization、prefill、decode、后处理和网络传输等部分。不同引擎暴露的指标并不一定能精确覆盖所有阶段，因此应结合客户端观测、服务端指标和日志分析。

观察 p95/p99 比只看平均值更容易发现长尾。流式请求还应分别观察首 token 时间和完整响应时间。

## 5. SLI、SLO 与告警

- SLI：实际测量的服务指标，例如成功请求比例或 p95 延迟。
- SLO：一段时间内希望达到的目标。
- SLA：对外承诺，可能附带合同或赔偿条件。

不要在没有基线数据的情况下随意承诺 SLO。先收集实际负载和错误分布，再选择业务相关的 SLI，并明确统计窗口、排除条件和分母。

告警应指向需要行动的症状，而不是只因某个资源数值短暂变化就报警。将告警关联到运行手册，写清确认、缓解、升级和恢复步骤。

## 6. 故障诊断示例

| 症状 | 可能方向 | 需要验证 |
|---|---|---|
| TTFT 升高 | 队列、输入变长、prefill 资源不足 | 排队时间、输入 token、并发 |
| TPOT 变差 | GPU 竞争、批处理变化、显存压力 | GPU 利用率、活动序列、输出长度 |
| GPU 利用率低但延迟高 | CPU、网络、tokenization、队列或同步等待 | CPU、网络、请求阶段耗时 |
| 错误率升高 | 模型加载、OOM、超时、输入不合法 | 错误分类、日志、资源事件 |
| Prometheus 内存增长 | 高基数或标签值爆炸 | numSeries、标签分布、近期变更 |

表格中的方向只是排查假设，不能替代实际证据。

## 7. 实验

1. 定义请求量、错误量、延迟和输出 token 吞吐量。
2. 设计一个按 route/status_class 分组的仪表盘。
3. 列出会造成高基数的标签。
4. 为“错误率持续升高”和“p95 延迟超标”写出告警条件与处置步骤。
5. 记录一次故障假设、证据和结论，区分已证实与未证实的原因。

## 验收

- 能解释 RED、USE、SLI、SLO 和 SLA。
- 能为 LLM 服务设计低基数指标。
- 能区分 TTFT、TPOT 与总延迟。
- 能从症状出发列出可验证的排查假设。

## 参考资料

- [Prometheus 文档](https://prometheus.io/docs/introduction/overview/)
- [Google SRE Workbook](https://sre.google/workbook/table-of-contents/)
- [vLLM 指标文档](https://docs.vllm.ai/)
