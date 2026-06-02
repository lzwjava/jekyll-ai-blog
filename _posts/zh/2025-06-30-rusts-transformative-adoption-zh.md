---
audio: false
generated: true
lang: zh
layout: post
title: Rust对Cloudflare的影响
translated: true
type: note
---

Cloudflare 对 Rust 的采用具有变革性意义，这得益于其在性能、安全性和可扩展性方面的独特优势。以下是 Cloudflare 选择 Rust 及其带来具体成果的详细解析：

---

### **Cloudflare 使用 Rust 的原因**
1. **内存安全性与性能兼得**
   - Rust 的所有权模型消除了 C/C++ 代码中常见的一系列漏洞（如缓冲区溢出、释放后使用错误），这对 Cloudflare 安全至上的基础设施至关重要。
   - 与垃圾回收语言不同，Rust 在实现这一目标的同时无需运行时开销，使其成为代理和边缘计算等高性能系统的理想选择。

2. **并发与可扩展性**
   - Rust 的异步运行时（Tokio）能够高效处理数百万个并发连接，性能优于 NGINX 的每请求线程模型。例如，Cloudflare 基于 Rust 的代理 Pingora 每秒处理 **超过 3500 万次请求**，且 CPU/内存使用率更低。
   - Workers 中的异步支持（通过 `wasm-bindgen-futures`）使基于 Rust 的 Worker 能够无缝处理 I/O 密集型任务。

3. **性能提升**
   - Cloudflare 基于 Rust 的 QUIC/HTTP/3 协议栈比其 C++ 前身 **快 30%**，在相同硬件上实现 **内存使用量降低 35%** 和 **吞吐量提高 50%**。
   - Rust 的微优化（例如将每个请求的延迟减少微秒级）在 Cloudflare 的规模下节省了数千美元的计算成本。

4. **开发效率**
   - Rust 强大的类型系统和现代工具链（如 Cargo）简化了维护工作并减少了错误。例如，Cloudflare 的代理框架 Oxy 允许用 **少于 200 行代码** 构建功能丰富的应用程序。
   - Workers 的 Rust SDK（`workers-rs`）为 KV、Durable Objects 和 AI 提供了符合人体工学的 API，支持快速开发。

5. **生态系统与未来适应性**
   - Rust 日益增长的应用（例如 AWS Lambda、Discord）与 Cloudflare 的长期愿景相符。开源 Pingora 和 Oxy 等项目促进了社区协作。

---

### **使用 Rust 的成果**
- **Pingora**：取代了 NGINX，每月处理数万亿次请求，实现 **更低延迟** 和 **更强的 DDoS 抵御能力**。
- **Workers**：Rust 支持使计算密集型任务（如 AI 推理）能够以接近原生的速度运行，吸引了金融科技和配送平台等知名客户。
- **可靠性**：Rust 的安全特性减少了 QUIC 和 TLS 等关键服务中的崩溃（例如 Oxy 中的 BoringSSL 集成）。
- **成本节约**：Pingora 的优化在全球节省了 **超过 500 个 CPU**，转化为显著运营成本降低。

---

### **挑战与应对措施**
- **学习曲线**：Rust 的复杂性需要前期培训，但 Cloudflare 通过内部库（如 `workers-rs`）和模板缓解了这一问题。
- **Wasm 限制**：早期的 Workers Rust 支持存在体积限制，但如今通过 `wasm-opt` 和 `worker-build` 等工具可有效优化二进制文件。

---

### **未来方向**
Cloudflare 继续扩展 Rust 的应用范围，包括：
- **容器**：基于 Rust 的 Durable Objects 为新的容器编排提供支持（预计 2025 年 6 月推出）。
- **AI**：Workers AI 利用 Rust 实现低延迟模型推理。

总之，Rust 已成为 Cloudflare 基础设施的基石，在降低成本的同时提供了 **安全性、性能和可扩展性**。它的采用标志着行业关键系统向内存安全语言更广泛转型的趋势。
