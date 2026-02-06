---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-sonnet
title: Java HTTP 调试选项
translated: true
type: note
---

在 Java 中，虽然没有与 Node.js 的 `NODE_DEBUG` 环境变量直接对应的等价物，但有几种方法可以启用 HTTP/HTTPS 连接的调试输出：

## 1. **System Properties (最常见)**

```bash
# 启用所有 SSL/TLS 调试
java -Djavax.net.debug=all MyApp

# 仅启用 SSL handshake 调试
java -Djavax.net.debug=ssl:handshake MyApp

# 启用 HTTP protocol 调试
java -Djava.net.debug=true MyApp
```

## 2. **HTTP Client Logging (Java 11+)**

对于现代的 `java.net.http.HttpClient`，你可以启用 logging：

```bash
java -Djdk.httpclient.HttpClient.log=all MyApp
```

或者通过编程方式：
```java
HttpClient client = HttpClient.newBuilder()
    .version(HttpClient.Version.HTTP_2)
    .build();
```

然后在你的 logging framework（如 java.util.logging）中配置日志。

## 3. **Apache HttpClient (如果使用该库)**

在你的 `log4j.properties` 或 `logback.xml` 中添加：
```properties
log4j.logger.org.apache.http=DEBUG
log4j.logger.org.apache.http.wire=DEBUG
```

## 4. **常见的 javax.net.debug 选项**

```bash
# 所有调试信息
-Djavax.net.debug=all

# 仅 SSL/TLS
-Djavax.net.debug=ssl

# SSL handshake 和 session
-Djavax.net.debug=ssl:handshake:session

# Key manager
-Djavax.net.debug=ssl:keymanager

# Trust manager
-Djavax.net.debug=ssl:trustmanager
```

最接近 `NODE_DEBUG=http,https` 的等价命令是：
```bash
java -Djavax.net.debug=all -Djdk.httpclient.HttpClient.log=all MyApp
```

这将为你提供有关 SSL/TLS 连接和 HTTP client 操作的详细信息，类似于 Node.js 所提供的内容。