---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: Telegraf：开源指标收集代理
translated: true
type: note
---

Telegraf 是由 InfluxData 开发的开源插件驱动型代理程序，用于从各类来源收集、处理、聚合并写入指标、日志及其他遥测数据。它采用轻量级设计，以单一二进制文件运行，支持 300 余种输入插件（例如系统状态、MySQL/PostgreSQL 等数据库、AWS 等云服务及 Apache Kafka 等应用程序）和 50 多种输出插件（例如输出至 InfluxDB、Prometheus、Kafka 或 Elasticsearch）。

### 核心特性

- **基于代理的架构**：可轻松部署在服务器、容器或物联网设备上，无需繁重的依赖项
- **通过插件扩展**：基于 Go 语言编写，支持按需开发自定义插件
- **TICK 技术栈组件**：与时间序列数据库 InfluxDB、可视化工具 Chronograf 和告警平台 Kapacitor 无缝集成
- **应用场景**：广泛用于 DevOps 领域的基础设施监控、应用性能追踪及物联网传感器数据采集

该工具基于 MIT 协议免费开源并持续维护，截至 2025 年底最新稳定版为 v1.29.x。配置指南请参阅官方文档 [telegraf.influxdata.com](https://docs.influxdata.com/telegraf/)。若此 Telegraf 非您所指（如其他语境中的品牌或术语），请提供更多说明！
