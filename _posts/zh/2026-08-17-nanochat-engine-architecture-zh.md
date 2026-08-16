---
audio: false
generated: true
image: false
lang: zh
layout: post
title: nanochat引擎架构
translated: true
type: note
---

以下是 `nanochat/engine.py` 的工作原理——它是 nanochat GPT 模型的**高效批量推理引擎**。它是一个 token 级引擎：输入 token ID 序列，输出 token ID 序列流，对文本本身一无所知。

## 三个组成部分

### 1. 计算器工具（`use_calculator`）

一个小的、沙箱化的“工具使用”钩子。模型可以在 `<|python_start|>` / `<|python_end|>` 特殊 token 之间输出一个 Python 表达式，引擎会计算该表达式并将结果注入到 `<|output_start|>` / `<|output_end|>` token 之间。安全性通过以下方式保证：
- 使用 `{"__builtins__": {}}` 的 `eval` 以及 **3 秒 SIGALRM 超时**
- 字符白名单（仅限数学字符，或用于字符串操作的字母/引号/点）
- 危险模式黑名单（`__`、`import`、`exec`、`open`、`getattr` 等）
- 仅允许 `.count()` 字符串方法，并且在数学模式下禁止 `**`（幂运算）

### 2. `KVCache`

一个专为 **Flash Attention 3 的 `flash_attn_with_kvcache` API** 构建的 KV 缓存。与经典 FA2 布局的主要区别：
- 张量形状为 `(n_layers, B, T, H, D)` —— FA3 的原生布局，**无需转置**
- FA3 在注意力计算期间会**原地**更新缓存，因此引擎只需传入视图
- 位置通过 `cache_seqlens` int32 张量按批次元素分别跟踪（而不是 Python 计数器）
- 同时存储 `prev_embedding` —— 模型 **“smear”** 技巧所需的上一 token 归一化嵌入（将上一 token 的嵌入混入当前位置，以获取廉价的 bigram 信息）
- `prefill(other)` 将已完成的 batch-1 缓存复制到更大的批次缓存中（并将 smear 嵌入从 batch 1 扩展到 N）

### 3. `Engine.generate` —— 主循环（生成器）

这是巧妙之处。策略：**先在 batch 1 上 prefill，然后克隆 KV 缓存以并行运行多个样本**。

1. 对 prompt 进行 **batch-1 prefill** → 对所有 prompt token 执行一次前向传播。
2. 将 KV 缓存**克隆**为 `num_samples` 大小的解码缓存（通过 `prefill()`），释放 prefill 缓存。
3. 逐行 **`RowState`** 跟踪：当前 token 序列、*强制* token 的 deque、是否在 Python 代码块内部、累积的表达式 token 以及完成状态。

每步循环：
- 每行采样一个 token（`sample_next_token`：若 `temperature=0` 则用 argmax，否则用 top-k + softmax + 带种子 RNG 的 `multinomial`）
- 但每行也可以改为从自己的 deque **强制**推出 token（例如注入的计算器输出），因此一个批次中可以包含处于不同“逻辑”位置的行——token 列是采样 token 和强制 token 的混合，返回的 `token_masks` 记录哪些是哪种（1 = 采样，0 = 强制/prompt）
- 运行**工具状态机**：遇到 `<|python_start|>` 开始累积表达式 token；遇到 `<|python_end|>` 通过计算器求值，并将 `<|output_start|>` + 结果 + `<|output_end|>` 推入强制 deque
- 遇到 `<|assistant_end|>` 或 `<|bos|>` 时完成该行
- 在下次前向传播之前 `yield` `(token_column, token_masks)` —— 使调用方可以增量流式/解码
- 下一次前向是**每行一个 token**（形状 `(B, 1)`），配合 KV 缓存，这是快速解码路径

### 4. `Engine.generate_batch`

一个非流式包装器，只负责耗尽生成器，将 token 追加到每行结果列表中（排除终止 token），并返回 `(results, masks)`。用于 RL rollout 采样（`scripts/chat_rl.py`）和评估（`scripts/base_eval.py`），其中 masks 标记哪些 token 是模型采样的，哪些是 prompt/工具强制的——这对 RL 损失掩码很重要。

## 关键集成点

- **模型侧**（`nanochat/gpt.py`）：每个注意力层调用 `kv_cache.get_layer_cache(layer_idx)` 并将视图交给 `flash_attn_with_kvcache`；最后一层推进 `cache_seqlens`。模型读写 `kv_cache.prev_embedding` 以实现 smear 残差，并通过 `kv_cache.get_pos()` 偏移旋转嵌入。
- `__main__` 块是一个自测，验证 `Engine.generate` 与朴素的 `model.generate` 一致（供评估脚本使用）。

## 整体概览

引擎的主要优化是用一次性的 KV 缓存复制来换取**批量并行采样**——prefill 一次，然后同时生成 N 个共享同一 prompt 的样本/rollout，并在其上运行逐行工具使用状态机。相关取舍记录在 `scripts/chat_rl.py` 中：它以 fp32（`COMPUTE_DTYPE`）运行，并且仅需 tokenizer 来处理工具使用的特殊 token。