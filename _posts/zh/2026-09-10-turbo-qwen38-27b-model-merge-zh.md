---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Turbo Qwen3.8 27B模型合并
translated: true
type: note
---

问题：**`DavidAU/Qwen3.8-27B-TURBO-Fable-Cold-Fusion-735-882-Heretic-Uncensored-NEO-CODER-MAX-MTP-GGUF` 是什么？**

答案：

这本质上是一个**社区修改版的 Qwen3.8 27B 模型**，并非全新的架构。它之所以有趣，是因为作者结合了多种技术：

```text
Qwen3.8-27B
      │
      ├── 微调 / 多阶段训练
      ├── Fable Fusion
      ├── Cold Fusion
      ├── 模型合并
      ├── Heretic / "abliteration"
      │
      └── GGUF 量化
             │
             ├── 常规 GGUF
             └── MTP GGUF
```

作者声称，该模型经过优化，相比原始 Qwen3.8-27B，**思考更快、更侧重编码、更具创造性，且拒绝率更低**。([Hugging Face][1])

### 有趣的部分："TURBO"

作者的主要论点是，该模型产生的推理 token 数量大幅减少。

他们报告的大致情况是：

> 与常规 Qwen3.8 相比，**思维 token 数量仅为 1/5 到 1/2**，在某些情况下甚至低至 **1/10**。([Hugging Face][2])

因此，预期的行为大致如下：

```text
普通推理模型：

问题
  ↓
思考：10k token
  ↓
回答


TURBO：

问题
  ↓
思考：2k–5k token
  ↓
回答
```

这对于**本地 agent** 来说可能非常有用，因为推理 token 浪费是运行本地思考模型的最大成本之一。

---

### "Heretic / Uncensored"

这是另一个主要区别。

该模型使用 **Heretic + 自定义任意秩消融 (ARA)** 来减少模型的拒绝行为。作者报告：

```text
                     原始模型       第一阶段
拒绝测试               99/100         0/100
```

经过额外调整后：

```text
                     原始模型       第二阶段
拒绝测试               86/100        11/100
```

他们还报告称，第二阶段后的 KL 散度仅为 `0.0025`，这意味着修改旨在保留基础模型的大部分行为，同时改变与拒绝相关的行为。([Hugging Face][1])

所以这里的 **"uncensored" 并不意味着一个完全不同的预训练模型**。它更接近于：

```text
Qwen3.8
   +
拒绝方向修改
   +
微调 / 合并
```

---

### "735-882"

这些数字来自作者声称的基准测试结果。

他们报告：

```text
ARC-C   0.735
ARC-E   0.882
```

对比他们列出的 Qwen3.8-27B 基线：

```text
ARC-C   0.591
ARC-E   0.782
```

因此他们将 `735-882` 放入了模型名称中。([Hugging Face][1])

**我不会将此解释为独立验证的 SOTA 声明。** 这些是创建者自己的基准测试结果，并且模型卡片包含大量宣传性语言。请将这些数字视为需要您自行复现的内容，而非既定事实。

---

### "NEO-CODER-MAX"

这本质上是作者将此次特定的合并/微调定位为 **编码 + 通用智能**。

HF 标签明确包含：

```text
coder
thinking
reasoning
creative
roleplaying
conversation
```

并且作者将其描述为一个通用模型，而非纯粹的编码模型。([Hugging Face][1])

针对您的用例，我建议在以下方面特别测试：

```text
仓库导航
代码编辑
调试
Bash
Python
Agent 工具调用
长期编码任务
```

而不是仅仅因为名称中有 "coder" 就假定它能击败专门的编码模型。

---

### "MTP"

这部分在技术上更有趣。

**MTP = Multi-Token Prediction（多 Token 预测）。**

模型不再仅预测：

```text
x_t → x_(t+1)
```

MTP 训练额外的预测头来预测多个未来 token：

```text
x_t
 ├──→ x_(t+1)
 ├──→ x_(t+2)
 ├──→ x_(t+3)
 └──→ ...
```

在推理时，这有可能允许运行时**一次性投机性生成多个 token**，从而减少昂贵的正向传播次数。

这与您尤其相关，因为您已经对 **vLLM / SGLang / nano-vLLM** 感兴趣。

该仓库特别提供了**常规 GGUF** 和 **MTP GGUF** 两种变体。([Hugging Face][3])

---

## "GGUF" 的含义

此仓库是 **llama.cpp 友好的量化分发版本**。

例如：

```bash
llama serve \
  -hf DavidAU/Qwen3.8-27B-TURBO-Fable-Cold-Fusion-735-882-Heretic-Uncensored-NEO-CODER-MAX-MTP-GGUF:Q4_K_M
```

模型卡片明确提供了此工作流程。([Hugging Face][3])

对于您的 RTX 4070 12GB，**Q4_K_M 是显而易见的起点**，尽管 27B 参数 + KV 缓存意味着您需要注意上下文长度和卸载策略。

大致估算如下：

```text
27B 参数

FP16       ~54 GB
Q8         ~27–30 GB
Q6         ~21 GB
Q5         ~18 GB
Q4         ~14–16 GB
```

实际的 GGUF 内存占用还会受到量化元数据、KV 缓存、运行时缓冲区等因素的影响，因此 **Q4 并不意味着“轻松装入 12 GB”**。

您可能需要：

```text
4070 12GB
   +
系统 RAM
   +
llama.cpp GPU 卸载
```

而不是期望整个模型完全驻留在 VRAM 中。

---

## 我的看法

有趣的点不仅仅是简单的 **"uncensored Qwen"**。

而是以下组合：

```text
强大的 27B 基础模型
        +
微调 / 合并
        +
拒绝消融
        +
推理 token 减少
        +
编码微调
        +
MTP
        +
GGUF
```

对于**本地 agent 实验**来说，这确实是一个相当有趣的组合。

我特别建议进行基准测试：

```text
Qwen3.8-27B
vs
DavidAU TURBO
vs
Qwen3.8-27B + 您自己的推理优化
```

在以下方面：

```text
1. token/秒
2. 首 token 延迟
3. 每个任务的推理 token 数
4. 代码基准测试
5. 工具调用成功率
6. SWE 风格的仓库任务
7. 拒绝率
8. VRAM/RAM 占用
```

关键问题是，**“TURBO”是否真的能以大幅减少的推理 token 提供同等任务质量**。如果是，那么对于 agent 来说，这比 ARC 上的小幅改进要有趣得多。

[Hugging Face 模型卡片](https://huggingface.co/DavidAU/Qwen3.8-27B-TURBO-Fable-Cold-Fusion-735-882-Heretic-Uncensored-NEO-CODER-MAX-MTP-GGUF?utm_source=chatgpt.com)

参考资料：

* [DavidAU 模型卡片](https://huggingface.co/DavidAU/Qwen3.8-27B-TURBO-Fable-Cold-Fusion-735-882-Heretic-Uncensored?utm_source=chatgpt.com)
* [GGUF 仓库](https://huggingface.co/DavidAU/Qwen3.8-27B-TURBO-Fable-Cold-Fusion-735-882-Heretic-Uncensored-NEO-CODER-MAX-MTP-GGUF?utm_source=chatgpt.com)

[1]: https://huggingface.co/DavidAU/Qwen3.8-27B-TURBO-Fable-Cold-Fusion-735-882-Heretic-Uncensored-NEO-CODER-MAX-MTP-GGUF?utm_source=chatgpt.com "DavidAU/Qwen3.8-27B-TURBO-Fable-Cold-Fusion-735-882-Heretic-Uncensored-NEO-CODER-MAX-MTP-GGUF · Hugging Face"
[2]: https://huggingface.co/DavidAU/Qwen3.8-27B-TURBO-Fable-Cold-Fusion-735-882-Heretic-Uncensored-NEO-CODER-MAX-MTP-GGUF?hardware=apple-m3-max-96gb&utm_source=chatgpt.com "DavidAU/Qwen3.8-27B-TURBO-Fable-Cold-Fusion-735-882-Heretic-Uncensored-NEO-CODER-MAX-MTP-GGUF · Hugging Face"
[3]: https://huggingface.co/DavidAU/Qwen3.8-27B-TURBO-Fable-Cold-Fusion-735-882-Heretic-Uncensored?utm_source=chatgpt.com "DavidAU/Qwen3.8-27B-TURBO-Fable-Cold-Fusion-735-882-Heretic-Uncensored · Hugging Face"