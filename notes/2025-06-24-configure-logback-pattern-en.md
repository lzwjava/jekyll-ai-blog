---
audio: false
generated: true
lang: en
layout: post
title: Configuring Logback for Custom Log Format
translated: false
type: note
---

To achieve the log format you provided, you'll need to configure your `logback.xml` file. The key is to use a `PatternLayout` within your appender and set the `pattern` property correctly.

Here's a breakdown of the components in your desired log format and how to map them to Logback pattern converters:

  * **`2025-06-15T01:37:52.452+08:00`**: This is the timestamp. You'll use `%d{yyyy-MM-dd'T'HH:mm:ss.SSSXXX}` for this.
      * `yyyy-MM-dd'T'HH:mm:ss.SSS`: Date and time with milliseconds.
      * `XXX`: ISO 8601 offset from UTC (e.g., `+08:00`).
  * **`DEBUG`**: This is the logging level. You'll use `%-5p` (left-aligned, 5 characters wide).
  * **`302244`**: This is the process ID. Logback doesn't directly expose the process ID in its standard converters. However, it *does* expose the **thread ID** (`%t` or `%thread`). If "302244" in your example is actually a thread ID (which is very common in application logs), then `%thread` is what you need. If it *must* be the OS process ID, you might need a custom Logback converter or a system property if your environment allows. For typical Spring Boot applications, this is usually the thread ID. I'll assume it's the thread ID for this example.
  * **`---`**: A literal string.
  * **`[nio-8090-exec-1]`**: This is the thread name. You'll use `[%thread]` or `%-40.40thread` if you want it fixed width.
  * **`o.s.w.s.m.m.a.HttpEntityMethodProcessor`**: This is the logger name (typically the fully qualified class name). You'll use `%-40.40logger{39}` to get a right-aligned, truncated logger name up to 39 characters.
  * **`:`**: A literal colon.
  * **`Writing ["{"vnstatversion":"2.9","jsonversion":"2","interfaces":[{"name":"enp4s0","alias":"","created":{"date" (truncated)..."]`**: This is the log message. You'll use `%msg%n`.

Here's a sample `logback.xml` configuration that should produce a very similar output:

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

**Explanation of the `pattern`:**

  * `%d{yyyy-MM-dd'T'HH:mm:ss.SSSXXX}`: Date and time in ISO 8601 format with milliseconds and timezone offset.
  * `%highlight(%-5p)`: This will output the logging level (e.g., DEBUG, INFO) left-aligned in 5 characters, and if you're outputting to a console, Logback will attempt to colorize it.
  * `%thread`: The name of the thread that logged the event. (If you need the process ID, it's more complex, but for Spring apps, thread ID is usually what's relevant here).
  * `---`: A literal string separator.
  * `[%thread]`: The thread name enclosed in square brackets.
  * `%-40.40logger{39}`: The name of the logger (usually the class name).
      * `%-40`: Left-aligned and padded to 40 characters.
      * `.40logger`: Truncates the logger name if it's longer than 40 characters.
      * `{39}`: This tells Logback to display at most 39 characters of the logger name, starting from the end of the package name (e.g., `o.s.w.s.m.m.a.HttpEntityMethodProcessor` might become `o.s.w.s.m.m.a.HttpEntityMethodProcessor` if it fits, or `...HttpEntityMethodProcessor` if truncated from the beginning). You can adjust this number.
  * ` :  `: A literal colon and space.
  * `%msg%n`: The actual log message followed by a new line.

**Important Notes:**

1.  **Placement:** Save this XML as `logback.xml` in your `src/main/resources` directory of your Spring Boot project.
2.  **Process ID vs. Thread ID:** As mentioned, Logback's standard pattern converters don't expose the OS process ID directly. If `302244` *must* be the process ID, you'd typically have to implement a custom `PatternLayoutConverter` or set a system property at startup that you then reference in your logback pattern. However, for most application logging, the thread ID (`%thread`) is sufficient and commonly used in this position.
3.  **Spring Boot Defaults:** Spring Boot often provides its own default Logback configuration if you don't provide one. By placing `logback.xml` in `src/main/resources`, you override the default.
4.  **Logger Levels:** Make sure the specific loggers (like `HttpEntityMethodProcessor` and `DispatcherServlet`) are set to `DEBUG` level if you want to see their DEBUG messages. If the root level is `INFO`, then by default, DEBUG messages won't be shown unless you explicitly set the level for specific loggers.

This configuration should get you very close to your desired log format.
