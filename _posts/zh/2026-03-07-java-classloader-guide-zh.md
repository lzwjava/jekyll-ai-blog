---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Java 类加载器详解
translated: true
type: note
---

**问题：** Java ClassLoader 是如何工作的？

**回答：**

## 概述

Java ClassLoader 是 Java Runtime Environment 的组成部分，它动态地将 Java 类加载到 JVM 中。通常，类仅在需要时才加载——虚拟机只加载执行程序所需的类文件。

Java 源代码由 `javac` 编译器编译成 `.class` 文件，JVM 通过运行这些文件中的字节码来执行程序。ClassLoader 负责从文件系统、网络或其他任何来源加载这些类文件。

---

## 三个内置 ClassLoader

每个 Java 程序至少有三个类加载器：

### 1. Bootstrap（Primordial）Class Loader
这是根类加载器，负责加载核心 Java 类，例如 `java.lang.Object` 和 Java 标准库中的其他类。它用 native code 实现，是 JVM 本身的一部分。没有对应的 `ClassLoader` 对象。

- **Java 8 及更早版本：** 从 `<JAVA_HOME>/jre/lib/rt.jar` 加载
- **Java 9 及更高版本：** 从模块化运行时镜像加载核心 Java 类，通常位于 `<JAVA_HOME>/lib/modules` 或 `<JAVA_HOME>/jmods`，与 Java Platform Module System (JPMS) 集成。

### 2. Platform（Extension）Class Loader
扩展类加载器负责加载 Java 扩展机制的一部分类。在 Java 8 中，它从 JRE 的 `lib/ext` 目录加载。在 Java 9+ 中，它变成了 **Platform Class Loader**，与模块系统协作。

### 3. Application（System）Class Loader
应用类加载器是一个标准的 Java 类，它从 `CLASSPATH` 环境变量或 `-classpath` 命令行选项中列出的目录和 JAR 文件加载类。如果有多个版本，它加载第一个找到的类，并且它是最后一个搜索类的类加载器。如果找不到类，JVM 会抛出 `ClassNotFoundException`。

---

## 委托模型（Parent Delegation）

ClassLoader 遵循委托层次结构算法。当 JVM 遇到一个类时，它会检查该类是否已加载。如果未加载，它会通过 ClassLoader 链委托加载过程。

委托流程如下：

1. **Application ClassLoader** 接收加载类的请求。
2. 它向上委托给 **Platform ClassLoader**。
3. Platform ClassLoader 向上委托给 **Bootstrap ClassLoader**。
4. Bootstrap 首先尝试加载类。如果成功，完成。
5. 如果 Bootstrap 失败，Platform ClassLoader 尝试。
6. 如果 Platform 也失败，Application ClassLoader 自己尝试加载。

作为委托模型的后果，很容易确保类的唯一性，因为系统总是尝试向上委托。只有当父类加载器找不到类时，当前实例才会尝试加载它。

---

## 三个核心原则

### 1. 委托
当被请求查找类或资源时，类加载器会在尝试自己查找之前，将搜索委托给其父类加载器。

### 2. 可见性
可见性原则规定，由父 ClassLoader 加载的类对子 ClassLoader 可见，但由子 ClassLoader 加载的类对父 ClassLoader 不可见。

### 3. 唯一性
唯一性属性确保类是唯一的，没有重复。这也确保由父类加载器加载的类不会被子类加载器再次加载。

但是，请注意，类由 `ClassLoader + ClassName` 唯一标识，这意味着由两个不同 ClassLoader 加载的相同类在 JVM 中被视为两个不同的类。

---

## `java.lang.ClassLoader` 中的关键方法

| 方法 | 描述 |
|---|---|
| `loadClass(String name)` | 入口点；应用 delegation model |
| `findClass(String name)` | 在自定义加载器中重写此方法以查找类字节 |
| `defineClass(byte[])` | 将原始字节转换为 `Class` 对象 |
| `findLoadedClass(String name)` | 检查类是否已加载 |

`ClassLoader` 的 `findClass` 方法在父类加载器未找到类时，在当前类加载器中搜索类。通常在实现自定义类加载器子类时重写此方法。

---

## 延迟（Lazy）加载

Java 实现了类的延迟加载。只有当应用明确引用引用字段时，才会执行其类加载。换句话说，字符引用解析是可选的，默认不发生。

---

## 自定义 ClassLoader

Java 允许创建自定义类加载器。这在需要以自定义方式加载类（如从网络来源或动态生成来源）的场景中很有用。自定义类加载器通常用于 Web 服务器、应用服务器和 IDE 等复杂应用中，在这些应用中，需要以特定方式加载类、与系统类隔离，或动态重新加载。

---

## 类加载阶段

当类加载到 JVM 中时，它会经历以下阶段：

1. **加载** — ClassLoader 查找并读取 `.class` 文件字节。
2. **链接**
   - *验证* — 确保字节码有效且安全。
   - *准备* — 为静态字段分配内存并设置默认值。
   - *解析* — 将符号引用替换为直接引用。
3. **初始化** — 执行静态初始化器和静态变量赋值。

---

## Java 9+ 的变化

Java 9 引入了 Java Platform Module System (JPMS)，它指定了 Java 代码和资源集合的分发格式、存储这些模块的仓库，以及如何发现、加载和检查其完整性。

---

**参考文献：**

- [Class Loaders in Java – Baeldung](https://www.baeldung.com/java-classloaders)
- [ClassLoader in Java – GeeksforGeeks](https://www.geeksforgeeks.org/java/classloader-in-java/)
- [Java class loader – Wikipedia](https://en.wikipedia.org/wiki/Java_class_loader)
- [Understanding Java Class Loaders – Medium](https://medium.com/@AlexanderObregon/understanding-java-class-loaders-1dbd5bc4ba06)
- [ClassLoaders in JVM – DZone](https://dzone.com/articles/classloaders-in-jvm-an-overview)
- [How ClassLoader Works in Java – Javarevisited](https://javarevisited.blogspot.com/2012/12/how-classloader-works-in-java.html)
- [All about Java class loaders – InfoWorld](https://www.infoworld.com/article/2077260/learn-java-the-basics-of-java-class-loaders.html)