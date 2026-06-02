---
audio: false
generated: true
lang: zh
layout: post
title: 日志中traceId与spanId为空的问题排查
translated: true
type: note
---

您的日志行 `[blog-server,,]` 中 `traceId` 和 `spanId` 为空，可能由以下原因之一导致：

* **缺少或错误的 Sleuth 依赖**：请确保在项目的 `pom.xml`（Maven）或 `build.gradle`（Gradle）中正确添加了 `spring-cloud-starter-sleuth` 依赖，并且使用的 Spring Boot 和 Spring Cloud 版本兼容。若缺少此依赖，Spring Cloud Sleuth 的自动配置将不会激活。

    ```xml
    <dependency>
        <groupId>org.springframework.cloud</groupId>
        <artifactId>spring-cloud-starter-sleuth</artifactId>
    </dependency>
    ```

* **自定义日志模式**：如果您定义了自定义日志模式（例如在 `logback-spring.xml` 或 `application.properties` 中），必须显式包含 `traceId` 和 `spanId` 的占位符。若缺少这些占位符，即使 Sleuth 处于活动状态，这些 ID 也不会出现在日志中。

    对于 Logback，请确保模式包含 `%X{traceId}` 和 `%X{spanId}`：

    ```xml
    <pattern>%d{yyyy-MM-dd HH:mm:ss.SSS} %-5level [${spring.application.name:-},%X{traceId:-},%X{spanId:-}] %thread %logger{36} - %msg%n</pattern>
    ```

* **无活跃的追踪/跨度上下文**：虽然 Sleuth 自动检测许多 Spring 组件（如用于 HTTP 请求的 `DispatcherServlet`），但这些特定日志消息可能是在尚未初始化或传播追踪或跨度的上下文中生成的。例如，某些非常早期的应用程序启动日志或来自不受 Sleuth 上下文传播管理的线程的日志可能没有这些 ID。但是，对于在活跃的 HTTP 请求处理期间（如 `HttpEntityMethodProcessor` 和 `DispatcherServlet` 完成请求时）的日志，如果 Sleuth 设置正确，这种情况较为少见。

要排查问题，请首先验证依赖项和日志配置。如果这些正确，请确保请求实际到达您的应用程序并由 Spring MVC `DispatcherServlet` 处理，这应触发 Sleuth 的检测。
