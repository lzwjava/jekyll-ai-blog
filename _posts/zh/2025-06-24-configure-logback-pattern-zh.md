---
audio: false
generated: true
lang: zh
layout: post
title: 配置Logback自定义日志格式
translated: true
type: note
---

要实现您提供的日志格式，您需要配置 `logback.xml` 文件。关键在于在 appender 中使用 `PatternLayout` 并正确设置 `pattern` 属性。

以下是您期望的日志格式中各组成部分的解析，以及如何将它们映射到 Logback 的模式转换器：

*   **`2025-06-15T01:37:52.452+08:00`**: 这是时间戳。您需要使用 `%d{yyyy-MM-dd'T'HH:mm:ss.SSSXXX}`。
    *   `yyyy-MM-dd'T'HH:mm:ss.SSS`: 包含毫秒的日期和时间。
    *   `XXX`: ISO 8601 标准的 UTC 时区偏移（例如，`+08:00`）。
*   **`DEBUG`**: 这是日志级别。您需要使用 `%-5p`（左对齐，宽度为5个字符）。
*   **`302244`**: 这是进程 ID。Logback 在其标准转换器中并不直接暴露进程 ID。但是，它*确实*暴露**线程 ID**（`%t` 或 `%thread`）。如果示例中的 "302244" 实际上是一个线程 ID（这在应用程序日志中非常常见），那么 `%thread` 就是您需要的。如果它*必须*是操作系统进程 ID，您可能需要一个自定义的 Logback 转换器，或者如果您的环境允许，可以使用系统属性。对于典型的 Spring Boot 应用程序，这通常是线程 ID。在此示例中，我将假定它是线程 ID。
*   **`---`**: 一个文字字符串。
*   **`[nio-8090-exec-1]`**: 这是线程名称。您可以使用 `[%thread]`，或者如果您希望它是固定宽度，可以使用 `%-40.40thread`。
*   **`o.s.w.s.m.m.a.HttpEntityMethodProcessor`**: 这是记录器名称（通常是完全限定的类名）。您需要使用 `%-40.40logger{39}` 来获得一个右对齐、最多截取 39 个字符的记录器名称。
*   **`:`**: 一个文字冒号。
*   **`Writing ["{"vnstatversion":"2.9","jsonversion":"2","interfaces":[{"name":"enp4s0","alias":"","created":{"date" (truncated)..."]`**: 这是日志消息。您需要使用 `%msg%n`。

以下是一个示例 `logback.xml` 配置，它应该能产生非常相似的输出：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<configuration>

    <appender name="CONSOLE" class="ch.qos.logback.core.ConsoleAppender">
        <encoder>
            <pattern>%d{yyyy-MM-dd'T'HH:mm:ss.SSSXXX} %highlight(%-5p) %thread --- [%thread] %-40.40logger{39} : %msg%n</pattern>
        </encoder>
    </appender>

    <root level="INFO">
        <appender-ref ref="CONSOLE"/>
    </root>

    <logger name="org.springframework.web.servlet.mvc.method.annotation.HttpEntityMethodProcessor" level="DEBUG"/>
    <logger name="org.springframework.web.servlet.DispatcherServlet" level="DEBUG"/>

</configuration>
```

**`pattern` 解释:**

*   `%d{yyyy-MM-dd'T'HH:mm:ss.SSSXXX}`: 采用 ISO 8601 格式的日期和时间，包含毫秒和时区偏移。
*   `%highlight(%-5p)`: 这将输出日志级别（例如，DEBUG, INFO），左对齐，宽度为5个字符，并且如果您输出到控制台，Logback 会尝试为其着色。
*   `%thread`: 记录事件的线程名称。（如果您需要进程 ID，这会比较复杂，但对于 Spring 应用程序，线程 ID 通常是这里相关的信息）。
*   `---`: 一个文字字符串分隔符。
*   `[%thread]`: 用方括号括起来的线程名称。
*   `%-40.40logger{39}`: 记录器的名称（通常是类名）。
    *   `%-40`: 左对齐并填充到 40 个字符。
    *   `.40logger`: 如果记录器名称超过 40 个字符，则进行截断。
    *   `{39}`: 这告诉 Logback 最多显示记录器名称的 39 个字符，从包名的末尾开始显示（例如，如果 `o.s.w.s.m.m.a.HttpEntityMethodProcessor` 能容纳得下，则保持不变，或者如果从开头截断，则可能变成 `...HttpEntityMethodProcessor`）。您可以调整此数字。
*   ` :  `: 一个文字冒号和空格。
*   `%msg%n`: 实际的日志消息，后跟一个换行符。

**重要注意事项：**

1.  **放置位置：** 将此 XML 保存为 `logback.xml`，放在您的 Spring Boot 项目的 `src/main/resources` 目录下。
2.  **进程 ID 与线程 ID：** 如前所述，Logback 的标准模式转换器不直接暴露操作系统进程 ID。如果 `302244` *必须*是进程 ID，您通常需要实现一个自定义的 `PatternLayoutConverter`，或者在启动时设置一个系统属性，然后在您的 logback 模式中引用它。然而，对于大多数应用程序日志记录，线程 ID（`%thread`）已经足够，并且通常在这个位置使用。
3.  **Spring Boot 默认配置：** 如果您不提供自定义配置，Spring Boot 通常会提供其自己的默认 Logback 配置。通过将 `logback.xml` 放在 `src/main/resources` 中，您将覆盖默认配置。
4.  **记录器级别：** 如果您希望看到特定记录器（如 `HttpEntityMethodProcessor` 和 `DispatcherServlet`）的 DEBUG 消息，请确保将它们设置为 `DEBUG` 级别。如果根级别是 `INFO`，那么默认情况下，除非您为特定记录器显式设置级别，否则不会显示 DEBUG 消息。

此配置应该能让您的日志格式非常接近您期望的格式。
