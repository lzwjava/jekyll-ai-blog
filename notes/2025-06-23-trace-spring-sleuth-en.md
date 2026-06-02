---
audio: false
generated: true
lang: en
layout: post
title: Mastering Spring Cloud Sleuth in Spring Boot
translated: false
type: note
---

Spring Cloud Sleuth is a powerful tool for adding distributed tracing capabilities to Spring applications. While it's particularly useful in microservice architectures to track requests across multiple services, it also provides significant benefits for single (monolith) applications by enhancing log correlation and debugging.

This guide will provide a comprehensive overview of using Spring Cloud Sleuth within a single Spring Boot application, drawing insights from Baeldung's approach.

## 1\. What is Spring Cloud Sleuth?

At its core, Spring Cloud Sleuth instruments Spring applications to automatically add tracing information to logs and propagate it across different components and even threads within a single application. It leverages OpenZipkin's Brave library for this functionality.

**Key Terminology:**

* **Trace:** Represents a single request or job that flows through the application. Each trace has a unique `traceId`. Think of it as the end-to-end journey of a request.
* **Span:** Represents a logical unit of work within a trace. A trace is composed of multiple spans, forming a tree-like structure. Each span has a unique `spanId`. For example, an incoming HTTP request might be one span, and a method call within that request could be another (child) span.
* **MDC (Mapped Diagnostic Context):** Sleuth integrates with Slf4J's MDC to inject `traceId` and `spanId` into your log messages, making it easy to filter and correlate logs for a specific request.

## 2\. Why use Sleuth in a Single Application?

Even in a monolith, requests often involve multiple layers, asynchronous operations, and different threads. Manually correlating log messages for a single request can be tedious and error-prone. Sleuth automates this by:

* **Simplifying Debugging:** By adding `traceId` and `spanId` to every log entry, you can easily filter logs to see everything related to a specific user request, even if it traverses multiple methods, services, or threads within your single application.
* **Improved Observability:** Provides a clearer picture of how a request flows and where potential bottlenecks or issues might occur.
* **Consistency:** Ensures a consistent approach to logging correlation without requiring manual effort in every part of your codebase.

## 3\. Getting Started: Setup and Configuration

### 3.1. Project Setup (Maven)

To get started, create a new Spring Boot project (you can use Spring Initializr) and add the `spring-cloud-starter-sleuth` dependency to your `pom.xml`:

```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-sleuth</artifactId>
</dependency>
```

**Important:** Ensure you are using a compatible Spring Boot and Spring Cloud version. Spring Cloud dependencies are typically managed using a Bill of Materials (BOM).

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

Replace `${spring-cloud.version}` with the appropriate release train version (e.g., `2021.0.1`, `2022.0.0`).

### 3.2. Application Name

It's highly recommended to set an application name in your `application.properties` or `application.yml` file. This name will appear in your logs, which is helpful for identifying the source of logs, especially if you later move to a distributed system.

```properties
# application.properties
spring.application.name=my-single-app
```

### 3.3. Logging Pattern

Spring Cloud Sleuth automatically modifies the default logging pattern to include `traceId` and `spanId`. A typical log output with Sleuth might look like this:

```
2025-06-23 23:30:00.123 INFO [my-single-app,a1b2c3d4e5f6a7b8,a1b2c3d4e5f6a7b8,false] 12345 --- [nio-8080-exec-1] c.e.m.MyController : This is a log message.
```

Here:

* `my-single-app`: Is the `spring.application.name`.
* `a1b2c3d4e5f6a7b8`: Is the `traceId`.
* `a1b2c3d4e5f6a7b8` (second one): Is the `spanId` (for the root span, traceId and spanId are often the same).
* `false`: Indicates if the span is exportable (true means it will be sent to a tracing collector like Zipkin).

If you have a custom logging pattern, you'll need to explicitly add the `traceId` and `spanId` to it using `%X{traceId}` and `%X{spanId}` (for Logback).

Example custom Logback pattern in `logback-spring.xml`:

```xml
<appender name="CONSOLE" class="ch.qos.logback.core.ConsoleAppender">
    <encoder>
        <pattern>%d{yyyy-MM-dd HH:mm:ss.SSS} %-5level [${spring.application.name:-},%X{traceId:-},%X{spanId:-}] %thread %logger{36} - %msg%n</pattern>
    </encoder>
</appender>
```

## 4\. How Sleuth Works in a Single Application

Once the `spring-cloud-starter-sleuth` dependency is on the classpath, Spring Boot's auto-configuration takes over.

### 4.1. Automatic Instrumentation

Sleuth automatically instruments common Spring components and communication channels:

* **Servlet Filter:** For incoming HTTP requests to your controllers.
* **RestTemplate:** For outgoing HTTP calls made using `RestTemplate` (ensure you're using a bean-managed `RestTemplate` for Sleuth to auto-instrument it).
* **Scheduled Actions:** For `@Scheduled` methods.
* **Message Channels:** For Spring Integration and Spring Cloud Stream.
* **Asynchronous Methods:** For `@Async` methods (ensures trace/span context is propagated across threads).

### 4.2. Simple Web Request Example

Consider a simple Spring Boot application with a REST controller:

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

When you access `http://localhost:8080/`, you'll see log messages like:

```
2025-06-23 23:35:00.123 INFO [my-single-app,c9d0e1f2a3b4c5d6,c9d0e1f2a3b4c5d6,false] 7890 --- [nio-8080-exec-1] c.e.m.MyController : Hello from MyController
```

Notice the `traceId` and `spanId` automatically added.

### 4.3. Propagating Context Across Methods (Same Span)

If your request flows through multiple methods within the same application and you want these methods to be part of the *same span*, Sleuth handles this automatically.

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
        Thread.sleep(100); // Simulate some work
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

Logs for `/same-span-example` will show the same `traceId` and `spanId` for both the controller and service methods:

```
2025-06-23 23:40:00.100 INFO [my-single-app,e4f5g6h7i8j9k0l1,e4f5g6h7i8j9k0l1,false] 1234 --- [nio-8080-exec-2] c.e.m.MyController : Entering same-span-example endpoint
2025-06-23 23:40:00.200 INFO [my-single-app,e4f5g6h7i8j9k0l1,e4f5g6h7i8j9k0l1,false] 1234 --- [nio-8080-exec-2] c.e.m.MyService : Doing some work in MyService
2025-06-23 23:40:00.205 INFO [my-single-app,e4f5g6h7i8j9k0l1,e4f5g6h7i8j9k0l1,false] 1234 --- [nio-8080-exec-2] c.e.m.MyController : Exiting same-span-example endpoint
```

### 4.4. Creating New Spans Manually

You might want to create a new span for a distinct unit of work within your application, even if it's part of the same overall trace. This allows for finer-grained tracking and timing. Spring Cloud Sleuth provides the `Tracer` API for this.

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
    private Tracer tracer; // Inject the Brave Tracer

    public void doSomeWorkNewSpan() throws InterruptedException {
        logger.info("I'm in the original span before new span");

        // Create a new span with a descriptive name
        Span newSpan = tracer.nextSpan().name("custom-internal-work").start();
        try (Tracer.SpanInScope ws = tracer.withSpanInScope(newSpan)) {
            Thread.sleep(200); // Simulate some work in the new span
            logger.info("I'm in the new custom span doing some cool work");
        } finally {
            newSpan.finish(); // Always finish the span
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

Logs for `/new-span-example` will show the trace ID staying the same, but a new `spanId` will appear for the "custom-internal-work":

```
2025-06-23 23:45:00.100 INFO [my-single-app,f0e1d2c3b4a5f6e7,f0e1d2c3b4a5f6e7,false] 1234 --- [nio-8080-exec-3] c.e.m.MyController : Entering new-span-example endpoint
2025-06-23 23:45:00.105 INFO [my-single-app,f0e1d2c3b4a5f6e7,f0e1d2c3b4a5f6e7,false] 1234 --- [nio-8080-exec-3] c.e.m.MyService : I'm in the original span before new span
2025-06-23 23:45:00.300 INFO [my-single-app,f0e1d2c3b4a5f6e7,8a9b0c1d2e3f4a5b,false] 1234 --- [nio-8080-exec-3] c.e.m.MyService : I'm in the new custom span doing some cool work
2025-06-23 23:45:00.305 INFO [my-single-app,f0e1d2c3b4a5f6e7,f0e1d2c3b4a5f6e7,false] 1234 --- [nio-8080-exec-3] c.e.m.MyService : I'm back in the original span
2025-06-23 23:45:00.310 INFO [my-single-app,f0e1d2c3b4a5f6e7,f0e1d2c3b4a5f6e7,false] 1234 --- [nio-8080-exec-3] c.e.m.MyController : Exiting new-span-example endpoint
```

Notice how the `spanId` changes to `8a9b0c1d2e3f4a5b` within the `custom-internal-work` section and then reverts.

### 4.5. Asynchronous Processing

Sleuth seamlessly integrates with Spring's `@Async` annotation to propagate the trace context across thread boundaries.

First, enable asynchronous processing in your main application class:

```java
@SpringBootApplication
@EnableAsync // Enable async execution
public class MyApplication {
    public static void main(String[] args) {
        SpringApplication.run(MyApplication.class, args);
    }
}
```

Then, create an async service:

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
        Thread.sleep(500); // Simulate some long-running task
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

The logs will show the same `traceId` but a different `spanId` for the asynchronous method, as it runs in a new thread and represents a new unit of work:

```
2025-06-23 23:50:00.100 INFO [my-single-app,1a2b3c4d5e6f7a8b,1a2b3c4d5e6f7a8b,false] 1234 --- [nio-8080-exec-4] c.e.m.MyController : Calling async task
2025-06-23 23:50:00.105 INFO [my-single-app,1a2b3c4d5e6f7a8b,9c0d1e2f3a4b5c6d,false] 1234 --- [           task-1] c.e.m.AsyncService : Starting async task
2025-06-23 23:50:00.110 INFO [my-single-app,1a2b3c4d5e6f7a8b,1a2b3c4d5e6f7a8b,false] 1234 --- [nio-8080-exec-4] c.e.m.MyController : Async task initiated, returning from controller
// ... some time later ...
2025-06-23 23:50:00.605 INFO [my-single-app,1a2b3c4d5e6f7a8b,9c0d1e2f3a4b5c6d,false] 1234 --- [           task-1] c.e.m.AsyncService : Finished async task
```

Notice the `traceId` remains the same, but the `spanId` changes for the async method, and the thread name also reflects the async executor.

### 4.6. Customizing Span Names with `@SpanName`

You can use the `@SpanName` annotation to provide more meaningful names for your automatically generated spans.

```java
import org.springframework.cloud.sleuth.annotation.SpanName;
import org.springframework.stereotype.Service;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@Service
public class AnnotatedService {
    private static final Logger logger = LoggerFactory.getLogger(AnnotatedService.class);

    @SpanName("Annotated_Service_Method") // Custom span name
    public void annotatedMethod() throws InterruptedException {
        logger.info("Inside annotated method");
        Thread.sleep(50);
    }
}

// ... in your controller or another service ...
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

The logs will reflect the custom span name:

```
2025-06-23 23:55:00.100 INFO [my-single-app,g1h2i3j4k5l6m7n8,g1h2i3j4k5l6m7n8,false] 1234 --- [nio-8080-exec-5] c.e.m.MyController : Calling annotated method
2025-06-23 23:55:00.150 INFO [my-single-app,g1h2i3j4k5l6m7n8,g1h2i3j4k5l6m7n8,false] 1234 --- [nio-8080-exec-5] c.e.m.AnnotatedService : Inside annotated method (span name: Annotated_Service_Method)
2025-06-23 23:55:00.155 INFO [my-single-app,g1h2i3j4k5l6m7n8,g1h2i3j4k5l6m7n8,false] 1234 --- [nio-8080-exec-5] c.e.m.MyController : Finished calling annotated method
```

## 5\. Integration with Zipkin (Optional but Recommended)

While this guide focuses on single applications, the real power of Sleuth comes when integrated with a distributed tracing system like Zipkin. Zipkin collects the trace and span data exported by Sleuth and provides a UI to visualize the flow and timing of requests.

To integrate with Zipkin, add the `spring-cloud-starter-zipkin` dependency:

```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-zipkin</artifactId>
</dependency>
```

By default, Sleuth will attempt to send traces to a Zipkin collector running at `http://localhost:9411`. You can configure this in `application.properties`:

```properties
spring.zipkin.base-url=http://localhost:9411
```

You can run a Zipkin server easily with Docker:

```bash
docker run -d -p 9411:9411 openzipkin/zipkin
```

Once Zipkin is running, your single Spring Boot application will automatically send its trace data, and you can view the traces at `http://localhost:9411/`.

## 6\. Sampling

By default, Sleuth applies a sampling strategy to avoid overwhelming the tracing system with data. It typically samples a percentage of requests. You can configure the sampling rate in `application.properties`:

```properties
# Samples 100% of requests
spring.sleuth.sampler.probability=1.0
```

A value of `1.0` means all requests will be traced, while `0.1` means 10% will be traced.

## 7\. Conclusion

Spring Cloud Sleuth, even in a single application, significantly enhances logging and debugging by automatically injecting `traceId` and `spanId` into your log messages. This allows you to easily follow the execution flow of a single request, even as it traverses different methods and threads. By understanding the core concepts of traces and spans and utilizing Sleuth's automatic instrumentation or manual span creation, you can gain much better observability into your monolithic applications. Integrating with Zipkin further unlocks the potential for visualization and analysis of your application's behavior.
