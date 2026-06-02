---
audio: false
generated: true
lang: zh
layout: post
title: TDengine 与 GreptimeDB：时序数据库双雄对决
translated: true
type: note
---

是的，TDengine 和 GreptimeDB 在时序数据库领域确实是竞争对手。两者都定位为高性能、开源的时序数据库，且目标用例相似。

**主要竞争领域：**

1. **性能宣称**：两家数据库都在基准测试中提出了强有力的性能主张。TDengine 声称其"磁盘空间消耗比 TimescaleDB 少 26.9 倍，比 InfluxDB 少 4.5 倍"且"在所有场景中拥有最快的查询响应时间"。同样，GreptimeDB 声称"写入吞吐量比 InfluxDB 高出 2 倍以上"且"在处理大型数据集时展现出显著的查询性能优势"。

2. **目标市场**：TDengine 主要与 InfluxDB、TimescaleDB、Prometheus、OpenTSDB 和 QuestDB 等其他主流时序数据库进行对标，而 GreptimeDB 则将自己定位为"面向指标、日志和追踪的统一且经济高效的可观测性数据库"。

3. **基准测试竞争**：两家数据库都出现在时序数据库基准测试中，其中 TDengine 属于"在数据摄取方面表现最快的厂商"。

**主要差异：**

- **侧重点**：TDengine 似乎更专注于传统时序用例和物联网场景，而 GreptimeDB 强调在单一数据库中实现统一可观测性（指标、日志、追踪）
- **架构设计**：TDengine 强调其"充分利用了时序数据的特性，如结构化特性、无事务性、极少删除或更新，以及写多读少的工作负载"
- **存储效率**：GreptimeDB 的存储成本被指出"显著低于 Elasticsearch，持久化数据大小仅为 ClickHouse 的 50%"

两家数据库都与相同的成熟产品（InfluxDB、TimescaleDB、ClickHouse）直接竞争，并瞄准类似的性能敏感型时序工作负载，这使它们成为该领域明确的竞争对手。
