---
audio: false
generated: true
lang: en
layout: post
title: CompletableFuture in Java
translated: false
type: note
---

In a Java Spring Boot project, there’s no direct equivalent to JavaScript’s `Promise.all`, which waits for multiple promises to complete and provides their results. However, you can achieve similar functionality—running multiple tasks concurrently in a for loop and using their results after all threads complete—using `CompletableFuture` from the `java.util.concurrent` package, specifically with the `CompletableFuture.allOf` method. This approach is well-suited for a Spring Boot project, especially when combined with Spring’s asynchronous programming features. Below, I’ll explain how to do this step-by-step, including a complete example.

### Why `CompletableFuture`?
`CompletableFuture` (introduced in Java 8) allows you to perform asynchronous operations and manage their completion. The `allOf` method takes multiple `CompletableFuture` instances and returns a new `CompletableFuture` that completes when all the given futures are done, making it ideal for your scenario where you want to:
- Execute tasks in parallel within a for loop.
- Wait for all tasks to finish.
- Use the results afterward.

### Steps to Implement
Here’s how you can structure your solution in a Spring Boot project:

1. **Define the Asynchronous Tasks**
   Each iteration of your for loop represents a task that can run independently. These tasks will return `CompletableFuture` instances, representing their eventual results.

2. **Collect the Futures**
   Store all `CompletableFuture` objects in a list as you create them in the loop.

3. **Wait for All Tasks to Complete**
   Use `CompletableFuture.allOf` to combine the futures into a single future that completes when all tasks are finished.

4. **Retrieve and Use the Results**
   After all tasks are complete, extract the results from each `CompletableFuture` and process them as needed.

5. **Handle Exceptions**
   Account for potential errors during task execution.

### Example Implementation
Let’s assume you have a list of items to process concurrently (e.g., calling a service or performing some computation). Here are two approaches: one using Spring’s `@Async` annotation and another using `CompletableFuture.supplyAsync`.

#### Approach 1: Using `@Async` with Spring
Spring Boot provides the `@Async` annotation to run methods asynchronously. You’ll need to enable async support in your application.

**Step 1: Enable Async Support**
Add the `@EnableAsync` annotation to a configuration class or your main application class:

```java
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableAsync;

@SpringBootApplication
@EnableAsync
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
```

**Step 2: Define a Service with an Async Method**
Create a service with a method that processes each item asynchronously:

```java
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;
import java.util.concurrent.CompletableFuture;

@Service
public class MyService {

    @Async
    public CompletableFuture<String> processItem(String item) {
        // Simulate some work (e.g., I/O or computation)
        try {
            Thread.sleep(1000); // 1-second delay
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            return CompletableFuture.completedFuture("Interrupted: " + item);
        }
        return CompletableFuture.completedFuture("Processed: " + item);
    }
}
```

**Step 3: Process Items in a Controller or Service**
In your controller or another service, use a for loop to submit tasks and wait for all results:

```java
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;
import java.util.concurrent.CompletableFuture;

@Component
public class ItemProcessor {

    @Autowired
    private MyService myService;

    public List<String> processItems(List<String> items) {
        // List to hold all futures
        List<CompletableFuture<String>> futures = new ArrayList<>();

        // Submit each task in the for loop
        for (String item : items) {
            CompletableFuture<String> future = myService.processItem(item);
            futures.add(future);
        }

        // Wait for all tasks to complete
        CompletableFuture<Void> allFutures = CompletableFuture.allOf(
            futures.toArray(new CompletableFuture[0])
        );

        // Block until all tasks are done
        allFutures.join();

        // Collect results
        List<String> results = futures.stream()
            .map(CompletableFuture::join) // Get each result
            .collect(Collectors.toList());

        return results;
    }
}
```

**Usage Example:**
```java
List<String> items = Arrays.asList("Item1", "Item2", "Item3");
List<String> results = itemProcessor.processItems(items);
System.out.println(results); // Prints: [Processed: Item1, Processed: Item2, Processed: Item3]
```

#### Approach 2: Using `CompletableFuture.supplyAsync`
If you prefer not to use `@Async`, you can manually manage threads with an `Executor` and `CompletableFuture.supplyAsync`.

**Step 1: Configure a Thread Pool**
Define a `TaskExecutor` bean to control the thread pool:

```java
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.scheduling.concurrent.ThreadPoolTaskExecutor;
import org.springframework.core.task.TaskExecutor;

@Configuration
public class AsyncConfig {

    @Bean
    public TaskExecutor taskExecutor() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        executor.setCorePoolSize(5);    // Number of threads to keep in the pool
        executor.setMaxPoolSize(10);    // Maximum number of threads
        executor.setQueueCapacity(25);  // Queue capacity for pending tasks
        executor.initialize();
        return executor;
    }
}
```

**Step 2: Process Items with `supplyAsync`**
Use the executor to run tasks asynchronously:

```java
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import java.util.List;
import java.util.concurrent.CompletableFuture;
import java.util.stream.Collectors;
import org.springframework.core.task.TaskExecutor;

@Component
public class ItemProcessor {

    @Autowired
    private TaskExecutor taskExecutor;

    public List<String> processItems(List<String> items) {
        // Create futures using supplyAsync
        List<CompletableFuture<String>> futures = items.stream()
            .map(item -> CompletableFuture.supplyAsync(() -> processItem(item), taskExecutor))
            .collect(Collectors.toList());

        // Wait for all tasks to complete
        CompletableFuture.allOf(futures.toArray(new CompletableFuture[0])).join();

        // Collect results
        List<String> results = futures.stream()
            .map(CompletableFuture::join)
            .collect(Collectors.toList());

        return results;
    }

    private String processItem(String item) {
        // Simulate some work
        try {
            Thread.sleep(1000);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            return "Interrupted: " + item;
        }
        return "Processed: " + item;
    }
}
```

### Key Points
- **Waiting for Completion**: `CompletableFuture.allOf(...).join()` or `.get()` ensures the main thread waits until all tasks finish. Use `join()` to avoid handling checked exceptions; it throws `CompletionException` if a task fails.
- **Exception Handling**: Wrap the `.join()` or `.get()` call in a try-catch block if you need to handle exceptions:

```java
try {
    allFutures.get();
} catch (InterruptedException e) {
    Thread.currentThread().interrupt();
    // Handle interruption
} catch (ExecutionException e) {
    // Handle task failures
    e.printStackTrace();
}
```

- **Thread Pool Configuration**: Adjust the thread pool size based on your workload. For I/O-bound tasks (e.g., database calls, API requests), a larger pool (e.g., 5–10 threads) is fine. For CPU-bound tasks, match the number of CPU cores (e.g., `Runtime.getRuntime().availableProcessors()`).
- **Result Order**: The results maintain the order of the input list since futures are collected in the same order as the loop.

### Which Approach to Choose?
- **Use `@Async`** if your tasks are naturally part of a Spring service and you want Spring to manage threading. It’s cleaner and integrates well with Spring Boot.
- **Use `supplyAsync`** if you need more control over task execution or don’t want to rely on Spring’s async framework.

### Final Answer
To replicate `Promise.all` in a Java Spring Boot project for a for-loop job where you want to use thread results after multithreaded execution, use `CompletableFuture.allOf` with a list of `CompletableFuture` instances. The `@Async` approach with Spring is recommended for simplicity, but `supplyAsync` with a custom executor works too. The example above with `@Async` demonstrates this:

- Create `CompletableFuture` instances in a for loop using an `@Async` method.
- Use `CompletableFuture.allOf` to wait for all tasks.
- Collect and use the results after completion.

This ensures all tasks run concurrently, and you can process their results once they’re all done, meeting your requirements effectively.
