---
audio: false
generated: false
image: false
lang: zh
layout: post
title: 超越注意力与Transformer
translated: true
---

本文仍在撰写中。

---

当我使用这里的脚本（https://github.com/lzwjava/zz）训练了13个小模型时，我的想法和学到的东西是什么？

每一次，我都学到了一些东西。首先，我使用了fineweb-edu数据集，后来使用了金融数据集和代码数据集。

代码更具确定性。使用代码训练时，会有很多空白空间。

对于金融数据，我们使用SEC-filings数据。我们使用Hermes agent来训练。一个长时间训练或数据准备的技巧：我们使用agent为我们生成命令，然后使用tmux打开另一个终端来运行长时间任务，这样我们可以更好地观察它们的进度。

有一次，我使用了SFT来微调模型。SFT微调过程也需要几个小时。

然后我买了一张AMD MI50显卡——实际上，它不完全是MI50，而是Radeon Pro VII。它们有一些区别。不过我和闲鱼卖家协商后退了货。而我原来的GPU，RTX 4070，和主板也有一些问题，被送回工厂维修，并重置了BIOS。

---

Q是查询向量，代表问题或我们正在寻找的信息。

K是token本身的表示——它的含义或用于与Q匹配的特征。

V是token携带的实际信息，将根据注意力分数进行聚合。

例如，如果`hidden_size = 4096`，注意力头数为`32`，那么：

`head_dim = hidden_size / num_heads = 4096 / 32 = 128`

KV缓存的大小大约为：

`sequence_length × num_heads × head_dim × 2`

（`2`是因为我们同时存储了K和V）。

Q也被分割到不同的注意力头中。每个头的小q是一个向量/矩阵，其维度与`head_dim`相关。

我对MLA（Multi-head Latent Attention）的理解是，它不会在投影后保留完整的K/V信息（这需要很大的`hidden_size × hidden_size`表示），而是先将K/V压缩到低维潜在表示中。在注意力计算时，使用这个潜在表示，并在需要时投影回来。

我对一些细节仍然有些困惑，但无论如何，感谢讨论！