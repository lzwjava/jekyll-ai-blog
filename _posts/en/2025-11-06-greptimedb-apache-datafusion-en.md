---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: GreptimeDB Relies on Apache DataFusion
translated: false
type: note
---

GreptimeDB, an open-source cloud-native time-series database for observability data (like metrics, logs, and traces), relies on Apache DataFusion as a core dependency because its query engine is fundamentally built on top of DataFusion. DataFusion is a high-performance, extensible query planning, optimization, and execution framework written in Rust, leveraging Apache Arrow's in-memory columnar data format for efficient processing.

### Key Reasons for This Dependency

- **Performance and Efficiency**: DataFusion enables fast query execution by utilizing Arrow's zero-copy data model, which minimizes serialization overhead and supports vectorized operations. This is crucial for handling massive volumes of time-series data in GreptimeDB without compromising speed.

- **Extensibility and Customization**: GreptimeDB extends DataFusion to add time-series-specific features, such as:
  - Support for PromQL (Prometheus Query Language) as a dialect for observability queries.
  - Enhanced SQL syntax tailored to time-series workloads.
  - Integration with external secondary indexes for faster lookups.
  - Domain-specific optimization rules that apply at various query stages (e.g., planning, rewriting, and execution).

- **Modular Architecture**: DataFusion acts as a flexible framework that allows GreptimeDB to manage queries across its distributed components (e.g., separating compute from storage). This modularity helps in building custom query plans optimized for different scenarios, like real-time analytics or historical aggregations.

- **Ecosystem Compatibility**: By inheriting DataFusion's built-in functions (scalar, window, array, etc.), GreptimeDB gains a rich set of SQL capabilities out-of-the-box, reducing development effort while ensuring compatibility with broader data ecosystems like Apache Arrow.

Without DataFusion, GreptimeDB would need to reimplement a full query engine from scratch, which would be resource-intensive and harder to maintain. Instead, this dependency accelerates development and delivers production-grade query performance.

[Greptime Engineer Ruihang Xia Presented at CMUDB Seminar — Apache DataFusion Database Practices](https://greptime.com/blogs/2024-12-19-apache-datafusion-database-practices)
[Functions | GreptimeDB Documentation](https://docs.greptime.com/reference/sql/functions/overview/)
