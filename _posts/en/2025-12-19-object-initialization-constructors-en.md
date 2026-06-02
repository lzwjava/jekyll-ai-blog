---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Constructors Automatically Initialize Objects
translated: false
type: note
---

Question: Which method is called automatically when an object is created? A. main() B. Constructor C. finalize() D. toString()

Answer:

The correct answer is **B. Constructor**.

In object-oriented programming (particularly in languages like Java and C++), the **constructor** is a special method that is automatically invoked when an object of a class is created (instantiated using the `new` keyword in Java). Its primary purpose is to initialize the object's state and allocate necessary resources.

- **main()**: This is the entry point method for program execution, not called during object creation.
- **finalize()** (in Java): This is called by the garbage collector before an object is destroyed, not during creation.
- **toString()**: This is a method for converting an object to a string representation and must be explicitly called (though it's often overridden).

This concept is fundamental in OOP for ensuring proper object initialization.

References:

- [Java Documentation: Constructors](https://docs.oracle.com/javase/tutorial/java/javaOO/constructors.html)
- [GeeksforGeeks: Constructors in Java](https://www.geeksforgeeks.org/constructors-in-java/)
