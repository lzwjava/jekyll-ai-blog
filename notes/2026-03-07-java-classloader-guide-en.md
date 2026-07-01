---
audio: false
generated: true
image: false
lang: en
layout: post
title: Java ClassLoader Explained Clearly
translated: false
type: note
---

**Question:** How does the Java ClassLoader work?

**Answer:**

## Overview

The Java ClassLoader is part of the Java Runtime Environment and dynamically loads Java classes into the JVM. Classes are typically only loaded on demand — the virtual machine loads only the class files required for executing the program.

Java source code is compiled into `.class` files by the `javac` compiler, and the JVM executes the program by running the bytecodes in those files. The ClassLoader is responsible for loading those class files from file systems, networks, or any other source.

---

## The Three Built-in ClassLoaders

Every Java program has at least three class loaders:

### 1. Bootstrap (Primordial) Class Loader

This is the root class loader, responsible for loading core Java classes such as `java.lang.Object` and other classes in the Java standard library. It is implemented in native code and is part of the JVM itself. There is no `ClassLoader` object corresponding to the Bootstrap Class Loader.

- **Java 8 and earlier:** Loads from `<JAVA_HOME>/jre/lib/rt.jar`
- **Java 9 and later:** Loads core Java classes from the modular runtime image, typically in `<JAVA_HOME>/lib/modules` or `<JAVA_HOME>/jmods`, integrated with the Java Platform Module System (JPMS).

### 2. Platform (Extension) Class Loader

The extension class loader is responsible for loading classes that are part of the Java extension mechanism. In Java 8, it loads from the `lib/ext` directory of the JRE. In Java 9+, it became the **Platform Class Loader** working with the module system.

### 3. Application (System) Class Loader

The application class loader is a standard Java class that loads classes from the directories and JAR files listed in the `CLASSPATH` environment variable or the `-classpath` command-line option. It loads the first class it finds if there are multiple versions, and it is the last class loader to search for a class. If it cannot find the class, the JVM throws a `ClassNotFoundException`.

---

## The Delegation Model (Parent Delegation)

ClassLoaders follow a delegation hierarchy algorithm. When the JVM encounters a class, it checks if it's already loaded. If not, it delegates the loading process through a chain of ClassLoaders.

The delegation flow works like this:

1. **Application ClassLoader** receives a request to load a class.
2. It delegates up to the **Platform ClassLoader**.
3. Platform ClassLoader delegates up to the **Bootstrap ClassLoader**.
4. Bootstrap tries to load the class first. If it succeeds, done.
5. If Bootstrap fails, Platform ClassLoader tries.
6. If Platform also fails, the Application ClassLoader tries to load it itself.

As a consequence of the delegation model, it is easy to ensure unique classes, as the system always tries to delegate upwards. If the parent class loader cannot find the class, only then will the current instance attempt to load it.

---

## Three Core Principles

### 1. Delegation

When requested to find a class or resource, a class loader will delegate the search to its parent class loader before attempting to find the class or resource itself.

### 2. Visibility

The Visibility Principle states that a class loaded by a parent ClassLoader is visible to the child ClassLoaders, but a class loaded by a child ClassLoader is not visible to the parent ClassLoaders.

### 3. Uniqueness

The Uniqueness Property ensures that classes are unique and there is no repetition. This also ensures that classes loaded by parent class loaders are not loaded again by the child class loaders.

However, note that a class is uniquely identified by `ClassLoader + ClassName`, meaning the same class loaded by two different ClassLoaders is treated as two distinct classes in the JVM.

---

## Key Methods in `java.lang.ClassLoader`

| Method | Description |
| --- | --- |
| `loadClass(String name)` | Entry point; applies delegation model |
| `findClass(String name)` | Override this in custom loaders to find class bytes |
| `defineClass(byte[])` | Converts raw bytes into a `Class` object |
| `findLoadedClass(String name)` | Checks if the class is already loaded |

The `findClass` method of `ClassLoader` searches for the class in the current class loader if the class was not found by the parent class loader. You will typically override this method when implementing a custom class loader subclass.

---

## Lazy (Deferred) Loading

Java implements lazy loading of classes. Class loading of referenced fields will not be performed until the application explicitly refers to them. In other words, character reference resolution is optional and does not happen by default.

---

## Custom Class Loaders

Java allows the creation of custom class loaders. This is useful in scenarios where you need to load classes in a custom way, such as from a network source or a dynamically generated source. Custom class loaders are typically used in complex applications like web servers, application servers, and IDEs where classes need to be loaded in a specific manner, isolated from the system classes, or reloaded dynamically.

---

## Class Loading Phases

When a class is loaded into the JVM, it goes through these phases:

1. **Loading** — ClassLoader finds and reads the `.class` file bytes.
2. **Linking**
   - *Verification* — Ensures bytecode is valid and safe.
   - *Preparation* — Allocates memory for static fields with default values.
   - *Resolution* — Replaces symbolic references with direct references.
3. **Initialization** — Executes static initializers and static variable assignments.

---

## Java 9+ Changes

Java 9 introduced the Java Platform Module System (JPMS), which specifies a distribution format for collections of Java code and resources, along with a repository for storing these modules, and identifies how they can be discovered, loaded, and checked for integrity.

---

**References:**

- [Class Loaders in Java – Baeldung](https://www.baeldung.com/java-classloaders)
- [ClassLoader in Java – GeeksforGeeks](https://www.geeksforgeeks.org/java/classloader-in-java/)
- [Java class loader – Wikipedia](https://en.wikipedia.org/wiki/Java_class_loader)
- [Understanding Java Class Loaders – Medium](https://medium.com/@AlexanderObregon/understanding-java-class-loaders-1dbd5bc4ba06)
- [ClassLoaders in JVM – DZone](https://dzone.com/articles/classloaders-in-jvm-an-overview)
- [How ClassLoader Works in Java – Javarevisited](https://javarevisited.blogspot.com/2012/12/how-classloader-works-in-java.html)
- [All about Java class loaders – InfoWorld](https://www.infoworld.com/article/2077260/learn-java-the-basics-of-java-class-loaders.html)
