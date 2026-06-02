---
audio: false
generated: true
lang: en
layout: post
title: Rust's Impact on Cloudflare
translated: false
type: note
---

Cloudflare's adoption of Rust has been transformative, driven by its unique blend of performance, safety, and scalability. Here’s a detailed breakdown of why Cloudflare chose Rust and the tangible results it has delivered:

---

### **Why Cloudflare Uses Rust**
1. **Memory Safety Without Compromising Performance**
   - Rust’s ownership model eliminates entire classes of vulnerabilities (e.g., buffer overflows, use-after-free errors) that plague C/C++ code, which was critical for Cloudflare’s security-first infrastructure .
   - Unlike garbage-collected languages, Rust achieves this without runtime overhead, making it ideal for high-performance systems like proxies and edge computing .

2. **Concurrency and Scalability**
   - Rust’s async runtime (Tokio) enables efficient handling of millions of concurrent connections, outperforming NGINX’s thread-per-request model. For example, Pingora, Cloudflare’s Rust-based proxy, processes **35M+ requests per second** with lower CPU/memory usage .
   - Async support in Workers (via `wasm-bindgen-futures`) allows Rust-based Workers to handle I/O-bound tasks seamlessly .

3. **Performance Gains**
   - Cloudflare’s Rust-powered QUIC/HTTP/3 stack is **30% faster** than its C++ predecessor, with **35% lower memory usage** and **50% higher throughput** on the same hardware .
   - Micro-optimizations in Rust (e.g., reducing per-request latency by microseconds) save thousands in compute costs at Cloudflare’s scale .

4. **Developer Productivity**
   - Rust’s strong type system and modern tooling (e.g., Cargo) simplify maintenance and reduce bugs. For instance, Oxy, Cloudflare’s proxy framework, allows feature-rich applications to be built with **<200 lines of code** .
   - Workers’ Rust SDK (`workers-rs`) provides ergonomic APIs for KV, Durable Objects, and AI, enabling rapid development .

5. **Ecosystem and Future-Proofing**
   - Rust’s growing adoption (e.g., AWS Lambda, Discord) aligns with Cloudflare’s long-term vision. Open-sourcing projects like Pingora and Oxy fosters community collaboration .

---

### **Results of Using Rust**
- **Pingora**: Replaced NGINX, handling trillions of monthly requests with **lower latency** and **stronger DDoS resilience** .
- **Workers**: Rust support enables compute-heavy tasks (e.g., AI inference) with near-native speed, attracting high-profile clients like fintech and delivery platforms .
- **Reliability**: Rust’s safety features reduced crashes in critical services like QUIC and TLS (e.g., BoringSSL integration in Oxy) .
- **Cost Savings**: Optimizations in Pingora saved **500+ CPUs** globally, translating to significant operational savings .

---

### **Challenges and Mitigations**
- **Learning Curve**: Rust’s complexity required upfront training, but Cloudflare mitigated this with internal libraries (e.g., `workers-rs`) and templates .
- **Wasm Limitations**: Early Workers Rust support had size constraints, but tools like `wasm-opt` and `worker-build` now optimize binaries effectively .

---

### **Future Directions**
Cloudflare continues to expand Rust’s role, including:
- **Containers**: Rust-based Durable Objects power new container orchestration (launching June 2025) .
- **AI**: Workers AI leverages Rust for low-latency model inference .

In summary, Rust has become a cornerstone of Cloudflare’s infrastructure, delivering **security, performance, and scalability** while reducing costs. Its adoption signals a broader industry shift toward memory-safe languages for critical systems .
