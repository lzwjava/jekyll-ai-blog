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

## **1. Memory Overhead**

- **StringBuffer**: 由于 Synchronization Metadata 和 Lock Objects，内存开销略高
- **StringBuilder**: 内存占用更低，不需要 Synchronization 结构

## **2. Method Invocation Cost**

- **StringBuffer**: 每次方法调用都有 Monitor 获取/释放成本（即使在单线程场景下）
- **StringBuilder**: 直接进行 Method Invocation，没有 Lock 开销

## **3. JVM Optimizations**

- **StringBuffer**: 由于 Synchronization Barriers，JIT Compiler 优化受限
- **StringBuilder**: 允许更激进的优化（Method Inlining、Escape Analysis、Stack Allocation）

## **4. Inheritance Hierarchy**

两者都继承自 `AbstractStringBuilder`（Package-private Class），其中包含了实际的实现：

```
Object
  └── AbstractStringBuilder (contains char array and logic)
      ├── StringBuffer (adds synchronized wrapper)
      └── StringBuilder (no synchronization)
```

## **5. Default Capacity**

两者具有相同的默认初始 Capacity：

- 默认值：16 个字符
- 动态增长：超出时按 `(oldCapacity * 2) + 2` 扩展

## **6. API Compatibility**

- **相同的方法**：append(), insert(), delete(), reverse(), substring(), charAt(), length(), capacity() 等
- **相同的返回类型**：两者都返回 `this` 以支持 Method Chaining
- **可互换性**：如果不需要 Thread Safety，只需更改类名即可互相替换

## **7. Serialization**

- **StringBuffer**: 实现了 `Serializable`
- **StringBuilder**: 实现了 `Serializable`
- 两者都可以序列化，序列化的是底层的 Char Array

## **8. Use in Collections/Frameworks**

- 两者都不应作为 HashMap 的 Key（两者都是 Mutable 的）
- 在 toString() 实现中首选 StringBuilder
- StringBuffer 常用于旧的 Thread-safe Utility Classes

## **9. Compiler Behavior**

```java
// String concatenation in loops
String s = "";
for(int i = 0; i < 100; i++) {
    s += i; // Compiler may use StringBuilder internally (Java 9+)
}
```

现代 Java Compiler 自动使用 StringBuilder 进行字符串拼接，而不是 StringBuffer。

## **10. Benchmarking Context**

在以下情况下，性能差异变得显著：

- 高循环次数（1000+ 次操作）
- Concurrent Access 模式
- 大规模字符串操作
- 性能关键型应用

## **11. Backwards Compatibility**

- **StringBuffer**: 由于遗留代码依赖，无法移除
- **StringBuilder**: 自 Java 5 起推荐用于所有新代码

## **12. Common Mistake**

```java
// WRONG: Sharing StringBuilder between threads
StringBuilder sb = new StringBuilder();
thread1.run(() -> sb.append("A"));
thread2.run(() -> sb.append("B")); // Race condition!

// CORRECT: Use StringBuffer or external synchronization
StringBuffer sbf = new StringBuffer();
thread1.run(() -> sbf.append("A"));
thread2.run(() -> sbf.append("B")); // Thread-safe
```

## **Summary Table**

| Aspect | StringBuffer | StringBuilder |
| -------- | ------------- | --------------- |
| Speed | Slower | Faster |
| Thread-Safe | Yes | No |
| Since | Java 1.0 | Java 5 |
| Synchronization | All methods | None |
| Use Case | Multi-threaded | Single-threaded |
| JVM Optimization | Limited | Aggressive |
| Memory | Higher | Lower |
| Default Choice | No | **Yes** |

**Bottom Line**: 除非你有明确的多线程需求，否则请始终使用 StringBuilder。它更快、更高效，并且是现代标准。
