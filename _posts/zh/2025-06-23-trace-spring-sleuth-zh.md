---
audio: false
generated: true
lang: zh
layout: post
title: 精通Spring Boot中的Spring Cloud Sleuth
translated: true
type: note
---

Spring Cloud Sleuth 是为 Spring 应用程序添加分布式追踪功能的强大工具。虽然在微服务架构中特别有用，可以跨多个服务跟踪请求，但它通过增强日志关联和调试功能，也为单体应用程序提供了显著优势。

本指南将基于 Baeldung 的方法，全面概述在单个 Spring Boot 应用程序中使用 Spring Cloud Sleuth。

## 1. 什么是 Spring Cloud Sleuth？

Spring Cloud Sleuth 的核心功能是对 Spring 应用程序进行检测，自动将追踪信息添加到日志中，并在单个应用程序内的不同组件甚至线程之间传播这些信息。它利用 OpenZipkin 的 Brave 库来实现此功能。

**关键术语：**

* **Trace（追踪）：** 表示流经应用程序的单个请求或作业。每个追踪都有一个唯一的 `traceId`。可以将其视为请求的端到端旅程。
* **Span（跨度）：** 表示追踪内的一个逻辑工作单元。一个追踪由多个跨度组成，形成树状结构。每个跨度都有一个唯一的 `spanId`。例如，一个传入的 HTTP 请求可能是一个跨度，而该请求内的方法调用可能是另一个（子）跨度。
* **MDC（映射诊断上下文）：** Sleuth 与 Slf4J 的 MDC 集成，将 `traceId` 和 `spanId` 注入到您的日志消息中，从而可以轻松筛选和关联特定请求的日志。

## 2. 为什么在单体应用中使用 Sleuth？

即使在单体应用中，请求也常常涉及多个层、异步操作和不同的线程。手动关联单个请求的日志消息可能既繁琐又容易出错。Sleuth 通过以下方式自动化此过程：

* **简化调试：** 通过将 `traceId` 和 `spanId` 添加到每个日志条目，您可以轻松筛选日志，查看与特定用户请求相关的所有内容，即使该请求在您的单个应用程序中遍历了多个方法、服务或线程。
* **提升可观测性：** 更清晰地展示请求的流动方式以及潜在瓶颈或问题可能出现的位置。
* **一致性：** 确保日志关联方法的一致性，无需在代码库的每个部分手动操作。

## 3. 入门：设置与配置

### 3.1. 项目设置 (Maven)

首先，创建一个新的 Spring Boot 项目（可以使用 Spring Initializr），并将 `spring-cloud-starter-sleuth` 依赖项添加到您的 `pom.xml` 中：

```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-sleuth</artifactId>
</dependency>
```

**重要：** 确保您使用的是兼容的 Spring Boot 和 Spring Cloud 版本。Spring Cloud 依赖项通常使用物料清单 (BOM) 进行管理。

```xml
<dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-dependencies</artifactId>
            <version>${spring-cloud.version}</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>
    </dependencies>
</dependencyManagement>
```

将 `${spring-cloud.version}` 替换为相应的发布序列版本（例如 `2021.0.1`、`2022.0.0`）。

### 3.2. 应用程序名称

强烈建议在您的 `application.properties` 或 `application.yml` 文件中设置应用程序名称。此名称将出现在您的日志中，有助于识别日志来源，尤其是在您以后迁移到分布式系统时。

```properties
# application.properties
spring.application.name=my-single-app
```

### 3.3. 日志模式

Spring Cloud Sleuth 会自动修改默认的日志模式以包含 `traceId` 和 `spanId`。使用 Sleuth 后的典型日志输出可能如下所示：

```
2025-06-23 23:30:00.123 INFO [my-single-app,a1b2c3d4e5f6a7b8,a1b2c3d4e5f6a7b8,false] 12345 --- [nio-8080-exec-1] c.e.m.MyController : This is a log message.
```

这里：

* `my-single-app`：是 `spring.application.name`。
* `a1b2c3d4e5f6a7b8`：是 `traceId`。
* `a1b2c3d4e5f6a7b8`（第二个）：是 `spanId`（对于根跨度，`traceId` 和 `spanId` 通常是相同的）。
* `false`：表示该跨度是否可导出（`true` 表示它将发送到像 Zipkin 这样的追踪收集器）。

如果您有自定义的日志模式，则需要使用 `%X{traceId}` 和 `%X{spanId}`（对于 Logback）将 `traceId` 和 `spanId` 显式添加到其中。

在 `logback-spring.xml` 中的自定义 Logback 模式示例：

```xml
<appender name="CONSOLE" class="ch.qos.logback.core.ConsoleAppender">
    <encoder>
        <pattern>%d{yyyy-MM-dd HH:mm:ss.SSS} %-5level [${spring.application.name:-},%X{traceId:-},%X{spanId:-}] %thread %logger{36} - %msg%n</pattern>
    </encoder>
</appender>
```

## 4. Sleuth 在单体应用中的工作原理

一旦 `spring-cloud-starter-sleuth` 依赖项出现在类路径上，Spring Boot 的自动配置就会接管。

### 4.1. 自动检测

Sleuth 自动检测常见的 Spring 组件和通信通道：

* **Servlet 过滤器：** 用于传入到控制器的 HTTP 请求。
* **RestTemplate：** 用于使用 `RestTemplate` 发出的传出 HTTP 调用（确保您使用的是 Bean 管理的 `RestTemplate`，以便 Sleuth 能够自动检测它）。
* **计划任务：** 用于 `@Scheduled` 方法。
* **消息通道：** 用于 Spring Integration 和 Spring Cloud Stream。
* **异步方法：** 用于 `@Async` 方法（确保追踪/跨度上下文在线程间传播）。

### 4.2. 简单 Web 请求示例

考虑一个带有 REST 控制器的简单 Spring Boot 应用程序：

```java
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class MyController {

    private static final Logger logger = LoggerFactory.getLogger(MyController.class);

    @GetMapping("/")
    public String helloSleuth() {
        logger.info("Hello from MyController");
        return "success";
    }
}
```

当您访问 `http://localhost:8080/` 时，您将看到类似以下的日志消息：

```
2025-06-23 23:35:00.123 INFO [my-single-app,c9d0e1f2a3b4c5d6,c9d0e1f2a3b4c5d6,false] 7890 --- [nio-8080-exec-1] c.e.m.MyController : Hello from MyController
```

请注意自动添加的 `traceId` 和 `spanId`。

### 4.3. 跨方法传播上下文（同一跨度）

如果您的请求在同一个应用程序内流经多个方法，并且您希望这些方法属于*同一跨度*，Sleuth 会自动处理这一点。

```java
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.stereotype.Service;

@Service
class MyService {
    private static final Logger logger = LoggerFactory.getLogger(MyService.class);

    public void doSomeWork() throws InterruptedException {
        Thread.sleep(100); // 模拟一些工作
        logger.info("Doing some work in MyService");
    }
}

@RestController
public class MyController {
    private static final Logger logger = LoggerFactory.getLogger(MyController.class);

    @Autowired
    private MyService myService;

    @GetMapping("/same-span-example")
    public String sameSpanExample() throws InterruptedException {
        logger.info("Entering same-span-example endpoint");
        myService.doSomeWork();
        logger.info("Exiting same-span-example endpoint");
        return "success";
    }
}
```

`/same-span-example` 的日志将显示控制器和服务方法具有相同的 `traceId` 和 `spanId`：

```
2025-06-23 23:40:00.100 INFO [my-single-app,e4f5g6h7i8j9k0l1,e4f5g6h7i8j9k0l1,false] 1234 --- [nio-8080-exec-2] c.e.m.MyController : Entering same-span-example endpoint
2025-06-23 23:40:00.200 INFO [my-single-app,e4f5g6h7i8j9k0l1,e4f5g6h7i8j9k0l1,false] 1234 --- [nio-8080-exec-2] c.e.m.MyService : Doing some work in MyService
2025-06-23 23:40:00.205 INFO [my-single-app,e4f5g6h7i8j9k0l1,e4f5g6h7i8j9k0l1,false] 1234 --- [nio-8080-exec-2] c.e.m.MyController : Exiting same-span-example endpoint
```

### 4.4. 手动创建新跨度

您可能希望在应用程序内为不同的工作单元创建一个新的跨度，即使它属于同一个整体追踪。这允许进行更细粒度的跟踪和计时。Spring Cloud Sleuth 为此提供了 `Tracer` API。

```java
import brave.Tracer;
import brave.Span;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@Service
class MyService {
    private static final Logger logger = LoggerFactory.getLogger(MyService.class);

    @Autowired
    private Tracer tracer; // 注入 Brave Tracer

    public void doSomeWorkNewSpan() throws InterruptedException {
        logger.info("I'm in the original span before new span");

        // 创建一个具有描述性名称的新跨度
        Span newSpan = tracer.nextSpan().name("custom-internal-work").start();
        try (Tracer.SpanInScope ws = tracer.withSpanInScope(newSpan)) {
            Thread.sleep(200); // 在新跨度中模拟一些工作
            logger.info("I'm in the new custom span doing some cool work");
        } finally {
            newSpan.finish(); // 始终完成跨度
        }

        logger.info("I'm back in the original span");
    }
}

@RestController
public class MyController {
    private static final Logger logger = LoggerFactory.getLogger(MyController.class);

    @Autowired
    private MyService myService;

    @GetMapping("/new-span-example")
    public String newSpanExample() throws InterruptedException {
        logger.info("Entering new-span-example endpoint");
        myService.doSomeWorkNewSpan();
        logger.info("Exiting new-span-example endpoint");
        return "success";
    }
}
```

`/new-span-example` 的日志将显示追踪 ID 保持不变，但会为 "custom-internal-work" 显示一个新的 `spanId`：

```
2025-06-23 23:45:00.100 INFO [my-single-app,f0e1d2c3b4a5f6e7,f0e1d2c3b4a5f6e7,false] 1234 --- [nio-8080-exec-3] c.e.m.MyController : Entering new-span-example endpoint
2025-06-23 23:45:00.105 INFO [my-single-app,f0e1d2c3b4a5f6e7,f0e1d2c3b4a5f6e7,false] 1234 --- [nio-8080-exec-3] c.e.m.MyService : I'm in the original span before new span
2025-06-23 23:45:00.300 INFO [my-single-app,f0e1d2c3b4a5f6e7,8a9b0c1d2e3f4a5b,false] 1234 --- [nio-8080-exec-3] c.e.m.MyService : I'm in the new custom span doing some cool work
2025-06-23 23:45:00.305 INFO [my-single-app,f0e1d2c3b4a5f6e7,f0e1d2c3b4a5f6e7,false] 1234 --- [nio-8080-exec-3] c.e.m.MyService : I'm back in the original span
2025-06-23 23:45:00.310 INFO [my-single-app,f0e1d2c3b4a5f6e7,f0e1d2c3b4a5f6e7,false] 1234 --- [nio-8080-exec-3] c.e.m.MyController : Exiting new-span-example endpoint
```

请注意，在 `custom-internal-work` 部分内，`spanId` 如何变为 `8a9b0c1d2e3f4a5b`，然后又恢复原样。

### 4.5. 异步处理

Sleuth 与 Spring 的 `@Async` 注解无缝集成，以跨线程边界传播追踪上下文。

首先，在您的主应用程序类中启用异步处理：

```java
@SpringBootApplication
@EnableAsync // 启用异步执行
public class MyApplication {
    public static void main(String[] args) {
        SpringApplication.run(MyApplication.class, args);
    }
}
```

然后，创建一个异步服务：

```java
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;

@Service
public class AsyncService {
    private static final Logger logger = LoggerFactory.getLogger(AsyncService.class);

    @Async
    public void performAsyncTask() throws InterruptedException {
        logger.info("Starting async task");
        Thread.sleep(500); // 模拟一些长时间运行的任务
        logger.info("Finished async task");
    }
}

@RestController
public class MyController {
    private static final Logger logger = LoggerFactory.getLogger(MyController.class);

    @Autowired
    private AsyncService asyncService;

    @GetMapping("/async-example")
    public String asyncExample() throws InterruptedException {
        logger.info("Calling async task");
        asyncService.performAsyncTask();
        logger.info("Async task initiated, returning from controller");
        return "success";
    }
}
```

日志将显示异步方法具有相同的 `traceId` 但不同的 `spanId`，因为它在一个新线程中运行并代表一个新的工作单元：

```
2025-06-23 23:50:00.100 INFO [my-single-app,1a2b3c4d5e6f7a8b,1a2b3c4d5e6f7a8b,false] 1234 --- [nio-8080-exec-4] c.e.m.MyController : Calling async task
2025-06-23 23:50:00.105 INFO [my-single-app,1a2b3c4d5e6f7a8b,9c0d1e2f3a4b5c6d,false] 1234 --- [           task-1] c.e.m.AsyncService : Starting async task
2025-06-23 23:50:00.110 INFO [my-single-app,1a2b3c4d5e6f7a8b,1a2b3c4d5e6f7a8b,false] 1234 --- [nio-8080-exec-4] c.e.m.MyController : Async task initiated, returning from controller
// ... 一段时间后 ...
2025-06-23 23:50:00.605 INFO [my-single-app,1a2b3c4d5e6f7a8b,9c0d1e2f3a4b5c6d,false] 1234 --- [           task-1] c.e.m.AsyncService : Finished async task
```

请注意，`traceId` 保持不变，但异步方法的 `spanId` 发生了变化，并且线程名称也反映了异步执行器。

### 4.6. 使用 `@SpanName` 自定义跨度名称

您可以使用 `@SpanName` 注解为自动生成的跨度提供更有意义的名称。

```java
import org.springframework.cloud.sleuth.annotation.SpanName;
import org.springframework.stereotype.Service;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@Service
public class AnnotatedService {
    private static final Logger logger = LoggerFactory.getLogger(AnnotatedService.class);

    @SpanName("Annotated_Service_Method") // 自定义跨度名称
    public void annotatedMethod() throws InterruptedException {
        logger.info("Inside annotated method");
        Thread.sleep(50);
    }
}

// ... 在您的控制器或其他服务中 ...
@Autowired
private AnnotatedService annotatedService;

@GetMapping("/annotated-span")
public String annotatedSpanExample() throws InterruptedException {
    logger.info("Calling annotated method");
    annotatedService.annotatedMethod();
    logger.info("Finished calling annotated method");
    return "success";
}
```

日志将反映自定义的跨度名称：

```
2025-06-23 23:55:00.100 INFO [my-single-app,g1h2i3j4k5l6m7n8,g1h2i3j4k5l6m7n8,false] 1234 --- [nio-8080-exec-5] c.e.m.MyController : Calling annotated method
2025-06-23 23:55:00.150 INFO [my-single-app,g1h2i3j4k5l6m7n8,g1h2i3j4k5l6m7n8,false] 1234 --- [nio-8080-exec-5] c.e.m.AnnotatedService : Inside annotated method (span name: Annotated_Service_Method)
2025-06-23 23:55:00.155 INFO [my-single-app,g1h2i3j4k5l6m7n8,g1h2i3j4k5l6m7n8,false] 1234 --- [nio-8080-exec-5] c.e.m.MyController : Finished calling annotated method
```

## 5. 与 Zipkin 集成（可选但推荐）

虽然本指南侧重于单体应用，但 Sleuth 的真正威力在于与像 Zipkin 这样的分布式追踪系统集成时才能发挥出来。Zipkin 收集 Sleuth 导出的追踪和跨度数据，并提供一个 UI 来可视化请求的流动和计时。

要与 Zipkin 集成，请添加 `spring-cloud-starter-zipkin` 依赖项：

```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-zipkin</artifactId>
</dependency>
```

默认情况下，Sleuth 会尝试将追踪发送到运行在 `http://localhost:9411` 的 Zipkin 收集器。您可以在 `application.properties` 中配置此设置：

```properties
spring.zipkin.base-url=http://localhost:9411
```

您可以使用 Docker 轻松运行 Zipkin 服务器：

```bash
docker run -d -p 9411:9411 openzipkin/zipkin
```

一旦 Zipkin 运行起来，您的单个 Spring Boot 应用程序将自动发送其追踪数据，您可以在 `http://localhost:9411/` 查看这些追踪。

## 6. 采样

默认情况下，Sleuth 应用采样策略以避免追踪系统被数据淹没。它通常对一定百分比的请求进行采样。您可以在 `application.properties` 中配置采样率：

```properties
# 对 100% 的请求进行采样
spring.sleuth.sampler.probability=1.0
```

值为 `1.0` 表示所有请求都将被追踪，而 `0.1` 表示 10% 的请求将被追踪。

## 7. 结论

Spring Cloud Sleuth，即使在单体应用中，也通过自动将 `traceId` 和 `spanId` 注入到您的日志消息中，显著增强了日志记录和调试功能。这使您可以轻松跟踪单个请求的执行流程，即使它遍历了不同的方法和线程。通过理解追踪和跨度的核心概念，并利用 Sleuth 的自动检测或手动跨度创建，您可以更好地观测您的单体应用程序。与 Zipkin 集成进一步释放了可视化和分析应用程序行为的潜力。
