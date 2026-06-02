---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 启用 Java SSL TLS 调试
translated: true
type: note
---

### 在 Java 中启用 SSL/TLS 调试

要在 Java 中启用 SSL/TLS 相关活动（如握手、证书验证、密钥交换）的详细日志记录，您需要使用 JVM 系统属性 `-Djavax.net.debug`。这会在 Java 应用程序运行时将调试信息输出到控制台（stdout/stderr）。

#### 分步说明

1. **选择调试级别**：
   - 使用 `ssl` 获取基本的 SSL/TLS 握手详情。
   - 使用 `ssl:handshake` 获取详细的握手消息（包括密码套件和证书）。
   - 使用 `all` 获取全面调试信息（包括 SSL 及其他网络协议——请谨慎使用，因为输出非常冗长）。
   - 常用建议：从 `ssl:handshake:verbose,keymanager:trustmanager` 开始以获取针对性 SSL 信息。

2. **运行 Java 应用程序时设置属性**：
   - **命令行执行**（例如通过 `java` 命令）：
     ```
     java -Djavax.net.debug=ssl:handshake -jar your-app.jar
     ```
     将 `your-app.jar` 替换为您的实际应用程序或类（例如 `com.example.Main`）。

   - **在 IDE 中（如 IntelliJ IDEA、Eclipse）**：
     - 转到运行/调试配置。
     - 在 **VM 选项** 字段中添加 `-Djavax.net.debug=ssl:handshake`。
     - 运行或调试配置。

   - **在构建工具中（如 Maven 或 Gradle）**：
     - **Maven**（在 `pom.xml` 的 `<build><plugins><plugin>` 下配置 surefire）：
       ```xml
       <configuration>
         <argLine>-Djavax.net.debug=ssl:handshake</argLine>
       </configuration>
       ```
     - **Gradle**（在 `build.gradle` 中）：
       ```groovy
       test {
         jvmArgs '-Djavax.net.debug=ssl:handshake'
       }
       ```

3. **捕获日志**：
   - 输出将显示在控制台/终端中。
   - 可重定向到文件以便查看：
     ```
     java -Djavax.net.debug=ssl:handshake -jar your-app.jar > ssl-debug.log 2>&1
     ```
   - 查找以 `***` 开头的行（例如握手开始的 `*** ClientHello`）或 `javax.net.ssl` 前缀。

4. **禁用调试**：
   - 完成后直接移除 `-D` 标志——默认未设置以避免性能开销。

#### 示例输出片段
启用后，您将看到类似以下内容：
```
*** ServerHello, TLSv1.2
RandomCookie:  GMT: 1731000000 bytes = { ... }
Cipher Suite: TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256
Compression Method: 0
***
```

#### 提示
- 适用于 Java 8+（包括 11、17、21）。在新版本中，您还可以启用 `-Djdk.tls.client.protocols=TLSv1.2,TLSv1.3` 来获取特定协议的日志。
- 高详细度会降低应用速度并淹没日志——请在开发环境中测试。
- 如果使用 Spring Boot 等框架，可将其添加到 `application.properties`：`debug=true`（通用调试）或通过命令行参数。

更多详细信息，请参阅官方 Oracle 文档：[Java Secure Socket Extension (JSSE) Reference Guide](https://docs.oracle.com/en/java/javase/17/docs/specs/security/standard-names.html#jsse-cipher-suite-names)。
