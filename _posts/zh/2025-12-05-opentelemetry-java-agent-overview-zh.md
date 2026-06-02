---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: OpenTelemetry Java 代理概述
translated: true
type: note
---

问题：OpenTelemetry Java agent 如何工作？

答案：

OpenTelemetry Java agent 是一种**零代码**的检测工具，无需任何代码更改即可自动检测 Java 应用程序。它是一个在启动时添加的单一 JVM 参数：`-javaagent:path/to/opentelemetry-javaagent.jar`。

### 核心机制：Java Instrumentation API (java.lang.instrument)

该 agent 利用了 Java 5 中引入的 **Java Instrumentation API**，具体如下：

- 它通过 `-javaagent` 标志（预主类加载挂钩）或后期动态挂钩到 JVM。
- agent 的 `premain`（或 `agentmain`）方法在应用程序的 `main` 方法之前运行。
- 它接收一个 `Instrumentation` 实例，允许它调用 `Instrumentation#addTransformer` 和 `retransformClasses`。

使用的关键能力是在类加载时（或通过对已加载类的重新转换）进行**字节码操作**。

### 自动检测实际如何发生

1. **类加载拦截**
   - agent 注册一个 `ClassFileTransformer`。
   - 每当 JVM 加载一个类（通过 `ClassLoader.defineClass`）时，transformer 都有机会在类定义之前修改字节码。

2. **使用 Byte Buddy 增强字节码**
   - OpenTelemetry 使用 **Byte Buddy** (一个高级字节码操作库) 而不是低级 ASM 来进行大部分检测。
   - Byte Buddy 使编写可读、可维护的检测模块变得更容易。
   - 当一个类匹配预定义规则时（例如，包/名称以 `javax.servlet.` 或 `org.springframework.web.` 开头），Byte Buddy 会注入 advice（方法进入/退出钩子）。

3. **检测模块**
   - agent 附带了大约 100 多个检测模块（单例、库、框架、JDBC、日志框架等）。
   - 每个模块定义：
     - 要检测的类/方法。
     - 要注入的 advice 代码（例如，在方法进入时创建 Span，在退出或异常时结束它）。
   - 示例：
     - `HttpServlet` → 创建 HTTP 服务器 Span。
     - `java.sql.Statement#execute*` → 创建 SQL Span。
     - `ExecutorService#submit` → 传播上下文并创建异步 Span。

4. **OpenTelemetry SDK 已嵌入**
   - jar 包含一个完整的 OpenTelemetry SDK (自动配置)。
   - 默认情况下，它通过系统属性/环境变量发现导出器：
     - `otlp.exporter.otlp.endpoint`
     - `otlp.traces.exporter=jaeger`, `logging`, 等。
   - 您可以通过系统属性或环境变量完全自定义行为（无需代码）。

5. **上下文传播**
   - agent 注入基于 `ThreadLocal` 的上下文存储 (通过 InheritableThreadLocal 或自定义机制的 ContextCurrent)。
   - 它自动包装 `Runnable`、`Callable`、执行器等，以在线程之间传播上下文。

6. **运行时开销控制**
   - 采样器、属性限制、Span 限制等通过属性进行配置。
   - agent 支持 Span 抑制、对等服务映射等。

### 生命周期总结

```
JVM 启动
   ↓
-javaagent:opentelemetry-javaagent.jar
   ↓
Agent premain() 运行
   ↓
安装 ClassFileTransformer (Byte Buddy)
   ↓
应用程序类加载 → 字节码即时增强
   ↓
被检测方法创建 Span → 发送到配置的导出器
```

### 主要优势

- 无需源代码更改或重新编译。
- 适用于任何构建工具（Maven、Gradle、fat jars、通过有限支持实现的原生镜像）。
- 支持 Java 8+（包括 21+）。

### 限制

- 无法在非常早期的阶段检测由 Bootstrap ClassLoader 加载的代码（罕见）。
- 一些使用重度类加载器隔离或原生代码的框架可能需要手动检测。
- GraalVM native-image 需要特殊的构建时检测（在原生镜像构建期间使用 agent）。

简而言之：OpenTelemetry Java agent 是一个基于 `java.lang.instrument` 的复杂 agent，它使用 Byte Buddy 在加载时动态重写应用程序类，根据数十个内置检测库插入跟踪、指标和上下文传播逻辑——所有这些都无需代码更改。

参考资料：

- [OpenTelemetry Java Instrumentation 仓库](https://github.com/open-telemetry/opentelemetry-java-instrumentation)
- [官方文档 – Java Agent](https://opentelemetry.io/docs/instrumentation/java/automatic/)
- [Byte Buddy – agent 背后的引擎](https://bytebuddy.net/)
