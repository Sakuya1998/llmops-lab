# 配置、结构化日志与服务安全

## 学习目标

掌握服务启动配置、日志字段设计、敏感信息处理和最小权限原则。建议用时 1–2 小时。

## 1. 配置与密钥不是一回事

普通配置包括端口、超时、日志级别和功能开关；密钥包括 API Token、密码、私钥和云凭据。两者的敏感等级不同，但都应避免散落在代码中。

推荐原则：
- 配置在启动时集中解析，并验证必填项和取值范围。
- 开发环境可以使用本地未提交的 .env 文件；生产环境优先使用平台的 Secret/密钥管理机制。
- 不要把真实凭据写入示例文件、测试快照、日志或 Git 历史。
- 轮换密钥时考虑旧密钥失效时间和应用重新加载行为。

## 2. 结构化日志

相较于自由文本，JSON 等结构化日志更容易过滤和聚合。常见字段：
- timestamp：事件时间；
- level：日志级别；
- service、environment、version：服务身份；
- request_id / trace_id：请求关联标识；
- event：稳定的事件名称；
- duration_ms、status_code：可量化的结果。

字段要有一致定义，避免同一含义在不同代码路径中使用不同名字。

## 3. 不应该默认记录的内容

不要记录：
- Authorization 头、Cookie、API Key、密码；
- 完整提示词、模型回复或用户原始输入，除非经过明确的数据治理和授权；
- 个人身份信息、支付数据、私有数据集；
- 数据库连接串中的凭据；
- 高基数字段作为指标标签。

如果确实需要排查内容相关问题，优先记录内容长度、哈希、错误类别、经过批准的采样摘要或不可逆脱敏信息，并遵守保留期限与访问控制。

## 4. 日志与指标的区别

日志适合描述单个事件及上下文；指标适合低成本地观察一段时间内的聚合趋势。不要将 request_id、user_id、prompt、原始 URL 查询参数等高基数字段作为 Prometheus 标签，否则会制造大量时间序列并增加内存和查询成本。

指标标签应使用有限集合，例如 method、route 模板、status_class、model_family。不要把具体资源 ID 放进 route 标签。

## 5. 请求关联与错误排查

为请求生成或接受受信任的 request ID，并确保该 ID 在日志、响应头和下游调用中一致传播。不要无条件信任外部传入的超长或特殊字符 ID；应限制长度并进行安全校验。

一个有用的错误日志应回答：哪个服务、哪个版本、什么操作、什么错误类别、持续多久、请求关联 ID 是什么。它不需要泄露完整用户内容。

## 6. 最小权限与信任边界

- 本地调试服务默认只监听回环地址，除非明确需要对外提供服务。
- 认证与授权是不同问题：认证确认身份，授权决定该身份可以执行什么操作。
- 不要将开发环境的无认证示例直接暴露到公网。
- 依赖升级、镜像来源、运行用户和文件权限都属于供应链与运行安全的一部分。

## 实验

1. 查看仓库的 .gitignore 和 .env.example。
2. 搜索日志代码，确认没有打印完整凭据或用户内容。
3. 为一个请求添加 request_id 关联字段（如项目已有实现，先解释它）。
4. 列出项目中适合做指标标签的低基数字段，以及不适合的高基数字段。
5. 检查 Git diff，确保没有真实密钥。

## 验收

- 能解释配置与密钥的区别。
- 能为一次失败请求设计安全且可检索的日志。
- 能解释高基数标签为何会影响 Prometheus。
- 能区分认证、授权与网络访问控制。

## 参考资料

- [OWASP Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html)
- [OWASP Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)
- [Prometheus：Instrumentation](https://prometheus.io/docs/practices/instrumentation/)
