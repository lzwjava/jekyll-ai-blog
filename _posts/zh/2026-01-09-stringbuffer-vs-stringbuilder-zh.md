---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-sonnet
title: StringBuffer 与 StringBuilder：主要区别
translated: true
type: note
---

## **1. Thread Safety**

- **StringBuffer**: Thread-safe (synchronized)。多个线程可以安全地同时访问而不会导致数据损坏
- **StringBuilder**: 非 Thread-safe。应仅在单线程环境中使用

## **2. Performance**

- **StringBuffer**: 由于 synchronization 开销，速度较慢。每个方法调用都会获取和释放 locks
- **StringBuilder**: 速度更快（通常快 10-15% 或更多），因为它没有 synchronization 开销

## **3. When to Use**

**StringBuffer:**

- 同一个实例被多个线程访问的多线程应用程序
- 当 Thread safety 是强制要求时
- 尚未更新的 Legacy code

**StringBuilder:**

- 单线程应用程序（最常见的场景）
- 方法内的局部变量（不在线程间共享）
- 对 Performance 有要求的现代 Java 应用程序

## **4. Synchronization Details**

- **StringBuffer**: 所有方法都使用 `synchronized` 关键字进行了同步
- **StringBuilder**: 无 synchronization，方法未进行同步

## **5. Introduction**

- **StringBuffer**: 自 Java 1.0 起可用
- **StringBuilder**: 在 Java 5 (2004) 中引入，作为更快的替代方案

## **6. Memory and Method Behavior**

这两个类共享相同的 API 和方法（append, insert, delete, reverse 等），除了 synchronization 之外，功能完全相同。

## **Code Example**

```java
// StringBuilder - faster for single-threaded use
StringBuilder sb = new StringBuilder();
sb.append("Hello");
sb.append(" World");

// StringBuffer - safer for multi-threaded use
StringBuffer sbf = new StringBuffer();
sbf.append("Thread");
sbf.append(" Safe");
```

## **Best Practice**

默认情况下使用 StringBuilder，除非你明确需要 Thread safety，在这种情况下请使用 StringBuffer 或对 StringBuilder 进行外部 synchronization。