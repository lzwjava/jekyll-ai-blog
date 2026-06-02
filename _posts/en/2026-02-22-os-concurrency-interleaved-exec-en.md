---
audio: false
generated: true
image: false
lang: en
layout: post
title: OS Concurrency Through Interleaved Execution
translated: false
type: note
---

Question: In a computer system, several programs are running simultaneously and executing in an interleaved manner. Which characteristic of an operating system does this demonstrate?

Answer:

This scenario demonstrates the **Concurrency** (并发性) of an operating system.

* **Definition**: Concurrency refers to the ability of an operating system to manage multiple tasks or processes that appear to execute simultaneously over a specific period.
* **Mechanism**: In a single-core processor environment, true parallel execution is impossible at any single instant. Instead, the OS rapidly switches the CPU between different programs (context switching). This creates the illusion that they are running at the same time, resulting in **interleaved execution** (交错执行).
* **Distinction**: While "Parallelism" (并行性) implies tasks actually running at the exact same moment (requiring multi-core/multi-processor hardware), "Concurrency" specifically describes the logical handling of multiple active tasks where their execution overlaps in time, even if they take turns on the CPU. The phrase "interleaved execution" is the classic definition of concurrency in operating system theory.

References:

* [Operating System Concurrency - GeeksforGeeks](https://www.geeksforgeeks.org/concurrency-in-operating-system/)
* [Concurrency vs Parallelism - Baeldung](https://www.baeldung.com/cs/concurrency-vs-parallelism)
