---
audio: false
generated: true
image: false
lang: zh
layout: post
title: SGLang 与 vLLM 的区别
translated: true
type: note
---

**问题：** SGLang 和 vLLM 之间有什么区别？

**答案：**

两者都是高性能的 LLM 推理引擎，但它们有着不同的设计理念和优化目标。

---

## 核心哲学

| | **vLLM** | **SGLang** |
|---|---|---|
| 来源 | 加州大学伯克利分校，2023 年 | 斯坦福大学，2024 年 |
| 主要创新 | PagedAttention（KV 缓存管理） | RadixAttention（前缀重用） |
| 设计目标 | 通过内存效率最大化吞吐量 | 通过计算重用最大化吞吐量 |
| 主要抽象 | 服务引擎 | 结构化生成语言 + 引擎 |

---

## 关键技术差异

### 1. KV 缓存管理

**vLLM — PagedAttention：**
- 将 KV 缓存拆分为固定大小的页面（类似于虚拟内存）
- 消除 KV 缓存碎片化
- 允许在并行序列之间共享页面（束搜索、推测解码）

**SGLang — RadixAttention：**
- 将 KV 缓存组织为**基数树**（基于 token 序列的字典树）
- 在共享公共前缀的请求之间自动重用 KV 缓存
- 关键优势：多轮对话、带有共享系统提示的 RAG、少样本提示——所有这些都免费获得前缀重用

```
前缀：[系统提示 tokens]
请求 A：[系统提示] + [用户查询 A]
请求 B：[系统提示] + [用户查询 B]
                ↑
        SGLang 计算一次，在 A 和 B 之间重用
```

### 2. 结构化输出 / 约束解码

SGLang 最初是围绕**结构化生成**构建的——它有一个原生的 DSL：

```python
# SGLang 原生 DSL（原始 API）
@sgl.function
def multi_turn_qa(s, question):
    s += sgl.system("你很乐于助人")
    s += sgl.user(question)
    s += sgl.assistant(sgl.gen("answer", max_tokens=256))
```

vLLM 后来通过 `guided_decoding`（基于 outlines/lm-format-enforcer 后端）增加了结构化输出。SGLang 的集成更紧密，因为引擎从一开始就是围绕此设计的。

### 3. 连续批处理与调度

两者都支持连续批处理，但：

- vLLM 使用**分块预填充** + 带重新计算或交换的抢占
- SGLang 使用**带 RadixAttention 的分块预填充**——预填充块落入基数树中，因此后续请求能立即受益

### 4. 多模态与架构支持

截至 2025 年中期：
- **vLLM** 拥有更广泛的模型支持（更多 HuggingFace 模型开箱即用）
- **SGLang** 在受支持的模型（LLaMA、Mistral、Qwen、DeepSeek）上通常更快，并且对 **DeepSeek MLA（多头潜在注意力）** 有非常强大的支持——鉴于你使用 DeepSeek，与你的工作相关

### 5. MoE / DeepSeek 支持

SGLang 特别针对 **DeepSeek V3/R1** MoE 模型进行了优化：
- GPU 间的专家并行
- MLA（潜在 KV 压缩）——DeepSeek 的变体，通过低秩投影压缩 KV 缓存
- 为 AMD 和 NVIDIA 调优的 FP8 量化路径

vLLM 也支持 DeepSeek，但 SGLang 的团队在这方面行动更快。

---

## 基准测试现实（近似值，随工作负载变化）

| 指标 | vLLM | SGLang |
|---|---|---|
| 吞吐量（共享前缀） | 基线 | 通过 RadixAttention 提升 +20–50% |
| 吞吐量（无共享前缀） | ~相似 | ~相似 |
| TTFT（首 token 生成时间） | 良好 | 通常通过前缀重用更好 |
| 模型覆盖范围 | 更广 | 更窄但正在增长 |
| 部署简便性 | 成熟、稳定 | 略具实验性 |

---

## 何时使用哪种

**使用 SGLang 的情况：**
- 你有很长的共享前缀（系统提示、RAG 上下文、少样本示例）
- 运行 DeepSeek V3/R1/MLA 模型
- 需要紧密的结构化输出 / 约束生成
- 在支持的架构上追求最大吞吐量

**使用 vLLM 的情况：**
- 你需要最大的模型兼容性
- 运行多样化的工作负载，没有主导的共享前缀
- 你想要经过更多实战考验的生产路径（更多运营商使用它）
- 与现有工具集成（Ray Serve、KServe 等）

---

## 快速入门对比

```bash
# vLLM
pip install vllm
python -m vllm.entrypoints.openai.api_server \
  --model meta-llama/Llama-3-8B-Instruct \
  --tensor-parallel-size 1

# SGLang
pip install sglang[all]
python -m sglang.launch_server \
  --model-path meta-llama/Llama-3-8B-Instruct \
  --tp 1
```

两者都暴露兼容 OpenAI 的 `/v1/chat/completions` 端点——对于大多数用例来说可以互换使用。

---

**针对你工作负载的总结：** 鉴于你运行 DeepSeek V3/V4 并关心大规模吞吐量，**SGLang 值得认真进行基准测试**——当你的提示共享结构时（在 Agent 流水线或多轮对话中确实如此），RadixAttention 的优势是实实在在的。如果你需要广泛的兼容性或正在服务多种模型，vLLM 是更安全的生产选择。

## 参考资料

- [SGLang 论文：结构化语言模型程序的高效执行](https://arxiv.org/abs/2312.07104)
- [vLLM：使用 PagedAttention 实现简单、快速、廉价的 LLM 服务](https://arxiv.org/abs/2309.06180)
- [SGLang GitHub](https://github.com/sgl-project/sglang)
- [vLLM GitHub](https://github.com/vllm-project/vllm)
- [SGLang DeepSeek 支持说明](https://github.com/sgl-project/sglang/blob/main/docs/references/deepseek.md)