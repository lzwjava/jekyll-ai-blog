---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Cloud Logging Quick Reference Guide
translated: false
type: note
---

**Question:** Comprehensive guide to Cloud Logging in Google Cloud

**Answer:**

Cloud Logging (formerly Stackdriver Logging) is Google Cloud's fully managed, real-time log management service. It allows ingestion, storage, searching, analysis, monitoring, and alerting on log data from Google Cloud services, Amazon Web Services (via agents), on-premises systems, and custom applications.

### 1. Core Concepts

- **Log Entry** — Basic unit containing:
  - Timestamp
  - Severity (DEBUG, INFO, NOTICE, WARNING, ERROR, CRITICAL, ALERT, EMERGENCY)
  - Payload (text or JSON structured)
  - Labels / resource (the thing that produced the log — GCE instance, GKE container, Cloud Function, etc.)
  - Log name (projects/PROJECT_ID/logs/...)

- **Log Name Format** — `projects/[PROJECT]/logs/[LOG_ID]`
  - Built-in logs: `cloudaudit.googleapis.com/activity`, `compute.googleapis.com/activity_log`, etc.
  - Custom logs: usually start with your application name.

- **Resource Types** — Monitored resource (e.g., `gce_instance`, `k8s_container`, `cloud_function`, `global`).

- **Ingestion** — Logs can be sent via:
  - Direct API (Logging API)
  - Client libraries (preferred)
  - Fluent Bit / Fluentd agents
  - Cloud Logging agent (legacy Ops Agent is now recommended)

### 2. Ingestion Methods

| Method                  | Best For                              | Structured Logging Support | Recommended Agent |
|-------------------------|---------------------------------------|-----------------------------|-------------------|
| Ops Agent               | Compute Engine, GKE Autopilot, VMs    | Yes                         | Yes (2025+)       |
| Cloud Logging libraries | Applications (Java, Go, Python, Node, .NET, etc.) | Excellent (JSON)           | —                 |
| Fluent Bit / Fluentd    | Kubernetes, containers, lightweight   | Yes                         | Yes               |
| Direct API calls        | Serverless, batch jobs                | Yes                         | —                 |
| Audit Logs              | Admin activity, Data Access, Policy   | Yes (auto)                  | Automatic         |

**Recommendation in 2025–2026**: Use **Ops Agent** for most VM/GCE/GKE workloads — it combines metrics + logs + traces in one binary.

### 3. Structured Logging (Strongly Recommended)

Instead of plain text logs, emit JSON objects:

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

Benefits:

- Query by fields (`jsonPayload.user_id="u_12345"`)
- Create distribution metrics
- Better alerting
- Lower parsing cost

Most official Google Cloud libraries support structured logging out of the box.

### 4. Querying Logs (Logging Query Language)

Basic examples:

- Simple text search: `"error" OR "failed"`
- Severity filter: `severity>=ERROR`
- Resource type: `resource.type="gce_instance"`
- JSON field: `jsonPayload.http_status=500`
- Time range: `timestamp>="2026-01-20T00:00:00Z"`
- Exclusion example: `NOT jsonPayload.message:"health check"`

Advanced patterns:

```
resource.type="k8s_container"
resource.labels.namespace_name="prod"
severity>=WARNING
jsonPayload."error.type"="DatabaseConnectionError"
```

Use the **Query builder** in the console or write queries directly.

### 5. Log-Based Metrics

Two types:

- **Counter** — count log entries matching a query (e.g., error rate)
- **Distribution** — extract numeric values (e.g., latency histograms)

Create → Use in Cloud Monitoring dashboards & alerting.

### 6. Log Routing & Sinks

Sinks route logs to destinations:

- Cloud Storage (for archival — cheap long-term storage)
- BigQuery (for analytics — partitioned tables)
- Pub/Sub (for real-time streaming to other systems)
- Another Cloud Logging bucket/project (organization-wide aggregation)

**Exclusion filters** (per sink or global) help reduce costs dramatically.

Example routing strategy:

- All audit logs → BigQuery + long retention
- ERROR+ logs → Pub/Sub → Slack/ PagerDuty
- INFO & DEBUG from dev projects → short retention or excluded

### 7. Retention & Storage Classes

| Bucket Type       | Default Retention | Cost Level | Use Case                     |
|-------------------|-------------------|------------|------------------------------|
| _Default          | 30 days           | Standard   | Most logs                    |
| _Required         | 400 days          | Standard   | Audit logs (immutable)       |
| Custom bucket     | 1 day – forever   | Varies     | Archival, compliance         |

**Note:** Logs in `_Required` bucket cannot be excluded or deleted early.

### 8. Cost Management Best Practices (2025–2026)

1. Use structured logging → better querying & metrics
2. Set aggressive exclusion filters (exclude health checks, load balancer probes, noisy DEBUG logs)
3. Route high-volume/low-value logs to short-retention or Storage
4. Use log-based metrics instead of querying huge volumes repeatedly
5. Monitor ingestion volume in Billing → Logs Router metrics
6. Create custom retention buckets for different log classes
7. Regularly review "Top log sources" in Logs Explorer

### 9. Integration with Other Google Cloud Services

- **Cloud Monitoring** — log-based metrics → alerting policies
- **Cloud Trace** — correlate logs with traces (add `trace` field)
- **Error Reporting** — automatically groups exceptions
- **Cloud Operations for GKE** — rich Kubernetes logs
- **BigQuery** → SQL analysis of logs
- **Gemini Cloud Assist** (2025+) → natural language log summarization & anomaly detection

### 10. Quick Start Checklist

1. Enable **Cloud Logging API** (usually already on)
2. Install **Ops Agent** on VMs or use library in code
3. Emit structured logs
4. Go to Logs Explorer → run basic queries
5. Create 2–3 log-based metrics (errors, latency)
6. Set up one exclusion filter (e.g., health checks)
7. Create one sink to BigQuery or Storage for important logs
8. Add alerting policy based on log-based metric

This covers the majority of practical Cloud Logging usage in production environments as of 2026.

**References:**

- [Cloud Logging overview](https://docs.cloud.google.com/logging/docs/overview)
- [Cloud Logging documentation home](https://docs.cloud.google.com/logging/docs)
- [Structured logging](https://docs.cloud.google.com/logging/docs/structured-logging)
- [Logging query language](https://docs.cloud.google.com/logging/docs/view/logging-query-language)
- [Route log entries (sinks)](https://docs.cloud.google.com/logging/docs/routing/overview)
- [Best practices for Cloud Audit Logs](https://docs.cloud.google.com/logging/docs/audit/best-practices)
- [How to centralize log management with Cloud Logging](https://cloud.google.com/blog/products/devops-sre/how-to-centralize-log-management-with-cloud-logging)
