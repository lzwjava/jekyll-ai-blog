---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 平坦低分辨率退化结果
translated: true
type: note
---

Step  | v2 (flat LR) | Old (full schedule)
------|-------------|---------------------
130k  | 0.780       | 0.780  (starting checkpoint)
140k  | 0.902       | 0.865
150k  | 0.890       | 0.854
160k  | 0.882       | 0.843
170k  | 0.874       | 0.831
180k  | 0.866       | 0.820
190k  | 0.859       | 0.810
200k  | 0.853       | 0.801

min_val_bpb = 0.780 (step 130k)。两次训练均未超过起始 checkpoint。两次训练都出现了退化——v2 退化得更严重（0.853 vs 0.801），原因是动量不匹配。

核心问题不仅仅是 LR 调度——而是将训练从 130k 扩展到 200k 导致模型在两次尝试中都变得更差。模型可能在 130k 时已经收敛（token:参数比 21.8x，接近 Chinchilla 最优）。在此规模下继续训练是过度训练，没有任何益处。

要实际超过 0.780，需要以下条件之一：

1. 更多数据（而不仅仅是相同数据的更多 epochs）
2. 更大的模型（d16 或 d20）
3. 更好的数据质量/过滤

需要我清理 checkpoint 并只保留 130k 的最佳结果吗？
