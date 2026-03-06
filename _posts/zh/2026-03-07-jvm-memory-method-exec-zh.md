---
audio: false
generated: true
image: false
lang: zh
layout: post
title: JVM 内存与方法执行
translated: true
type: note
---

**问题：** JVM 内存模型是如何工作的，它如何管理对象和方法调用？

**回答：**

---

## 概述

JVM 将其内存分为几个逻辑运行时数据区域，每个区域在程序执行期间扮演特定角色。这种结构化的内存模型确保不同类型数据之间的隔离，支持多线程，并启用如自动垃圾回收等功能。

---

## JVM 内存区域

### 1. Heap

Java Heap 是动态内存分配的主要区域。程序执行期间创建的所有类实例、数组和对象都存储在这里。与限于单个线程的 stack 内存不同，heap 是 JVM 中所有线程可访问的共享内存空间。

Heap 分为两个主要区域：**Young Generation** 和 **Old Generation**。Young Generation 进一步分为 **Eden Space**（新对象首先创建的地方）和两个 **Survivor Spaces**（S0 和 S1），幸存垃圾回收的对象会被移动到这里。

### 2. Stack（每个线程）

JVM 中运行的每个线程都有自己的 thread stack。基本类型的本地变量完全存储在 thread stack 上，对其他线程不可见。即使两个线程执行相同的代码，它们也会在其各自的 thread stack 中创建本地变量的独立副本。

Stack 内存随着新方法的调用和返回而增长和收缩。当方法被调用时，会创建一个新的 stack frame；当方法返回时，对应的 stack frame 被移除。在 stack 中声明的变量仅在创建它们的 메서드运行期间存在。

### 3. Method Area / Metaspace

Method Area 是 Java heap 的一部分，由所有线程共享。它存储类级信息，如类元数据、静态变量和常量池（存储如字符串字面量和引用的常量）。

在 Java 8+ 中，Metaspace 取代了旧的 PermGen。与 PermGen 的固定大小不同，Metaspace 可以动态增长，仅受可用 native memory 的限制。这种灵活性避免了令人畏惧的 `OutOfMemoryError: PermGen space`，但如果发生类加载器泄漏或动态类生成导致的失控增长，则会引入风险。

### 4. PC（Program Counter）寄存器

每个 JVM 线程都有一个 Program Counter (PC) 寄存器。对于 non-native 方法，它存储当前正在执行的 JVM 指令地址。

### 5. Native Method Stack

Native method stack 处理与 Java 代码交互的 native 方法的执行。此内存在每个线程创建时为其分配，可以具有固定或动态大小。

---

## 方法调用工作原理（Stack Frames）

每次调用方法时，JVM 都会在 thread 的 stack 上分配一个新的 **stack frame**。此 frame 是一个自包含的内存单元，持有执行该方法所需的所有数据。Frame 在 stack 上保留，直到方法正常完成或异常退出（例如由于异常）。方法返回后，其 frame 从 stack 中移除，内存会自动回收——stack 内存无需垃圾回收。

每个 stack frame 包含：
- **Local variable array**：持有所有方法参数和方法内声明的本地变量。
- **Operand stack**：JVM 内部用于评估表达式和存储中间计算结果。
- **Return value slot**：如果有，在将结果传递回调用方法之前存储方法调用结果。
- **Reference to the runtime constant pool**：允许方法解析字段名、方法名和字面量。

**实际示例**——调用 `m1 → m2 → m3`：
当 m1 调用 m2 时，一个新 frame 被推到 m1 的 frame 之上。当 m2 调用 m3 时，另一个 frame 被推到顶部。m3 完成后，其 frame 被弹出，控制权返回 m2。然后 m2 和 m1 也同样处理。

如果 stack 超过其分配空间（例如由于无限递归），则会发生 `StackOverflowError`。

---

## 对象管理原理（Heap 和 Garbage Collection）

### 对象生命周期

新对象在 Heap 的 Young Generation（Eden Space）中分配。当 Young Generation 填满时，会发生 minor garbage collection。长期存活的对象会被移动到 Old（Tenured）Generation。

经多次 Minor GC 存活的对象最终会被提升到 Old Generation。这种“代际假设”——大多数对象很快就会死亡——驱动所有现代 JVM 的垃圾收集器设计。

### Garbage Collection —— 工作原理

核心原则是识别应用不再“reachable”的对象。GC roots 包括：当前线程调用栈中的对象、类的静态变量以及用于同步的对象。垃圾收集器从这些 roots 开始，遍历整个对象引用图。它能到达的任何对象被视为“live”；无法到达的对象则是垃圾。

大多数现代 GC 使用 **Mark-and-Sweep** 算法：
**Mark Phase**：垃圾收集器从 GC roots 开始遍历对象图，并标记遇到的每个 live 对象。**Sweep Phase**：标记完成后，收集器扫描整个 heap；任何未标记的对象现在被视为 unreachable，其内存被回收。

### GC 事件类型

- **Minor GC**：清理 Young Generation。它频繁且快速，能快速回收大量内存，而不会导致长时间应用暂停。
- **Major / Full GC**：发生在 Old Generation，其中驻留长寿对象。它不频繁但耗时更多，因为它处理更大的内存空间并进行更彻底的清理。

### 现代 GC 收集器

不同的收集器提供不同的权衡：**Serial GC** 用于单线程环境；**Parallel GC** 使用多个线程进行 GC；**CMS (Concurrent Mark-Sweep)** 用于低暂停时间；**G1 (Garbage First)** 平衡延迟和吞吐量。

---

## 总结：各项存放位置

| 数据 | 内存区域 |
|---|---|
| 本地变量（基本类型） | Stack |
| 对象引用 | Stack（引用） + Heap（实际对象） |
| 新对象 / 数组 | Heap —— Young Generation（Eden） |
| 长寿对象 | Heap —— Old Generation |
| 静态变量 | Metaspace / Method Area |
| 类元数据 | Metaspace |
| 方法字节码 | Metaspace / Code Cache |
| 当前指令指针 | PC Register |
| Native 方法执行 | Native Method Stack |

---

## 并发注意事项（Java Memory Model / JMM）

JMM 定义了一个线程所做的更改何时对其他线程可见。由于 CPU caches，一个线程对变量的更新可能不会立即对另一个线程可见。JVM 和处理器也可以重新排序指令以优化性能——如果不正确管理，这种重新排序可能导致意外行为。

确保线程安全的关键工具：
- `volatile` —— 保证跨线程可见性
- `synchronized` —— 确保互斥和内存可见性
- `happens-before` —— 对所有动作的部分顺序，确保如果程序顺序中一个动作发生在另一个之前，它会在 happens-before 顺序中发生在另一个之前，从而在并发程序中启用安全推理。

---

**参考资料：**

- [DigitalOcean — Java Memory Management Explained](https://www.digitalocean.com/community/tutorials/java-jvm-memory-model-memory-management-in-java)
- [GeeksForGeeks — Java Memory Management](https://www.geeksforgeeks.org/java/java-memory-management/)
- [Netdata — Garbage Collection in Java](https://www.netdata.cloud/academy/java-garbage-collection/)
- [Java Code Geeks — Heap, Stack and Beyond](https://www.javacodegeeks.com/2025/12/java-memory-management-understanding-heap-stack-and-beyond.html)
- [DEV Community — Understanding the JMM](https://dev.to/adaumircosta/understanding-the-java-memory-model-jmm-p63)
- [Wikipedia — Java Memory Model](https://en.wikipedia.org/wiki/Java_memory_model)