---
audio: false
generated: true
lang: zh
layout: post
title: Java中的CompletableFuture
translated: true
type: note
---

在 Java Spring Boot 项目中，没有与 JavaScript 的 `Promise.all` 直接等效的功能——后者会等待多个 Promise 完成并提供它们的结果。不过，你可以通过 `java.util.concurrent` 包中的 `CompletableFuture`（特别是 `CompletableFuture.allOf` 方法）实现类似的功能：在 for 循环中并发运行多个任务，并在所有线程完成后使用它们的结果。这种方法非常适合 Spring Boot 项目，尤其是结合 Spring 的异步编程特性时。下面我将逐步解释如何实现，包括一个完整示例。

### 为什么选择 `CompletableFuture`？
`CompletableFuture`（Java 8 引入）允许你执行异步操作并管理它们的完成状态。`allOf` 方法接受多个 `CompletableFuture` 实例，并返回一个新的 `CompletableFuture`，该 future 在所有给定的 future 完成时完成，这非常适合你的场景，即希望：
- 在 for 循环中并行执行任务。
- 等待所有任务完成。
- 之后使用结果。

### 实现步骤
以下是在 Spring Boot 项目中构建解决方案的方法：

1. **定义异步任务**
   你的 for 循环的每次迭代代表一个可以独立运行的任务。这些任务将返回 `CompletableFuture` 实例，表示它们的最终结果。

2. **收集 Future**
   在循环中创建 `CompletableFuture` 对象时，将它们全部存储在一个列表中。

3. **等待所有任务完成**
   使用 `CompletableFuture.allOf` 将这些 future 合并为一个单独的 future，该 future 在所有任务完成时完成。

4. **检索并使用结果**
   所有任务完成后，从每个 `CompletableFuture` 中提取结果并按需处理。

5. **处理异常**
   考虑任务执行期间可能出现的错误。

### 示例实现
假设你有一个需要并发处理的项目列表（例如，调用服务或执行某些计算）。以下是两种方法：一种使用 Spring 的 `@Async` 注解，另一种使用 `CompletableFuture.supplyAsync`。

#### 方法 1：使用 Spring 的 `@Async`
Spring Boot 提供了 `@Async` 注解来异步运行方法。你需要在应用程序中启用异步支持。

**步骤 1：启用异步支持**
在配置类或主应用程序类上添加 `@EnableAsync` 注解：

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

**步骤 2：定义带有异步方法的服务**
创建一个服务，其中包含异步处理每个项目的方法：

```java
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;
import java.util.concurrent.CompletableFuture;

@Service
public class MyService {

    @Async
    public CompletableFuture<String> processItem(String item) {
        // 模拟一些工作（例如 I/O 或计算）
        try {
            Thread.sleep(1000); // 1 秒延迟
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            return CompletableFuture.completedFuture("Interrupted: " + item);
        }
        return CompletableFuture.completedFuture("Processed: " + item);
    }
}
```

**步骤 3：在控制器或服务中处理项目**
在你的控制器或另一个服务中，使用 for 循环提交任务并等待所有结果：

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
        // 用于保存所有 future 的列表
        List<CompletableFuture<String>> futures = new ArrayList<>();

        // 在 for 循环中提交每个任务
        for (String item : items) {
            CompletableFuture<String> future = myService.processItem(item);
            futures.add(future);
        }

        // 等待所有任务完成
        CompletableFuture<Void> allFutures = CompletableFuture.allOf(
            futures.toArray(new CompletableFuture[0])
        );

        // 阻塞直到所有任务完成
        allFutures.join();

        // 收集结果
        List<String> results = futures.stream()
            .map(CompletableFuture::join) // 获取每个结果
            .collect(Collectors.toList());

        return results;
    }
}
```

**使用示例：**
```java
List<String> items = Arrays.asList("Item1", "Item2", "Item3");
List<String> results = itemProcessor.processItems(items);
System.out.println(results); // 输出：[Processed: Item1, Processed: Item2, Processed: Item3]
```

#### 方法 2：使用 `CompletableFuture.supplyAsync`
如果你不想使用 `@Async`，可以使用 `Executor` 和 `CompletableFuture.supplyAsync` 手动管理线程。

**步骤 1：配置线程池**
定义一个 `TaskExecutor` bean 来控制线程池：

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
        executor.setCorePoolSize(5);    // 池中保留的线程数
        executor.setMaxPoolSize(10);    // 最大线程数
        executor.setQueueCapacity(25);  // 待处理任务的队列容量
        executor.initialize();
        return executor;
    }
}
```

**步骤 2：使用 `supplyAsync` 处理项目**
使用执行器异步运行任务：

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
        // 使用 supplyAsync 创建 future
        List<CompletableFuture<String>> futures = items.stream()
            .map(item -> CompletableFuture.supplyAsync(() -> processItem(item), taskExecutor))
            .collect(Collectors.toList());

        // 等待所有任务完成
        CompletableFuture.allOf(futures.toArray(new CompletableFuture[0])).join();

        // 收集结果
        List<String> results = futures.stream()
            .map(CompletableFuture::join)
            .collect(Collectors.toList());

        return results;
    }

    private String processItem(String item) {
        // 模拟一些工作
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

### 关键点
- **等待完成**：`CompletableFuture.allOf(...).join()` 或 `.get()` 确保主线程等待所有任务完成。使用 `join()` 可以避免处理受检异常；如果任务失败，它会抛出 `CompletionException`。
- **异常处理**：如果需要处理异常，可以在 try-catch 块中包装 `.join()` 或 `.get()` 调用：

```java
try {
    allFutures.get();
} catch (InterruptedException e) {
    Thread.currentThread().interrupt();
    // 处理中断
} catch (ExecutionException e) {
    // 处理任务失败
    e.printStackTrace();
}
```

- **线程池配置**：根据工作负载调整线程池大小。对于 I/O 密集型任务（例如数据库调用、API 请求），较大的池（例如 5–10 个线程）是合适的。对于 CPU 密集型任务，匹配 CPU 核心数（例如 `Runtime.getRuntime().availableProcessors()`）。
- **结果顺序**：结果保持输入列表的顺序，因为 future 是按照循环的顺序收集的。

### 选择哪种方法？
- **使用 `@Async`**：如果你的任务自然属于 Spring 服务的一部分，并且你希望 Spring 管理线程，那么这种方法更简洁，并且与 Spring Boot 集成良好。
- **使用 `supplyAsync`**：如果你需要更多控制任务执行，或者不想依赖 Spring 的异步框架。

### 最终答案
要在 Java Spring Boot 项目中复制 `Promise.all` 的功能，用于 for 循环作业，在多线程执行后使用线程结果，请使用 `CompletableFuture.allOf` 和一个 `CompletableFuture` 实例列表。推荐使用 Spring 的 `@Async` 方法以简化操作，但使用自定义执行器的 `supplyAsync` 也可以。上面使用 `@Async` 的示例演示了这一点：

- 使用 `@Async` 方法在 for 循环中创建 `CompletableFuture` 实例。
- 使用 `CompletableFuture.allOf` 等待所有任务。
- 完成后收集并使用结果。

这确保了所有任务并发运行，并且你可以在它们全部完成后处理结果，从而有效地满足你的要求。
