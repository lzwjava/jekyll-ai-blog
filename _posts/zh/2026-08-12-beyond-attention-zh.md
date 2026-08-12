---
audio: false
generated: false
image: false
lang: zh
layout: post
title: 超越注意力与Transformer
translated: true
---

这篇文章仍在完善中。

---

当我使用这里的脚本（<https://github.com/lzwjava/zz>）训练了13个小模型时，我的想法和收获是什么？

每次我都多学到一点。首先，我使用了 fineweb-edu 数据集，然后后来又用了金融数据集和代码。

代码更具确定性。在训练代码时，会有很多空白区域。

对于金融数据，我们使用 SEC 文件。我们使用一个 Hermes agent 来帮助训练。一个关于长时间训练或数据准备的技巧：我们用 agent 生成命令，然后使用 tmux 打开另一个终端来运行长时间的任务，这样我们可以更密切地观察它们的进度。

有一次，我使用 SFT 对模型进行微调。SFT 微调过程也需要几个小时。

我还买了一块 AMD MI50 显卡——实际上，它不完全是 MI50，而是 Radeon Pro VII。它们之间有一些区别。我通过协商将其退给了闲鱼卖家。而我的原 GPU，RTX 4070，也与主板有一些问题，所以它被送回工厂进行 BIOS 重置维修。

---

Q 是查询向量，代表我们正在寻找的问题或信息。

K 是 token 自身的表示——它的含义或特征——用于与 Q 匹配。

V 是 token 携带的实际信息，将根据注意力得分进行聚合。

例如，如果 `hidden_size = 4096`，注意力头数为 `32`，那么：

`head_dim = hidden_size / num_heads = 4096 / 32 = 128`

KV cache 的大小大约为：

`sequence_length × num_heads × head_dim × 2`

（`2` 是因为我们同时存储 K 和 V）。

Q 也会被分割到不同的 head 上。每个 head 的小 q 是一个向量/矩阵，其维度与 `head_dim` 相关。

我对 MLA（Multi-head Latent Attention）的理解是：它不是在投影后保留完整的 K/V 信息（这需要大的 `hidden_size × hidden_size` 表示），而是先将 K/V 压缩到更低维的潜在表示中。在注意力计算时，使用这个潜在表示，并在需要时将其投影回来。

我仍然对一些细节感到困惑，但无论如何，感谢讨论！

---

Q 的形状类似于 hidden_size。如果 head 数为 12，head_dim 为 64，那么 hidden_size 是 768。

Q 将被分割成小 q。Wq 是 q 的权重矩阵，这意味着……

每个 Q 首先通过 nn.Linear(n_embd, n_embd)，并且有一个 WQ 权重矩阵。WQ 是为 Q 计算并训练的。

K 和 V 也是一样，都是训练出来的。
