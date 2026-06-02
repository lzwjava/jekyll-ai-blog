---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Java 中的数组是对象
translated: true
type: note
---

**正确答案是 B. Objects。**

在 Java 中，数组是 **对象**，即使它们存储的是原始类型（如 `int[]`）。《Java 语言规范》（JLS §4.3.1 和 §10）明确指出：“在 Java 编程语言中，数组是对象，它们是动态创建的，可以赋值给 Object 类型的变量。类 Object 的所有方法都可以在数组上调用。”

### 关键证据：
- 数组继承自 `Object`（它们的直接超类是 `Object`）。
- 它们实现了 `Cloneable` 和 `java.io.Serializable`。
- 你可以在数组上调用 Object 方法，例如 `myArray.toString()`、`myArray.hashCode()`，或者检查 `myArray instanceof Object`（返回 `true`）。
- 数组有一个 `length` 字段和一个特殊的 `clone()` 方法。
- 它们使用 `new` 在堆上创建（像其他对象一样）。

### 为什么不是其他选项？
- **A. Primitive data types**：不正确。Java 只有 8 种原始类型（例如 `int`、`boolean`、`char`）。数组是引用类型，不是原始类型。（注意：数组 *可以包含* 原始类型，但数组本身是一个对象。）
- **C. Methods**：不正确。数组是数据结构，不是方法。
- **D. Interfaces**：不正确。数组不是接口；它们是具有特殊 JVM 处理的具体类型。

你选择 A 是一个常见的误解，但官方规范和行为都证实数组是对象。
