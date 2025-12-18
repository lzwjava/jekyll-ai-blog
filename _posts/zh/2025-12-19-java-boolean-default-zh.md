---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Java 布尔值默认值
translated: true
type: note
---

问题：类中 boolean 实例变量的默认值是什么？

答案：

在 Java 中，未明确初始化的类实例变量（字段）会根据其类型自动赋默认值。

对于原始类型：
- `boolean` 默认为 **false**
- `int`、`byte`、`short`、`long` 默认为 0
- `float`、`double` 默认为 0.0
- `char` 默认为 ''（null 字符）
- 引用类型（例如，对象、字符串）默认为 `null`

因此，`boolean` 实例变量的默认值为 **false**。

正确答案是 **B. false**。

注意：这适用于实例变量和静态变量。局部变量（在方法内声明的变量）没有默认值，必须在使用前明确初始化。

参考文献：

- [Oracle Java Documentation - Default Values](https://docs.oracle.com/javase/specs/jls/se21/html/jls-4.html#jls-4.12.5)
- [Oracle Java Tutorials - Primitive Data Types](https://docs.oracle.com/javase/tutorial/java/nutsandbolts/datatypes.html)