---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Parquet 源码内部剖析
translated: true
type: note
---

现在我已经获得了所有的实际源代码。以下是完整的源码级分析。

---

## Parquet: 源码级内部机制

### 1. 格式规范（Thrift IDL）

一切都始于 `parquet-format/src/main/thrift/parquet.thrift` 中的 Thrift 定义。这本身就是规范——所有 Parquet 读写器都必须遵循这些结构体。

**FileMetaData** —— 页脚，最后写入：

```thrift
struct FileMetaData {
  1: required i32 version              // 始终为 1
  2: required list<SchemaElement> schema  // DFS 展平的树
  3: required i64 num_rows
  4: required list<RowGroup> row_groups
  5: optional list<KeyValue> key_value_metadata
  6: optional string created_by
  7: optional list<ColumnOrder> column_orders  // 最小/最大排序顺序
}
```

**RowGroup** —— 水平分区：

```thrift
struct RowGroup {
  1: required list<ColumnChunk> columns   // 每个 schema 叶子节点一个
  2: required i64 total_byte_size         // 未压缩大小
  3: required i64 num_rows
  4: optional list<SortingColumn> sorting_columns
  5: optional i64 file_offset             // 第一个页面的字节偏移
  6: optional i64 total_compressed_size
  7: optional i16 ordinal
}
```

**ColumnChunk** —— 指向列数据 + 元数据的指针：

```thrift
struct ColumnChunk {
  1: optional string file_path           // 外部文件（极少使用）
  2: required i64 file_offset = 0        // 已弃用
  3: optional ColumnMetaData meta_data   // 关键字段
  4: optional i64 offset_index_offset    // 页面索引位置
  5: optional i32 offset_index_length
  6: optional i64 column_index_offset    // 页面级统计信息
  7: optional i32 column_index_length
}
```

**ColumnMetaData** —— 每列的统计信息、编码、压缩：

```thrift
struct ColumnMetaData {
  1: required Type type
  2: required list<Encoding> encodings          // 例如 [RLE_DICTIONARY, PLAIN]
  3: required list<string> path_in_schema
  4: required CompressionCodec codec             // SNAPPY, ZSTD, GZIP 等
  5: required i64 num_values
  6: required i64 total_uncompressed_size
  7: required i64 total_compressed_size
  9: required i64 data_page_offset              // 第一个数据页面的字节偏移
  10: optional i64 index_page_offset
  11: optional i64 dictionary_page_offset       // 字典页面的字节偏移
  12: optional Statistics statistics             // 最小值/最大值/空值计数
  13: optional list<PageEncodingStats> encoding_stats
}
```

**PageHeader** —— 每个页面在数据之前都有一个头部：

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

**Statistics** —— 在页脚中按页面和列块存储：

```thrift
struct Statistics {
  1: optional binary max              // 已弃用，仅支持有符号比较
  2: optional binary min              // 已弃用
  3: optional i64 null_count
  4: optional i64 distinct_count
  5: optional binary max_value        // 当前：遵循 ColumnOrder
  6: optional binary min_value        // 当前
  9: optional i64 nan_count           // 用于 FLOAT/DOUBLE/FLOAT16
}
```

### 2. 写入器实际工作方式（Java 源码）

来自 `parquet-hadoop/.../ParquetFileWriter.java`：

**步骤 1：写入魔术头**

```java
public void start() throws IOException {
    state = state.start();
    byte[] magic = MAGIC;  // "PAR1" = [0x50, 0x41, 0x52, 0x31]
    if (null != fileEncryptor && fileEncryptor.isFooterEncrypted()) {
        magic = EFMAGIC;   // 加密页脚时使用 "PARE"
    }
    out.write(magic);
}
```

**步骤 2：开始行组（对齐 + 元数据初始化）**

```java
public void startBlock(long recordCount) throws IOException {
    state = state.startBlock();
    alignment.alignForRowGroup(out);  // 填充到块边界（HDFS 块）
    currentBlock = new BlockMetaData();
    currentRecordCount = recordCount;
    currentColumnIndexes = new ArrayList<>();
    currentOffsetIndexes = new ArrayList<>();
}
```

**步骤 3：开始列（重置累加器）**

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

**步骤 4：写入字典页（如果使用字典编码）**

```java
public void writeDictionaryPage(DictionaryPage dictionaryPage, ...) {
    state = state.write();
    currentChunkDictionaryPageOffset = out.getPos();  // 记录偏移
    int uncompressedSize = dictionaryPage.getUncompressedSize();
    int compressedPageSize = dictionaryPage.getBytes().size();
    // 写入 PageHeader（Thrift 序列化）和 DictionaryPageHeader
    metadataConverter.writeDictionaryPageHeader(
        uncompressedSize, compressedPageSize,
        dictionaryPage.getDictionarySize(),
        dictionaryPage.getEncoding(), ...);
    // 写入实际的字典字节
    dictionaryPage.getBytes().writeAllTo(out);
    this.uncompressedLength += uncompressedSize + headerSize;
    this.compressedLength += compressedPageSize + headerSize;
}
```

**步骤 5：写入数据页**

```java
public void writeDataPage(int valueCount, int uncompressedPageSize,
                           BytesInput bytes, Statistics<?> statistics, ...) {
    state = state.write();
    long beforeHeader = out.getPos();
    if (currentChunkFirstDataPage < 0) {
        currentChunkFirstDataPage = beforeHeader;  // 第一个数据页偏移
    }
    int compressedPageSize = bytes.size();
    // 写入 PageHeader 和 DataPageHeader（包含编码、统计信息）
    metadataConverter.writeDataPageV1Header(
        uncompressedPageSize, compressedPageSize, valueCount,
        rlEncoding, dlEncoding, valuesEncoding, ...);
    // 写入实际页面数据（重复级别 + 定义级别 + 值）
    bytes.writeAllTo(out);
    this.uncompressedLength += uncompressedPageSize + headerSize;
    this.compressedLength += compressedPageSize + headerSize;
    // 更新统计信息
    currentStatistics = Statistics.merge(currentStatistics, statistics);
}
```

**步骤 6：结束列（构建 ColumnChunkMetaData）**

```java
public void endColumn() throws IOException {
    state = state.endColumn();
    // 构建页级列索引（每页的最小/最大值）
    currentColumnIndexes.add(columnIndexBuilder.build());
    currentOffsetIndexes.add(offsetIndexBuilder.build(currentChunkFirstDataPage));
    // 将列块元数据添加到当前行组
    currentBlock.addColumn(ColumnChunkMetaData.get(
        currentChunkPath, currentChunkType, currentChunkCodec,
        encodingStatsBuilder.build(), currentEncodings,
        currentStatistics, currentChunkFirstDataPage,
        currentChunkDictionaryPageOffset,
        currentChunkValueCount, compressedLength, uncompressedLength, ...));
}
```

**步骤 7：结束行组**

```java
public void endBlock() throws IOException {
    state = state.endBlock();
    currentBlock.setRowCount(currentRecordCount);
    currentBlock.setOrdinal(blocks.size());
    blocks.add(currentBlock);  // 追加到行组列表
}
```

**步骤 8：序列化页脚（关键步骤）**

```java
public void end(Map<String, String> extraMetaData) throws IOException {
    state = state.end();
    // 在数据之后写入列索引和偏移索引
    serializeColumnIndexes(columnIndexes, blocks, out, fileEncryptor);
    serializeOffsetIndexes(offsetIndexes, blocks, out, fileEncryptor);
    serializeBloomFilters(bloomFilters, blocks, out, fileEncryptor);
    // 构建页脚并序列化
    this.footer = new ParquetMetadata(
        new FileMetaData(schema, extraMetaData, Version.FULL_VERSION), blocks);
    serializeFooter(footer, out, fileEncryptor, metadataConverter);
}

private static void serializeFooter(...) throws IOException {
    long footerIndex = out.getPos();
    // 将内部元数据转换为 Thrift 格式
    FileMetaData parquetMetadata = metadataConverter.toParquetMetadata(...);
    // 写入 Thrift 序列化的 FileMetaData
    writeFileMetaData(parquetMetadata, out);
    // 将页脚长度写入为小端序 4 字节
    BytesUtils.writeIntLittleEndian(out, (out.getPos() - footerIndex));
    // 再次写入 PAR1 魔术
    out.write(MAGIC);  // "PAR1"
}
```

### 3. 字典编码：实际的编码器

来自 `parquet-column/.../DictionaryValuesWriter.java`：

```java
public abstract class DictionaryValuesWriter extends ValuesWriter {
    protected int maxDictionaryByteSize;  // 例如 parquet.dictionary.page.size
    protected boolean dictionaryTooBig;
    protected long dictionaryByteSize;
    protected IntList encodedValues;      // 字典中的整数 ID

    // 何时回退到 PLAIN 编码
    public boolean shouldFallBack() {
        return dictionaryByteSize > maxDictionaryByteSize
            || getDictionarySize() > MAX_DICTIONARY_ENTRIES;
    }

    // 检查字典是否真正节省空间
    public boolean isCompressionSatisfying(long rawSize, long encodedSize) {
        return (encodedSize + dictionaryByteSize) < rawSize;
    }

    // 序列化：使用 RLE/位打包编码整数 ID
    public BytesInput getBytes() {
        int maxDicId = getDictionarySize() - 1;
        int bitWidth = BytesUtils.getWidthFromMaxInt(maxDicId);
        RunLengthBitPackingHybridEncoder encoder =
            new RunLengthBitPackingHybridEncoder(bitWidth, ...);
        IntIterator iterator = encodedValues.iterator();
        while (iterator.hasNext()) {
            encoder.writeInt(iterator.next());
        }
        // 格式：[1 字节 bitWidth] [RLE 编码的 ID]
        byte[] bytesHeader = new byte[] {(byte) bitWidth};
        BytesInput rleEncodedBytes = encoder.toBytes();
        return concat(BytesInput.from(bytesHeader), rleEncodedBytes);
    }
}
```

**具体实现：PlainBinaryDictionaryValuesWriter**（用于字符串）：

```java
public static class PlainBinaryDictionaryValuesWriter extends DictionaryValuesWriter {
    protected Object2IntMap<Binary> binaryDictionaryContent;

    public void writeBytes(Binary v) {
        int id = binaryDictionaryContent.getInt(v);
        if (id == -1) {
            id = binaryDictionaryContent.size();
            binaryDictionaryContent.put(v.copy(), id);
            dictionaryByteSize += 4L + v.length();  // 4 字节长度前缀 + 字节
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

### 4. 物理文件布局

以上所有内容按以下确切顺序写入字节：

```
[PAR1]                                          ← 4 字节，start() 写入
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
[FileMetaData (Thrift)]                         ← writeFileMetaData(), 页脚
[footer_length (4 bytes, LE)]                   ← BytesUtils.writeIntLittleEndian()
[PAR1]                                          ← 4 字节，文件末尾
```

读取器首先定位到 `file_size - 8`，读取 4 字节的页脚长度，然后回退读取 Thrift 序列化的 `FileMetaData`。这样，无需读取任何实际数据就能获得所有行组偏移、列偏移、统计信息、编码和压缩编码器。

### 5. 这种设计为何有效

- **谓词下推**：读取器读取页脚 → 获取每个列块的 `ColumnMetaData.statistics.{min_value, max_value}` → 跳过 `max_value < filter_value` 的整个行组。
- **列裁剪**：页脚包含按 schema 排序的 `ColumnChunk` 列表。读取器从 50 列中选取 3 列 → 仅读取这 3 个列块的字节范围。
- **字典回退**：写入器在 `dictionaryContent` 映射中累积值。如果 `dictionaryByteSize > maxDictionaryByteSize`，则回退到 PLAIN。写入一个页面后，`isCompressionSatisfying()` 检查字典+索引是否比原始值节省空间。
- **单次 I/O 遍历**：数据顺序写入，元数据在末尾。写入期间无需寻道。读取器寻道一次到页脚，然后每个列块寻道一次。

### 参考文献

- [Apache Parquet Format Thrift IDL](https://github.com/apache/parquet-format/blob/master/src/main/thrift/parquet.thrift)
- [ParquetFileWriter.java](https://github.com/apache/parquet-java/blob/master/parquet-hadoop/src/main/java/org/apache/parquet/hadoop/ParquetFileWriter.java)
- [DictionaryValuesWriter.java](https://github.com/apache/parquet-java/blob/master/parquet-column/src/main/java/org/apache/parquet/column/values/dictionary/DictionaryValuesWriter.java)
- [Parquet Format Spec](https://github.com/apache/parquet-format/blob/master/README.md)
