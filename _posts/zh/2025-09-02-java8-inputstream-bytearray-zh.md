---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Java 8 输入流转字节数组
translated: true
type: note
---

发现得很准确 👍——在 **Java 8** 中确实不存在 `InputStream.readAllBytes()` 方法（该方法是 Java 9 才添加的）。
你需要手动将请求体读取到 `byte[]` 中。

以下是几种常见实现方式：

---

### 1. 使用 `ByteArrayOutputStream`（最标准的方式）

```java
public static byte[] toByteArray(InputStream input) throws IOException {
    ByteArrayOutputStream buffer = new ByteArrayOutputStream();
    byte[] data = new byte[1024];
    int nRead;
    while ((nRead = input.read(data, 0, data.length)) != -1) {
        buffer.write(data, 0, nRead);
    }
    buffer.flush();
    return buffer.toByteArray();
}
```

在包装类构造函数中的使用：

```java
public CachedBodyHttpServletRequest(HttpServletRequest request) throws IOException {
    super(request);
    this.cachedBody = toByteArray(request.getInputStream());
}
```

---

### 2. 使用 Apache Commons IO (`IOUtils`)

如果你的项目中已经引入了 **Apache Commons IO**：

```java
import org.apache.commons.io.IOUtils;

public CachedBodyHttpServletRequest(HttpServletRequest request) throws IOException {
    super(request);
    this.cachedBody = IOUtils.toByteArray(request.getInputStream());
}
```

---

### 3. 使用 Guava (`ByteStreams`)

如果使用 Guava 工具库：

```java
import com.google.common.io.ByteStreams;

public CachedBodyHttpServletRequest(HttpServletRequest request) throws IOException {
    super(request);
    this.cachedBody = ByteStreams.toByteArray(request.getInputStream());
}
```

---

### 日志输出的最终处理

```java
public String getBody() {
    return new String(this.cachedBody, StandardCharsets.UTF_8);
}
```

---

✅ 因此在 Java 8 环境中，**方案 #1（使用 ByteArrayOutputStream）** 具有最佳兼容性。
如果你不介意引入 Commons IO 或 Guava 依赖，**方案 #2 或 #3** 的代码会更加简洁。

---

需要我将完整的 `CachedBodyHttpServletRequest` 代码重构为 **兼容 Java 8 的版本**吗（自包含实现，不依赖 `readAllBytes()`）？
