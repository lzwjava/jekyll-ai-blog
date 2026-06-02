---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Java Boolean Default Value
translated: false
type: note
---

Question: What is the default value of a boolean instance variable in a class?

Answer:

In Java, instance variables (fields) of a class that are not explicitly initialized are automatically assigned default values based on their type.

For primitive types:
- `boolean` defaults to **false**
- `int`, `byte`, `short`, `long` default to 0
- `float`, `double` default to 0.0
- `char` defaults to '' (null character)
- Reference types (e.g., objects, strings) default to `null`

Therefore, the default value of a `boolean` instance variable is **false**.

The correct answer is **B. false**.

Note: This applies to instance variables and static variables. Local variables (declared inside methods) do not have default values and must be explicitly initialized before use.

References:

- [Oracle Java Documentation - Default Values](https://docs.oracle.com/javase/specs/jls/se21/html/jls-4.html#jls-4.12.5)
- [Oracle Java Tutorials - Primitive Data Types](https://docs.oracle.com/javase/tutorial/java/nutsandbolts/datatypes.html)
