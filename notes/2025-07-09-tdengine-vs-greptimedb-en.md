---
audio: false
generated: true
lang: en
layout: post
title: 'TDengine vs. GreptimeDB: Time Series Rivals'
translated: false
type: note
---

Yes, TDengine and GreptimeDB are definitely competitors in the time series database space. Both are positioned as high-performance, open-source time series databases with similar target use cases.

**Key Areas of Competition:**

1. **Performance Claims**: Both databases make strong performance claims in their benchmarks. TDengine claims it "consumes 26.9 times less disk space than TimescaleDB, and 4.5 times less than InfluxDB" and "has the fastest query response time across all scenarios". Similarly, GreptimeDB claims "write throughput is more than 2x that of InfluxDB" and "shows significant advantages in query performance when handling large datasets".

2. **Target Markets**: TDengine focuses on comparing itself with other major time series databases like InfluxDB, TimescaleDB, Prometheus, OpenTSDB, and QuestDB, while GreptimeDB positions itself as a "unified & cost-effective observability database for metrics, logs, and traces".

3. **Benchmark Competition**: Both databases appear in time series database benchmarks, with TDengine among the vendors that "showed themselves as the fastest at ingestion".

**Key Differences:**

- **Focus**: TDengine appears more focused on traditional time series use cases and IoT scenarios, while GreptimeDB emphasizes unified observability (metrics, logs, traces) in a single database
- **Architecture**: TDengine emphasizes its "thorough utilization of time-series data characteristics such as structured nature, lack of transactions, infrequent deletions or updates, and a write-heavy, read-light workload"
- **Storage**: GreptimeDB's storage cost is noted as "significantly lower than Elasticsearch, with the size of persisted data being only 50% of ClickHouse"

Both databases compete directly with the same established players (InfluxDB, TimescaleDB, ClickHouse) and target similar performance-sensitive time series workloads, making them clear competitors in this space.
