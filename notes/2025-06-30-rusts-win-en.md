---
audio: false
generated: true
lang: en
layout: post
title: Discord's Rust Performance Boost
translated: false
type: note
---

Discord's adoption of Rust was driven by performance bottlenecks in their Go-based "Read States" service, which tracks user message reads across channels. The switch to Rust delivered significant latency improvements, eliminated garbage collection spikes, and showcased Rust's strengths in memory management and concurrency. Here's a detailed breakdown:

---

### **Why Discord Switched to Rust**

1. **Garbage Collection (GC) Issues in Go**
   - Discord's Go service experienced latency spikes every ~2 minutes due to Go's conservative, non-generational GC, which *had to scan the entire LRU cache* (containing millions of objects) even with minimal garbage production .
   - Tuning Go's GC (e.g., adjusting cache size) either failed to resolve spikes or worsened 99th-percentile latency .

2. **Rust's Memory Management**
   - Rust's ownership model *immediately frees memory* upon eviction from the LRU cache, avoiding GC-induced pauses. This deterministic approach eliminated latency spikes .
   - No runtime GC overhead meant consistent performance under high load (hundreds of thousands of updates/sec) .

3. **Performance Optimization**
   - Even a naive Rust implementation matched Go's performance. Further optimizations (e.g., using `BTreeMap` instead of `HashMap`, reducing memory copies) *lowered CPU usage by 70%* and cut average response times to microseconds .

4. **Ecosystem and Async Support**
   - Discord embraced Rust's nightly async features early (later stabilized), enabling efficient networked services without GC trade-offs .

---

### **Results of the Switch**

- **Latency**: Eliminated 2-minute GC spikes, achieving sub-millisecond response times .
- **Resource Efficiency**: Reduced CPU and memory usage, allowing cache capacity to scale to 8 million read states without performance degradation .
- **Reliability**: Fewer runtime bugs due to Rust's compile-time safety checks .

---

### **Advantages of Rust for Discord**

1. **Performance**
   - Predictable low latency, ideal for real-time services .
   - Fine-grained memory control outperforms GC-dependent languages .

2. **Safety**
   - Ownership model prevents memory leaks, null pointers, and data races .
   - Concurrency safety without manual synchronization .

3. **Modern Tooling**
   - Cargo (package manager) and rich generics reduced boilerplate vs. Go .

4. **Ecosystem Growth**
   - Upgrades (e.g., Tokio async runtime) delivered free performance gains .

---

### **Disadvantages & Challenges**

1. **Learning Curve**
   - Rust's ownership and lifetimes require upfront investment .

2. **Early Async Limitations**
   - Initial reliance on unstable nightly features posed maintenance risks .

3. **Smaller Ecosystem**
   - Fewer libraries compared to Go or C++, though growing rapidly .

---

### **Key Takeaways**

Discord's success with Rust highlights its fit for *latency-sensitive, high-scale services* where GC pauses are unacceptable. While the transition required overcoming Rust's steep learning curve, the payoff included **faster performance, lower resource usage, and fewer runtime errors** . For teams prioritizing long-term maintainability and performance, Rust offers compelling advantages over GC-reliant languages like Go.

For deeper technical insights, refer to Discord's [original blog post](https://discord.com/blog/why-discord-is-switching-from-go-to-rust) .
