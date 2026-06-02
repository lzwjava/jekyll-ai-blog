---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: OpenTelemetry 概述和要点
translated: true
type: note
---

问题：什么是 OpenTelemetry？

回答：

OpenTelemetry（通常缩写为 **OTel**）是一套开源工具、API、SDK 和规范，旨在以供应商中立、标准化的方式，从应用程序和基础设施中创建和管理遥测数据（Metrics、Logs 和 Traces）。

### 关键点
- **Cloud Native Computing Foundation (CNCF) 的一部分**：它是该基金会中活跃度第二高的项目（仅次于 Kubernetes）。
- **OpenTracing 和 OpenCensus 的合并**：2019 年，两个早期的开源追踪项目（OpenTracing 和 OpenCensus）合并，成立了 OpenTelemetry，以结束碎片化状态。
- **完全供应商无关**：与那些与特定供应商（例如 Jaeger、Zipkin）绑定的旧标准不同，OpenTelemetry 允许您一次性检测代码，并将数据发送到任何兼容的后端（Datadog、New Relic、Jaeger、Prometheus + Grafana、Splunk、Honeycomb、Lightstep、Azure Monitor、AWS X-Ray 等）。
- **三大支柱**：
  1. **Traces** – 分布式追踪（跨服务追踪请求）。
  2. **Metrics** – 随时间变化的数值测量（计数器、量规、直方图）。
  3. **Logs** – 结构化日志条目，越来越多地与 Traces 相关联。
- **组件**：
  - 规范和 API（语言特定，稳定）
  - SDK（每种语言，您可以在其中配置导出器、处理器等）
  - OpenTelemetry Collector（一个独立的代理/接收器，可以接收、处理和导出遥测数据）
  - 自动检测库（针对流行框架的零代码或低代码检测）
- **支持的语言**（截至 2025 年）：Go、Java、JavaScript/Node.js、Python、.NET/C#、Ruby、PHP、Rust、C++、Erlang/Elixir、Swift 已完全支持，更多语言正在开发中或由社区维护。

### 重要性
在 OTel 出现之前，团队通常需要添加多个检测库（每个可观测性供应商一个）或在早期选择单一供应商。OpenTelemetry 允许您标准化一个检测层，并在不更改代码的情况下切换或多重导出后端。

简而言之：OpenTelemetry 是在云原生和微服务环境中使您的应用程序可观测的现代、行业标准方式。
