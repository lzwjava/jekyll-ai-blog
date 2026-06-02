---
audio: false
generated: true
lang: zh
layout: post
title: Java并发编程
translated: true
type: note
---

### 核心要点

- `java.util.concurrent` 包帮助 Java 同时管理多个任务，使程序运行更快、响应更及时。
- 使用 `ExecutorService` 似乎是处理线程的常见方式，允许在后台运行任务。
- 研究表明，像 `ConcurrentHashMap` 这样的并发集合是线程安全的，确保多个线程可以安全访问数据。
- 与传统方法相比，证据倾向于使用 `Lock` 等同步工具来更好地控制共享资源。

### Java 并发工具包简介

`java.util.concurrent` 包是 Java 标准库的一部分，旨在简化编写同时运行多个任务的程序。这对于提高性能非常有用，尤其是在具有多核的现代计算机上。

### 使用 ExecutorService

`ExecutorService` 是管理线程的关键工具。它允许创建线程池并提交任务在后台运行。例如，可以设置线程池并运行返回结果的任务，然后等待它们完成。

### 并发集合

该包包含线程安全的集合，例如 `ConcurrentHashMap`，多个线程可以在没有冲突的情况下读取和写入。这与可能需要额外同步的常规集合不同。

### 同步工具

像 `Lock` 和 `Condition` 这样的工具比 `synchronized` 关键字提供更大的灵活性。它们有助于控制对共享资源的访问，确保一次只有一个线程可以修改数据。

---

### 调研笔记：Java 并发工具包使用全面指南

本节详细探讨 `java.util.concurrent` 包，扩展核心要点，并为希望在 Java 中实现并发编程的用户提供全面指南。内容结构模仿专业文章，确保包含初始分析的所有相关细节，并增加技术理解的深度。

#### Java 并发与 `java.util.concurrent` 包概述

Java 中的并发允许多个任务并行执行，从而提高应用程序的性能和响应能力，尤其是在多核处理器上。`java.util.concurrent` 包在 Java 5 中引入，是 Java 标准库的关键组成部分，提供了一套类和接口来简化并发编程。该包解决了线程管理、同步和数据共享的挑战，这些挑战以前需要手动处理，并且常常导致复杂且容易出错的代码。

该包包括线程池、并发数据结构和同步辅助工具，使得开发可扩展且高效的应用程序更加容易。例如，像 Web 服务器这样的现代应用程序受益于同时处理多个请求，而该包提供了有效执行此操作的工具。

#### 关键组件及其用法

##### ExecutorService：高效管理线程

`ExecutorService` 是管理线程执行的核心接口，提供了处理线程池和异步任务执行的高级 API。它抽象了线程的创建和管理，使开发人员能够专注于任务逻辑而不是线程生命周期管理。

要使用 `ExecutorService`，可以使用 `Executors` 类中的工厂方法创建线程池，例如 `newFixedThreadPool`、`newCachedThreadPool` 或 `newSingleThreadExecutor`。以下是一个演示其用法的示例：

```java
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;

public class ExecutorServiceExample {
    public static void main(String[] args) {
        // 创建一个包含 2 个线程的固定线程池
        ExecutorService executor = Executors.newFixedThreadPool(2);

        // 向执行器提交任务
        Future<String> future1 = executor.submit(() -> {
            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
            return "任务 1 完成";
        });

        Future<String> future2 = executor.submit(() -> {
            try {
                Thread.sleep(2000);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
            return "任务 2 完成";
        });

        try {
            // 等待任务完成并获取结果
            System.out.println(future1.get());
            System.out.println(future2.get());
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            // 关闭执行器
            executor.shutdown();
        }
    }
}
```

此示例展示了如何创建线程池、提交通过 `Future` 返回结果的任务，并确保正确关闭。`Future` 对象允许检查任务是否完成并检索其结果，同时适当处理异常。这对于异步编程特别有用，其中像处理事务或处理请求这样的任务可以独立运行。

##### 并发集合：线程安全的数据结构

并发集合是标准 Java 集合的线程安全实现，设计用于多线程上下文。示例包括 `ConcurrentHashMap`、`ConcurrentSkipListMap`、`ConcurrentSkipListSet`、`CopyOnWriteArrayList` 和 `CopyOnWriteArraySet`。这些集合消除了外部同步的需要，降低了死锁风险并提高了性能。

例如，`ConcurrentHashMap` 是 `HashMap` 的线程安全替代方案，允许多个线程并发读写而无需阻塞。以下是一个示例：

```java
import java.util.concurrent.ConcurrentHashMap;

public class ConcurrentHashMapExample {
    public static void main(String[] args) {
        ConcurrentHashMap<String, Integer> map = new ConcurrentHashMap<>();

        map.put("apple", 1);
        map.put("banana", 2);

        // 多个线程可以安全地读写此映射
        Thread t1 = new Thread(() -> {
            map.put("cherry", 3);
        });

        Thread t2 = new Thread(() -> {
            System.out.println(map.get("apple"));
        });

        t1.start();
        t2.start();

        try {
            t1.join();
            t2.join();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
}
```

此示例展示了 `ConcurrentHashMap` 如何被多个线程访问而无需额外同步，使其非常适合并发读写操作频繁的场景，例如在缓存系统中。

##### 同步工具：超越 `synchronized`

该包包括同步工具，如 `Lock`、`ReentrantLock`、`Condition`、`CountDownLatch`、`Semaphore` 和 `Phaser`，提供比 `synchronized` 关键字更大的灵活性。这些工具对于协调线程对共享资源的访问和管理复杂的同步场景至关重要。

例如，`ReentrantLock` 提供了更灵活的锁定机制，允许对锁定和解锁操作进行更精细的控制。以下是一个示例：

```java
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

public class LockExample {
    private final Lock lock = new ReentrantLock();

    public void doSomething() {
        lock.lock();
        try {
            // 临界区
            System.out.println("正在执行某些操作");
        } finally {
            lock.unlock();
        }
    }

    public static void main(String[] args) {
        LockExample example = new LockExample();

        Thread t1 = new Thread(() -> example.doSomething());
        Thread t2 = new Thread(() -> example.doSomething());

        t1.start();
        t2.start();
    }
}
```

此示例展示了如何使用 `Lock` 来同步对临界区的访问，确保一次只有一个线程执行它。与 `synchronized` 不同，`Lock` 允许更高级的功能，例如定时锁和可中断锁，这在需要超时处理或中断的场景中非常有用。

其他工具包括：

- **CountDownLatch**：一种同步辅助工具，允许一个或多个线程等待其他线程中的一组操作完成。例如，它可以用于确保所有工作线程在继续之前已完成。
- **Semaphore**：通过维护可用许可的数量来控制对共享资源的访问，对于限制访问资源的线程数（如数据库连接）非常有用。
- **Phaser**：一种可重用的屏障，用于协调阶段中的线程，适用于具有多个执行阶段的应用程序，例如迭代算法。

#### 其他工具和最佳实践

该包还包括原子类，如 `AtomicInteger`、`AtomicLong` 和 `AtomicReference`，它们为变量提供原子操作，确保线程安全而无需锁。例如：

```java
import java.util.concurrent.atomic.AtomicInteger;

public class AtomicIntegerExample {
    private AtomicInteger count = new AtomicInteger(0);

    public void increment() {
        count.incrementAndGet();
    }

    public int getCount() {
        return count.get();
    }

    public static void main(String[] args) throws InterruptedException {
        AtomicIntegerExample example = new AtomicIntegerExample();

        Thread t1 = new Thread(() -> {
            for (int i = 0; i < 1000; i++) {
                example.increment();
            }
        });

        Thread t2 = new Thread(() -> {
            for (int i = 0; i < 1000; i++) {
                example.increment();
            }
        });

        t1.start();
        t2.start();

        t1.join();
        t2.join();

        System.out.println("最终计数: " + example.getCount());
    }
}
```

此示例展示了 `AtomicInteger` 如何安全地从多个线程递增计数器，避免竞态条件而无需显式同步。

最佳实践包括：

- 始终使用 `shutdown()` 或 `shutdownNow()` 关闭 `ExecutorService`，以防止资源泄漏。
- 在读取密集型场景中，使用并发集合而不是同步集合以获得更好的性能。
- 使用 `Future.get()` 处理提交给 `ExecutorService` 的任务中的异常，因为它可能抛出 `ExecutionException`。

#### 比较分析：传统方法与并发方法

为了突出优势，考虑使用传统线程和 `java.util.concurrent` 包之间的区别。传统方法通常涉及手动创建 `Thread` 实例和管理同步，这可能导致样板代码和死锁等错误。相比之下，该包提供了高级抽象，降低了复杂性并提高了可维护性。

例如，手动同步 `HashMap` 需要使用 `Collections.synchronizedMap` 包装它，这仍然可能导致争用问题。然而，`ConcurrentHashMap` 使用细粒度锁定，允许并发读写，这对于习惯于传统同步方法的用户来说是一个意想不到的细节。

#### 进一步学习资源

对于希望加深理解的人，有几种资源可用：

- 官方的 [Oracle Java 并发教程](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/concurrent/package-summary.html) 提供了详细的文档和示例。
- [Baeldung 的 java.util.concurrent 概述](https://www.baeldung.com/java-util-concurrent) 提供了实用指南和代码片段。
- [Jenkov 的 Java 并发工具](https://jenkov.com/tutorials/java-util-concurrent/index.html) 包括一系列深入介绍每个组件的教程。

这些资源截至 2025 年 3 月是最新的，确保用户能够获取最新信息以在 Java 中实现并发编程。

#### 表格：`java.util.concurrent` 中关键类的比较

| 类/接口           | 用途                                       | 示例用例                     |
|-------------------|-------------------------------------------|-----------------------------|
| `ExecutorService` | 管理线程池和任务执行                        | 运行多个 HTTP 请求          |
| `ConcurrentHashMap` | 线程安全的哈希映射                         | 在 Web 应用程序中缓存数据   |
| `ReentrantLock`   | 灵活的锁定机制                             | 保护临界区                  |
| `CountDownLatch`  | 等待多个操作完成                           | 确保所有线程完成设置        |
| `Semaphore`       | 控制对共享资源的访问                       | 限制数据库连接池            |

此表格总结了主要用途，有助于为特定并发需求选择正确的工具。

总之，`java.util.concurrent` 包对于现代 Java 开发至关重要，为并发编程提供了强大的工具。通过利用这些工具，开发人员可以构建高效、可扩展的应用程序，满足当代计算环境的需求。

#### 关键引用

- [Oracle Java 并发教程摘要](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/concurrent/package-summary.html)
- [Baeldung java.util.concurrent 概述](https://www.baeldung.com/java-util-concurrent)
- [Jenkov Java 并发工具索引](https://jenkov.com/tutorials/java-util-concurrent/index.html)
