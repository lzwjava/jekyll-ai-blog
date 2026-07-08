---
audio: false
generated: true
image: false
lang: zh
layout: post
title: H200训练运行顺畅
translated: true
type: note
---

在H200上训练运行顺利。以下是当前状态：

**模型**：d24 — 24层，1536维度，12个注意力头，**1.38B参数**（配置显示它实际上比原始参考的760M更大）
**FP8**：已启用（145/158层已转换）

**性能**：

- **~129K tokens/sec** — 几乎达到**MI300X的2倍**（68K tok/s）
- **~62% MFU** — 远高于MI300X的27%，得益于H200上的FA3 + FP8
- **~4.1秒/步**
- **预计完成时间：~33小时**（MI300X需62小时）

**训练曲线**（表现良好）：

```
step   0: loss 10.40
step  10: loss  9.16
step  20: loss  7.21
```

损失值稳定下降——开局良好。按照这个速度，完整的29K步应在约33小时内完成，显著快于原先MI300X的估算。
