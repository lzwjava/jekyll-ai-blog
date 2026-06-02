---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Arrays Are Objects in Java
translated: false
type: note
---

**The correct answer is B. Objects.**

In Java, arrays are **objects**, even if they hold primitive types (like `int[]`). This is explicitly stated in the Java Language Specification (JLS §4.3.1 and §10): "In the Java programming language, arrays are objects, are dynamically created, and may be assigned to variables of type Object. All methods of class Object may be invoked on an array."

### Key evidence:
- Arrays inherit from `Object` (their direct superclass is `Object`).
- They implement `Cloneable` and `java.io.Serializable`.
- You can call Object methods on arrays, e.g., `myArray.toString()`, `myArray.hashCode()`, or check `myArray instanceof Object` (returns `true`).
- Arrays have a `length` field and a special `clone()` method.
- They are created on the heap with `new` (like other objects).

### Why not the other options?
- **A. Primitive data types**: Incorrect. Java has only 8 primitive types (e.g., `int`, `boolean`, `char`). Arrays are reference types, not primitives. (Note: Arrays *can contain* primitives, but the array itself is an object.)
- **C. Methods**: Incorrect. Arrays are data structures, not methods.
- **D. Interfaces**: Incorrect. Arrays are not interfaces; they are concrete types with special JVM handling.

Your selection of A is a common misconception, but the official spec and behavior confirm arrays are objects.
