---
audio: false
generated: true
image: false
lang: zh
layout: post
title: FineWeb数据布局验证与说明
translated: true
type: note
---

布局正确：`edufineweb_val_000000.npy`（验证集）+ 训练集 1..1407，符合 nanoGPT 的预期格式。

需要注意两个小问题：

1. **你拥有约 1407 亿个 token，而非 1000 亿。** 176 个输入 parquet 文件多于仅使用 `sample-100BT` 子集的情况（通常约 150 个）。请检查输入目录是否混合了 100BT 样本与另一个快照——额外的数据不会影响训练，只是意味着目录名称现在已不准确。

2. **最后一个分片不完整（3630 万个 token）。** 这对 nanoGPT 的加载器来说没问题，但如果以后恢复 tokenization 过程，脚本会覆盖分片 0（第 75-76 行仅给出警告），因此从头重新运行会破坏 `val_000000`。

除此之外，一切就绪——将你的训练配置指向 `/mnt/data/nanoGPT/data/fineweb/edu_fineweb100B`。
