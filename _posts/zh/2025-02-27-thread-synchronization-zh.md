---
audio: false
generated: true
lang: zh
layout: post
title: Java中的线程同步
translated: true
type: note
---

让我们深入探讨Java中的线程同步！当多个线程访问共享资源（如变量、集合或文件）时，需要防止竞态条件——即线程相互干扰导致不可预测的结果。Java为此提供了几种工具：`synchronized`、`Lock`和`Semaphore`。我将分别解释它们，展示示例并进行比较，以便您根据需求选择合适的方法。

---

### 1. `synchronized`关键字

`synchronized`关键字确保一次只有一个线程可以执行代码块或方法。这是最简单的同步工具，内置于Java核心中。

#### 工作原理

- 锁定对象的监视器（每个Java对象都有一个）。
- 其他线程等待锁被释放。

#### 示例：使用`synchronized`的计数器

```java
class Counter {
    private int count = 0;

    public synchronized void increment() {
        count++;
    }

    public int getCount() {
        return count;
    }
}

public class Main {
    public static void main(String[] args) throws InterruptedException {
        Counter counter = new Counter();
        Runnable task = () -> {
            for (int i = 0; i < 1000; i++) {
                counter.increment();
            }
        };

        Thread t1 = new Thread(task);
        Thread t2 = new Thread(task);
        t1.start();
        t2.start();
        t1.join();
        t2.join();

        System.out.println("最终计数: " + counter.getCount()); // 始终为2000
    }
}
```

- 如果没有`synchronized`，`count++`（读取-修改-写入）可能会重叠，导致结果小于2000。
- `synchronized`锁定`Counter`实例，确保原子更新。

#### 同步块

您也可以锁定特定代码而不是整个方法：

```java
public void increment() {
    synchronized (this) {
        count++;
    }
}
```

- 如果需要更精细的控制，可以使用不同的对象作为锁：

```java
private final Object lock = new Object();
public void increment() {
    synchronized (lock) {
        count++;
    }
}
```

#### 优缺点

- **优点**：简单、内置，适用于基本用途。
- **缺点**：缺乏灵活性（例如无法中断等待线程），会一直阻塞直到释放。

---

### 2. `Lock`接口（java.util.concurrent.locks）

`Lock`接口（例如`ReentrantLock`）比`synchronized`提供更多控制。它是`java.util.concurrent`包的一部分，旨在解决`synchronized`的局限性。

#### 关键特性

- 显式的`lock()`和`unlock()`调用。
- 支持尝试锁、超时和可中断锁定。
- 公平性选项（线程按顺序等待）。

#### 示例：使用`ReentrantLock`的计数器

```java
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

class Counter {
    private int count = 0;
    private final Lock lock = new ReentrantLock();

    public void increment() {
        lock.lock();
        try {
            count++;
        } finally {
            lock.unlock(); // 始终在finally中解锁
        }
    }

    public int getCount() {
        return count;
    }
}

public class Main {
    public static void main(String[] args) throws InterruptedException {
        Counter counter = new Counter();
        Runnable task = () -> {
            for (int i = 0; i < 1000; i++) {
                counter.increment();
            }
        };

        Thread t1 = new Thread(task);
        Thread t2 = new Thread(task);
        t1.start();
        t2.start();
        t1.join();
        t2.join();

        System.out.println("最终计数: " + counter.getCount()); // 始终为2000
    }
}
```

- `try-finally`确保即使发生异常也能释放锁。

#### 高级特性

- **尝试锁**：非阻塞尝试获取锁：

```java
if (lock.tryLock()) {
    try {
        count++;
    } finally {
        lock.unlock();
    }
} else {
    System.out.println("无法获取锁");
}
```

- **超时**：等待有限时间：

```java
if (lock.tryLock(1, TimeUnit.SECONDS)) { ... }
```

- **可中断**：允许中断等待线程：

```java
lock.lockInterruptibly();
```

#### 优缺点

- **优点**：灵活，支持高级特性，显式控制。
- **缺点**：更冗长，需要手动解锁（可能忘记）。

---

### 3. `Semaphore`

`Semaphore`通过维护一组许可来控制对资源的访问。它非常适合限制并发性（例如最多5个线程可以访问资源）。

#### 工作原理

- 线程通过`acquire()`获取许可。
- 通过`release()`释放许可。
- 如果没有可用许可，线程等待。

#### 示例：限制数据库连接

```java
import java.util.concurrent.Semaphore;

class ConnectionPool {
    private final Semaphore semaphore = new Semaphore(3); // 最多3个连接

    public void connect() {
        try {
            semaphore.acquire();
            System.out.println(Thread.currentThread().getName() + " 已连接");
            Thread.sleep(1000); // 模拟工作
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        } finally {
            semaphore.release();
            System.out.println(Thread.currentThread().getName() + " 已断开连接");
        }
    }
}

public class Main {
    public static void main(String[] args) {
        ConnectionPool pool = new ConnectionPool();
        Runnable task = () -> pool.connect();

        Thread[] threads = new Thread[10];
        for (int i = 0; i < 10; i++) {
            threads[i] = new Thread(task, "线程-" + i);
            threads[i].start();
        }
    }
}
```

- 一次只有3个线程可以“连接”；其他线程等待直到许可被释放。

#### 高级特性

- **公平性**：`new Semaphore(3, true)`确保先进先出顺序。
- **尝试获取**：`semaphore.tryAcquire()`非阻塞检查。

#### 优缺点

- **优点**：适用于资源池，灵活的许可系统。
- **缺点**：比`synchronized`或`Lock`更复杂，不适用于简单的互斥。

---

### 与`ExecutorService`结合使用

以下是如何在线程池中使用这些工具：

```java
import java.util.concurrent.*;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

class SharedResource {
    private int value = 0;
    private final Lock lock = new ReentrantLock();

    public void increment() {
        lock.lock();
        try {
            value++;
        } finally {
            lock.unlock();
        }
    }

    public int getValue() {
        return value;
    }
}

public class Main {
    public static void main(String[] args) throws InterruptedException {
        SharedResource resource = new SharedResource();
        ExecutorService executor = Executors.newFixedThreadPool(4);

        for (int i = 0; i < 10; i++) {
            executor.submit(() -> {
                for (int j = 0; j < 100; j++) {
                    resource.increment();
                }
            });
        }

        executor.shutdown();
        executor.awaitTermination(5, TimeUnit.SECONDS);
        System.out.println("最终值: " + resource.getValue()); // 始终为1000
    }
}
```

---

### 比较

| 特性               | `synchronized`       | `Lock` (ReentrantLock) | `Semaphore`         |
|--------------------|----------------------|------------------------|---------------------|
| 易用性             | 高                   | 中等                   | 低                  |
| 灵活性             | 低                   | 高                     | 中等                |
| 粒度               | 方法/块             | 显式                   | 基于许可            |
| 可中断性           | 否                   | 是                     | 是                  |
| 公平性选项         | 否                   | 是                     | 是                  |
| 使用场景           | 简单互斥             | 高级控制               | 资源限制            |

---

### 何时使用什么？

- **`synchronized`**：快速、简单的互斥（例如保护单个变量）。
- **`Lock`**：需要尝试锁、超时或可中断性（例如复杂工作流）。
- **`Semaphore`**：限制对资源的并发访问（例如连接池、速率限制）。
