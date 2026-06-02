---
audio: false
generated: true
image: false
lang: en
layout: post
title: Parquet File Format Internals Explained
translated: false
type: note
---

**Question:** What is Parquet? How do row groups, column metadata, and compression dictionaries work under the hood? Can you show the actual source-level implementation?

## Answer

Parquet is a columnar storage format with three high-level sections: header (magic number PAR1), data (organized into row groups → column chunks → pages), and footer (containing all metadata: schema, encoding, statistics, compression info). The key insight: **metadata goes in the footer**, so query engines read it first without scanning the entire file.

### File Layout (Binary)

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

The footer contains:

- Schema, version, row count, row group metadata (offsets, compression, encodings, statistics for min/max/nulls), key-value metadata
- Each column chunk has: offset, size, compression codec, encodings used, number of values

### Reading the Metadata (Python)

Here's how to inspect a real Parquet file's structure without reading data:

```python
import pyarrow.parquet as pq
import struct

# Read metadata footer
parquet_file = pq.ParquetFile('data.parquet')

# Schema (read from footer, no data scanning)
print(parquet_file.schema)

# File-level metadata
print(parquet_file.metadata)

# Row group info
for i in range(parquet_file.num_row_groups):
    rg = parquet_file.metadata.row_group(i)
    print(f"\nRow Group {i}:")
    print(f"  Rows: {rg.num_rows}")
    print(f"  Bytes: {rg.total_byte_size}")

    # Column chunks within this row group
    for j in range(rg.num_columns):
        col = rg.column(j)
        print(f"  Column {j}:")
        print(f"    Type: {col.physical_type}")
        print(f"    Encoding: {col.encodings}")  # e.g., PLAIN, RLE, DICT
        print(f"    Compression: {col.compression}")  # SNAPPY, GZIP, ZSTD, etc
        print(f"    Min: {col.statistics.min}")
        print(f"    Max: {col.statistics.max}")
        print(f"    Null count: {col.statistics.null_count}")
```

### Row Groups: Horizontal Partitioning

A row group is a horizontal partition containing all column data for a subset of rows, allowing independent parallel processing.

```python
# Default: row groups of ~128MB
table = pq.read_table('data.parquet')

# Write with custom row group size
pq.write_table(table, 'output.parquet', row_group_size=10000)

# Typical scenario: 1B row table with 128MB row groups = ~8000 row groups
# This enables:
# - Skip entire row groups via statistics (min/max filtering)
# - Read only relevant row groups in parallel
# - Fault tolerance (corrupt one row group ≠ lose entire file)
```

### Column Chunks & Dictionary Encoding

Dictionary encoding is used for columns with many repeated values. This is where compression dictionaries come in:

```python
# When a column has low cardinality, Parquet encodes as:
# [Dictionary: {0: 'US', 1: 'CN', 2: 'JP'}, ...]
# [Data: 0, 0, 1, 2, 0, ...]  <- indexes into dictionary

# Example: country column with only 3 unique values in a billion rows
# Without dict: 3B * 2 bytes per string ≈ 6GB
# With dict: 3 strings + 1B indexes ≈ 50MB

# Check if column used dictionary encoding:
import pyarrow as pa

table = pa.table({
    'country': ['US', 'US', 'CN', 'JP', 'US'] * 1000000
})

# Write with dictionary encoding
pq.write_table(
    table,
    'output.parquet',
    compression='snappy',
    coerce_timestamps='ms',
    use_dictionary=['country']  # Force dict for this column
)

# Verify in footer
pf = pq.ParquetFile('output.parquet')
col_metadata = pf.metadata.row_group(0).column(0)
print(col_metadata.encodings)  # Should include PLAIN_DICTIONARY
```

### Decoding the Physical Layout

Here's a minimal parser to show how Parquet structures data at byte level:

```python
import struct

def read_parquet_footer(filename):
    """Read footer without parsing thrift — just show structure"""
    with open(filename, 'rb') as f:
        # Seek to last 8 bytes: [footer_len (4)] [magic (4)]
        f.seek(-8, 2)
        footer_len_bytes = f.read(4)
        magic = f.read(4)

        if magic != b'PAR1':
            raise ValueError("Not a Parquet file")

        # Footer length is little-endian
        footer_len = struct.unpack('<I', footer_len_bytes)[0]

        # Seek to footer start
        f.seek(-8 - footer_len, 2)
        footer_bytes = f.read(footer_len)

        print(f"Footer size: {footer_len} bytes")
        print(f"Magic: {magic}")

        # Footer is serialized as Thrift binary
        # (full parsing requires Thrift library, but structure is there)
        return footer_bytes

read_parquet_footer('data.parquet')
```

### Compression & Codecs

```python
# Different compression strategies for different row groups
# (Parquet supports per-column, per-row-group compression)

import pyarrow as pa
import pyarrow.parquet as pq

data = pa.table({'numbers': range(1000000)})

# Benchmark different codecs
for codec in ['snappy', 'gzip', 'zstd', 'lz4']:
    try:
        pq.write_table(data, f'test_{codec}.parquet', compression=codec)
        size = os.path.getsize(f'test_{codec}.parquet')
        print(f"{codec}: {size / (1024*1024):.2f} MB")
    except:
        print(f"{codec}: not available")
```

Zstd typically wins on ratio-to-speed.

### Why This Matters

The architecture enables:

1. **Predicate pushdown**: Filter on `amount > 500` → read footer stats → skip row groups where max(amount) ≤ 500
2. **Column pruning**: Query 3 of 50 columns → read only those 3 column chunks
3. **Single-pass writing**: Data written first, metadata at end → no seeking
4. **Fault tolerance**: Corrupt one row group ≠ unreadable file

### Dive Deeper

The format is explicitly designed to separate metadata from data, allowing columns to be split into multiple files with a single metadata file reference. This is how Iceberg and Delta leverage Parquet — they layer their own metadata on top.

**References:**

- [Apache Parquet Format Spec](https://github.com/apache/parquet-format)
- [Parquet File Anatomy](https://dev.to/databro/apache-parquet-file-anatomy-row-groups-column-chunks-pages-and-metadata-explained-4ebg)
- [PyArrow Parquet Docs](https://arrow.apache.org/docs/python/parquet.html)
