---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Rust 炒作忽略了真实后端问题
translated: true
type: note
---

这篇文章对最近科技公司——尤其是初创公司——声称使用 **Rust** 构建其“backend”的热潮表示强烈怀疑。作者认为这是从众行为，可能由炒作而非真正技术需求驱动。

### 核心论点：大多数 Web Backends 是 IO-Bound，而不是 CPU-Bound

- 在典型的 web/API/data-management backends（CRUD 服务、auth、business logic 层）中，主导瓶颈是 **IO wait time** —— 等待：
  - Network responses（其他服务、external APIs）
  - Database queries
  - Cache lookups
  - File system operations

- 应用本身进行的实际 CPU 计算通常很少。繁重工作（indexing、joins、sorting、aggregation）发生在 database engine 内部。

- 对于此类工作负载，语言的 raw single-threaded speed 或 zero-cost abstractions 的重要性远低于高效的 **concurrency handling**（能够处理数千并发请求而不阻塞）。

- 具有良好 **async/await** 或 lightweight concurrency primitives 的现代语言（Python+asyncio、Go goroutines、JavaScript/Node、Java virtual threads、Kotlin coroutines、C# async/await、Rust+tokio/async-std）都能在 IO-bound 工作上实现非常高的 throughput，前提是代码避免常见反模式。

### 作者的真实世界示例

作者分享了一个个人轶事：

- 他们的团队将糟糕性能归咎于 Python（及其 GIL）。
- 详细 profiling 显示真实问题是：
  - 不必要的 locking
  - 反复通过 network 获取相同数据而不是 caching
  - O(n²) algorithms
  - 其他经典的算法和架构错误

- 在针对性修复后（未更换语言），性能提升 **200×+**，资源使用量大幅下降。

- 结论：**bad engineering** 制造了人为瓶颈；语言被当作替罪羊。

### 主要论点——这是人员/设计问题，而不是语言问题

即使那些工程师切换到 Rust：

- 他们很可能在 Rust 中写出 **同样低效** 的代码（错误的数据结构、过度 cloning、不佳的 async 模式、不必要的 synchronization 等）。
- Rust 能防止某些类别的 bug（memory safety、data races），但 **不会** 防止：
  - Algorithmic inefficiency
  - Bad caching strategy
  - Chatty network patterns
  - Over-complicated business logic
  - Misuse of async（例如，在 async 上下文中进行 blocking calls）

- 真正的高并发设计需要理解 OS 概念（scheduling、polling vs threads、epoll/kqueue/IOCP、cancellation、backpressure），这些通常在 Operating Systems 课程中教授——并非通过学习新语言自动获得。

- Microsoft 的轶事：即使是拥有“30+ 年大规模并发系统经验”的团队，也在 C# 代码中犯下基本的 locking 错误。仅切换语言无法修复根本原因。

### 额外批评：夸大的需求与行业时尚

- 许多公司夸大其规模（“millions of concurrent users”），实际上它们服务的是数百或数千企业客户。
- 他们制造“artificial difficulty”来证明 trendy technology choices 的合理性 → “有困难要上，没有困难制造困难也要上”。
- 这反映了行业更广泛的 perceived decline：专注于 shiny languages/tools 而非 fundamentals（“掌握思想”），这是作者早在 1997 年就听到的教训。

### 平衡的反方观点（帖子中未提及但值得注意）

许多近期来源（2024–2025）显示公司采用 Rust 构建 backends 的真实原因：

- 更低的 memory/CPU 使用 → 在极高规模下实现 meaningful cloud cost savings
- 在 high-throughput 服务中 predictable low-tail latency（p99/p999）
- Memory & thread safety 减少 production incidents
- 在 Axum/Actix 等框架中的优秀性能（频繁位居 Techempower benchmarks 首位）
- 不断增长的 ecosystem 和 big-tech endorsements（AWS、Discord、Cloudflare、Microsoft parts）

对于 **真正 IO-heavy** 的简单 CRUD APIs 和 moderate load，Go、Java、C# 甚至 Python 往往更 pragmatic（更快的 iteration、更大的 talent pool）。Rust 在遇到 CPU spikes、需要 extreme efficiency 或希望在 concurrent code 中获得 maximum safety 时更闪耀。

作者的核心观点对大多数情况仍然有效：炒作和切换语言无法替代扎实的 computer science fundamentals、良好的 architecture，以及 competent profiling/fixing 实际瓶颈。

References:  

- [Why Rust is Winning in Backend Systems: A Startup Must-Know](https://dockyard.com/blog/2025/03/18/why-rust-is-winning-backend-systems-startup-must-know)
- [Why you should use Rust on the backend](https://www.shuttle.dev/blog/2024/07/31/rust-on-the-backend)
- [Rust vs Go: When to use Rust and when to use Go](https://blog.logrocket.com/go-vs-rust-when-use-rust-when-use-go)
- [The 2025 Backend Playbook: Rust vs Java vs Go](https://medium.com/@toyezyadav/the-2025-backend-playbook-rust-1-90-vs-java-25-lts-vs-go-1-25-what-to-choose-and-why-bb74eb9369be)