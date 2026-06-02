---
audio: false
generated: true
lang: en
layout: post
title: Spring Boot Multithreading
translated: false
type: note
---

In a Spring Boot project, the concepts of "executors" and "threads" typically relate to how the application handles concurrent tasks and manages its workload, especially in scenarios involving asynchronous processing, task scheduling, or handling multiple requests. Let’s break this down step-by-step:

---

### **What Are Executors and Threads in Spring Boot?**

1. **Threads**:
   - A thread is the smallest unit of execution in a Java program. In a Spring Boot application, threads are used to handle tasks like processing HTTP requests, executing background jobs, or performing I/O operations.
   - Spring Boot, by default, runs within an embedded web server (e.g., Tomcat, Jetty, or Undertow), which uses a thread pool to manage incoming requests. Each request is typically assigned to a thread from this pool.

2. **Executors**:
   - An `Executor` in Java (and Spring Boot) is an abstraction over thread management. It’s part of the `java.util.concurrent` package and provides a way to manage and execute tasks asynchronously without manually creating and managing threads.
   - In Spring Boot, executors are often used to offload tasks from the main application thread (e.g., the thread handling an HTTP request) to a separate thread pool. This is useful for long-running tasks, parallel processing, or scheduled jobs.

3. **Spring-Specific Context**:
   - Spring Boot provides utilities like `ThreadPoolTaskExecutor` (for general task execution) and `ThreadPoolTaskScheduler` (for scheduled tasks) to simplify working with executors and threads.
   - These are built on top of Java’s `ExecutorService` and are commonly used for:
     - Asynchronous method execution (via `@Async`).
     - Task scheduling (via `@Scheduled`).
     - Managing workloads in high-concurrency scenarios.

---

### **How Do They Work in Spring Boot?**

#### **1. Default Thread Management in Spring Boot**

- When you start a Spring Boot web application, the embedded server (e.g., Tomcat) initializes a thread pool to handle incoming HTTP requests.
- For example, Tomcat’s default configuration might allocate 200 threads (configurable via `server.tomcat.threads.max` in `application.properties`).
- Each incoming request is assigned a thread from this pool. If all threads are busy and a new request arrives, it may queue up (depending on the server’s configuration) or be rejected.

#### **2. Executors in Spring Boot**

- Spring Boot provides the `TaskExecutor` interface (an extension of Java’s `Executor`) to manage custom thread pools for specific tasks.
- A common implementation is `ThreadPoolTaskExecutor`, which allows you to configure:
  - **Core Pool Size**: The number of threads always kept alive.
  - **Max Pool Size**: The maximum number of threads allowed in the pool.
  - **Queue Capacity**: The number of tasks that can wait in the queue before new threads are spawned (up to the max pool size).
  - **Thread Naming**: For easier debugging (e.g., "my-executor-thread-1").

  Example configuration in a Spring Boot app:

  ```java
  import org.springframework.context.annotation.Bean;
  import org.springframework.context.annotation.Configuration;
  import org.springframework.scheduling.concurrent.ThreadPoolTaskExecutor;

  @Configuration
  public class ExecutorConfig {

      @Bean
      public ThreadPoolTaskExecutor taskExecutor() {
          ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
          executor.setCorePoolSize(5);      // Minimum 5 threads
          executor.setMaxPoolSize(10);      // Maximum 10 threads
          executor.setQueueCapacity(100);   // Queue up to 100 tasks
          executor.setThreadNamePrefix("MyExecutor-");
          executor.initialize();
          return executor;
      }
  }
  ```

#### **3. Using `@Async` with Executors**

- Spring Boot supports asynchronous method execution with the `@Async` annotation. When you annotate a method with `@Async`, it runs on a separate thread managed by an executor.
- By default, Spring uses a `SimpleAsyncTaskExecutor`, which creates a new thread for each task (not ideal for high load). To optimize this, you can provide your own `ThreadPoolTaskExecutor` (as shown above) and reference it:

  ```java
  @Service
  public class MyService {

      @Async("taskExecutor") // Refers to the bean name from the config
      public void doAsyncTask() {
          System.out.println("Running on thread: " + Thread.currentThread().getName());
      }
  }
  ```

#### **4. Task Scheduling**

- For scheduled tasks (e.g., running a job every 5 minutes), Spring Boot uses `ThreadPoolTaskScheduler`. It’s similar to `ThreadPoolTaskExecutor` but tailored for scheduling.
- Example:

  ```java
  @Scheduled(fixedRate = 5000) // Runs every 5 seconds
  public void scheduledTask() {
      System.out.println("Scheduled task on: " + Thread.currentThread().getName());
  }
  ```

#### **5. How Threads and Executors Interact**

- When a task is submitted to an executor (e.g., via `@Async` or manual submission), the executor decides whether to:
  - Use an existing idle thread from the pool.
  - Create a new thread (if the core pool size is exceeded but below the max pool size).
  - Queue the task (if the max pool size is reached and the queue isn’t full).
  - Reject the task (if the queue is full and no more threads can be created).
- Threads execute the tasks and return to the pool when done, ready for the next task.

---

### **Practical Example**

Imagine a Spring Boot app handling user registrations:

- **HTTP Request Thread**: A user submits a registration form, handled by a thread from the Tomcat thread pool.
- **Async Task**: Sending a confirmation email is offloaded to a `ThreadPoolTaskExecutor` via an `@Async` method, so the HTTP thread can respond immediately without waiting for the email to send.
- **Scheduled Task**: A cleanup job runs every hour to remove unverified accounts, managed by a `ThreadPoolTaskScheduler`.

---

### **Key Points**

- **Executors** abstract thread management, making it easier to scale and tune concurrency.
- **Threads** do the actual work, and their lifecycle is managed by executors or the web server.
- Spring Boot’s defaults are sufficient for small apps, but for high-load or complex apps, you’ll configure custom executors to optimize performance.

If you have a specific Spring Boot project in mind and want help analyzing its executor/thread setup, feel free to share more details!
