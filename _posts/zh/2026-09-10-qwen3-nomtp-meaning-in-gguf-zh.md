---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Qwen3 noMTP 在 GGUF 中的含义
translated: true
type: note
---

问题：`Qwen3.8-27B-Uncensored-noMTP-IQ2_M.gguf` 中的 `noMTP` 是什么意思？

答案：

`noMTP` 表示 **GGUF 文件中已移除多令牌预测（MTP）头**。

在该特定模型中，架构如下：

```text
Qwen3.8-27B
├── 64 个普通 Transformer 层
└── 1 个 MTP 层 / 草稿头
```

普通模型：

```text
Qwen3.8-27B-Uncensored-IQ2_M.gguf
```

包含 **65/65 个块**，其中包括 MTP 组件。

`noMTP` 版本：

```text
Qwen3.8-27B-Uncensored-noMTP-IQ2_M.gguf
```

仅包含 **64/64 个块**。作者已明确验证过这一点。（[Hugging Face][1]）

### 为什么要移除 MTP？

MTP 对于**推测解码**非常有用。

概念上：

```text
普通模型：
提示词
  ↓
64 个 Transformer 层
  ↓
下一个令牌预测
```

使用 MTP 时：

```text
提示词
  ↓
64 个 Transformer 层
  ↓
主预测 ───────────────→ 令牌
  ↓
MTP 草稿头
  ↓
提出额外令牌
  ↓
主模型验证它们
```

因此，相比昂贵的 27B 模型逐次生成：

```text
A → B → C → D → E
```

推测解码大致可以做到：

```text
主模型：   A
草稿/MTP： B C D E
主模型：   验证 B C D E
```

如果预测被接受，则可以在不改变最终验证输出的情况下获得更高的**每秒令牌数**。

作者将普通融合 GGUF 描述为 MTP“作为内置草稿内联”，而 `noMTP` 则适用于需要显式提供独立草稿模型的运行时环境。（[Hugging Face][1]）

### 在此仓库中的具体用法

预期的配对方式为：

```bash
Qwen3.8-27B-Uncensored-noMTP-IQ2_M.gguf
+
Qwen3.8-27B-Uncensored-draft-Q8_0.gguf
```

而不是：

```bash
Qwen3.8-27B-Uncensored-IQ2_M.gguf
```

该仓库提供了这两种配置。（[Hugging Face][1]）

### 针对你的 RTX 4070 12GB

值得关注的是 **10.2 GB 的 `IQ2_M` noMTP 模型**。它理论上能装进你的 12 GB 显卡，但还需要考虑以下因素：

```text
10.2 GB  模型权重
+ KV 缓存
+ CUDA/运行时开销
+ 上下文
```

因此，不要将 `10.2 GB < 12 GB` 理解为“我可以轻松运行 128K 上下文”。

此外，`noMTP` **并不意味着低质量或未审查版本**。它只是移除了 MTP/草稿组件。已发布的评测数据显示，IQ2_M 在有无 MTP 的情况下，报告的 Wikitext-2 PPL 相同。（[Hugging Face][1]）

**简而言之：**

```text
MTP    = 多令牌预测，用于推测解码
noMTP  = 移除该额外的预测/草稿头
IQ2_M  = 量化格式
27B    = 基础模型规模
```

对于**单块 RTX 4070**，如果你的目标是测试，我建议先尝试 `noMTP-IQ2_M` 版本。

[1]: https://huggingface.co/