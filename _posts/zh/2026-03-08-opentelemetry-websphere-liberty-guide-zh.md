---
audio: false
generated: true
image: false
lang: zh
layout: post
title: WebSphere Liberty 中的 OpenTelemetry 指南
translated: true
type: note
---

问题：如何在 WebSphere Liberty Profile 应用程序中使用 OpenTelemetry？

答案：

## 概述

WebSphere Liberty Profile（也称为 Open Liberty，这是其开源基础）通过 **MicroProfile Telemetry** 功能实现 OpenTelemetry。OpenTelemetry 是一组开源的、供应商独立的资源，用于收集和管理应用程序遥测数据。使用 Open Liberty 和 MicroProfile Telemetry 2.0 及更高版本，您可以以标准化方式使用 OpenTelemetry 协议管理日志、指标和跟踪。

主要有两种主要方法：使用 **MicroProfile Telemetry 功能**（推荐用于 Liberty）或直接附加 **OpenTelemetry Java Agent**。

---

## 方法 1：MicroProfile Telemetry 功能（推荐）

### 步骤 1：在 `server.xml` 中启用功能

将 `mpTelemetry-2.0` 功能添加到您的 `server.xml`：

```xml
<featureManager>
    <feature>mpTelemetry-2.0</feature>
    <!-- or use the umbrella feature -->
    <feature>microProfile-7.0</feature>
</featureManager>
```

### 步骤 2：启用 OpenTelemetry SDK

出于性能原因，MicroProfile Telemetry 默认禁用。要收集和导出遥测数据，您必须将 MicroProfile Telemetry 功能添加到 `server.xml` 文件，并指定系统属性 `otel.sdk.disabled=false`。

**对于单个应用程序（例如容器化），在 `bootstrap.properties` 中运行时级别设置：**

```properties
# bootstrap.properties
otel.sdk.disabled=false
otel.service.name=my-liberty-app
otel.exporter.otlp.endpoint=http://localhost:4317
```

**对于多个应用程序，在应用程序级别的 `microprofile-config.properties` 中设置**（位于应用程序的 `META-INF/` 文件夹中）：

```properties
# META-INF/microprofile-config.properties
otel.sdk.disabled=false
otel.service.name=my-app-service
otel.exporter.otlp.endpoint=http://collector:4317
```

运行时级别的配置优先于应用程序级别的配置。您可以为每个应用程序单独启用 OpenTelemetry 并分配服务名称，但将其他设置指定为运行时级别，以全局应用于运行时上的所有应用程序。

### 步骤 3：自动插桩（无需代码更改）

启用 Open Liberty 的 OpenTelemetry 时，Jakarta RESTful Web Services 和 JAX-RS 应用程序默认进行跟踪插桩。会自动为传入的 HTTP 请求生成 Span，包括静态文件、servlet 和 JSP。

无需任何代码插桩，以下组件会自动收集和导出：来自 HTTP 请求的跟踪、带有时间戳事件的服务器启动消息日志、JVM 指标（类、CPU 使用率、堆内存）和显示请求持续时间的 HTTP 指标。

---

## 方法 2：手动插桩（用于非 JAX-RS 代码）

要为其他操作（如数据库调用）创建 Span，您可以使用 OpenTelemetry API 在源代码中为这些操作添加手动插桩。

### 步骤 1：使第三方 API 可见

将此添加到 `server.xml`：

```xml
<webApplication id="my-app" location="my-app.war">
    <classloader apiTypeVisibility="+third-party"/>
</webApplication>
```

### 步骤 2：注入并使用 OpenTelemetry API

```java
import io.opentelemetry.api.OpenTelemetry;
import io.opentelemetry.api.trace.Span;
import io.opentelemetry.api.trace.Tracer;
import jakarta.inject.Inject;

@RequestScoped
public class MyService {

    @Inject
    private OpenTelemetry openTelemetry;

    @Inject
    private Span currentSpan;

    public void doWork() {
        Tracer tracer = openTelemetry.getTracer("my-service");
        Span span = tracer.spanBuilder("myOperation").startSpan();
        try {
            // your business logic
            span.setAttribute("custom.attr", "value");
        } finally {
            span.end();
        }
    }
}
```

> **重要提示：** 在 Open Liberty 中使用 MicroProfile Telemetry 功能时，必须通过注入获取 OpenTelemetry 和 Tracer 对象，而不是自行创建。

您还可以使用 `@WithSpan` 注解来简化 Span 创建：

```java
import io.opentelemetry.instrumentation.annotations.WithSpan;

@WithSpan
public void myTracedMethod() {
    // This method will automatically create a span
}
```

---

## 方法 3：OpenTelemetry Java Agent

对于经典 WebSphere Liberty（通过 Admin Console 的传统 WAS 与 Liberty Profile）：

打开 WebSphere Admin Console，导航至 Servers > Server type > WebSphere application servers。选择服务器，转至 Java and Process Management > Process Definition，然后选择 Java Virtual Machine。在 Generic JVM arguments 中，输入代理路径：`-javaagent:/path/to/opentelemetry-javaagent.jar`。保存配置并重启服务器。

对于 Open Liberty，添加到 `jvm.options`：

```
-javaagent:/opt/opentelemetry-javaagent.jar
-Dotel.service.name=my-app
-Dotel.exporter.otlp.endpoint=http://collector:4317
```

**代理限制需注意：**

- 配置在部署到服务器的所有应用程序之间共享。配置属性仅从系统属性和环境变量读取 — 不从 MicroProfile Config 配置源读取。由于代理在启动过程早期读取其配置，因此系统属性不会从 `bootstrap.properties` 文件读取。相反，在 `jvm.options` 中使用语法 `-Dname=value` 设置系统属性。
- 该代理与 Java 2 安全不兼容。

---

## 导出到后端（例如 Jaeger、Grafana）

您可以将 Jaeger 作为容器运行，以接收和显示分布式跟踪。使用环境变量配置 Liberty 将记录发送到 Jaeger 实例：`OTEL_TRACES_EXPORTER=jaeger` 和 `OTEL_EXPORTER_JAEGER_ENDPOINT=http://localhost:14250`。

对于 OTLP（默认，支持 Grafana、Prometheus、Jaeger 等）：

```properties
otel.exporter.otlp.endpoint=http://otel-collector:4317
otel.exporter.otlp.protocol=grpc
```

---

## 总结表格

| 特性 | MicroProfile Telemetry | Java Agent |
|---|---|---|
| 自动跟踪 JAX-RS | ✅ | ✅ |
| 自动跟踪其他库 | ❌ | ✅ |
| 每个应用的配置 | ✅ | ❌ |
| CDI 注入 API | ✅ | ❌ |
| 兼容 Java 2 安全 | ✅ | ❌ |

参考资料：

- [Open Liberty: Collect logs, metrics, and traces with OpenTelemetry](https://openliberty.io/docs/latest/microprofile-telemetry.html)
- [Open Liberty: Code instrumentation for MicroProfile Telemetry tracing](https://openliberty.io/docs/latest/telemetry-trace.html)
- [OpenTelemetry: Application server configuration (WebSphere)](https://opentelemetry.io/docs/zero-code/java/agent/server-config/)
- [Open Liberty Blog: MicroProfile Telemetry 2.0](https://openliberty.io/blog/2025/03/28/microprofile-telemetry-20.html)
- [Using OpenTelemetry in OpenLiberty (Medium)](https://medium.com/@crshnburn/using-opentelemetry-in-openliberty-7a517421795f)
