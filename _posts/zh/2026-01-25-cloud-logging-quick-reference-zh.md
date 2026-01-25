---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Cloud Logging 快速参考指南
translated: true
type: note
---

**Question:** Google Cloud 中 Cloud Logging 的全面指南

**Answer:**

Cloud Logging（原名 Stackdriver Logging）是 Google Cloud 的全托管、实时日志管理服务。它允许对来自 Google Cloud 服务、Amazon Web Services（通过代理）、本地系统和自定义应用程序的日志数据进行摄取、存储、搜索、分析、监控和告警。

### 1. 核心概念

- **Log Entry** — 包含以下内容的基本单位：
  - Timestamp
  - Severity (DEBUG, INFO, NOTICE, WARNING, ERROR, CRITICAL, ALERT, EMERGENCY)
  - Payload (文本或 JSON 结构化数据)
  - Labels / resource (生成日志的实体 — GCE instance, GKE container, Cloud Function 等)
  - Log name (projects/PROJECT_ID/logs/...)

- **Log Name 格式** — `projects/[PROJECT]/logs/[LOG_ID]`
  - 内置日志：`cloudaudit.googleapis.com/activity`, `compute.googleapis.com/activity_log` 等。
  - 自定义日志：通常以您的应用程序名称开头。

- **Resource Types** — 被监控的资源（例如 `gce_instance`, `k8s_container`, `cloud_function`, `global`）。

- **Ingestion** — 日志可以通过以下方式发送：
  - 直接 API (Logging API)
  - Client libraries（首选）
  - Fluent Bit / Fluentd agents
  - Cloud Logging agent（目前推荐使用更现代的 Ops Agent）

### 2. 摄取方法 (Ingestion Methods)

| 方法 | 适用场景 | Structured Logging 支持 | 推荐代理 |
|-------------------------|---------------------------------------|-----------------------------|-------------------|
| Ops Agent | Compute Engine, GKE Autopilot, VMs | 是 | 是 (2025+) |
| Cloud Logging libraries | Applications (Java, Go, Python, Node, .NET, etc.) | 极佳 (JSON) | — |
| Fluent Bit / Fluentd | Kubernetes, containers, lightweight | 是 | 是 |
| 直接 API 调用 | Serverless, batch jobs | 是 | — |
| Audit Logs | Admin activity, Data Access, Policy | 是 (自动) | 自动 |

**2025–2026 年推荐**：对于大多数 VM/GCE/GKE 工作负载，使用 **Ops Agent** —— 它在一个二进制文件中集成了 metrics + logs + traces。

### 3. 结构化日志 (Structured Logging - 强烈推荐)

输出 JSON 对象而不是纯文本日志：

```json
{
  "severity": "INFO",
  "message": "User login succeeded",
  "user_id": "u_12345",
  "ip": "203.0.113.42",
  "latency_ms": 48,
  "http_status": 200
}
```

优点：
- 通过字段查询 (`jsonPayload.user_id="u_12345"`)
- 创建分布分析指标 (distribution metrics)
- 更精准的告警
- 更低的解析成本

大多数官方 Google Cloud 库都开箱即用支持结构化日志。

### 4. 查询日志 (Logging Query Language)

基本示例：

- 简单文本搜索：`"error" OR "failed"`
- 严重程度过滤：`severity>=ERROR`
- 资源类型：`resource.type="gce_instance"`
- JSON 字段：`jsonPayload.http_status=500`
- 时间范围：`timestamp>="2026-01-20T00:00:00Z"`
- 排除示例：`NOT jsonPayload.message:"health check"`

高级模式：

```
resource.type="k8s_container"
resource.labels.namespace_name="prod"
severity>=WARNING
jsonPayload."error.type"="DatabaseConnectionError"
```

使用控制台中的 **Query builder** 或直接编写查询语句。

### 5. 基于日志的指标 (Log-Based Metrics)

两种类型：

- **Counter** — 计算匹配查询的日志条目数（例如：错误率）
- **Distribution** — 提取数值（例如：延迟直方图）

创建后 → 在 Cloud Monitoring 仪表板和告警中使用。

### 6. 日志路路由与接收器 (Log Routing & Sinks)

Sinks 将日志路由到目的地：

- Cloud Storage（用于归档 — 廉价的长期存储）
- BigQuery（用于分析 — 分区表）
- Pub/Sub（用于实时流式传输至其他系统）
- 另一个 Cloud Logging bucket/project（组织级聚合）

**排除过滤器 (Exclusion filters)**（针对单个 sink 或全局）有助于大幅降低成本。

示例路由策略：

- 所有审计日志 → BigQuery + 长期保留
- ERROR+ 日志 → Pub/Sub → Slack/ PagerDuty
- 来自开发项目的 INFO 和 DEBUG → 短期保留或排除

### 7. 保留期与存储类别 (Retention & Storage Classes)

| Bucket 类型 | 默认保留期 | 成本级别 | 使用场景 |
|-------------------|-------------------|------------|------------------------------|
| _Default | 30 天 | 标准 | 大多数日志 |
| _Required | 400 天 | 标准 | 审计日志 (不可变) |
| 自定义 bucket | 1 天 – 永久 | 视情况而定 | 归档, 合规性 |

**注意：** `_Required` bucket 中的日志无法被排除或提前删除。

### 8. 成本管理最佳实践 (2025–2026)

1. 使用结构化日志 → 更好的查询和指标分析
2. 设置积极的排除过滤器（排除健康检查、负载均衡器探测、嘈杂的 DEBUG 日志）
3. 将高流量/低价值的日志路由到短期保留空间或 Storage
4. 使用基于日志的指标，而不是反复查询海量数据
5. 通过 Billing → Logs Router 指标监控摄取量
6. 为不同的日志类别创建自定义保留 bucket
7. 定期查看 Logs Explorer 中的 "Top log sources"

### 9. 与其他 Google Cloud 服务的集成

- **Cloud Monitoring** — 基于日志的指标 → 告警策略
- **Cloud Trace** — 将日志与 trace 关联（添加 `trace` 字段）
- **Error Reporting** — 自动对异常进行分组
- **Cloud Operations for GKE** — 丰富的 Kubernetes 日志
- **BigQuery** → 对日志进行 SQL 分析
- **Gemini Cloud Assist** (2025+) → 自然语言日志摘要和异常检测

### 10. 快速入门清单

1. 启用 **Cloud Logging API**（通常已默认开启）
2. 在 VM 上安装 **Ops Agent** 或在代码中使用 client library
3. 发送结构化日志
4. 前往 Logs Explorer → 执行基本查询
5. 创建 2–3 个基于日志的指标（错误数、延迟）
6. 设置一个排除过滤器（例如：排除健康检查）
7. 为重要日志创建一个指向 BigQuery 或 Storage 的 sink
8. 基于日志指标设置告警策略

这涵盖了截至 2026 年在生产环境中使用 Cloud Logging 的大部分实用场景。

**参考资料：**

- [Cloud Logging overview](https://docs.cloud.google.com/logging/docs/overview)
- [Cloud Logging documentation home](https://docs.cloud.google.com/logging/docs)
- [Structured logging](https://docs.cloud.google.com/logging/docs/structured-logging)
- [Logging query language](https://docs.cloud.google.com/logging/docs/view/logging-query-language)
- [Route log entries (sinks)](https://docs.cloud.google.com/logging/docs/routing/overview)
- [Best practices for Cloud Audit Logs](https://docs.cloud.google.com/logging/docs/audit/best-practices)
- [How to centralize log management with Cloud Logging](https://cloud.google.com/blog/products/devops-sre/how-to-centralize-log-management-with-cloud-logging)