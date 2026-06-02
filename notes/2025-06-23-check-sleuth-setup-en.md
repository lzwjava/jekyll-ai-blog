---
audio: false
generated: true
lang: en
layout: post
title: Troubleshooting Empty `traceId` and `spanId` in Logs
translated: false
type: note
---

The `traceId` and `spanId` are empty in your log lines `[blog-server,,]` likely due to one of the following reasons:

* **Missing or Incorrect Sleuth Dependency:** Ensure that the `spring-cloud-starter-sleuth` dependency is correctly added to your project's `pom.xml` (for Maven) or `build.gradle` (for Gradle), and that you're using compatible Spring Boot and Spring Cloud versions. Without this dependency, Spring Cloud Sleuth's auto-configuration won't activate.

    ```xml
    <dependency>
        <groupId>org.springframework.cloud</groupId>
        <artifactId>spring-cloud-starter-sleuth</artifactId>
    </dependency>
    ```

* **Custom Logging Pattern:** If you have defined a custom logging pattern (e.g., in `logback-spring.xml` or `application.properties`), you must explicitly include placeholders for the `traceId` and `spanId`. If these placeholders are missing, the IDs will not appear in your logs even if Sleuth is active.

    For Logback, ensure your pattern includes `%X{traceId}` and `%X{spanId}`:

    ```xml
    <pattern>%d{yyyy-MM-dd HH:mm:ss.SSS} %-5level [${spring.application.name:-},%X{traceId:-},%X{spanId:-}] %thread %logger{36} - %msg%n</pattern>
    ```

* **No Active Trace/Span Context:** While Sleuth automatically instruments many Spring components (like `DispatcherServlet` for HTTP requests), it's possible these specific log messages are generated in a context where no trace or span has been initiated or propagated yet. For instance, some very early application startup logs or logs from threads not managed by Sleuth's context propagation might not have these IDs. However, for logs during active HTTP request processing like `HttpEntityMethodProcessor` and `DispatcherServlet` completing a request, this is less common if Sleuth is properly set up.

To troubleshoot, first verify your dependencies and logging configuration. If those are correct, ensure that requests are actually hitting your application and being processed by the Spring MVC `DispatcherServlet`, which should trigger Sleuth's instrumentation.
