---
audio: false
generated: true
image: false
lang: en
layout: post
title: JVM Memory and Method Execution
translated: false
type: note
---

**Question:** How does the JVM memory model work, and how does it manage objects and method calls?

**Answer:**

---

## Overview

The JVM divides its memory into several logical runtime data areas, each serving a specific role during program execution. This structured memory model ensures isolation between different types of data, supports multithreading, and enables features like automatic garbage collection.

---

## JVM Memory Areas

### 1. Heap

The Java Heap is the primary area for dynamic memory allocation. All class instances, arrays, and objects created during program execution are stored here. Unlike stack memory, which is isolated to individual threads, the heap is a shared memory space accessible by all threads in the JVM.

The heap is divided into two main regions: the **Young Generation** and the **Old Generation**. The Young Generation is further split into the **Eden Space** (where new objects are first created) and two **Survivor Spaces** (S0 and S1), where objects that survive garbage collection are moved.

### 2. Stack (Per Thread)

Each thread running within the JVM has its own thread stack. Local variables for primitive types are fully stored on the thread stack and are not visible to other threads. Even if two threads are executing the same code, they will create their own separate copies of local variables in their respective thread stacks.

Stack memory grows and shrinks as new methods are called and returned, respectively. When a method is called, a new stack frame is created, and when the method returns, the corresponding stack frame is removed. Variables declared in the stack exist only as long as the method that created them is running.

### 3. Method Area / Metaspace

The Method Area is part of the Java heap, shared among all threads. It stores class-level information such as class metadata, static variables, and the constant pool (which holds constants like string literals and references).

In Java 8+, Metaspace replaced the older PermGen. Unlike PermGen's fixed size, Metaspace can grow dynamically, limited only by available native memory. This flexibility prevents the dreaded `OutOfMemoryError: PermGen space`, but introduces risk if uncontrolled growth happens from classloader leaks or dynamic class generation.

### 4. PC (Program Counter) Register

Each JVM thread has a Program Counter (PC) register. For non-native methods, it stores the address of the current JVM instruction being executed.

### 5. Native Method Stack

Native method stacks handle the execution of native methods that interact with the Java code. This memory is allocated for each thread when it is created and can have either a fixed or dynamic size.

---

## How Method Calling Works (Stack Frames)

Every time a method is invoked, the JVM allocates a new **stack frame** on the thread's stack. This frame is a self-contained unit of memory that holds all the necessary data for executing that method. The frame remains on the stack until the method completes normally or exits abruptly (e.g., due to an exception). Once the method returns, its frame is removed from the stack, and the memory is automatically reclaimed — no garbage collection is required for stack memory.

Each stack frame contains:

- **Local variable array**: Holds all method parameters and local variables declared within the method.
- **Operand stack**: Used internally by the JVM to evaluate expressions and store intermediate computations.
- **Return value slot**: Stores the result of the method call, if any, before passing it back to the calling method.
- **Reference to the runtime constant pool**: Allows the method to resolve field names, method names, and literals.

**Practical example** — calling `m1 → m2 → m3`:
When m1 calls m2, a new frame is pushed on top of m1's frame. When m2 calls m3, another frame is pushed on top. After m3 finishes, its frame is flushed and control returns to m2. The same then happens for m2 and m1.

If the stack exceeds its allocated space (e.g., due to infinite recursion), a `StackOverflowError` occurs.

---

## How Objects Are Managed (Heap & Garbage Collection)

### Object Lifecycle

New objects are allocated in the Heap's Young Generation (Eden Space). A minor garbage collection happens when the Young Generation fills up. Long-surviving objects are moved to the Old (Tenured) Generation.

Objects that survive multiple Minor GCs eventually get promoted to the Old Generation. This "generational hypothesis" — that most objects die young — drives garbage collector design across all modern JVMs.

### Garbage Collection — How It Works

The core principle is to identify objects that are no longer "reachable" by the application. GC roots include: objects in the current thread's call stack, static variables of classes, and objects used for synchronization. The garbage collector starts at these roots and traverses the entire graph of object references. Any object it can reach is considered "live"; any object it cannot reach is garbage.

Most modern GCs use the **Mark-and-Sweep** algorithm:
**Mark Phase**: The garbage collector traverses the object graph starting from GC roots and marks every live object it encounters. **Sweep Phase**: After marking is complete, the collector scans the entire heap; any object that was not marked is now known to be unreachable and its memory is reclaimed.

### Types of GC Events

- **Minor GC**: Cleans up the Young Generation. It is frequent and fast, reclaiming large amounts of memory quickly without long application pauses.
- **Major / Full GC**: Occurs in the Old Generation where long-lived objects reside. It is less frequent but more time-consuming, as it deals with a larger memory space and performs more thorough cleanup.

### Modern GC Collectors

Different collectors offer different trade-offs: **Serial GC** for single-threaded environments; **Parallel GC** uses multiple threads for GC; **CMS (Concurrent Mark-Sweep)** for low pause times; and **G1 (Garbage First)** which balances latency and throughput.

---

## Summary: Where Things Live

| Data | Memory Area |
|---|---|
| Local variables (primitives) | Stack |
| Object references | Stack (reference) + Heap (actual object) |
| New objects / arrays | Heap — Young Generation (Eden) |
| Long-lived objects | Heap — Old Generation |
| Static variables | Metaspace / Method Area |
| Class metadata | Metaspace |
| Method bytecode | Metaspace / Code Cache |
| Current instruction pointer | PC Register |
| Native method execution | Native Method Stack |

---

## Concurrency Note (Java Memory Model / JMM)

The JMM defines how and when changes made by one thread become visible to other threads. Due to CPU caches, an update made by one thread to a variable may not be immediately visible to another. The JVM and processor can also reorder instructions to optimize performance — this reordering can cause unexpected behavior if not managed properly.

Key tools to ensure thread safety:

- `volatile` — guarantees visibility across threads
- `synchronized` — ensures mutual exclusion and memory visibility
- `happens-before` — a partial order over all actions ensuring that if one action occurs before another in program order, it will occur before the other in the happens-before order, enabling safe reasoning in concurrent programs.

---

**References:**

- [DigitalOcean — Java Memory Management Explained](https://www.digitalocean.com/community/tutorials/java-jvm-memory-model-memory-management-in-java)
- [GeeksForGeeks — Java Memory Management](https://www.geeksforgeeks.org/java/java-memory-management/)
- [Netdata — Garbage Collection in Java](https://www.netdata.cloud/academy/java-garbage-collection/)
- [Java Code Geeks — Heap, Stack and Beyond](https://www.javacodegeeks.com/2025/12/java-memory-management-understanding-heap-stack-and-beyond.html)
- [DEV Community — Understanding the JMM](https://dev.to/adaumircosta/understanding-the-java-memory-model-jmm-p63)
- [Wikipedia — Java Memory Model](https://en.wikipedia.org/wiki/Java_memory_model)
