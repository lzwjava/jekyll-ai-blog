---
audio: false
generated: true
lang: zh
layout: post
title: Spring Boot多线程
translated: true
type: note
---

在 Spring Boot 项目中，“执行器”和“线程”的概念通常涉及应用程序如何处理并发任务和管理工作负载，特别是在涉及异步处理、任务调度或处理多个请求的场景中。让我们逐步解析：

---

### **Spring Boot 中的执行器与线程是什么？**

1. **线程**：
   - 线程是 Java 程序中最小的执行单元。在 Spring Boot 应用中，线程用于处理诸如处理 HTTP 请求、执行后台作业或执行 I/O 操作等任务。
   - Spring Boot 默认在嵌入式 Web 服务器（如 Tomcat、Jetty 或 Undertow）中运行，该服务器使用线程池来管理传入的请求。每个请求通常从该线程池中分配一个线程来处理。

2. **执行器**：
   - Java（以及 Spring Boot）中的 `Executor` 是对线程管理的抽象。它是 `java.util.concurrent` 包的一部分，提供了一种异步管理和执行任务的方式，而无需手动创建和管理线程。
   - 在 Spring Boot 中，执行器通常用于将任务从主应用线程（例如处理 HTTP 请求的线程）卸载到单独的线程池。这对于长时间运行的任务、并行处理或计划任务非常有用。

3. **Spring 特定上下文**：
   - Spring Boot 提供了诸如 `ThreadPoolTaskExecutor`（用于通用任务执行）和 `ThreadPoolTaskScheduler`（用于计划任务）等实用工具，以简化与执行器和线程的协作。
   - 这些工具构建在 Java 的 `ExecutorService` 之上，通常用于：
     - 异步方法执行（通过 `@Async`）。
     - 任务调度（通过 `@Scheduled`）。
     - 在高并发场景中管理工作负载。

---

### **它们在 Spring Boot 中如何工作？**

#### **1. Spring Boot 中的默认线程管理**
- 当您启动 Spring Boot Web 应用程序时，嵌入式服务器（例如 Tomcat）会初始化一个线程池来处理传入的 HTTP 请求。
- 例如，Tomcat 的默认配置可能分配 200 个线程（可通过 `application.properties` 中的 `server.tomcat.threads.max` 进行配置）。
- 每个传入的请求都会从此线程池中分配一个线程。如果所有线程都处于忙碌状态且有新请求到达，则请求可能会排队（取决于服务器的配置）或被拒绝。

#### **2. Spring Boot 中的执行器**
- Spring Boot 提供了 `TaskExecutor` 接口（Java `Executor` 的扩展）来管理特定任务的自定义线程池。
- 常见的实现是 `ThreadPoolTaskExecutor`，它允许您配置：
  - **核心池大小**：始终保持活动状态的线程数。
  - **最大池大小**：池中允许的最大线程数。
  - **队列容量**：在生成新线程（最多达到最大池大小）之前可以在队列中等待的任务数。
  - **线程命名**：便于调试（例如 "my-executor-thread-1"）。

  Spring Boot 应用中的配置示例：
  ```java
  import org.springframework.context.annotation.Bean;
  import org.springframework.context.annotation.Configuration;
  import org.springframework.scheduling.concurrent.ThreadPoolTaskExecutor;

  @Configuration
  public class ExecutorConfig {

      @Bean
      public ThreadPoolTaskExecutor taskExecutor() {
          ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
          executor.setCorePoolSize(5);      // 最小 5 个线程
          executor.setMaxPoolSize(10);      // 最大 10 个线程
          executor.setQueueCapacity(100);   // 队列最多容纳 100 个任务
          executor.setThreadNamePrefix("MyExecutor-");
          executor.initialize();
          return executor;
      }
  }
  ```

#### **3. 与执行器一起使用 `@Async`**
- Spring Boot 支持使用 `@Async` 注解进行异步方法执行。当您使用 `@Async` 注解一个方法时，它会在由执行器管理的单独线程上运行。
- 默认情况下，Spring 使用 `SimpleAsyncTaskExecutor`，它为每个任务创建一个新线程（不适用于高负载）。为了优化这一点，您可以提供自己的 `ThreadPoolTaskExecutor`（如上所示）并引用它：
  ```java
  @Service
  public class MyService {

      @Async("taskExecutor") // 引用配置中的 Bean 名称
      public void doAsyncTask() {
          System.out.println("Running on thread: " + Thread.currentThread().getName());
      }
  }
  ```

#### **4. 任务调度**
- 对于计划任务（例如每 5 分钟运行一次作业），Spring Boot 使用 `ThreadPoolTaskScheduler`。它与 `ThreadPoolTaskExecutor` 类似，但专为调度而设计。
- 示例：
  ```java
  @Scheduled(fixedRate = 5000) // 每 5 秒运行一次
  public void scheduledTask() {
      System.out.println("Scheduled task on: " + Thread.currentThread().getName());
  }
  ```

#### **5. 线程与执行器如何交互**
- 当任务被提交给执行器（例如通过 `@Async` 或手动提交）时，执行器决定是否：
  - 使用池中现有的空闲线程。
  - 创建新线程（如果核心池大小已满但未达到最大池大小）。
  - 将任务排队（如果达到最大池大小且队列未满）。
  - 拒绝任务（如果队列已满且无法创建更多线程）。
- 线程执行任务，完成后返回到池中，准备执行下一个任务。

---

### **实际示例**
假设一个 Spring Boot 应用处理用户注册：
- **HTTP 请求线程**：用户提交注册表单，由 Tomcat 线程池中的一个线程处理。
- **异步任务**：通过 `@Async` 方法将发送确认邮件的工作卸载到 `ThreadPoolTaskExecutor`，因此 HTTP 线程可以立即响应而无需等待邮件发送完成。
- **计划任务**：每小时运行一次清理作业以删除未验证的账户，由 `ThreadPoolTaskScheduler` 管理。

---

### **关键点**
- **执行器** 抽象了线程管理，使得扩展和调整并发性更加容易。
- **线程** 执行实际工作，其生命周期由执行器或 Web 服务器管理。
- Spring Boot 的默认配置对于小型应用足够，但对于高负载或复杂应用，您需要配置自定义执行器以优化性能。

如果您有特定的 Spring Boot 项目，并希望分析其执行器/线程设置，请随时分享更多细节！
