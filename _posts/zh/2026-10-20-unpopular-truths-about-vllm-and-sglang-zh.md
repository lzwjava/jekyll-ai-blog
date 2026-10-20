---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 关于vLLM和SGLang的鲜为人知的真相
translated: true
type: note
---

**问题：** 关于 vLLM 和 SGLang 有哪些不受欢迎/诚实的事实？

**回答：**

以下是对这两个框架的、来自社区的、诚实的、令人不适的现实剖析。

---

## ⚔️ Benchmark 之争多半是剧场效果

两个团队都公开就 benchmark 数字争论不休——vLLM 发布了令人印象深刻的结果，声称对 SGLang 有优势，SGLang 以完全不同的数字“非常激进地”回应，然后 vLLM 再次更新回答。中立观察者的结论是：performance gap 不足以重要到产生影响，尤其是在较长序列上。

vLLM 和 SGLang 两年来相互超越——本月领先的一方往往在下一个小版本发布时易位。一个 benchmark 只有在版本匹配、flag 匹配并且针对你的实际 request distribution 运行时才可用。

头条数字本质上具有误导性：著名的 SGLang 在 8B 类模型上约 29% 的 throughput 优势随着 model size 和 concurrency 的变化而急剧压缩——在 70B 规模时，它缩小到个位数。

---

## 🔴 vLLM 的不受欢迎的事实

**1. Kubernetes 自动伸缩默认情况下基本是坏的**

即使在最大 throughput 下，vLLM pod 上的 CPU utilization 也保持较低——工作在 GPU 上进行，并且由于 vLLM 为 KV cache 预分配了 GPU memory，所以 GPU memory 保持不变。Kubernetes 用来做出伸缩决策的两个指标在无论负载如何时都是平坦的。一个处于高流量下的 vLLM 部署在 Kubernetes 调度器眼中看起来是空闲的，而 requests 在引擎内部排队，latency 恶化。

**2. PagedAttention 并不能解决所有问题**

经过数小时的连续 requests，memory fragmentation 可能导致 OOM 错误，即使 theoretical memory 应该充足。修复方法通常是重启 server——对于生产环境来说并不理想。一个单一的 128K context request 可能使处理较短 requests 的 server 不稳定。

**3. 多个高严重性安全 CVE**

自 2025 年以来至少有六个高严重性 CVE，通过公共 API 实现远程代码执行、SSRF 和 DoS，包括 CVE-2025–30165 (CVSS 8.0)，通过在 vLLM 的多节点 ZeroMQ 通信中不安全的 pickle 反序列化实现 RCE。

**4. 生产版本携带 bug**

所有大型云推理提供商都使用 vLLM 或 SGLang 的定制版本，并添加了他们自己的 bugfix，因为开箱即用存在 bug。

**5. 硬件支持范围比宣传的要窄**

原生 Windows 支持仅在 2026 年才实现，并且需要 CUDA 13.0 和 RTX 6000 Ada 或更新版本。对于具有 8–12 GB VRAM 的消费级硬件，vLLM 的原生量化针对的是 server GPUs——它的优势只在你不太可能单独达到的 concurrency 下才显现。

---

## 🔴 SGLang 的不受欢迎的事实

**1. RadixAttention 只在 prefix 共享时才神奇**

在没有高 prefix-cache hit rates 的情况下，SGLang 大致是一个更慢的 vLLM，多了一些额外旋钮。具有高度多样化和非重叠 prompts 的 workloads——其中 prefix cache hit rate 下降到约 20% 以下——会看到 RadixAttention 增加开销而没有好处。

在一个受控 benchmark 中，面对 64 个并发的独特提示 requests，vLLM 的中位数 time-to-first-token 是 849ms，而 SGLang 是 3,045ms——当 prefix reuse 不适用时，首次 token 慢三倍以上。

**2. SGLang 使用更多 VRAM，而不是更少**

SGLang 的 KV cache 随着 prefix tree 的扩展而动态增长——需要比同等 vLLM 部署多约 15% 的 VRAM。

**3. 每个实例一个模型——没有 multi-tenancy**

运行多个模型意味着要为单独的 SGLang instances 及其自身的 GPU memory slice 付费。没有适用于更简单部署的轻量级或精简模式。

**4. 硬件覆盖范围落后于 vLLM**

ROCm (AMD) 支持只是部分的，Apple Silicon 缺失，并且截至 2026 年年中，它在大多数配置中仍仅限 CUDA。vLLM 支持超过 200 种 model architectures 以及 TPU、Trainium 和 Gaudi；SGLang 的列表更窄。

---

## 🔴 共同问题：它们改变你的模型的输出

这一点很少被讨论：

保持 model weights、decoding parameters 和 hardware 不变，仅 inference backend 的选择就能在 benchmark 结果中引起显著变化，使报告的性能偏移多达 **16 个百分点**。这在研究验证和生产现实之间创造了一个危险的“deployment gap”，其中 backend 引起的差异不仅会破坏性能声明，还会破坏安全性保证。

---

## 🟡 结论

诚实的答案是两者都没有明确胜出。SGLang 的 RadixAttention 领先在 shared-prefix traffic (RAG, agents, chat history) 上是真实的，当每个 prompt 都是唯一时则趋于零。在真实的饱和负载下，vLLM 在 unique-prompt traffic 上测量出更快的 time-to-first-token。在做出决定之前，用你的**实际生产 workload** 运行两者。

---

**References:**

- [10 Best vLLM Alternatives for Production 2026](https://www.premai.io/blog/10-best-vllm-alternatives-for-llm-inference-in-production-2026/)
- [vLLM in Production: Security Hardening Guide](https://medium.com/@michael.hannecke/vllm-in-production-a-security-hardening-guide-for-enterprise-deployments-56a9c2c213dd)
- [The Silent Hyperparameter — Inference Backend Reproducibility](https://arxiv.org/pdf/2605.19537)
- [vLLM vs SGLang: What Published Data Actually Shows](https://markaicode.com/benchmarks/sglang-production-benchmark-latency/)
- [SGLang vs vLLM Fighting Over Meaningless Numbers (The Weekly Kaitchup)](https://kaitchup.substack.com/p/the-weekly-kaitchup-89)
- [vLLM vs Ollama vs SGLang vs TensorRT-LLM](https://theaiengineer.substack.com/p/vllm-vs-ollama-vs-sglang-vs-tensorrt)
- [vLLM Kubernetes: 7 Proven Production Patterns](https://thegoodshell.com/vllm-kubernetes/)
- [What Is SGLang? 2026 Guide](https://www.digitalocean.com/resources/articles/what-is-sglang)