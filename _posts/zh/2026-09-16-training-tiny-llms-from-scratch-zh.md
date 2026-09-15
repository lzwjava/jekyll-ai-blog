---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 从头训练小型LLMs
translated: true
type: note
---

问题：**Hugging Face SmolLM2-135M 简介**

答案：

[Hugging Face 上的 SmolLM2-135M](https://huggingface.co/HuggingFaceTB/SmolLM2-135M?utm_source=chatgpt.com) 是 Hugging Face SmolLM2 系列中一个非常小的**纯解码器 Transformer 语言模型**。

有趣的地方不在于“135M 参数”，而在于这是一个相对完整、开源的示例，展示了**如何从头训练一个有用的微型 LLM**。

---

### 1. 它是什么？

SmolLM2 包含以下版本：

```text
SmolLM2-135M
SmolLM2-360M
SmolLM2-1.7B
```

你正在看的这个是最小的：

```text
~135M 参数
2T 预训练 token
BF16
64 × H100 GPU
Transformer 解码器
Apache 2.0
以英语为主
```

([Hugging Face][1])

可以将其想象为：

```text
                    SmolLM2-135M
                         │
              ┌──────────┴──────────┐
              │                     │
         预训练                 指令微调
              │                     │
        2T token                 SFT
              │                     │
     下一个 token 预测             DPO
                                    │
                              UltraFeedback
```

基座模型**不是聊天机器人**。它的学习目标是：

> 给定 token `x₁ ... xₜ`，预测 `xₜ₊₁`

即：

$$
\mathcal L =
-\sum_t \log P_\theta(x_t \mid x_{<t})
$$

这就是全部的基本目标。

---

### 2. 为什么 135M 有趣？

按照现代 LLM 的标准，135M 非常小。

粗略对比：

```text
GPT-2 small       124M
SmolLM2           135M
Llama 3.2         1B+
Qwen 2.5          0.5B+
```

然而 SmolLM2-135M 在**2 万亿个 token** 上进行了训练。这大致相当于：

$$
\frac{2T}{135M} \approx 14,800
$$

每个参数的训练 token 数。

这是一个极高的数据/参数比。

因此，这是一个很好的模型，用于研究以下问题：

> **当模型极小但训练极其充分时，会发生什么？**

Hugging Face 明确将 SmolLM2 描述为以数据为中心的工作，135M 模型使用了 FineWeb-Edu、DCLM、The Stack 以及其他经过过滤的数据集。([Hugging Face][1])

---

### 3. 基座模型与指令模型对比

这里有两个你需要区分开的概念。

**基座模型：**

```text
SmolLM2-135M
```

它基本上就是：

```python
input_ids
    ↓
Transformer
    ↓
logits
    ↓
next token
```

例如：

```text
"The capital of France is"
                         ↓
                       " Paris"
```

它学习了语言统计、知识、代码等，但并没有专门针对遵循指令进行优化。

然后是：

```text
SmolLM2-135M-Instruct
```

它基于预训练 checkpoint 并应用了：

```text
base model
    ↓
SFT
    ↓
DPO
    ↓
instruction model
```

SFT 数据包括公开数据集以及 Hugging Face 的 Smol-SmolTalk 数据集，DPO 则使用了 UltraFeedback。([Hugging Face][1])

因此，如果你想了解**预训练**，请从 `SmolLM2-135M` 开始。

如果你想构建一个微型 agent/聊天机器人，请关注 `SmolLM2-135M-Instruct`。

---

### 4. 实际的 Transformer 是什么样的？

从概念上讲：

```text
tokens
  │
  ▼
Embedding
  │
  ▼
┌─────────────────────┐
│ Transformer Block   │
│                     │
│ RMSNorm             │
│   ↓                 │
│ GQA / Attention     │
│   ↓                 │
│ residual             │
│   ↓                 │
│ RMSNorm             │
│   ↓                 │
│ SwiGLU MLP          │
│   ↓                 │
│ residual             │
└─────────────────────┘
          × N
  │
  ▼
LM Head
  │
  ▼
logits [vocab_size]
```

这是一个传统的解码器 Transformer，而不是某种全新的架构。模型卡片将其标识为 Transformer 解码器。([Hugging Face][1])

因此，有趣的工程问题不在于：

> “他们发明了什么新的注意力机制？”

而在于：

> **如何通过架构 + 数据 + 训练让一个微小的 Transformer 具备令人惊讶的能力？**

---

### 5. 训练规模才是疯狂之处

Hugging Face 报告了如下信息：

```text
参数数量：       135M
Token 数量：     2T
硬件：           64 × H100
精度：           BF16
框架：           nanotron
```

([Hugging Face][1])

对于一个密集自回归 Transformer，粗略的训练 FLOPs 估算为：

$$
C \approx 6NT
$$

其中：

* \\(N = 135M\\)
* \\(T = 2T\\)

因此：

$$
C \approx 6(1.35\times10^8)(2\times10^{12})
$$

$$
\approx 1.62\times10^{21}
$$

FLOPs。

这是一个值得记住的数字：**小型模型，巨大的 token 预算**。

---

### 6. 它实际能做什么？

基座模型的基准测试分数相对于其规模而言还算可以，但并不突出：

| Benchmark  | SmolLM2-135M |
| ---------- | -----------: |
| HellaSwag  |         42.1 |
| ARC        |         43.9 |
| PIQA       |         68.4 |
| MMLU       |         31.5 |
| Winogrande |         51.3 |
| GSM8K      |          1.4 |

指令版本在指令遵循方面有显著提升；例如，IFEval 达到了 29.9，而之前的 SmolLM-135M-Instruct 只有 17.2。([Hugging Face][1])

但不要将 135M 理解为微型 GPT-4。

在这个规模下，它最好被看作：

```text
优秀的研究/实验模型
              +
廉价的本地模型
              +
从玩具到生产的训练基板
```

而不是一个强大的通用助手。

---

### 7. 你可以在大约 10 行代码中运行它

```bash
pip install transformers torch
```

```python
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

name = "HuggingFaceTB/SmolLM2-135M"

tokenizer = AutoTokenizer.from_pretrained(name)
model = AutoModelForCausalLM.from_pretrained(
    name,
    torch_dtype=torch.bfloat16,
).cuda()

x = tokenizer("The future of AI is", return_tensors="pt").to("cuda")

y = model.generate(
    **x,
    max_new_tokens=100,
    temperature=0.7,
)

print(tokenizer.decode(y[0]))
```

官方模型卡片提供了基本上就是这个加载/生成路径。([Hugging Face][1])

---

### 8. 对你来说真正有趣的实验

鉴于你已经在训练模型，我建议将 SmolLM2 看作一个**用于剖析**的模型，而不是一个**用于使用**的模型。

克隆训练代码：

```bash
git clone https://github.com/huggingface/smollm
```

然后重现这个流程：

```text
                    ┌──────────────┐
                    │ 原始语料库    │
                    └──────┬───────┘
                           │
                    过滤 /
                    去重
                           │
                           ▼
                    ┌──────────────┐
                    │ 2T tokens    │
                    └──────┬───────┘
                           │
                           ▼
                 ┌──────────────────┐
                 │ SmolLM2-135M     │
                 │                  │
                 │ embedding        │
                 │ transformer × N  │
                 │ lm_head          │
                 └────────┬─────────┘
                          │
                     下一个 token CE
                          │
                          ▼
                     checkpoint
                          │
                     SFT / DPO
                          │
                          ▼
                    Instruct model
```

官方仓库包含了 SmolLM 训练材料以及数据/训练细节。([GitHub][2])

**如果你的目标是理解 SmolLM2-135M 的实际构建方式**，下一步有用的做法是查看其 `config.json`，并**逐层计算参数数量**——嵌入层 → QKV/GQA → SwiGLU → 归一化 → LM head——直到得到约 135M 这个数字。这比仅仅阅读模型卡片更能学到东西。

参考文献：

* [SmolLM2-135M 模型卡片](https://huggingface.co/HuggingFaceTB/SmolLM2-135M?utm_source=chatgpt.com)
* [SmolLM GitHub 仓库](https://github.com/huggingface/smollm?utm_source=chatgpt.com)
* [SmolLM2 技术报告](https://arxiv.org/abs/2502.02737?utm_source=chatgpt.com)

[1]: https://huggingface.co/HuggingFaceTB/SmolLM2-135M "HuggingFaceTB/SmolLM2-135M · Hugging Face"
[2]: https://github.com/huggingface/smollm/blob/main/text/README.md?utm_source=chatgpt.com "smollm/text/README.md at main · huggingface/smollm · GitHub"