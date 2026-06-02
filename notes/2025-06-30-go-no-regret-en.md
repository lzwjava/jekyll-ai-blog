---
audio: false
generated: true
lang: en
layout: post
title: PingCAP and Cloudflare Praise Go
translated: false
type: note
---

Neither PingCAP nor Cloudflare has expressed "regret" about using Go. In fact, both companies have publicly praised Go for its strengths and continue to use it extensively in their core products. However, they are also pragmatic about language choices and use other languages where they are a better fit for specific problems.

Here's a breakdown:

### PingCAP (TiDB) and Go

* **No Regret:** PingCAP chose Go for the SQL layer (`tidb-server`) of TiDB due to its excellent concurrency model (goroutines and channels), ease of development, and strong standard library. These features enabled them to build a complex distributed database relatively quickly.
* **Acknowledged Challenges:** While Go is central to TiDB, PingCAP is very transparent about the challenges, particularly regarding Go's garbage collector. Their documentation and blog posts frequently discuss:
    * **GC pauses:** They acknowledge that GC pauses, even if short, can introduce latency jitter in a high-performance database. They actively work on mitigating this through tuning `GOGC`, `GOMEMLIMIT`, and implementing adaptive GC triggering.
    * **Memory management:** They provide detailed guides on monitoring memory usage and troubleshooting OOM issues, recognizing that inefficient memory patterns in Go can lead to problems.
* **Strategic Use of Rust:** PingCAP chose **Rust** for TiKV, their distributed key-value storage engine. This wasn't a "regret" of Go, but rather a **strategic decision** for the storage layer where extreme low-latency, predictable performance, and fine-grained memory control are paramount.
    * Rust's ownership and borrowing model, along with its lack of a garbage collector, are ideal for systems-level programming where every microsecond and byte matters.
    * They recognized that the trade-off of Rust's steeper learning curve and slower compilation times was acceptable for the critical storage engine, but less desirable for the more rapidly evolving SQL layer.
* **Conclusion for PingCAP:** They clearly see Go and Rust as complementary tools. Go for the higher-level logic and rapid iteration, Rust for the low-level, performance-critical components.

### Cloudflare and Go

* **Extensive Go Adoption:** Cloudflare was an early and enthusiastic adopter of Go. They use Go for a vast array of their services, including DNS infrastructure, SSL handling, load testing tools, and many internal systems. They have consistently spoken positively about Go's concurrency, ease of deployment, and developer productivity.
* **Evolution, Not Regret:** Cloudflare has certainly diversified its language usage, with a notable shift towards **Rust** in certain critical areas. This is driven by performance, security, and resource efficiency needs, not a "regret" of Go.
    * **Pingora (Rust):** A prime example is Cloudflare's development of **Pingora**, a new HTTP proxy built in Rust to replace parts of their NGINX infrastructure (which was written in C). This move to Rust was largely about:
        * **Memory Safety:** Rust's guarantees against common memory bugs (buffer overflows, use-after-free) which are prevalent in C/C++ (like NGINX). This significantly improves security and stability.
        * **Extreme Performance:** For a core component handling trillions of requests, Rust's "zero-cost abstractions" and fine-grained control allow for even higher performance and lower resource consumption than what's easily achievable in Go (due to Go's GC overhead).
        * **Improved Developer Experience for Systems Programming:** While Rust has a steeper learning curve initially, for systems engineers working on extremely low-level network components, its strictness and powerful type system can lead to more robust and easier-to-reason-about code in the long run.
    * **Go still strong:** Even with Pingora, Cloudflare continues to develop and maintain many services in Go. They view Go as "fast enough" for most of their workloads and appreciate its development speed and operational simplicity.
* **Conclusion for Cloudflare:** Cloudflare embraces a multi-language strategy, choosing the best tool for the job. Go remains a foundational language for them, particularly for services that benefit from its rapid development and concurrency. Rust is increasingly used for systems-level components where maximum performance, memory safety, and fine-grained control are paramount.

In essence, both companies are sophisticated engineering organizations that understand the trade-offs of different programming languages. They don't express "regret" for choosing Go, but rather demonstrate a pragmatic approach to using other languages like Rust for specific problem domains where their strengths (e.g., lack of GC, memory safety) offer significant advantages for critical infrastructure.
