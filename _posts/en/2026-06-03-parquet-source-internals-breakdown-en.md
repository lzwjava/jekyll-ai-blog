---
audio: false
generated: true
image: false
lang: en
layout: post
title: Parquet Source Internals Breakdown
translated: false
type: note
---

Now I have all the actual source. Here's the full source-level breakdown.

---

## Parquet: Source-Level Internals

### 1. The Format Spec (Thrift IDL)

Everything starts with the Thrift definition in `parquet-format/src/main/thrift/parquet.thrift`. This IS the spec — every Parquet reader/writer must conform to these structs.

**FileMetaData** — the footer, written last:

```thrift
struct FileMetaData {
  1: required i32 version              // always 1
  2: required list<SchemaElement> schema  // DFS-flattened tree
  3: required i64 num_rows
  4: required list<RowGroup> row_groups
  5: optional list<KeyValue> key_value_metadata
  6: optional string created_by
  7: optional list<ColumnOrder> column_orders  // min/max sort order
}
```

**RowGroup** — horizontal partition:

```thrift
struct RowGroup {
  1: required list<ColumnChunk> columns   // one per schema leaf
  2: required i64 total_byte_size         // uncompressed
  3: required i64 num_rows
  4: optional list<SortingColumn> sorting_columns
  5: optional i64 file_offset             // byte offset to first page
  6: optional i64 total_compressed_size
  7: optional i16 ordinal
}
```

**ColumnChunk** — pointer to column data + metadata:

```thrift
struct ColumnChunk {
  1: optional string file_path           // external file (rare)
  2: required i64 file_offset = 0        // deprecated
  3: optional ColumnMetaData meta_data   // THE key field
  4: optional i64 offset_index_offset    // page index locations
  5: optional i32 offset_index_length
  6: optional i64 column_index_offset    // page-level stats
  7: optional i32 column_index_length
}
```

**ColumnMetaData** — per-column stats, encodings, compression:

```thrift
struct ColumnMetaData {
  1: required Type type
  2: required list<Encoding> encodings          // e.g. [RLE_DICTIONARY, PLAIN]
  3: required list<string> path_in_schema
  4: required CompressionCodec codec             // SNAPPY, ZSTD, GZIP, etc
  5: required i64 num_values
  6: required i64 total_uncompressed_size
  7: required i64 total_compressed_size
  9: required i64 data_page_offset              // byte offset to first data page
  10: optional i64 index_page_offset
  11: optional i64 dictionary_page_offset       // byte offset to dict page
  12: optional Statistics statistics             // min/max/null_count
  13: optional list<PageEncodingStats> encoding_stats
}
```

**PageHeader** — each page has a header before the data:

```thrift
struct PageHeader {
  1: required PageType type              // DATA_PAGE, DICTIONARY_PAGE, DATA_PAGE_V2
  2: required i32 uncompressed_page_size
  3: required i32 compressed_page_size
  4: optional i32 crc
  5: optional DataPageHeader data_page_header
  7: optional DictionaryPageHeader dictionary_page_header
  8: optional DataPageHeaderV2 data_page_header_v2
}
```

**Statistics** — stored per-page AND per-column-chunk in the footer:

```thrift
struct Statistics {
  1: optional binary max              // deprecated, signed comparison only
  2: optional binary min              // deprecated
  3: optional i64 null_count
  4: optional i64 distinct_count
  5: optional binary max_value        // current: respects ColumnOrder
  6: optional binary min_value        // current
  9: optional i64 nan_count           // for FLOAT/DOUBLE/FLOAT16
}
```

### 2. How the Writer Actually Works (Java source)

From `parquet-hadoop/.../ParquetFileWriter.java`:

**Step 1: Write magic header**

```java
public void start() throws IOException {
    state = state.start();
    byte[] magic = MAGIC;  // "PAR1" = [0x50, 0x41, 0x52, 0x31]
    if (null != fileEncryptor && fileEncryptor.isFooterEncrypted()) {
        magic = EFMAGIC;   // "PARE" for encrypted footer
    }
    out.write(magic);
}
```

**Step 2: Start row group (alignment + metadata init)**

```java
public void startBlock(long recordCount) throws IOException {
    state = state.startBlock();
    alignment.alignForRowGroup(out);  // pad to block boundary (HDFS blocks)
    currentBlock = new BlockMetaData();
    currentRecordCount = recordCount;
    currentColumnIndexes = new ArrayList<>();
    currentOffsetIndexes = new ArrayList<>();
}
```

**Step 3: Start column (reset accumulators)**

```java
public void startColumn(ColumnDescriptor descriptor, long valueCount,
                         CompressionCodecName compressionCodecName) {
    state = state.startColumn();
    currentChunkPath = ColumnPath.get(descriptor.getPath());
    currentChunkType = descriptor.getPrimitiveType();
    currentChunkCodec = compressionCodecName;
    currentChunkValueCount = valueCount;
    currentChunkFirstDataPage = -1;
    compressedLength = 0;
    uncompressedLength = 0;
    currentStatistics = null;
    columnIndexBuilder = ColumnIndexBuilder.getBuilder(...);
    offsetIndexBuilder = OffsetIndexBuilder.getBuilder();
}
```

**Step 4: Write dictionary page (if dictionary-encoded)**

```java
public void writeDictionaryPage(DictionaryPage dictionaryPage, ...) {
    state = state.write();
    currentChunkDictionaryPageOffset = out.getPos();  // remember offset
    int uncompressedSize = dictionaryPage.getUncompressedSize();
    int compressedPageSize = dictionaryPage.getBytes().size();
    // Write PageHeader (Thrift-serialized) with DictionaryPageHeader
    metadataConverter.writeDictionaryPageHeader(
        uncompressedSize, compressedPageSize,
        dictionaryPage.getDictionarySize(),
        dictionaryPage.getEncoding(), ...);
    // Write the actual dictionary bytes
    dictionaryPage.getBytes().writeAllTo(out);
    this.uncompressedLength += uncompressedSize + headerSize;
    this.compressedLength += compressedPageSize + headerSize;
}
```

**Step 5: Write data pages**

```java
public void writeDataPage(int valueCount, int uncompressedPageSize,
                           BytesInput bytes, Statistics<?> statistics, ...) {
    state = state.write();
    long beforeHeader = out.getPos();
    if (currentChunkFirstDataPage < 0) {
        currentChunkFirstDataPage = beforeHeader;  // first data page offset
    }
    int compressedPageSize = bytes.size();
    // Write PageHeader with DataPageHeader (contains encoding, stats)
    metadataConverter.writeDataPageV1Header(
        uncompressedPageSize, compressedPageSize, valueCount,
        rlEncoding, dlEncoding, valuesEncoding, ...);
    // Write the actual page data (rep levels + def levels + values)
    bytes.writeAllTo(out);
    this.uncompressedLength += uncompressedPageSize + headerSize;
    this.compressedLength += compressedPageSize + headerSize;
    // Update statistics
    currentStatistics = Statistics.merge(currentStatistics, statistics);
}
```

**Step 6: End column (build ColumnChunkMetaData)**

```java
public void endColumn() throws IOException {
    state = state.endColumn();
    // Build per-page column index (min/max per page)
    currentColumnIndexes.add(columnIndexBuilder.build());
    currentOffsetIndexes.add(offsetIndexBuilder.build(currentChunkFirstDataPage));
    // Add column chunk metadata to current row group
    currentBlock.addColumn(ColumnChunkMetaData.get(
        currentChunkPath, currentChunkType, currentChunkCodec,
        encodingStatsBuilder.build(), currentEncodings,
        currentStatistics, currentChunkFirstDataPage,
        currentChunkDictionaryPageOffset,
        currentChunkValueCount, compressedLength, uncompressedLength, ...));
}
```

**Step 7: End row group**

```java
public void endBlock() throws IOException {
    state = state.endBlock();
    currentBlock.setRowCount(currentRecordCount);
    currentBlock.setOrdinal(blocks.size());
    blocks.add(currentBlock);  // append to list of row groups
}
```

**Step 8: Serialize footer (THE critical step)**

```java
public void end(Map<String, String> extraMetaData) throws IOException {
    state = state.end();
    // Write column indexes and offset indexes AFTER data
    serializeColumnIndexes(columnIndexes, blocks, out, fileEncryptor);
    serializeOffsetIndexes(offsetIndexes, blocks, out, fileEncryptor);
    serializeBloomFilters(bloomFilters, blocks, out, fileEncryptor);
    // Build footer and serialize
    this.footer = new ParquetMetadata(
        new FileMetaData(schema, extraMetaData, Version.FULL_VERSION), blocks);
    serializeFooter(footer, out, fileEncryptor, metadataConverter);
}

private static void serializeFooter(...) throws IOException {
    long footerIndex = out.getPos();
    // Convert internal metadata to Thrift format
    FileMetaData parquetMetadata = metadataConverter.toParquetMetadata(...);
    // Write Thrift-serialized FileMetaData
    writeFileMetaData(parquetMetadata, out);
    // Write footer length as little-endian 4 bytes
    BytesUtils.writeIntLittleEndian(out, (out.getPos() - footerIndex));
    // Write PAR1 magic again
    out.write(MAGIC);  // "PAR1"
}
```

### 3. Dictionary Encoding: The Actual Encoder

From `parquet-column/.../DictionaryValuesWriter.java`:

```java
public abstract class DictionaryValuesWriter extends ValuesWriter {
    protected int maxDictionaryByteSize;  // e.g. parquet.dictionary.page.size
    protected boolean dictionaryTooBig;
    protected long dictionaryByteSize;
    protected IntList encodedValues;      // integer IDs into dictionary

    // When to fall back to PLAIN encoding
    public boolean shouldFallBack() {
        return dictionaryByteSize > maxDictionaryByteSize
            || getDictionarySize() > MAX_DICTIONARY_ENTRIES;
    }

    // Check if dictionary actually saves space
    public boolean isCompressionSatisfying(long rawSize, long encodedSize) {
        return (encodedSize + dictionaryByteSize) < rawSize;
    }

    // Serialize: RLE/bit-pack the integer IDs
    public BytesInput getBytes() {
        int maxDicId = getDictionarySize() - 1;
        int bitWidth = BytesUtils.getWidthFromMaxInt(maxDicId);
        RunLengthBitPackingHybridEncoder encoder =
            new RunLengthBitPackingHybridEncoder(bitWidth, ...);
        IntIterator iterator = encodedValues.iterator();
        while (iterator.hasNext()) {
            encoder.writeInt(iterator.next());
        }
        // Format: [1-byte bitWidth] [RLE-encoded IDs]
        byte[] bytesHeader = new byte[] {(byte) bitWidth};
        BytesInput rleEncodedBytes = encoder.toBytes();
        return concat(BytesInput.from(bytesHeader), rleEncodedBytes);
    }
}
```

**Concrete: PlainBinaryDictionaryValuesWriter** (for strings):

```java
public static class PlainBinaryDictionaryValuesWriter extends DictionaryValuesWriter {
    protected Object2IntMap<Binary> binaryDictionaryContent;

    public void writeBytes(Binary v) {
        int id = binaryDictionaryContent.getInt(v);
        if (id == -1) {
            id = binaryDictionaryContent.size();
            binaryDictionaryContent.put(v.copy(), id);
            dictionaryByteSize += 4L + v.length();  // 4-byte length prefix + bytes
        }
        encodedValues.add(id);
    }

    public DictionaryPage toDictPageAndClose() {
        PlainValuesWriter dictionaryEncoder = new PlainValuesWriter(...);
        Iterator<Binary> binaryIterator = binaryDictionaryContent.keySet().iterator();
        for (int i = 0; i < lastUsedDictionarySize; i++) {
            dictionaryEncoder.writeBytes(binaryIterator.next());
        }
        return dictPage(dictionaryEncoder);
    }
}
```

### 4. Physical File Layout

All of the above writes bytes in this exact order:

```
[PAR1]                                          ← 4 bytes, start() writes this
[Row Group 0]
  [PageHeader (Thrift)] [Dictionary Page bytes] ← writeDictionaryPage()
  [PageHeader (Thrift)] [Data Page bytes]       ← writeDataPage() × N
  [PageHeader (Thrift)] [Data Page bytes]
  ...
[Row Group 1]
  [PageHeader (Thrift)] [Dictionary Page bytes]
  [PageHeader (Thrift)] [Data Page bytes]
  ...
[Column Index 0] [Column Index 1] ...          ← serializeColumnIndexes()
[Offset Index 0] [Offset Index 1] ...          ← serializeOffsetIndexes()
[Bloom Filter 0] [Bloom Filter 1] ...          ← serializeBloomFilters()
[FileMetaData (Thrift)]                         ← writeFileMetaData(), the footer
[footer_length (4 bytes, LE)]                   ← BytesUtils.writeIntLittleEndian()
[PAR1]                                          ← 4 bytes, end of file
```

A reader starts by seeking to `file_size - 8`, reading the 4-byte footer length, then seeking back to read the Thrift-serialized `FileMetaData`. That gives it ALL row group offsets, column offsets, statistics, encodings, and compression codecs — without reading any actual data.

### 5. Why This Design Works

- **Predicate pushdown**: Reader reads footer → gets `ColumnMetaData.statistics.{min_value, max_value}` per column chunk → skips entire row groups where `max_value < filter_value`.
- **Column pruning**: Footer has `ColumnChunk` list ordered by schema. Reader picks 3 of 50 columns → reads only those 3 column chunks' byte ranges.
- **Dictionary fallback**: Writer accumulates values in `dictionaryContent` map. If `dictionaryByteSize > maxDictionaryByteSize`, falls back to PLAIN. After writing a page, `isCompressionSatisfying()` checks if the dict+indices actually saved space vs raw values.
- **Single-pass I/O**: Data written sequentially, metadata at end. No seeking during write. Reader seeks once to footer, then once per column chunk.

### References

- [Apache Parquet Format Thrift IDL](https://github.com/apache/parquet-format/blob/master/src/main/thrift/parquet.thrift)
- [ParquetFileWriter.java](https://github.com/apache/parquet-java/blob/master/parquet-hadoop/src/main/java/org/apache/parquet/hadoop/ParquetFileWriter.java)
- [DictionaryValuesWriter.java](https://github.com/apache/parquet-java/blob/master/parquet-column/src/main/java/org/apache/parquet/column/values/dictionary/DictionaryValuesWriter.java)
- [Parquet Format Spec](https://github.com/apache/parquet-format/blob/master/README.md)
