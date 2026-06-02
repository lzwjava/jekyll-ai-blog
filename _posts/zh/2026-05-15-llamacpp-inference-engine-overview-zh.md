---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Llama.cpp 推理引擎概述
translated: true
type: note
---

我受够了。这是图片。

## 这段代码是什么

**llama.cpp** 是一个用 C/C++ 编写的生产级 LLM **推理引擎**。它加载量化后的 GGUF 模型权重，并在 CPU/GPU（CUDA、Metal、Vulkan、HIP、SYCL、WebGPU 等）上高效运行，无需 Python 运行时。它是 Ollama、LM Studio、llamafile 以及许多其他工具背后的参考实现。

它**不是**训练框架。无法进行反向传播。它是 HuggingFace `transformers` 在服务端的 C++ 等价物，底层还包含一个张量库。

代码分层清晰：

| 层                | 说明                                                                                   | 文件                                     |
| ----------------- | -------------------------------------------------------------------------------------- | ---------------------------------------- |
| `ggml/`           | 张量库：算子 + 多后端执行器（CPU/CUDA/Metal/…）                                       | `ggml/src/ggml*.{c,cpp}`                 |
| `src/`            | “Transformer 引擎”：模型加载器、KV 缓存、图构造器、采样器、分词器                      | `src/llama-*.{cpp,h}`                    |
| `src/models/`     | 129 个按架构划分的文件，定义每个模型的前向计算图                                       | `gpt2.cpp`、`llama.cpp`、`qwen3.cpp`、… |
| `tools/`          | 可执行程序：`cli`、`server`、`quantize`、`perplexity`、`bench`                        | `tools/cli/cli.cpp`                      |
| `include/llama.h` | 公开 C API（约 1570 行）                                                               |                                           |

## 与 nanoGPT 对比

nanoGPT 是 **353 行、一个文件、训练 + 推理、PyTorch、仅支持 GPT-2。** llama.cpp 仅核心代码就有约 2 万行，仅支持推理，支持约 130 种架构、约 10 种后端和约 20 种量化格式。

有趣的对比在于它们**共享**的东西。看 nanoGPT 的 `Block.forward`（`/mnt/data/nanoGPT/model.py:116`）：

```python
x = x + self.attn(self.ln_1(x))
x = x + self.mlp(self.ln_2(x))
```

以及 llama.cpp 中 GPT-2 的图（`src/models/gpt2.cpp:82-124`）——相同的结构，只是用 ggml 张量运算编写：

```cpp
cur = build_norm(inpL, attn_norm, attn_norm_b, LLM_NORM, il);          // ln_1
auto [Q,K,V] = build_qkv(...);                                          // c_attn 拆分
cur = build_attn(inp_attn, wo, wo_b, ..., Q, K, V, ..., 1/sqrt(d), il);// attn + c_proj
ffn_inp = ggml_add(ctx0, cur, inpL);                                    // 残差连接
cur = build_norm(ffn_inp, ffn_norm, ffn_norm_b, LLM_NORM, il);          // ln_2
cur = build_ffn(cur, ffn_up, ffn_up_b, ..., ffn_down, ..., LLM_FFN_GELU, ...); // MLP
cur = ggml_add(ctx0, cur, ffn_inp);                                     // 残差连接
```

**相同的算法。** GPT-2 用 147 行，而 nanoGPT 整个文件 353 行——llama.cpp 更短，因为分词器/采样器/KV 缓存放在其他地方，并且带有偏置的 LayerNorm、学习得到的位置嵌入、绑定的 lm_head 都被参数化到 `build_norm` / `build_inp_pos` / 加载器中。

## llama.cpp 中 Llama 与 nanoGPT 中 GPT-2 的关键区别（`src/models/llama.cpp`）

这里也能看出“现代”模型与 GPT-2 的不同之处：

| GPT-2（nanoGPT）                     | Llama（llama.cpp）                                                              |
| ------------------------------------ | ------------------------------------------------------------------------------- |
| `LayerNorm`（可选偏置）              | `RMSNorm`，无偏置                                                              |
| 学习得到的位置嵌入（`wpe`）          | **RoPE**（旋转位置编码，作用于 attention 内部的 Q 和 K）                       |
| `n_head_kv == n_head`（多头注意力）  | **GQA**：`n_head_kv` 可以更小（分组查询注意力）                                |
| MLP：`up → GELU → down`（顺序）      | MLP：`SiLU(gate) * up → down`（**SwiGLU**，并行）                              |
| 单个稠密 MLP                         | 可选 **MoE**：门控选择 N 个专家中的 top-k（`build_moe_ffn`）                   |
| `c_attn` 通过一次矩阵乘法生成 Q、K、V | Q、K、V 通过一次或分开的矩阵乘法生成，然后应用 RoPE 旋转                        |

你可以看到这四种（RMSNorm、RoPE、GQA、SwiGLU）都出现在 `src/models/llama.cpp:130-217` 中——这基本上就是“2019 年的 GPT-2”与“2024 年的 Llama-3”之间的区别。

## 核心推理循环逻辑

nanoGPT 在 `generate()` 中（model.py:328）实现这一点——纯 Python，每个 token 都重新计算整个前向传播。llama.cpp 的等价逻辑分散在以下部分：

1. **模型加载**（`llama-model-loader.cpp` → `src/models/<arch>.cpp::load_arch_tensors`）——mmap GGUF，为每层注册张量。
2. **图构造**（`src/models/<arch>.cpp::graph` 构造函数）——每批次一次，构建 ggml 计算 DAG。这相当于“model.py 的前向”，但它构造的是图而非直接运行算子。
3. **后端执行**（`ggml-backend.cpp`）——将 DAG 调度到 CPU/CUDA/Metal 内核上。
4. **KV 缓存**（`llama-kv-cache.cpp`，2502 行）——*相比 nanoGPT 的关键加速*。nanoGPT 每 token 重新计算整个前缀的 K、V（每一步 O(T²) 工作）。llama.cpp 为每层存储 K、V，只计算新 token 的 K、V，并与缓存的过去进行注意力计算。这就是生产引擎存在的全部原因。
5. **采样器**（`llama-sampler.cpp`）——与 nanoGPT 中 `temperature / top_k / multinomial` 块（model.py:339-348）概念相同，但作为可链式流水线：温度 → top-k → top-p → min-p → typical → mirostat → grammar → softmax → 采样。每个都是带有 `apply()` 的小型结构体。
6. **Token 循环**（`tools/cli/cli.cpp`）——输入提示批次 → 解码 → 采样 → 追加 → 解码 1 个 token → 重复。与 nanoGPT 的 `for _ in range(max_new_tokens)` 循环形状相同，只是包裹了批处理、流式输出和聊天模板。

## 总结

nanoGPT 教你数学是什么。llama.cpp 是当你真正需要它在别人笔记本上快速运行时交付的东西：底层是相同的 transformer 数学，但具有 (a) 可移植的张量 IR（ggml）代替 PyTorch，(b) KV 缓存使生成复杂度为 O(T) 而非 O(T²)，(c) 整数量化以将大模型装入小内存，(d) 每个架构一个文件，因此添加新模型主要是使用共享的 `build_norm`、`build_qkv`、`build_attn`、`build_ffn` 原语编写其前向图。
