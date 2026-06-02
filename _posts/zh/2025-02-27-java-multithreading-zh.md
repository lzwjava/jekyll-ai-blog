---
audio: false
generated: true
lang: zh
layout: post
title: Java多线程编程
translated: true
type: note
---

让我们深入探讨 Java 多线程以及如何有效使用 `Executor` 框架。多线程允许程序并发运行多个任务，从而提升 I/O 密集型或 CPU 密集型操作的性能。`Executor` 框架通过抽象底层的线程创建和处理过程，简化了线程管理。我将先介绍基础知识，然后演示如何使用 `Executor` 及相关工具。

---

### 1. Java 多线程基础
Java 提供两种主要创建线程的方式：
- **继承 `Thread` 类**：

```java
class MyThread extends Thread {
    public void run() {
        System.out.println("Thread running: " + Thread.currentThread().getName());
    }
}

public class Main {
    public static void main(String[] args) {
        MyThread thread = new MyThread();
        thread.start(); // 启动线程
    }
}
```

- **实现 `Runnable` 接口**：

```java
class MyRunnable implements Runnable {
    public void run() {
        System.out.println("Runnable running: " + Thread.currentThread().getName());
    }
}

public class Main {
    public static void main(String[] args) {
        Thread thread = new Thread(new MyRunnable());
        thread.start();
    }
}
```

- 调用 `start()`（而非 `run()`）来启动线程——`run()` 仅在当前线程中执行代码。

---

### 2. 为何使用 `Executor`？
手动创建线程适用于简单场景，但管理大量任务时效率低下（例如线程开销、资源耗尽）。`Executor` 框架（Java 5 引入，位于 `java.util.concurrent` 包）提供了线程池和任务管理系统，使多线程更清晰且更具扩展性。

---

### 3. 使用 `ExecutorService`
`ExecutorService` 接口（`Executor` 的子接口）是核心工具。以下是其用法：

#### 步骤 1：创建 ExecutorService
使用 `Executors` 工具类创建线程池：
```java
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class Main {
    public static void main(String[] args) {
        // 创建包含 4 个线程的固定大小线程池
        ExecutorService executor = Executors.newFixedThreadPool(4);

        // 提交任务
        for (int i = 0; i < 10; i++) {
            executor.submit(() -> {
                System.out.println("Task executed by: " + Thread.currentThread().getName());
                try {
                    Thread.sleep(1000); // 模拟工作
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            });
        }

        // 关闭执行器
        executor.shutdown(); // 阻止新任务提交，等待现有任务完成
    }
}
```
- `newFixedThreadPool(4)` 创建包含 4 个线程的池，超额任务在队列中等待。
- `submit()` 接受 `Runnable` 或 `Callable` 任务（`Callable` 可返回结果）。

#### 常见执行器类型
- `Executors.newSingleThreadExecutor()`：单线程，按顺序处理任务。
- `Executors.newCachedThreadPool()`：按需创建线程，重用空闲线程（适用于短时任务）。
- `Executors.newScheduledThreadPool(n)`：用于延迟或周期性任务调度。

---

### 4. 使用 `Callable` 和 `Future` 处理结果
若需获取任务结果，使用 `Callable` 替代 `Runnable`：
```java
import java.util.concurrent.*;

public class Main {
    public static void main(String[] args) throws Exception {
        ExecutorService executor = Executors.newFixedThreadPool(2);

        // 提交 Callable 任务
        Future<Integer> future = executor.submit(() -> {
            Thread.sleep(1000);
            return 42;
        });

        // 任务运行时执行其他工作
        System.out.println("Task submitted...");

        // 获取结果（阻塞直至完成）
        Integer result = future.get();
        System.out.println("Result: " + result);

        executor.shutdown();
    }
}
```
- `Future.get()` 获取结果，若任务未完成则阻塞。
- 使用 `future.isDone()` 非阻塞检查任务是否完成。

---

### 5. 进阶：线程池调优
实际应用中可能需要自定义 `ThreadPoolExecutor`：
```java
import java.util.concurrent.*;

public class Main {
    public static void main(String[] args) {
        // 自定义线程池：2-4 个线程，队列容量 10
        ThreadPoolExecutor executor = new ThreadPoolExecutor(
            2, // 核心线程数
            4, // 最大线程数
            60L, // 空闲线程超时时间
            TimeUnit.SECONDS,
            new LinkedBlockingQueue<>(10) // 任务队列
        );

        for (int i = 0; i < 15; i++) {
            executor.execute(() -> {
                System.out.println("Task by: " + Thread.currentThread().getName());
                try {
                    Thread.sleep(500);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            });
        }

        executor.shutdown();
    }
}
```
- 核心线程数（2）：保持活跃的最小线程数。
- 最大线程数（4）：队列满时可创建的最大线程数。
- 队列：所有线程繁忙时容纳任务。

---

### 6. 最佳实践
- **正确关闭**：始终调用 `shutdown()` 或 `shutdownNow()` 避免资源泄漏。
- **处理中断**：在循环中检查 `Thread.currentThread().isInterrupted()`。
- **避免过载**：过多线程会降低性能——根据 CPU 核心数调整池大小（例如 `Runtime.getRuntime().availableProcessors()`）。
- **结合 `try-finally` 使用 `ExecutorService`**：
```java
ExecutorService executor = Executors.newFixedThreadPool(4);
try {
    // 提交任务
} finally {
    executor.shutdown();
}
```

---

### 结合 Log4j 的示例（整合应用）
将多线程与之前讨论的 Log4j 结合：
```java
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import java.util.concurrent.*;

public class Main {
    private static final Logger logger = LogManager.getLogger(Main.class);

    public static void main(String[] args) {
        ExecutorService executor = Executors.newFixedThreadPool(3);

        for (int i = 0; i < 5; i++) {
            final int taskId = i;
            executor.submit(() -> {
                logger.info("Task {} started by {}", taskId, Thread.currentThread().getName());
                try {
                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                    logger.error("Task {} interrupted", taskId, e);
                    Thread.currentThread().interrupt();
                }
                logger.info("Task {} completed", taskId);
            });
        }

        executor.shutdown();
    }
}
```
配合之前配置的 `log4j2.xml`，此代码会将任务进度记录到控制台和文件。
