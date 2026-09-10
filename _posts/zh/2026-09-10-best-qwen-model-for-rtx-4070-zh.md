---
audio: false
generated: true
image: false
lang: zh
layout: post
title: RTX 4070最佳Qwen模型
translated: true
type: note
---

问题：**对于你的 RTX 4070 12GB，应该在本地运行哪个未经审查的 Qwen 模型？**

答案：**我会从 Qwen3-8B abliterated 开始，最好是 Q8_0。** 你的 12GB 显存对于 8B 模型来说其实非常舒适。

### 我的排名

| 模型                        |   量化  |  显存占用 | 我的评价                   |
| -------------------------- | ------: | --------: | ------------------------- |
| **Qwen3-8B Abliterated**   | **Q8_0** |     ~9 GB | ⭐ 综合最佳                |
| Qwen3-8B Abliterated       |     Q6_K |     ~7 GB | 很好                      |
| Qwen3-8B Abliterated       |   Q4_K_M |     ~5 GB | 最快 / 显存余量最多        |
| Qwen3-14B Uncensored       |   Q4_K_M |     ~9 GB | ⭐ 最佳质量尝试            |
| Qwen3-14B Uncensored       |    Q5/Q6 | 10–12+ GB | 在 12GB 上略显紧张         |
| 27B+                       |       Q4 |    >15 GB | 在一张 4070 上不值得尝试   |

目前在 HF 上有多个 Qwen3-8B abliterated 变体。([Hugging Face][1])

### 1. 首选：Qwen3-8B Abliterated Q8

我会尝试：

[Rootkit7/Qwen3-8B-abliterated](https://huggingface.co/Rootkit7/Qwen3-8B-abliterated?utm_source=chatgpt.com)

这个模型特别有趣，因为作者实际测试了不同的量化版本。Q8_0 约为 **8.7 GB**，而 Q4_K_M 约为 **5 GB**。作者报告称 Q8 的拒绝率明显低于 Q4。([Hugging Face][2])

对于你的 4070：

```bash
# 大致上我会从这里开始
Qwen3-8B-abliterated-Q8_0.gguf
```

你还能剩下足够的显存用于 KV 缓存和不错的上下文长度。

### 2. 如果你追求极致质量：14B Q4

还有一个模型：

[mradermacher/Qwen3-14B-Uncensored-GGUF](https://huggingface.co/mradermacher/Qwen3-14B-Uncensored-GGUF?utm_source=chatgpt.com)

它包含：

```text
Q4_K_M   9.0 GB
Q5_K_M  10.5 GB
Q6_K    12.1 GB
Q8_0    15.7 GB
```

([Hugging Face][3])

所以 **Q4_K_M 对你的 4070 来说是最佳选择**。

我预计：

```text
8B Q8
    ↓
速度更快
内存占用更低
推理能力不错

14B Q4
    ↓
速度较慢
~9 GB 权重
更好的模型容量
```

对于 agent/coding 工作负载，我实际上会**两者都做基准测试**。

### 3. 不要立刻追求疯狂的 `Heretic / Turbo / Fusion` 模型

那些名字很有趣：

```text
Qwen
 → Abliteration
 → Heretic
 → Merge
 → Turbo
 → Fusion
 → NEO
 → GGUF
```

但你在叠加变换和量化。

对于**研究**，我更倾向于一个干净的基线：

```text
Qwen3-8B
     ↓
abliteration
     ↓
Q8_0
     ↓
llama.cpp
```

然后对比：

```text
base Qwen3-8B
vs
abliterated Qwen3-8B
vs
Qwen3-14B Q4
```

这样你就能得到一个真正的控制实验。

### 4. 在你的 4070 上，我会这样运行

如果你使用 llama.cpp：

```bash
./llama-cli \
  -m Qwen3-8B-abliterated-Q8_0.gguf \
  -ngl 99 \
  -c 16384 \
  -t 12
```

对于 14B：

```bash
./llama-cli \
  -m Qwen3-14B-Uncensored.Q4_K_M.gguf \
  -ngl 99 \
  -c 8192 \
  -t 12
```

并进行基准测试：

```text
tokens/sec
显存使用
提示处理
长上下文退化
编程能力
工具调用
推理能力
拒绝率
```

**对于你的机器，我的个人选择是：**

> **Qwen3-8B abliterated Q8_0 → 首选。**
>
> **Qwen3-14B uncensored Q4_K_M → 其次。**

有趣的是，**8B Q8 作为本地 agent 可能比 14B Q4 更好**，因为你在保持足够小的体积以流畅运行的同时，保留了更多的模型精度。

我还可以为你制作一个**专为 4070 定制的基准测试矩阵（8B/14B/30B-A3B × Q4/Q5/Q6/Q8 × llama.cpp/vLLM/SGLang）**，这样你就可以直接决定下载什么，而不是反复试错。

[1]: https://huggingface.co/models?search=Qwen3-8B-abliterated&utm_source=chatgpt.com "Models – Hugging Face"
[2]: https://huggingface.co/Rootkit7/Qwen3-8B-abliterated?utm_source=chatgpt.com "Rootkit7/Qwen3-8B-abliterated · Hugging Face"
[3]: https://huggingface.co/mradermacher/Qwen3-14B-Uncensored-GGUF/tree/main?utm_source=chatgpt.com "mradermacher/Qwen3-14B-Uncensored-GGUF at main"
