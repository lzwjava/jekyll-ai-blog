---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 构造函数自动初始化对象
translated: true
type: note
---

问题：对象创建时会自动调用哪个方法？ A. main() B. Constructor C. finalize() D. toString()

答案：

正确答案是 **B. Constructor**。

在面向对象编程中（特别是 Java 和 C++ 等语言），**constructor** 是一种特殊方法，当类的对象被创建时（在 Java 中使用 `new` 关键字实例化）会自动调用。其主要目的是初始化对象的 state 并分配必要的 resources。

- **main()**: 这是程序执行的入口方法，而不是在对象创建期间调用的。
- **finalize()** (在 Java 中): 这是由垃圾收集器在对象被销毁前调用的，而不是在创建期间。
- **toString()**: 这是一个将对象转换为 string representation 的方法，必须显式调用（尽管它经常被 overridden）。

这个概念是 OOP 中确保 proper object initialization 的基础。

参考文献：

- [Java Documentation: Constructors](https://docs.oracle.com/javase/tutorial/java/javaOO/constructors.html)
- [GeeksforGeeks: Constructors in Java](https://www.geeksforgeeks.org/constructors-in-java/)