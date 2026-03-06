---
audio: false
generated: true
image: false
lang: en
layout: post
title: Core OS Characteristics Explained
translated: false
type: note
---

**Question:** What are the four basic characteristics (common features) shared by all operating systems, and why is the correct answer D (Concurrency, Sharing, Virtuality, Asynchrony) rather than A (Concurrency, Sharing, Real-time, Synchrony)?

**Answer:**

## The Four Basic Characteristics of an Operating System

The correct answer is **D: Concurrency (并发性), Sharing (共享性), Virtuality (虚拟性), Asynchrony (异步性)**.

This is a classic foundational question in operating systems theory, particularly in Chinese computer science curricula. Here is a comprehensive breakdown of each characteristic and why the other options are wrong.

---

### ✅ The Four Correct Characteristics

#### 1. Concurrency (并发性)
Concurrency refers to the capability of an OS to handle more than one task or process at the same time, thereby enhancing efficiency and responsiveness. It may be supported by multi-threading or multi-processing, whereby more than one process or thread is executed simultaneously or in an interleaved fashion.

In a multiprogramming environment, multiple processes exist in memory simultaneously and take turns using the CPU. This is the most fundamental characteristic of a modern OS — without it, true multitasking would be impossible.

#### 2. Sharing (共享性)
On modern personal computers, the operating system gives each application a share of resources, either in time (CPU) or space (memory), to ensure no one program can monopolize limited hardware.

Sharing means that system resources (CPU, memory, I/O devices, files) are shared among multiple concurrently running processes, either in a mutually exclusive manner or by simultaneous access.

#### 3. Virtuality (虚拟性)
Virtual memory provides the programmer or user with the perception that there is a much larger amount of RAM in the computer than is really there. Virtualization also enables the operating system to mask limited hardware resources.

The OS uses techniques like virtual memory, virtual CPUs (time-sharing), and virtual devices to give each user/process the illusion of having dedicated resources, even when physical resources are limited and shared.

#### 4. Asynchrony (异步性)
The result of execution of cooperating processes depends on the relative execution sequence and cannot be predicted in advance (non-deterministic). The result of execution will not always be the same for the same input.

In a multitasking OS, processes proceed at unpredictable speeds — they may be interrupted, suspended, or resumed at any time. The OS must handle this non-deterministic behavior correctly. This is asynchrony: processes do not proceed at a fixed, predictable pace.

---

### ❌ Why the Other Options Are Wrong

| Option | Problem |
|--------|---------|
| **A** (Concurrency, Sharing, **Real-time**, **Synchrony**) | Real-time (实时性) is a feature of **real-time operating systems** specifically, not all OSes. Synchrony (同步性) is a *mechanism* used within an OS (e.g., semaphores), not a basic characteristic of the OS itself. |
| **B** (Mutual exclusion, Independence, Virtuality, Asynchrony) | Mutual exclusion (互斥性) and independence (独立性) are concepts related to process management, not top-level OS characteristics. |
| **C** (Timeliness, Sharing, Virtuality, Synchrony) | Timeliness (及时性) belongs to real-time systems only. Synchrony replaces the correct term Asynchrony. |

---

### Key Insight: Concurrency and Asynchrony Are Closely Related

Concurrency is what **makes** asynchrony necessary. Because multiple processes run concurrently and share resources, their individual execution speeds become unpredictable — that unpredictability is exactly what asynchrony describes. Together, the four characteristics form an interconnected system:

- **Concurrency** → multiple processes run "simultaneously"
- **Sharing** → they share the same resources
- **Virtuality** → the OS abstracts real hardware into virtual resources to support the above
- **Asynchrony** → because of concurrency and sharing, execution order/speed is non-deterministic

---

### Summary

> The four basic characteristics of an operating system are: **Concurrency, Sharing, Virtuality, and Asynchrony** — option **D**.

Option A incorrectly substitutes "Real-time" for "Virtuality" and "Synchrony" for "Asynchrony." Both substitutions introduce concepts that either apply only to specialized systems (real-time OS) or describe mechanisms rather than fundamental OS traits.

References:

- [GeeksforGeeks – Concurrency in Operating System](https://www.geeksforgeeks.org/operating-systems/concurrency-in-operating-system/)
- [Wikipedia – Operating System](https://en.wikipedia.org/wiki/Operating_system)
- [OpenStax – Processes and Concurrency](https://openstax.org/books/introduction-computer-science/pages/6-3-processes-and-concurrency)