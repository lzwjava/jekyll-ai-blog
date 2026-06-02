---
audio: false
generated: true
image: false
lang: en
layout: post
title: OpenTelemetry in WebSphere Liberty Guide
translated: false
type: note
---

Question: How do you use OpenTelemetry in a WebSphere Liberty Profile application?

Answer:

## Overview

WebSphere Liberty Profile (also known as Open Liberty, which is its open-source foundation) implements OpenTelemetry through the **MicroProfile Telemetry** feature. OpenTelemetry is a collection of open source, vendor-independent resources for collecting and managing application telemetry data. With Open Liberty and MicroProfile Telemetry 2.0 and later, you can manage logs, metrics, and traces in a standardized way using the OpenTelemetry protocol.

There are two primary approaches: using the **MicroProfile Telemetry feature** (recommended for Liberty) or attaching the **OpenTelemetry Java Agent** directly.

---

## Approach 1: MicroProfile Telemetry Feature (Recommended)

### Step 1: Enable the Feature in `server.xml`

Add the `mpTelemetry-2.0` feature to your `server.xml`:

```xml
<featureManager>
    <feature>mpTelemetry-2.0</feature>
    <!-- or use the umbrella feature -->
    <feature>microProfile-7.0</feature>
</featureManager>
```

### Step 2: Enable OpenTelemetry SDK

MicroProfile Telemetry is disabled by default for performance reasons. To collect and export telemetry data, you must add the MicroProfile Telemetry feature to your `server.xml` file and specify the `otel.sdk.disabled=false` system property.

**For a single application (e.g., containerized), set it at runtime level in `bootstrap.properties`:**

```properties
# bootstrap.properties
otel.sdk.disabled=false
otel.service.name=my-liberty-app
otel.exporter.otlp.endpoint=http://localhost:4317
```

**For multiple applications, set it at the application level in `microprofile-config.properties`** (inside your app's `META-INF/` folder):

```properties
# META-INF/microprofile-config.properties
otel.sdk.disabled=false
otel.service.name=my-app-service
otel.exporter.otlp.endpoint=http://collector:4317
```

Any runtime-level configuration takes precedence over application-level configuration. You can enable OpenTelemetry and assign a service name individually for each application, but specify other settings at the runtime level to apply globally to all applications on the runtime.

### Step 3: Automatic Instrumentation (No Code Changes Required)

When you enable OpenTelemetry for Open Liberty, Jakarta RESTful Web Services and JAX-RS applications are instrumented for trace by default. Spans are automatically generated for incoming HTTP requests, including static files, servlets, and JSPs.

Without any code instrumentation, the following components are automatically collected and exported: traces from HTTP requests, message logs with timestamped events from server startup, JVM metrics (classes, CPU utilization, heap memory), and HTTP metrics showing request durations.

---

## Approach 2: Manual Instrumentation (For Non-JAX-RS Code)

To create spans for other operations, such as database calls, you can add manual instrumentation to the source code for those operations by using the OpenTelemetry API.

### Step 1: Make Third-Party APIs Visible

Add this to `server.xml`:

```xml
<webApplication id="my-app" location="my-app.war">
    <classloader apiTypeVisibility="+third-party"/>
</webApplication>
```

### Step 2: Inject and Use the OpenTelemetry API

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

> **Important:** When you use the MicroProfile Telemetry feature in Open Liberty, you must obtain the OpenTelemetry and Tracer objects by injecting them, not by creating your own.

You can also use `@WithSpan` annotation for simpler span creation:

```java
import io.opentelemetry.instrumentation.annotations.WithSpan;

@WithSpan
public void myTracedMethod() {
    // This method will automatically create a span
}
```

---

## Approach 3: OpenTelemetry Java Agent

For classic WebSphere Liberty (traditional WAS with Liberty Profile via the Admin Console):

Open the WebSphere Admin Console and navigate to Servers > Server type > WebSphere application servers. Select the server, go to Java and Process Management > Process Definition, then select Java Virtual Machine. In Generic JVM arguments, enter the path to the agent: `-javaagent:/path/to/opentelemetry-javaagent.jar`. Save the configuration and restart the server.

For Open Liberty, add to `jvm.options`:

```
-javaagent:/opt/opentelemetry-javaagent.jar
-Dotel.service.name=my-app
-Dotel.exporter.otlp.endpoint=http://collector:4317
```

**Agent limitations to be aware of:**

- Configuration is shared between all applications deployed to the server. Configuration properties are only read from system properties and environment variables — not from MicroProfile Config configuration sources. Because the agent reads its configuration early in the startup process, system properties are not read from the `bootstrap.properties` file. Instead, set system properties in `jvm.options` using the syntax: `-Dname=value`.
- The agent is not compatible with Java 2 security.

---

## Exporting to a Backend (e.g., Jaeger, Grafana)

You can run Jaeger as a container to receive and display distributed traces. Configure Liberty to send records to the Jaeger instance using environment variables: `OTEL_TRACES_EXPORTER=jaeger` and `OTEL_EXPORTER_JAEGER_ENDPOINT=http://localhost:14250`.

For OTLP (default, works with Grafana, Prometheus, Jaeger, etc.):

```properties
otel.exporter.otlp.endpoint=http://otel-collector:4317
otel.exporter.otlp.protocol=grpc
```

---

## Summary Table

| Feature | MicroProfile Telemetry | Java Agent |
|---|---|---|
| Auto-trace JAX-RS | ✅ | ✅ |
| Auto-trace other libs | ❌ | ✅ |
| Per-app config | ✅ | ❌ |
| CDI injection of API | ✅ | ❌ |
| Java 2 Security compatible | ✅ | ❌ |

References:

- [Open Liberty: Collect logs, metrics, and traces with OpenTelemetry](https://openliberty.io/docs/latest/microprofile-telemetry.html)
- [Open Liberty: Code instrumentation for MicroProfile Telemetry tracing](https://openliberty.io/docs/latest/telemetry-trace.html)
- [OpenTelemetry: Application server configuration (WebSphere)](https://opentelemetry.io/docs/zero-code/java/agent/server-config/)
- [Open Liberty Blog: MicroProfile Telemetry 2.0](https://openliberty.io/blog/2025/03/28/microprofile-telemetry-20.html)
- [Using OpenTelemetry in OpenLiberty (Medium)](https://medium.com/@crshnburn/using-opentelemetry-in-openliberty-7a517421795f)
