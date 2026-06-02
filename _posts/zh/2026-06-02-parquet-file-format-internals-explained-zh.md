---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Parquet文件格式内部原理解析
translated: true
type: note
---

**问题：** 什么是 Parquet？Row groups、column metadata 和 compression dictionaries 在底层是如何工作的？能否展示实际的源码级实现？

## 答案

Parquet 是一种列式存储格式，包含三个高级部分：文件头（魔数 PAR1）、数据（按 row group → column chunk → page 组织）和文件尾（包含所有元数据：schema、编码、统计信息、压缩信息）。关键要点：**元数据放在文件尾**，因此查询引擎无需扫描整个文件即可先读取它。

### 文件布局（二进制）

```
[PAR1 magic (4 bytes)]
[Row Group 0]
  [Column 0 data]
  [Column 1 data]
  ...
[Row Group 1]
  [Column 0 data]
  ...
[Footer metadata (variable)]
[Footer length (4 bytes)]
[PAR1 magic (4 bytes)]
```

文件尾包含：

- Schema、版本、行数、row group 元数据（偏移量、压缩、编码、min/max/nulls 统计信息）、键值元数据
- 每个 column chunk 包含：偏移量、大小、压缩编解码器、使用的编码、值数量

### 读取元数据（Python）

以下是如何在不读取数据的情况下检查真实 Parquet 文件的结构：

```python
import pyarrow.parquet as pq
import struct

# 读取元数据文件尾
parquet_file = pq.ParquetFile('data.parquet')

# Schema（从文件尾读取，无需扫描数据）
print(parquet_file.schema)

# 文件级元数据
print(parquet_file.metadata)

# Row group 信息
for i in range(parquet_file.num_row_groups):
    rg = parquet_file.metadata.row_group(i)
    print(f"\nRow Group {i}:")
    print(f"  Rows: {rg.num_rows}")
    print(f"  Bytes: {rg.total_byte_size}")

    # 该 row group 内的 column chunks
    for j in range(rg.num_columns):
        col = rg.column(j)
        print(f"  Column {j}:")
        print(f"    Type: {col.physical_type}")
        print(f"    Encoding: {col.encodings}")  # 例如 PLAIN, RLE, DICT
        print(f"    Compression: {col.compression}")  # SNAPPY, GZIP, ZSTD 等
        print(f"    Min: {col.statistics.min}")
        print(f"    Max: {col.statistics.max}")
        print(f"    Null count: {col.statistics.null_count}")
```

### Row Groups：水平分区

Row group 是一个水平分区，包含一个行子集的所有列数据，支持独立的并行处理。

```python
# 默认：约128MB 的 row group
table = pq.read_table('data.parquet')

# 使用自定义 row group 大小写入
pq.write_table(table, 'output.parquet', row_group_size=10000)

# 典型场景：1B 行表，128MB row groups ≈ 8000 个 row groups
# 这可以实现：
# - 通过统计信息（min/max 过滤）跳过整个 row groups
# - 并行读取相关 row groups
# - 容错（一个 row group 损坏 ≠ 整个文件不可用）
```

### Column Chunks 与字典编码

对于具有大量重复值的列，会使用字典编码。这就是 compression dictionaries 发挥作用的地方：

```python
# 当列基数较低时，Parquet 的编码方式为：
# [Dictionary: {0: 'US', 1: 'CN', 2: 'JP'}, ...]
# [Data: 0, 0, 1, 2, 0, ...]  <- 字典索引

# 示例：十亿行中只有3个唯一值的国家列
# 无字典：3B * 2 bytes 每字符串 ≈ 6GB
# 有字典：3 个字符串 + 10 亿个索引 ≈ 50MB

# 检查列是否使用了字典编码：
import pyarrow as pa

table = pa.table({
    'country': ['US', 'US', 'CN', 'JP', 'US'] * 1000000
})

# 使用字典编码写入
pq.write_table(
    table,
    'output.parquet',
    compression='snappy',
    coerce_timestamps='ms',
    use_dictionary=['country']  # 强制对该列使用字典
)

# 在文件尾中验证
pf = pq.ParquetFile('output.parquet')
col_metadata = pf.metadata.row_group(0).column(0)
print(col_metadata.encodings)  # 应包含 PLAIN_DICTIONARY
```

### 解码物理布局

以下是一个小型解析器，展示 Parquet 在字节级别如何结构化数据：

```python
import struct

def read_parquet_footer(filename):
    """读取文件尾而不解析 thrift —— 仅展示结构"""
    with open(filename, 'rb') as f:
        # 定位到最后8个字节：[footer_len (4)] [magic (4)]
        f.seek(-8, 2)
        footer_len_bytes = f.read(4)
        magic = f.read(4)

        if magic != b'PAR1':
            raise ValueError("Not a Parquet file")

        # 文件尾长度为小端序
        footer_len = struct.unpack('<I', footer_len_bytes)[0]

        # 定位到文件尾起始位置
        f.seek(-8 - footer_len, 2)
        footer_bytes = f.read(footer_len)

        print(f"Footer size: {footer_len} bytes")
        print(f"Magic: {magic}")

        # 文件尾以 Thrift 二进制序列化
        # （完整解析需要 Thrift 库，但结构就在那里）
        return footer_bytes

read_parquet_footer('data.parquet')
```

### 压缩与编解码器

```python
# 不同 row group 可以采用不同的压缩策略
# （Parquet 支持按列、按 row group 压缩）

import pyarrow as pa
import pyarrow.parquet as pq
import os

data = pa.table({'numbers': range(1000000)})

# 对比不同编解码器
for codec in ['snappy', 'gzip', 'zstd', 'lz4']:
    try:
        pq.write_table(data, f'test_{codec}.parquet', compression=codec)
        size = os.path.getsize(f'test_{codec}.parquet')
        print(f"{codec}: {size / (1024*1024):.2f} MB")
    except:
        print(f"{codec}: not available")
```

Zstd 通常在压缩比与速度的权衡上表现最佳。

### 为何重要

该架构实现了以下功能：

1. **谓词下推**：过滤 `amount > 500` → 读取文件尾统计信息 → 跳过 max(amount) ≤ 500 的 row groups
2. **列剪枝**：查询50列中的3列 → 仅读取这3个 column chunks
3. **单遍写入**：数据先写入，元数据最后写入 → 无需寻道
4. **容错**：一个 row group 损坏 ≠ 文件不可读

### 深入探索

该格式明确将元数据与数据分离，允许列被分割到多个文件，并通过单个元数据文件引用。这正是 Iceberg 和 Delta 利用 Parquet 的方式 —— 它们将自己的元数据层叠在顶部。

**参考：**

- [Apache Parquet Format Spec](https://github.com/apache/parquet-format)
- [Parquet File Anatomy](https://dev.to/databro/apache-parquet-file-anatomy-row-groups-column-chunks-pages-and-metadata-explained-4ebg)
- [PyArrow Parquet Docs](https://arrow.apache.org/docs/python/parquet.html)