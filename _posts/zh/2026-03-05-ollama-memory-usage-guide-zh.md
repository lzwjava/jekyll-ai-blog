---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Ollama 内存使用详解
translated: true
type: note
---

**您看到的 159 MB 数字并不是模型的实际内存使用量——它很可能只是主 Ollama 服务器进程本身的驻留内存 (RES)，或者是从 Activity Monitor / `top` / `htop` 等工具中获取的误导性部分读数，这些工具没有考虑到现代 LLM 运行器如何处理内存。**

在 Apple Silicon Macs (M2/M3) 上，Ollama 非常高效地使用 **memory-mapped files** 和 **unified memory**。这意味着：

- ~6.6 GB 量化模型文件 (Q4_K_M for qwen3.5:9b) 直接从磁盘映射到内存中。
- 操作系统将其中大部分视为 **file-backed memory** (cached / inactive / compressed)，因此它通常不会完全显示在“App Memory”或简单的进程 RES 列中。
- 当您实际发送提示并开始推理时，真实使用量会激增——通常达到 **~8–12 GB 总系统内存** (包括 KV cache、开销和上下文)。
- Activity Monitor 等工具最初经常低报此值，因为内存是“共享”/“压缩”的，或者显示在“Cached Files”下而不是直接归属 Ollama 进程。
- Ollama 服务器进程在空闲或仅保持 API 开放时保持较小 (~100–300 MB)；繁重工作发生在 GPU 加速的 Metal buffers 或共享内存池中，macOS 并不总是清楚地将它们归属到一个进程。

### qwen3.5:9b 在 Mac M2/M3 上的典型真实内存使用量 (2026 年 3 月)

- 磁盘上的模型文件：**6.6 GB**
- 加载 + 短上下文推理：**~8–10 GB** unified memory 使用 (大部分通过 Metal 在 GPU 侧)
- 更长上下文 (例如 8k–16k tokens)：**10–14 GB**，取决于确切配置
- 在 16 GB Mac 上：运行舒适，但留给其他应用的余量较少
- 在 24 GB+ Mac 上：感觉非常流畅，通常 40–70+ tokens/second

### 为什么最初看起来这么小

- 在发送任何提示之前：模型可能尚未完全加载 (Ollama 会延迟加载或在不活动后卸载以节省资源)。
- `ps`、`top` 或 Activity Monitor 的“Memory”选项卡针对 `ollama` 进程通常只显示 **~150–300 MB**，因为主体部分在：
  - Metal GPU buffers (不总是按进程列出)
  - mmap'd 模型权重 (计入文件缓存)
  - 压缩 / 交换内存
- 在开始推理后运行 `ollama ps`——它显示更准确的“SIZE”列 (对于此模型通常 8–12 GB)。
- 使用 Activity Monitor → Memory 选项卡 → 查看“Memory Used”总系统增加，或启用“GPU”视图查看 Metal 使用量激增。

简而言之：**159 MB 对于空闲服务器进程是正常的**。模型在活动时实际使用数 GB——这是 Apple Silicon 上预期的且高效的。如果您看到性能差或错误，请检查总系统内存压力，而不是仅看进程大小。

References:

- [Ollama qwen3.5:9b 模型页面 (6.6 GB Q4_K_M)](https://ollama.com/library/qwen3.5:9b)
- [Stack Overflow: 为什么 Ollama 不使用更多 RAM？(memory mapping 解释)](https://stackoverflow.com/questions/78068285/why-doesnt-ollama-use-more-ram)
- [GitHub Ollama issues 关于内存报告 (file cache & under-reporting)](https://github.com/ollama/ollama/issues/2496)
- [Apple Silicon unified memory 行为的本地 LLM 指南](https://localllm.in/blog/ollama-vram-requirements-for-local-llms)

问题：为什么 `ollama run qwen3.5:9b` 只显示 159 MB 内存使用量，这看起来很小？

答案：
