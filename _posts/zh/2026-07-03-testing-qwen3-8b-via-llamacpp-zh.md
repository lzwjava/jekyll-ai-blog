---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 通过 llama.cpp 测试 Qwen3-8B
translated: true
type: note
---

**问题：** 根据你对 llama.cpp（相对于 LM Studio/Ollama）的推荐——我应该下载哪个模型来测试它，然后日常使用？

**答案：**

分两步回答：先用一个小模型验证构建是否成功，然后根据你的硬件选择真正的日常驱动模型。

## 第一步 —— 快速测试（30 秒，无需手动下载）

llama.cpp 现在可以通过 `-hf` 标志直接从 Hugging Face 拉取 GGUF 模型——`llama-cli -hf ggml-org/gemma-3-1b-it-GGUF` 可以直接运行 Hugging Face 上的模型，`llama-server -hf ggml-org/gemma-3-1b-it-GGUF` 则启动一个兼容 OpenAI 的 API 服务器：

```bash
# Mac Air M2（Metal 自动启用）
brew install llama.cpp
llama-cli -hf ggml-org/gemma-3-1b-it-GGUF

# 或者在 4070 机器上从源码构建（更好——反正你也会读代码）
git clone https://github.com/ggml-org/llama.cpp && cd llama.cpp
cmake -B build -DGGML_CUDA=ON && cmake --build build -j
./build/bin/llama-cli -hf ggml-org/gemma-3-1b-it-GGUF
```

如果能正常输出 token，说明整个技术栈工作正常。Gemma-3-1B 是一次性模型——测试完后可以删除。

## 第二步 —— 实际模型：Qwen3-8B Q4_K_M

对于你的两台机器，这是 2026 年的共识选择。Qwen3 8B 是受限硬件上通用场景的推荐模型——在 Q4_K_M 量化下占用约 5.5 GB 显存，为上下文留出空间，并在编程和通用任务上提供有竞争力的质量。5.5 GB 完全可以容纳在你的 4070 的 12 GB 显存中（支持完全 GPU 卸载加长上下文），也能装进 M2 Air 的 16 GB 统一内存中（在 Apple Silicon 上，全部 RAM 池都可供 GPU 使用，所以显存区别不适用——但需为 macOS 留出约 8 GB，因此 8B Q4 是 Air 的实际上限）。

```bash
llama-server -hf Qwen/Qwen3-8B-GGUF:Q4_K_M \
  --port 8080 -ngl 99 -c 16384 --flash-attn

# 然后通过任何 OpenAI 客户端进行调用
curl localhost:8080/v1/chat/completions -d '{
  "messages": [{"role":"user","content":"用三句话解释分页 KV 缓存"}]
}'
```

Qwen3 还具备混合思维模式（提示中的 `/think` / `/no_think`），由于你正在研究采样和推理 token 行为，这值得一试。

## 针对你硬件的尺寸建议

| 机器 | 最佳选择 | 上限 | 备注 |
|---|---|---|---|
| M2 Air 16 GB | Qwen3-4B Q4 | Qwen3-8B Q4（约 5.5 GB） | 注意内存交换；同时试试 MLX——在 Apple Silicon 上 MLX 比 llama.cpp 快 20–50% |
| RTX 4070 12 GB | Qwen3-8B Q4 完全卸载 | Qwen3-14B Q4（约 9 GB，上下文受限） | 这是你的 llama-server 主机 |
| 纯 CPU 备选 | Phi-4-mini 3.8B | — | Q4_K_M 下约 3.5 GB，8 GB 机器的唯一可行选择 |

一个值得牢记的规则：在相同内存预算下，更大的 Q4 模型通常胜过更小的 Q8 模型——所以优先选择 8B-Q4 而非 4B-Q8。

## 为什么不选其他模型

- **DeepSeek-R1 蒸馏模型** —— 适合推理密集型任务，但在严格的 XML 工具调用模式（在智能体框架中）方面可能不如 Qwen 稳定。由于你构建 CLI 智能体（iclaw），工具调用的可靠性比原始推理基准更重要。以后可以下载 `deepseek-r1-distill-qwen-14b` 作为第二个模型，而不是第一个。
- **Gemma 4 E4B/26B-A4B** —— 有趣的 MoE 架构（E4B 仅需 3 GB 显存即可运行，MoE 设置通过每 token 仅激活部分模型来保持内存可控），值得为你的 DeepSeek-MoE 学习路线进行学习，但 Qwen3 在代码任务上每字节性能更强。
- **任何 30B 以上的模型** —— 在两台机器上都无法达到可用质量。当你想进行大模型实验时，那是 MI300X 实例的任务（而且那里你会使用 vLLM，而非 llama.cpp——如我们之前讨论的，这是不同的层面）。

与你学习路线直接相关的是：一旦 Qwen3-8B 在 `llama-server` 下运行，将其与 4070 上的 nano-vllm 下相同模型的行为进行对比。相同的权重，两个推理引擎——这是理解 PagedAttention 与 GGUF 风格 KV 缓存之间区别的最快方式。

**参考资料：**

- [llama.cpp (GitHub)](https://github.com/ggml-org/llama.cpp)
- [2026 年最佳本地 LLM 模型推荐 (daily.dev)](https://daily.dev/blog/best-local-llm-models-run/)
- [本地 LLM 正在变得更简单：2026 完整指南 (SitePoint)](https://www.sitepoint.com/local-llms-are-getting-easier-the-complete-guide-2026/)
- [2026 年最佳本地 LLM 模型——开发者对比 (SitePoint)](https://www.sitepoint.com/best-local-llm-models-2026/)