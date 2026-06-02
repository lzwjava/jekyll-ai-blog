---
audio: false
generated: true
lang: zh
layout: post
title: Java中的NIO使用
translated: true
type: note
---

下面通过实际示例讲解如何在 Java 中使用 NIO（New Input/Output）。相比传统的 java.io 包，Java NIO 提供了更高效的非阻塞 I/O 处理方式。

### 核心组件概览
1. **缓冲区（Buffers）**：数据容器（如 `ByteBuffer`）
2. **通道（Channels）**：数据读写流（如 `FileChannel`、`SocketChannel`）
3. **选择器（Selectors）**：实现非阻塞模式下的多路复用通道

### 基础示例：使用 NIO 读取文件
以下演示如何通过 `FileChannel` 与 `ByteBuffer` 读取文件：

```java
import java.nio.ByteBuffer;
import java.nio.channels.FileChannel;
import java.nio.file.Paths;
import java.nio.file.StandardOpenOption;

public class NIOFileReader {
    public static void main(String[] args) {
        try {
            // 打开文件通道
            FileChannel fileChannel = FileChannel.open(
                Paths.get("example.txt"),
                StandardOpenOption.READ
            );

            // 分配缓冲区
            ByteBuffer buffer = ByteBuffer.allocate(1024);

            // 将数据读入缓冲区
            while (fileChannel.read(buffer) > 0) {
                // 翻转缓冲区为读取模式
                buffer.flip();

                // 处理数据
                while (buffer.hasRemaining()) {
                    System.out.print((char) buffer.get());
                }

                // 清空缓冲区准备下次读取
                buffer.clear();
            }

            // 关闭通道
            fileChannel.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

### 运行原理
1. **FileChannel**：建立与文件的连接通道
2. **ByteBuffer**：作为数据临时存储区（示例分配1024字节容量）
3. **缓冲区操作**：
   - `flip()`：写入数据后切换为读取模式
   - `clear()`：重置缓冲区以接收新数据
4. **读取流程**：`read()` 方法填充缓冲区后，逐字节提取数据

---

### NIO 文件写入示例
以下演示如何向文件写入数据：

```java
import java.nio.ByteBuffer;
import java.nio.channels.FileChannel;
import java.nio.file.Paths;
import java.nio.file.StandardOpenOption;

public class NIOFileWriter {
    public static void main(String[] args) {
        try {
            // 打开文件写入通道
            FileChannel fileChannel = FileChannel.open(
                Paths.get("output.txt"),
                StandardOpenOption.CREATE,
                StandardOpenOption.WRITE
            );

            // 准备写入数据
            String data = "Hello, NIO!";
            ByteBuffer buffer = ByteBuffer.allocate(1024);

            // 将数据放入缓冲区
            buffer.put(data.getBytes());

            // 翻转缓冲区为写入模式
            buffer.flip();

            // 将缓冲区数据写入文件
            fileChannel.write(buffer);

            // 关闭通道
            fileChannel.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

---

### 选择器非阻塞示例
以下是通过 `Selector` 与 `SocketChannel` 实现网络编程的服务器示例：

```java
import java.nio.ByteBuffer;
import java.nio.channels.SelectionKey;
import java.nio.channels.Selector;
import java.nio.channels.ServerSocketChannel;
import java.nio.channels.SocketChannel;
import java.net.InetSocketAddress;
import java.util.Iterator;

public class NIOServer {
    public static void main(String[] args) throws Exception {
        // 创建选择器
        Selector selector = Selector.open();

        // 创建服务器套接字通道
        ServerSocketChannel serverChannel = ServerSocketChannel.open();
        serverChannel.bind(new InetSocketAddress(8080));
        serverChannel.configureBlocking(false);

        // 向选择器注册通道
        serverChannel.register(selector, SelectionKey.OP_ACCEPT);

        System.out.println("服务器已在 8080 端口启动");

        while (true) {
            selector.select(); // 阻塞直到事件发生
            Iterator<SelectionKey> keys = selector.selectedKeys().iterator();

            while (keys.hasNext()) {
                SelectionKey key = keys.next();
                keys.remove();
