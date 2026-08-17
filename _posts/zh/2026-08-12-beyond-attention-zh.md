---
audio: false
generated: false
image: false
lang: zh
layout: post
title: 超越注意力与Transformer
translated: true
---

本文仍在编写中。

---

当我使用这里的脚本（<https://github.com/lzwjava/zz>）训练了13个小模型时，我的想法和收获是什么？

每次我都学到更多。首先，我使用了fineweb-edu数据集，后来使用了金融数据集和代码。

代码更具确定性。在训练代码时，有很多空白区域。

对于金融数据，我们使用SEC文件。我们使用Hermes代理来协助训练。对于长时间运行的训练或数据准备，有一个技巧：我们使用代理来为我们生成命令，然后使用tmux打开另一个终端来运行长时间的任务，这样我们可以更密切地观察它们的进度。

有一次，我使用SFT对模型进行微调。SFT微调过程也需要数小时。

我还购买了一张AMD MI50显卡——实际上，它不完全是MI50，而是一张Radeon Pro VII。它们之间存在一些差异。我与闲鱼卖家协商后退还了它。而我原本的GPU，RTX 4070，也与主板存在一些问题，因此返回工厂通过重置BIOS进行维修。

---

Q是查询向量，代表我们正在寻找的问题或信息。

K是token本身的表示——其含义或特征——用于与Q进行匹配。

V是token承载的实际信息，将根据注意力得分进行聚合。

例如，如果`hidden_size = 4096`且注意力头数量为`32`，那么：

`head_dim = hidden_size / num_heads = 4096 / 32 = 128`

KV缓存大小应约为：

`sequence_length × num_heads × head_dim × 2`

（`2`是因为我们同时存储K和V）。

Q也会被分割到不同的头上。每个头的小q是一个向量/矩阵，其维度与`head_dim`相关。

我对MLA（Multi-head Latent Attention）的理解是，它不是在投影后保留完整的K/V信息（这需要巨大的`hidden_size × hidden_size`表示），而是先将K/V压缩到更低维度的潜在表示中。在注意力计算期间，使用这个潜在表示，并在需要时可以投影回来。

我仍然对一些细节感到困惑，但无论如何，感谢讨论！

---

Q的形状类似于hidden_size。如果头数为12且head_dim为64，那么hidden_size为768。

Q会被分割成小q。Wq是q的权重矩阵，这意味着……

每个Q首先通过nn.Linear(n_embd, n_embd)，并且有一个WQ权重矩阵供它们使用。WQ是经过计算和训练得出的。

K和V也是如此；它们都是训练出来的。

---

对于注意力，绝对位置编码。

---

对于旋转位置编码，它是如何工作的？