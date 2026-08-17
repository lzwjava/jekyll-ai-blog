---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Qwen3.8-27B-Uncensored-FP8的技术理解
translated: true
type: note
---

问题：**什么是`orcarouter/Qwen3.8-27B-Uncensored-FP8`，以及如何在技术上理解它？**

答案：

[Hugging Face上的Qwen3.8-27B-Uncensored-FP8](https://huggingface.co/orcarouter/Qwen3.8-27B-Uncensored-FP8?utm_source=chatgpt.com) 本质上就是：

> **Qwen3.8-27B + 拒绝机制移除（"abliteration"）+ FP8量化**

它**并非从头训练的新模型架构**。

### 1. 从基础模型开始

底层模型是 **Qwen3.8-27B**，一个270亿参数的密集多模态模型。上传者列出的架构为：

```text
64层
hidden_size = 5120

48 × Gated DeltaNet / 线性注意力层
16 × 全注意力层

+ 视觉编码器
+ MTP推测解码头
```

因此，其架构相当有趣：它并非传统Transformer中每一层都是标准softmax注意力。它采用了**混合注意力**：

```text
输入
  │
  ├── Gated DeltaNet      ← 廉价线性循环
  ├── Gated DeltaNet
  ├── Gated DeltaNet
  ├── 全注意力           ← 每第4层
  ├── Gated DeltaNet
  ├── ...
  └── 全注意力
```

该模型支持**视觉+文本**、推理/思考控制、工具调用以及MTP推测解码。根据模型介绍，它拥有**262,144令牌的上下文窗口**。([Hugging Face][1])

---

### 2. "Uncensored"实际上是什么意思？

有趣的部分在于**abliteration**。

上传者表示他们执行了以下操作：

```text
Qwen3.8-27B
      │
      ▼
找到拒绝方向
      │
      ▼
正交化/移除拒绝方向
      │
      ▼
修改后的权重
      │
      ▼
FP8量化
      │
      ▼
Qwen3.8-27B-Uncensored-FP8
```

目标并非重新训练整个模型。

相反，其思路是拒绝行为部分对应于模型残差表示中的特定方向。你识别出一个"拒绝方向"，并修改模型以移除该方向。

模型介绍将此过程明确描述为**"将拒绝方向从残差流中正交化出去。"** ([Hugging Face][1])

概念上理解：

```python
# x = 残差表示

r = 拒绝方向

# 移除x沿r方向的分量
x_uncensored = x - projection(x, r)

# 投影：
projection(x, r) = (x @ r) / (r @ r) * r
```

因此：

```text
x
│
│       ↗ 拒绝方向 r
│      /
│     /
│    ●
│   /
│  /
└──────────────

       ↓

移除与r平行的分量

       ●
      /
     /
────●──────────
```

这就是为什么 **abliteration比重新训练便宜得多**。

---

### 3. 那么为什么用FP8？

生成的模型被量化为**块FP8 E4M3**格式。

模型介绍说明：

```text
weight_block_size = [128, 128]
activation = dynamic
weights = FP8 E4M3
```

而某些组件保持BF16格式：

```text
FP8:
    线性层权重

BF16:
    视觉塔
    归一化层
    路由器
    嵌入层
    lm_head
```

生成的文件大小约为**30.9 GB**，分为7个safetensors分片。([Hugging Face][1])

所以不要认为：

```text
27B × 1 字节 = 27 GB
```

精确来说不是。

其中包含FP8元数据/缩放因子以及BF16组件等，因此磁盘上约为**31 GB**。

---

### 4. 为什么这个模型对你来说有意思

实际上，我会将这个模型归入一个非常有用的学习类别：

```text
                 Qwen3.8
                    │
          ┌─────────┴─────────┐
          │                   │
       架构                后训练
          │                   │
   混合注意力             对齐
   DeltaNet              拒绝机制
   全注意力              安全性
   视觉                  RL/SFT
   MTP                    abliteration
          │                   │
          └─────────┬─────────┘
                    │
                 量化
                    │
                  FP8
```

你可以从一个检查点研究**现代LLM工程中的三个不同部分**：

1. **混合架构**
   * Gated DeltaNet
   * 全注意力
   * 多模态塔
   * MTP

2. **模型修改**
   * 拒绝方向发现
   * 激活空间操作
   * abliteration

3. **推理优化**
   * 块FP8
   * vLLM
   * MTP推测解码
   * 262K上下文

这比仅仅下载一个随机的GGUF文件要具有教育意义得多。

---

### 5. 你可以在24 GB GPU上运行它吗？

**单GPU运行并不轻松。**

检查点本身约为31 GB，这还没考虑：

```text
权重
+ KV缓存
+ 激活值
+ CUDA工作空间
+ 视觉模型
```

因此，24 GB显存不足以直接部署FP8版本。

官方模型介绍专门提供了vLLM和SGLang服务指令。([Hugging Face][1])

例如：

```bash
pip install vllm

vllm serve \
  orcarouter/Qwen3.8-27B-Uncensored-FP8
```

但你需要**超过24 GB的显存**，或者使用多GPU/卸载/其他量化格式。

---

### 6. 一个重要区别

"Uncensored"并**不**意味着：

```text
更智能
```

它主要意味着：

```text
更少的拒绝 / 更少的安全对齐限制
```

上传者明确警告，abliteration可能会影响超出单纯移除拒绝行为之外的行为，且该模型旨在用于研究/红队测试，而非直接向最终用户开放。([Hugging Face][1])

因此，从科学角度看，有趣的问题实际上是：

> **在修改了负责拒绝行为的表示之后，有多少能力得以保留？**

这比"它能否生成未经审查的内容"要有趣得多。

模型介绍包含了针对**有害提示拒绝、过度拒绝、能力保留、推理和视觉**的单独评估，这恰恰是你在研究模型手术时想要检查的实验类型。([Hugging Face][1])

### 我的建议

鉴于你正在学习**模型训练+推理**，我会按照这个顺序进行研究：

```text
Qwen3.8 架构
       ↓
Gated DeltaNet
       ↓
Qwen多模态前向传播
       ↓
MTP
       ↓
FP8块量化
       ↓
abliteration
       ↓
vLLM实现
```

**abliteration + FP8组合特别值得你自己复现**：拿一个小型开放模型，识别一个拒绝方向，移除它，评估前后效果，然后进行量化。这将为你提供一个具体的端到端**"模型手术→量化→推理"**项目，而不仅仅是学习如何调用LLM API。([Hugging Face][1])

参考文献：

* [Qwen3.8-27B-Uncensored-FP8模型介绍](https://huggingface.co/orcarouter/Qwen3.8-27B-Uncensored-FP8?utm_source=chatgpt.com)
* [Qwen官方模型](https://huggingface.co/Qwen/models?utm_source=chatgpt.com)

[1]: https://huggingface.co/orcarouter/Qwen3.8-27B-Uncensored-FP8 "orcarouter/Qwen3.8-27B-Uncensored-FP8 · Hugging Face"