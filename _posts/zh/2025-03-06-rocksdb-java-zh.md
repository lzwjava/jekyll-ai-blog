---
audio: false
generated: true
lang: zh
layout: post
title: RocksDB Java API
translated: true
type: note
---

要使用 `org.rocksdb` 库（RocksDB 的 Java API——一个用于键值数据的高性能嵌入式数据库），您需要遵循以下步骤。RocksDB 针对快速存储和检索进行了优化，非常适合需要通过已知键快速访问数据的应用程序。以下是一份全面的入门指南：

---

### 1. **添加依赖项**

要在 Java 项目中使用 `org.rocksdb`，您需要包含 RocksDB JNI（Java 原生接口）依赖项。如果使用 Maven，请将以下内容添加到 `pom.xml` 文件中：

```xml
<dependency>
    <groupId>org.rocksdb</groupId>
    <artifactId>rocksdbjni</artifactId>
    <version>7.10.2</version>
</dependency>
```

对于 Gradle，请将以下内容添加到 `build.gradle` 中：

```groovy
implementation 'org.rocksdb:rocksdbjni:7.10.2'
```

**注意**：请查看 [Maven Central](https://search.maven.org/search?q=g:org.rocksdb%20AND%20a:rocksdbjni) 获取最新版本，因为 `7.10.2` 可能不是当前版本。

---

### 2. **加载原生库**

RocksDB 依赖于原生 C++ 代码，因此在使用前必须加载原生库。在代码开头添加以下行：

```java
RocksDB.loadLibrary();
```

如果未执行此操作，将导致运行时错误。

---

### 3. **打开数据库**

要开始使用 RocksDB，您需要通过指定数据库存储的文件路径来打开数据库实例。使用 `Options` 类来配置设置，例如在数据库不存在时创建数据库：

```java
import org.rocksdb.Options;
import org.rocksdb.RocksDB;

Options options = new Options().setCreateIfMissing(true);
RocksDB db = RocksDB.open(options, "/path/to/db");
```

- **`options`**：配置数据库行为（例如，`setCreateIfMissing(true)` 确保在数据库不存在时创建数据库）。
- **`/path/to/db`**：将其替换为系统上数据库文件将存储的有效目录路径。

---

### 4. **执行基本操作**

RocksDB 是一个键值存储，其核心操作是 `put`、`get` 和 `delete`。键和值以字节数组形式存储，因此您需要将数据（例如字符串）转换为字节。

- **Put**：插入或更新键值对。

  ```java
  db.put("key".getBytes(), "value".getBytes());
  ```

- **Get**：检索与键关联的值。

  ```java
  byte[] value = db.get("key".getBytes());
  if (value != null) {
      System.out.println(new String(value));  // 输出 "value"
  } else {
      System.out.println("Key not found");
  }
  ```

- **Delete**：删除键值对。

  ```java
  db.delete("key".getBytes());
  ```

---

### 5. **关闭数据库**

正确关闭数据库对于释放资源至关重要。最简单的方法是使用 try-with-resources 块，它会在操作完成后自动关闭数据库：

```java
try (RocksDB db = RocksDB.open(options, "/path/to/db")) {
    // 在此执行操作
} catch (Exception e) {
    e.printStackTrace();
}
```

---

### 6. **处理异常**

RocksDB 操作可能会抛出 `RocksDBException`，因此请始终包含异常处理，以防止资源泄漏或数据损坏：

```java
try {
    db.put("key".getBytes(), "value".getBytes());
} catch (RocksDBException e) {
    e.printStackTrace();
}
```

---

### 7. **配置选项**

您可以使用 `Options` 类微调 RocksDB 的性能。例如：

```java
Options options = new Options()
    .setCreateIfMissing(true)
    .setWriteBufferSize(64 * 1024 * 1024);  // 64MB 写入缓冲区
```

常见选项包括：

- `setWriteBufferSize`：控制用于写入的内存。
- `setMaxOpenFiles`：限制打开文件的数量。
- `setCompactionStyle`：调整磁盘上数据的压缩方式。

有关更多选项，请参阅 [RocksDB 文档](https://github.com/facebook/rocksdb/wiki)。

---

### 8. **简单示例**

以下是一个完整示例，演示了打开数据库、存储键值对并检索它的过程：

```java
import org.rocksdb.RocksDB;
import org.rocksdb.Options;

public class SimpleRocksDBExample {
    public static void main(String[] args) {
        RocksDB.loadLibrary();  // 加载原生库
        Options options = new Options().setCreateIfMissing(true);

        try (RocksDB db = RocksDB.open(options, "/tmp/rocksdb_example")) {
            // 放入键值对
            db.put("hello".getBytes(), "world".getBytes());

            // 获取值
            byte[] value = db.get("hello".getBytes());
            if (value != null) {
                System.out.println(new String(value));  // 输出 "world"
            } else {
                System.out.println("Key not found");
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

**输出**：`world`

---

### 关键注意事项

- **嵌入式特性**：RocksDB 在应用程序进程内运行，而不是作为单独的服务器。
- **字节数组**：键和值是 `byte[]`，因此您需要处理复杂对象的序列化/反序列化。
- **性能**：RocksDB 在快速存储（例如 SSD）上表现出色，并用于高性能系统，如开发它的 Facebook。
- **非关系型**：它是一个键值存储，而不是关系型数据库——不支持 SQL 或连接操作。

---

### 常见陷阱

- **忘记 `RocksDB.loadLibrary()`**：导致 `UnsatisfiedLinkError`。
- **资源管理不当**：不关闭数据库可能会导致问题，尤其是在资源受限的系统上。
- **数据类型错误**：直接传递字符串或对象，而不是转换为 `byte[]`。

---

### 进一步学习

- **高级功能**：探索事务、快照或列族以应对更复杂的用例。
- **资源**：查看 [RocksDB Java API](https://github.com/facebook/rocksdb/tree/main/java) 和 [RocksDB Wiki](https://github.com/facebook/rocksdb/wiki) 获取详细文档和示例。

本指南为您使用 `org.rocksdb` 提供了坚实的基础。如果您需要有关特定功能或用例的帮助，请随时提问！
