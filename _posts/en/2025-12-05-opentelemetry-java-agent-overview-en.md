---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: OpenTelemetry Java Agent Overview
translated: false
type: note
---

Question: How does the OpenTelemetry Java agent work?

Answer:

The OpenTelemetry Java agent is a **zero-code** instrumentation tool that automatically instruments Java applications without requiring any code changes. It is a single `-javaagent:path/to/opentelemetry-javaagent.jar` JVM argument added at startup.

### Core Mechanism: Java Instrumentation API (java.lang.instrument)

The agent leverages the **Java Instrumentation API** introduced in Java 5, specifically:

- It is attached to the JVM via the `-javaagent` flag (pre-main attachment) or dynamically later.
- The agent's `premain` (or `agentmain`) method runs before the application's `main` method.
- It receives an `Instrumentation` instance, which allows it to call `Instrumentation#addTransformer` and `retransformClasses`.

The key capability used is **bytecode manipulation** at class-loading time (or via retransformation for already-loaded classes).

### How Automatic Instrumentation Actually Happens

1. **Class Loading Interception**
   - The agent registers a `ClassFileTransformer`.
   - Every time the JVM loads a class (via `ClassLoader.defineClass`), the transformer gets a chance to modify the bytecode before the class is defined.

2. **Bytecode Enhancement with Byte Buddy**
   - OpenTelemetry uses **Byte Buddy** (a high-level bytecode manipulation library) instead of low-level ASM for most instrumentation.
   - Byte Buddy makes it easier to write readable, maintainable instrumentation modules.
   - When a class matches a predefined rule (e.g., package/name starts with `javax.servlet.` or `org.springframework.web.`), Byte Buddy injects advice (method enter/exit hooks).

3. **Instrumentation Modules**
   - The agent ships with ~100+ instrumentation modules (singletons, libraries, frameworks, JDBC, logging frameworks, etc.).
   - Each module defines:
     - Which classes/methods to instrument.
     - What advice code to inject (e.g., create a Span on method entry, end it on exit or exception).
   - Examples:
     - `HttpServlet` → creates HTTP server spans.
     - `java.sql.Statement#execute*` → creates SQL spans.
     - `ExecutorService#submit` → propagates context and creates async spans.

4. **OpenTelemetry SDK is Embedded**
   - The jar contains a full OpenTelemetry SDK (auto-configured).
   - By default it discovers exporters via system properties/environment variables:
     - `otlp.exporter.otlp.endpoint`
     - `otlp.traces.exporter=jaeger`, `logging`, etc.
   - You can completely customize behavior via system properties or environment variables (no code needed).

5. **Context Propagation**
   - The agent injects `ThreadLocal`-based context storage (ContextCurrent via InheritableThreadLocal or custom mechanisms).
   - It automatically wraps `Runnable`, `Callable`, executors, etc., to propagate context across threads.

6. **Runtime Overhead Control**
   - Samplers, attribute limits, span limits, etc., are configured via properties.
   - The agent supports span suppression, peer service mapping, etc.

### Lifecycle Summary

```
JVM Start
   ↓
-javaagent:opentelemetry-javaagent.jar
   ↓
Agent premain() runs
   ↓
Installs ClassFileTransformer (Byte Buddy)
   ↓
Application classes load → bytecode enhanced on-the-fly
   ↓
Instrumented methods create spans → sent to configured exporters
```

### Key Advantages

- No source code changes or recompilation.
- Works with any build tool (Maven, Gradle, fat jars, native images via limited support).
- Supports Java 8+ (including 21+).

### Limitations

- Cannot instrument code loaded by Bootstrap ClassLoader in very early stages (rare).
- Some frameworks using heavy classloader isolation or native code may need manual instrumentation.
- GraalVM native-image requires special build-time instrumentation (using the agent during native image build).

In short: The OpenTelemetry Java agent is a sophisticated java.lang.instrument-based agent that uses Byte Buddy to dynamically rewrite application classes at load time, inserting tracing, metrics, and context propagation logic according to dozens of built-in instrumentation libraries — all with zero code changes.

References:
- [OpenTelemetry Java Instrumentation Repository](https://github.com/open-telemetry/opentelemetry-java-instrumentation)
- [Official Documentation – Java Agent](https://opentelemetry.io/docs/instrumentation/java/automatic/)
- [Byte Buddy – The engine behind the agent](https://bytebuddy.net/)
