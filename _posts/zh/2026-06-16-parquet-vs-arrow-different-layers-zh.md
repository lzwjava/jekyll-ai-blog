---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Parquet与Arrow：不同的层
translated: true
type: note
---

**问题：** 在 Parquet 和 Arrow 之间，哪个性能更好？

**回答：**

它们并非真正的竞争者——在数据栈的不同层级解决**不同的问题**。但我们可以精确地比较它们。

## 它们是什么

| | Parquet | Arrow |
| ------- | --------- | ------- |
| 类型 | **列式存储格式**（磁盘上） | **列式内存格式**（内存中） |
| 设计目标 | 长期存储、压缩、查询下推 | 零拷贝 IPC、进程内分析、SIMD |
| 行组/批次 | 行组（MB 级数据块） | RecordBatches（可配置） |
| 编码方式 | RLE、字典、增量、位打包 + Snappy/Zstd/LZ4 | 原始类型缓冲区（默认无压缩） |
| 标准归属 | Apache（源于 Twitter/Cloudera） | Apache（源于 Wes McKinney / Cloudera） |

## 性能分解

### 磁盘 I/O → Parquet 获胜

Parquet 的压缩与编码意味着文件大小比原始 Arrow IPC 文件**小 5–10 倍**。对于从 S3/NFS 的冷读取，Parquet 凭借谓词下推和列剪枝大幅胜出——你在**文件格式层面**就跳过了数据读取。

```python
# Parquet 只读取你请求的列——在 C++ 读取器层面实现
import pyarrow.parquet as pq
table = pq.read_table("data.parquet", columns=["user_id", "event"])
```

### 内存计算 → Arrow 获胜（差距悬殊）

Arrow 缓冲区具有 **SIMD 友好**、缓存对齐、进程/语言间零拷贝的特点。无需反序列化。

```python
import pyarrow as pa
import pyarrow.compute as pc

# SIMD 向量化，无 Python 循环开销
result = pc.sum(table.column("revenue"))
```

Parquet 数据在进行计算前必须先**解码为 Arrow**——这正是 DuckDB、Polars 和 pandas 2.0 内部所做的。

### 序列化 / IPC → Arrow 获胜

Arrow IPC（Feather v2）本质上是零拷贝的。读取和写回一个 1GB 数据集：

```
Parquet 写入：~2–5 秒（压缩开销）
Arrow IPC 写入：~0.1–0.3 秒（memcpy 速度）

Parquet 读取：~0.5–1 秒（解压 + 解码）
Arrow IPC 读取：~0.05 秒（mmap，近乎零）
```

### 查询引擎同时使用两者

真正的模式是**磁盘上的 Parquet → 内存中的 Arrow**：

```
S3/磁盘          ──[Parquet]──►  DuckDB/Polars  ──[Arrow]──►  结果
（压缩、                        （解码为
 列剪枝、                        Arrow 缓冲区，
 谓词下推）                       运行 SIMD 操作）
```

DuckDB、Polars、DataFusion、Spark 和 BigQuery 都在内部执行此操作。

## 具体数据（粗略，依赖硬件）

| 操作 | Parquet | Arrow IPC |
| --- | --- | --- |
| 从磁盘读取 1GB | ~0.5–2 秒 | ~0.05–0.1 秒（mmap） |
| 写入 1GB | ~2–5 秒 | ~0.1–0.3 秒 |
| 文件大小（原始 1GB） | ~100–300MB | ~900MB–1GB |
| 列扫描（内存中） | 不适用（已解码） | ~1–5 GB/s SIMD |

## 何时使用哪个

**使用 Parquet 的场景：**

- 长期存储数据集（S3、HDFS、本地）
- 数据集很大且你只查询部分列
- 需要跨系统互操作性（Spark、BigQuery、Athena、DuckDB）
- 冷存储 / 归档

**使用 Arrow（IPC/Feather）的场景：**

- 在进程间传递大型数据集（例如 Python → Rust CLI 代理）
- 缓存管道中的中间结果（避免重复解码）
- 构建对延迟敏感的数据服务
- 进程间的共享内存（Arrow 的 `plasma` 存储或 `mmap`）

## 实际示例——你的 CLI 代理工作流

如果你的 `ww`/`zz` 代理处理大型数据集：

```python
import pyarrow as pa
import pyarrow.ipc as ipc
import pyarrow.parquet as pq

# 从冷存储加载（Parquet，压缩）
table = pq.read_table("events.parquet", columns=["ts", "event", "user_id"])

# 将热工作集缓存为 Arrow IPC，以便快速重读
with ipc.new_file("events_cache.arrow", table.schema) as writer:
    writer.write_table(table)

# 下次运行——亚 100 毫秒重新加载
with ipc.open_file("events_cache.arrow") as reader:
    table = reader.read_all()
```

## 总结

- **Parquet** = 最适合**存储效率和磁盘 I/O**（压缩、列剪枝、生态系统兼容性）
- **Arrow** = 最适合**计算吞吐量和 IPC**（SIMD、零拷贝、无序列化开销）
- 实际中：**Parquet 存储它，Arrow 处理它**——它们被设计为协同工作，而非竞争。
