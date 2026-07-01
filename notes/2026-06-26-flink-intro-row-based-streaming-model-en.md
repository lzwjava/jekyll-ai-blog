---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Flink Intro: Row-Based Streaming Model"
translated: false
type: note
---

Question: Give an intro to Apache Flink and clarify whether its data model is row-based or column-based.

Answer:

## What Flink Is

Apache Flink is a distributed **stream-processing engine**. The core abstraction is an unbounded stream of events processed record-by-record with low latency. Batch is treated as a special case of streaming (a bounded stream), unifying both under one runtime — this is the "everything is a stream" thesis that distinguishes it from Spark's "everything is a batch (micro-batch)" origin.

The pillars:

- **Stateful stream processing** — operators hold state (e.g., running aggregates, windows, joins), checkpointed to durable storage for exactly-once semantics.
- **Event time + watermarks** — handles out-of-order events by reasoning about when an event *happened* vs when it *arrived*.
- **Layered APIs** — DataStream API (low-level, imperative), Table API / SQL (declarative, relational).

## Row-based or Column-based?

Flink's runtime is fundamentally **row-based**. The streaming model processes one record (one row) at a time as it flows through the operator DAG. This is the natural fit for streaming: you can't wait to accumulate a column's worth of values when events arrive continuously and you need millisecond latency.

Concretely:

- **DataStream API** → each element is a record/object. Row-oriented.
- **Table API / SQL** → the logical abstraction is a table, but the physical execution still streams `RowData` objects (Flink's internal row representation, `org.apache.flink.table.data.RowData`). Each `RowData` is a single logical row with typed field accessors.
- **State backends** (RocksDB, heap) → key-value, where values are serialized rows.

The nuance you flagged earlier is correct: Flink's *connectors* read from and write to columnar formats. When Flink reads a Parquet or ORC file, it does **vectorized columnar reads** for efficiency at the source, then converts to row-oriented `RowData` for processing. So columnar appears at the I/O boundary, not in the streaming core.

There's an exception worth knowing: Flink has added **batch operators with columnar/vectorized execution** in some paths (and integrates with Apache Arrow for PyFlink UDFs, where Arrow's columnar in-memory format avoids per-row serialization overhead crossing the JVM↔Python boundary). But the default streaming engine is row-at-a-time.

## Why This Matters for Your Mental Model

| Engine | Native model | Optimized for |
| -------- | ------------- | --------------- |
| Flink | Row, streaming | Low-latency, stateful event processing (OLTP-ish streams) |
| Spark | Micro-batch, increasingly columnar (Tungsten + Arrow) | Throughput, batch analytics |
| DuckDB / ClickHouse | Columnar, vectorized | OLAP scans/aggregations |

Row-based is the right default when you process *whole events as they arrive* and need full-record state. Columnar wins when you scan few columns over huge static datasets. Flink lives in the former world; it borrows columnar tricks only at the edges (file I/O, cross-language UDFs) where vectorization pays off without compromising the streaming model.

If you're touching Flink at the bank (common in financial event/transaction pipelines), the practical takeaway: think in `RowData` for your processing logic, and let connectors handle the columnar↔row conversion at sources/sinks.
