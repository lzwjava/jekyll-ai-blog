---
audio: false
generated: true
lang: en
layout: post
title: Why is Redis Fast
translated: false
type: note
---

### Key Points
- It seems likely that the YouTube video "System Design: Why is single-threaded Redis so fast?" by ByteByteGo explains Redis's speed due to in-memory storage, IO multiplexing, and efficient data structures.
- Research suggests these factors allow Redis to handle up to 100,000 queries per second, despite being single-threaded for request processing.
- The evidence leans toward recent Redis versions adding multi-threading for specific tasks, but the core remains single-threaded.

---

### Introduction
This blog post is based on the YouTube video "System Design: Why is single-threaded Redis so fast?" by ByteByteGo, part of their system design series. Redis, known for its high performance, can handle up to 100,000 queries per second on a single machine, which is impressive for a single-threaded system. Let's explore why this is possible and what makes Redis so fast.

### Reasons for Redis's Speed
Redis's speed can be attributed to several key factors, likely covered in the video:

- **In-Memory Storage**: Redis stores data in RAM, which is much faster than disk storage. This reduces latency and increases throughput, as memory access times are in nanoseconds compared to milliseconds for disk access.

- **IO Multiplexing and Single-Threaded Execution**: IO multiplexing, using mechanisms like epoll on Linux, allows a single thread to handle multiple client connections efficiently. This avoids the overhead of context switching, and the single-threaded loop simplifies operations by eliminating synchronization issues.

- **Efficient Data Structures**: Redis uses optimized data structures like hash tables (O(1) lookups), linked lists, and skip lists, which enhance performance by minimizing memory usage and speeding up operations.

### Scaling and Evolution
For high concurrency, Redis can be scaled horizontally using multiple instances or clustering. An unexpected detail is that while the core request processing remains single-threaded, recent versions (since 4.0) have introduced multi-threading for tasks like background object deletion, improving performance further without changing the primary model.

---

### Survey Note: Detailed Analysis of Redis's Single-Threaded Performance

This section provides a comprehensive analysis of why single-threaded Redis is so fast, based on the YouTube video "System Design: Why is single-threaded Redis so fast?" by ByteByteGo and related research. The video, published on August 13, 2022, is part of a series focused on system design, authored by the creators of bestselling System Design Interview books. Given the channel's focus, the video likely provides detailed insights suitable for technical interviews and system design discussions.

#### Background and Context
Redis, an open-source in-memory key-value store, is widely used as a cache, message broker, and streaming engine. It supports data structures like strings, lists, sets, hashes, sorted sets, and probabilistic structures like Bloom Filter and HyperLogLog. The video's title suggests an exploration of why Redis maintains high performance despite its single-threaded request processing, which is central to its design.

From related articles, Redis can handle up to 100,000 Queries Per Second (QPS) on a single machine, a figure often cited in performance benchmarks. This speed is surprising given the single-threaded model, but research indicates it's due to several architectural choices.

#### Key Factors Contributing to Redis's Speed

1. **In-Memory Storage**
   Redis stores data in RAM, which is at least 1000 times faster than random disk access. This eliminates the latency of disk I/O, with RAM access times around 100-120 nanoseconds compared to 50-150 microseconds for SSDs and 1-10 milliseconds for HDDs. The video likely emphasizes this as a primary reason, as it aligns with the channel's focus on system design fundamentals.

   | Aspect               | Details                                      |
   |----------------------|----------------------------------------------|
   | Storage Medium       | RAM (in-memory)                              |
   | Access Time          | ~100-120 nanoseconds                        |
   | Comparison to Disk   | 1000x faster than random disk access        |
   | Impact on Performance| Reduces latency, increases throughput        |

2. **IO Multiplexing and Single-Threaded Execution Loop**
   IO multiplexing allows a single thread to monitor multiple I/O streams concurrently using system calls like `select`, `poll`, `epoll` (Linux), `kqueue` (Mac OS), or `evport` (Solaris). This is crucial for handling multiple client connections without blocking, a point likely detailed in the video. The single-threaded execution loop avoids context switching and synchronization overhead, simplifying development and debugging.

   | Mechanism            | Description                                  |
   |----------------------|----------------------------------------------|
   | epoll/kqueue         | Efficient for high concurrency, non-blocking |
   | select/poll          | Older, less scalable, O(n) complexity        |
   | Impact               | Reduces connection overhead, enables pipelining |

   However, client-blocking commands like `BLPOP` or `BRPOP` can delay traffic, a potential drawback mentioned in related articles. The video may discuss how this design choice balances simplicity with performance.

3. **Efficient Lower-Level Data Structures**
   Redis leverages data structures like hash tables for O(1) key lookups, linked lists for lists, and skip lists for sorted sets. These are optimized for in-memory operations, minimizing memory usage and maximizing speed. The video likely includes diagrams or examples, such as how hash tables enable fast key-value operations, a common topic in system design interviews.

   | Data Structure       | Use Case                                     | Time Complexity |
   |----------------------|----------------------------------------------|-----------------|
   | Hash Table           | Key-value storage                           | O(1) average    |
   | Linked List          | Lists, efficient at ends                    | O(1) for ends   |
   | Skip List            | Sorted sets, ordered storage                | O(log n)        |

   This optimization is critical, as most Redis operations are memory-based, with bottlenecks typically in memory or network, not CPU.

#### Additional Considerations and Evolution
While the core request processing is single-threaded, recent versions of Redis have introduced multi-threading for specific tasks. Since Redis 4.0, asynchronous memory release (lazy-free) has been implemented, and since 6.0, multi-threading for protocol parsing under high concurrency has been added. These changes, likely mentioned in the video, enhance performance without altering the single-threaded model for main operations.

For scaling beyond a single instance, Redis supports clustering and running multiple instances, a strategy that may be discussed to address high concurrency needs. This is an important aspect for system design, aligning with the channel's focus on large-scale systems.

#### Potential Drawbacks and Comparisons
The single-threaded model has advantages like no lock contention and simpler debugging, but it can face challenges with blocking operations and memory/network bottlenecks under high load. Related articles suggest that for CPU-intensive tasks, multi-threaded databases might perform better, but for Redis's typical use cases, the single-threaded design is optimal.

#### Conclusion
The video "System Design: Why is single-threaded Redis so fast?" by ByteByteGo likely covers in-memory storage, IO multiplexing, and efficient data structures as key reasons for Redis's speed. These factors enable it to handle high QPS, with recent versions adding multi-threading for specific optimizations. This analysis provides a comprehensive understanding, suitable for both technical learners and system design professionals.

---

### Key Citations
- [Why is redis so fast blog post](https://blog.bytebytego.com/p/why-is-redis-so-fast)
- [Why is Redis So Fast Despite Being Single-Threaded article](https://medium.com/@aditimishra_541/why-is-redis-so-fast-despite-being-single-threaded-dc06ba33fc75)
- [Interview on Redis thread model article](https://medium.com/javarevisited/interview-why-is-redis-so-fast-even-though-it-is-single-threaded-bfe663dabe08)
- [Why is single threaded Redis so fast article](https://www.pixelstech.net/article/1677580861-Why-is-single-threaded-Redis-so-fast)
