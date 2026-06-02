---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在 M2 上加速本地 Qwen3.5
translated: true
type: note
---

**是的，`qwen3.5:9b` 在 MacBook Air M2 上（尤其是基础 8GB 或 16GB 配置）仍然会感觉明显较慢，与在线 Grok、Mistral 或类似云服务的近即时流式传输相比——但它通常可用，许多优化措施可以在 2026 年显著缩小差距。**

### MacBook Air M2 上的典型真实世界速度

- 使用 Metal 加速的 Ollama（Apple Silicon 默认）：在 16GB M2 Air 上生成 **~25–45 tokens/second** (t/s)，取决于上下文长度、量化以及提示复杂性。
  - 简短响应感觉很快（一段话 ~2–5 秒）。
  - 较长或复杂推理 → 10–30+ 秒，与云服务的亚秒级启动 + 快速流式传输相比感觉“慢”。
- 在线服务（Grok、Mistral、GPT、Claude）：相当于 80–200+ t/s 的感觉，得益于海量服务器 GPU 集群、优化的流式传输以及无本地热量/功耗限制。
- MacBook Air M2 特点：无风扇设计 → 重负载 1–2 分钟后热节流导致速度下降 20–40%。基础 M2 的 GPU 核心比 Pro/Max 芯片少。

在 2026 年，许多人确实运行本地模型——本地 LLM 使用量已大幅增长（数千万用户定期使用 Ollama/LM Studio/MLX 等工具在个人硬件上），驱动因素包括隐私、零成本、离线访问，以及 Qwen3.5 等模型媲美较旧云前沿模型。它在开发者、研究人员和注重隐私的用户中尤其流行，尽管大多数休闲用户仍偏好云服务以获得原始速度/便利性。

### 如何改善 MacBook Air M2 上的速度

1. **使用更轻量化的量化或更小的模型变体**
   - 坚持默认 Q4_K_M（~6.6GB），但如果可用可试 Q3_K_M 或 Q2_K（更快，质量略低）。
   - 切换到更小的 Qwen3.5 变体：4B 或 2B 模型运行速度快 2–3×（~50–80+ t/s），简单任务几乎无明显质量下降。

2. **优化 Ollama 设置**
   - 限制上下文大小：编辑 `~/.ollama/config` 或使用 `--num_ctx 2048`（或最大 4096）以减少 KV cache 内存/速度影响。
   - 设置更少的线程/并行：`OLLAMA_NUM_PARALLEL=1` 和 `OLLAMA_NUM_THREADS=4–6`（防止 Air 有限核心过载）。
   - 强制 Metal GPU：确保 `OLLAMA_ORIGINS=*` 且 Metal 激活（默认，但确认无 Rosetta）。
   - 更新到最新 Ollama 版本——2026 年发布版有重大 Metal 改进。

3. **减少热节流（无风扇 Air 至关重要）**
   - 关闭低功耗模式，保持通风口畅通，使用硬表面运行。
   - 仅短时爆发——长生成之间暂停。
   - 部分用户禁用 GPU 卸载（`num_gpu: 0`）转为纯 CPU（初始较慢但热量积累少）。

4. **切换到更快的 frontend 或引擎**
   - 试用 **MLX** 框架（Apple 优化）：Qwen3.5-9B 在 M2 上达到 **50–65 t/s**（许多测试中比 Ollama 快）。
   - 使用 LM Studio 或类似 GUI——流式传输 + 更好缓存往往感觉更敏捷。
   - 对于 API 应用（例如 Continue.dev、VS Code），如果流式传输严重滞后则设置 `"stream": false`。

5. **通用提示**
   - 关闭所有其他应用以释放统一内存（推荐 16GB+；8GB 挣扎）。
   - 保持 macOS 和 Ollama 更新以获 Metal/MLX 提升。
   - 对于编码/聊天：如果可用，使用 Qwen3.5-Coder 变体——优化且快速。

通过这些调整，许多 M2 Air 用户报告“足够好”的日常使用（比 2024 年初本地尝试快），尽管云服务在超响应感觉上仍占优。如果速度是首要优先级，云服务仍是王者；对于隐私/离线，本地（带优化）在 2026 年非常可行。

References:

- [Ollama Qwen3.5:9b 模型页面](https://ollama.com/library/qwen3.5:9b)
- [2026 年 Apple Silicon 上最佳本地 LLM 指南](https://apxml.com/posts/best-local-llm-apple-silicon-mac)
- [Reddit 上关于 M2 Air Ollama 性能讨论](https://www.reddit.com/r/ollama/comments/1n7uhkv/hows_your_experience_running_ollama_on_apple)
- [M2 上 MLX 与 Ollama 速度比较](https://x.com/StephanFerraro/status/2028723111386915055)
- [2026 年本地 LLM 采用趋势](https://datareportal.com/reports/digital-2026-one-billion-people-using-ai)
