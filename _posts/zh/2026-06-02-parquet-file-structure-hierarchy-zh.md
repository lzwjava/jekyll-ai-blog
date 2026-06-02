---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Parquet 文件结构层次
translated: true
type: note
---

问题：Apache Parquet 中行组（Row Group）、列元数据（Column Metadata）和压缩字典（Compression Dictionary）之间有什么关系？

答案：

这三者构成了 Parquet 文件物理结构中的**层级关系**：

```
┌─ Parquet File
   ├─ [Magic: "PAR1"]
   ├─ Row Group 0
   │  ├─ Column Chunk (col_0)
   │  │  ├─ Dictionary Page (可选)
   │  │  │  └─ Compression Dictionary (例如，1000 个唯一字符串)
   │  │  ├─ Data Pages (使用 dict + codec 压缩)
   │  │  └─ Column Metadata
   │  │     ├─ statistics (min/max)
   │  │     ├─ encoding (PLAIN_DICTIONARY, RLE 等)
   │  │     └─ compression (SNAPPY, GZIP, ZSTD)
   │  ├─ Column Chunk (col_1)
   │  └─ ...
   ├─ Row Group 1
   │  └─ [相同结构]
   ├─ [Metadata Footer]
   │  ├─ FileMetaData
   │  │  ├─ schema
   │  │  ├─ num_rows
   │  │  └─ row_groups[] (每个行组的元数据)
   │  │     └─ RowGroup.columns[]
   │  │        └─ ColumnMetaData (指向字典页位置、统计信息等)
   └─ [Magic + footer length]
```

**关键关系：**

1.  **Row Group → Column Chunks**：一个行组包含每个列的一个 `ColumnChunk`。行组是水平分区（写入元数据之前包含多少行）。

2.  **ColumnChunk → Dictionary Page → Compression Dictionary**：
    *   字典页*就是*压缩后的字典，物理上存储在列块的开头
    *   后续的数据页引用字典索引，而不是原始值
    *   仅在 `encoding=PLAIN_DICTIONARY` 且 `is_sorted=false` 时写入

3.  **ColumnMetadata** 指向：
    *   字典页的起始位置 (`meta_data.dictionary_page_offset`)
    *   字典页的压缩方式 (`meta_data.codec`，例如 SNAPPY)
    *   数据页的位置 (`meta_data.data_page_offset`)
    *   关于该列的统计信息（基数帮助读取器判断字典是否有效）

**来自 Thrift schema (parquet.thrift)：**

```thrift
struct ColumnChunk {
  1: optional i64 file_path,              // 单文件中始终为 null
  2: required i64 file_offset,            // 文件中的字节偏移
  3: required ColumnMetaData meta_data,   // 指向字典页、数据页
  4: optional i32 offset_index_offset,
  5: optional i32 offset_index_length,
}

struct ColumnMetaData {
  1: required Type type,
  2: required list<Encoding> encodings,   // 例如 [RLE, PLAIN_DICTIONARY, RLE_PACKED]
  3: required list<PageType> path_in_schema,
  4: required i64 num_values,
  5: required i64 total_uncompressed_size,
  6: required i64 total_compressed_size,
  7: optional list<KeyValue> key_value_metadata,
  8: optional Statistics statistics,
  9: required Compression codec,          // SNAPPY, GZIP, ZSTD
  10: optional i64 dictionary_page_offset,
  11: optional i64 data_page_offset,
}

struct DataPageHeader {
  1: required i32 num_values,
  2: required Encoding encoding,
  3: required Encoding definition_level_encoding,
  4: required Encoding repetition_level_encoding,
  5: optional Statistics statistics,
}

struct DictionaryPageHeader {
  1: required i32 num_values,
  2: required Encoding encoding,          // 始终为 RLE 或 PLAIN
  3: optional bool is_sorted,
}
```

**示例：读取一个字典编码的列：**

```python
# 当读取器遇到此列块时：
# 1. 检查 meta_data.dictionary_page_offset → 跳转到该字节位置
# 2. 读取 DictionaryPageHeader 并用 meta_data.codec 解压缩
# 3. 加载字典（例如 ["apple", "banana", "cherry"]）
# 4. 对于每个数据页：读取索引 [0, 2, 1, 0, ...] → 映射到字典值
# 5. 如果 meta_data.is_sorted=true，索引是单调的（优化）

with pq.ParquetFile("file.parquet") as pf:
    meta = pf.metadata
    rg = meta.row_group(0)
    col_meta = rg.column(0)

    print(f"Dict offset: {col_meta.dictionary_page_offset}")
    print(f"Data offset: {col_meta.data_page_offset}")
    print(f"Codec: {col_meta.codec}")  # 例如 "snappy"
    print(f"Total compressed: {col_meta.total_compressed_size}")
```

**为什么这很重要：**

*   **Row Groups** 是并行处理单元——读取器可以独立处理它们
*   **Column Metadata** 是清单——告诉你所有内容的位置以及压缩方式
*   **Compression Dictionary** 是压缩策略——对低基数列减小体积（重复值的字符串节省约 70-90% 空间）

字典是**可选的**，但在 Parquet 库中对于字符串/二进制列是自动启用的。你可以禁用它，但列式压缩依赖于它。