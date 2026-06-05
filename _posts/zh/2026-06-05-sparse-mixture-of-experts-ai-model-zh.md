---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 稀疏混合专家人工智能模型
translated: true
type: note
---

**问题：** Qwen3.6-35B-A3B 中的 "A3B" 是什么意思？"A" 代表 "activation"（激活）吗？

**回答：**

是的。"A3B" 表示每次前向传播仅激活 30 亿参数，尽管完整的权重文件包含 350 亿参数——这是一种稀疏混合专家（Mixture-of-Experts）设计。

**架构解析：**

Qwen3.6-35B-A3B 采用 Gated DeltaNet MoE 架构，包含 256 个专家，每个 token 路由到 8 个专家加上 1 个共享专家。路由器网络学习为每个 token 激活哪些专家子网络；其余 247 个专家保持静默。稀疏比约为 12:1（总 350 亿中激活 30 亿）——在所有公开发布的模型中属于最为激进的之一。

**这对你的意义：**

该模型仅需 30 亿激活参数即可提供前沿级别的编程和智能体（agent）性能，使其在部署时极具吸引力，因为它在降低推理成本的同时，在编程和工具密集型任务上表现得像一个更大的模型。在 SWE-bench Verified 上，Qwen3.6-35B-A3B 得分 73.4%，而 Gemma 4-31B（一个稠密 31B 模型）得分为 52.0%。

它支持 262K token 的本地上下文窗口（通过 YaRN 可扩展至 1M），并包含集成思考模式，在多轮对话中保留推理轨迹。可通过阿里云 API 以 `qwen3.6-flash` 使用，或在 HuggingFace 上以 Apache 2.0 协议开源。

考虑到你的 MI300X 配置以及对 MoE 架构的兴趣——这值得测试。其稀疏模式和门控注意力混合（Gated DeltaNet 混合线性 + 门控注意力）更接近 DeepSeek v4 风格架构，而非典型的稠密 Transformer。

---

**参考文献：**

- [Qwen3.6-35B-A3B：超小活跃参数的开源模型](https://medium.com/data-science-in-your-pocket/qwen3-6-35b-a3b-the-tiny-active-open-model-that-thinks-codes-and-agents-like-a-much-bigger-one-486d535e372e)
- [Qwen3.6-35B-A3B：像巨人一样编程的小模型](https://www.labellerr.com/blog/qwen3-6-35b-a3b-open-source-ai-model/)
- [vLLM 配方 - Qwen3.6-35B-A3B](https://recipes.vllm.ai/Qwen/Qwen3.6-35B-A3B)