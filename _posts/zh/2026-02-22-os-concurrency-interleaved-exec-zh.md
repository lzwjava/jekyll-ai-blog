---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 通过交错执行实现操作系统并发
translated: true
type: note
---

问题：在计算机系统中，多个程序同时运行并以交错方式执行。这展示了操作系统的哪种特性？

答案：

这个场景展示了操作系统的 **Concurrency** (并发性)。

* **Definition**: Concurrency 是操作系统管理多个任务或进程的能力，这些任务或进程在特定时期内看似同时执行。
* **Mechanism**: 在单核处理器环境中，任何单一瞬间都不可能实现真正的并行执行。相反，OS 在不同程序之间快速切换 CPU（context switching）。这创造了它们同时运行的错觉，从而导致 **interleaved execution** (交错执行)。
* **Distinction**: 虽然 "Parallelism" (并行性) 意味着任务在确切同一时刻实际运行（需要多核/多处理器硬件），但 "Concurrency" 专门描述了对多个活动任务的逻辑处理，这些任务的执行在时间上重叠，即使它们在 CPU 上轮流执行。短语 "interleaved execution" 是操作系统理论中并发性的经典定义。

参考文献：

* [Operating System Concurrency - GeeksforGeeks](https://www.geeksforgeeks.org/concurrency-in-operating-system/)
* [Concurrency vs Parallelism - Baeldung](https://www.baeldung.com/cs/concurrency-vs-parallelism)
