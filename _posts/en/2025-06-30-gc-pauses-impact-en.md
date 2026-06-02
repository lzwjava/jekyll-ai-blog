---
audio: false
generated: true
lang: en
layout: post
title: 'Go GC Pauses: Cloudflare vs TiDB'
translated: false
type: note
---

Yes, Go's garbage collector (GC) pauses can impact both Cloudflare's services and TiDB database, as both leverage Go heavily in their architecture. However, the nature and impact of these pauses, and how they are mitigated, differ.

Here's a breakdown:

**Go's GC and its Characteristics:**

* **Mark-Sweep GC:** Go uses a concurrent, tri-color mark-sweep garbage collector. This means that most of the GC work (marking live objects) happens concurrently with the application's execution.
* **Stop-the-World (STW) Pauses:** While concurrent, Go's GC still requires brief "stop-the-world" (STW) pauses. These pauses occur in specific phases (like the initial "mark" setup and the final "mark termination" and "sweep termination" phases) where the application's goroutines are halted to ensure memory consistency. The goal of the Go runtime engineers is to minimize these STW durations, typically keeping them in the microsecond range.
* **Factors influencing GC:** The frequency and duration of GC pauses are influenced by:
    * **Allocation rate:** How quickly the application allocates new memory.
    * **Heap size:** The total amount of memory managed by the Go runtime.
    * **`GOGC`:** A parameter that controls the garbage collection target percentage (default 100%). A lower `GOGC` means more frequent GCs.
    * **`GOMEMLIMIT`:** A new parameter (Go 1.19+) that sets an upper bound on the target heap size, helping to prevent OOMs and manage memory more predictably.

**Impact on Cloudflare:**

Cloudflare uses Go extensively for many of its critical services, including DNS infrastructure, SSL handling, load testing, and more. For a high-performance, low-latency system like Cloudflare, even microsecond pauses can be significant.

* **Latency-sensitive services:** Services handling high request rates (like DNS or proxying) are very sensitive to latency spikes. GC pauses, even if short, can contribute to these spikes, affecting user experience.
* **Memory-intensive applications:** Some Cloudflare services might be memory-intensive, leading to more frequent GC cycles if not tuned properly.
* **Mitigation at Cloudflare:** Cloudflare engineers actively work on:
    * **Tuning `GOGC` and `GOMEMLIMIT`:** They experiment with these parameters to balance memory usage and GC frequency.
    * **Profiling and optimizing code:** Identifying and reducing unnecessary memory allocations in their Go code.
    * **Profile-Guided Optimizations (PGO):** Cloudflare has seen significant CPU savings (and thus likely reduced GC pressure) by leveraging Go's PGO feature.
    * **Architectural considerations:** Designing services to be resilient to short pauses, potentially by having enough redundancy or by processing requests in a way that minimizes the impact of a single goroutine's pause.

**Impact on TiDB Database:**

TiDB is a distributed SQL database built by PingCAP, with its SQL layer (`tidb-server`) primarily written in Go. As a database, it has different performance characteristics and requirements compared to a proxy service.

* **Database-specific GC:** TiDB has its own garbage collection mechanisms for MVCC (Multi-Version Concurrency Control) data (cleaning up old data versions in TiKV, its storage engine). This is distinct from Go's runtime GC, though the TiDB "coordinator" (written in Go) initiates and manages this.
* **Go Runtime GC in TiDB:** The Go GC *does* impact TiDB because `tidb-server` processes SQL requests, manages memory for query plans, results, and other runtime data.
    * **Latency jitter:** Frequent STW pauses can lead to latency spikes in query execution, affecting database responsiveness.
    * **CPU overhead:** GC activity consumes CPU resources, which could otherwise be used for processing queries.
    * **Adaptive GC triggering:** TiDB proactively triggers Go GC when memory usage reaches a certain threshold (configurable via `tidb_server_memory_limit` and `tidb_server_memory_limit_gc_trigger`). It also uses an adaptive strategy for `tidb_server_memory_limit_gc_trigger` to avoid excessively frequent GCs.
* **Monitoring and Tuning:** PingCAP provides extensive monitoring tools (like the TiDB Runtime Dashboard) to observe Go GC behavior (GC frequency, duration, STW latency, CPU time spent on GC) and allows users to configure `GOGC` and `GOMEMLIMIT` to optimize performance.
* **Ongoing efforts:** PingCAP engineers are continuously working on optimizing TiDB's Go memory management and GC behavior to minimize its impact on performance and stability.

**In summary:**

Both Cloudflare and TiDB, being high-performance systems relying on Go, are susceptible to the impacts of Go's GC pauses. While Go's GC is highly optimized for short STW durations, at scale, these pauses can contribute to latency spikes and CPU overhead. Both companies actively monitor, tune, and optimize their Go applications and infrastructure to mitigate these effects, leveraging Go's runtime parameters and their own specific architectural designs.
