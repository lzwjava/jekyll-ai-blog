---
audio: false
generated: true
image: false
lang: en
layout: post
title: Parquet File Structure Hierarchy
translated: false
type: note
---

Question: What's the relationship between row groups, column metadata, and compression dictionaries in Apache Parquet?

Answer:

These three are **hierarchical layers** of a Parquet file's physical structure:

```
┌─ Parquet File
   ├─ [Magic: "PAR1"]
   ├─ Row Group 0
   │  ├─ Column Chunk (col_0)
   │  │  ├─ Dictionary Page (optional)
   │  │  │  └─ Compression Dictionary (e.g., 1000 unique strings)
   │  │  ├─ Data Pages (compressed using dict + codec)
   │  │  └─ Column Metadata
   │  │     ├─ statistics (min/max)
   │  │     ├─ encoding (PLAIN_DICTIONARY, RLE, etc.)
   │  │     └─ compression (SNAPPY, GZIP, ZSTD)
   │  ├─ Column Chunk (col_1)
   │  └─ ...
   ├─ Row Group 1
   │  └─ [same structure]
   ├─ [Metadata Footer]
   │  ├─ FileMetaData
   │  │  ├─ schema
   │  │  ├─ num_rows
   │  │  └─ row_groups[] (metadata for each row group)
   │  │     └─ RowGroup.columns[]
   │  │        └─ ColumnMetaData (points to dictionary page loc, stats, etc.)
   └─ [Magic + footer length]
```

**Key relationships:**

1. **Row Group → Column Chunks**: A row group contains one `ColumnChunk` per column. Row groups are horizontal partitions (how many rows before writing metadata).

2. **ColumnChunk → Dictionary Page → Compression Dictionary**:
   - The dictionary page *is* the compressed dictionary, physically stored at the start of the column chunk
   - Subsequent data pages reference dictionary indices instead of raw values
   - Only written if `encoding=PLAIN_DICTIONARY` and `is_sorted=false`

3. **ColumnMetadata** points to:
   - Where the dictionary page starts (`meta_data.dictionary_page_offset`)
   - How it's compressed (`meta_data.codec`, e.g., SNAPPY)
   - Data page locations (`meta_data.data_page_offset`)
   - Statistics about the column (cardinality helps reader know if dict is useful)

**From the Thrift schema (parquet.thrift):**

```thrift
struct ColumnChunk {
  1: optional i64 file_path,              // always null in single file
  2: required i64 file_offset,            // byte offset in file
  3: required ColumnMetaData meta_data,   // points to dict page, data pages
  4: optional i32 offset_index_offset,
  5: optional i32 offset_index_length,
}

struct ColumnMetaData {
  1: required Type type,
  2: required list<Encoding> encodings,   // e.g., [RLE, PLAIN_DICTIONARY, RLE_PACKED]
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
  2: required Encoding encoding,          // always RLE or PLAIN
  3: optional bool is_sorted,
}
```

**Example: Reading a dictionary-encoded column:**

```python
# When a reader hits this column chunk:
# 1. Check meta_data.dictionary_page_offset → seek to byte position
# 2. Read DictionaryPageHeader + decompress with meta_data.codec
# 3. Load the dictionary (e.g., ["apple", "banana", "cherry"])
# 4. For each data page: read indices [0, 2, 1, 0, ...] → map to dict values
# 5. If meta_data.is_sorted=true, indices are monotonic (optimization)

with pq.ParquetFile("file.parquet") as pf:
    meta = pf.metadata
    rg = meta.row_group(0)
    col_meta = rg.column(0)

    print(f"Dict offset: {col_meta.dictionary_page_offset}")
    print(f"Data offset: {col_meta.data_page_offset}")
    print(f"Codec: {col_meta.codec}")  # e.g., "snappy"
    print(f"Total compressed: {col_meta.total_compressed_size}")
```

**Why this matters:**

- **Row groups** are the unit of parallelism — readers process them independently
- **Column metadata** is the manifest — tells you where everything is and how it's compressed
- **Compression dictionary** is the compression tactic — reduces size for low-cardinality columns (strings with repeated values save ~70-90% space)

The dictionary is **optional** but automatic in Parquet libraries for string/binary columns. You can disable it, but columnar compression thrives on it.
