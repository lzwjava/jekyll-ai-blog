---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 模型训练性能与问题审查
translated: true
type: note
---

## 📊 训练轨迹 (950 iters / 10K target)

| Iter | Train Loss | Val Loss |
| ------ | ----------- | ---------- |
| 0 | 11.05 | 11.06 |
| 250 | 5.93 | 5.93 |
| 500 | 5.07 | 5.06 |
| 750 | 4.26 | 4.22 |
| 950 | 4.00 | — |

**已看到约 640M tokens** (950 × 1M × gradient_accumulation effect)。10B target 是 10× 更多。

## ⚠️ 问题

1. **即使 compile 后 Step time 仍卡在 21s** — 应该为 1-3s。出了问题。可能是：
   - 数据加载瓶颈 (disk I/O)
   - Inductor workers 仍在运行
   - CPU preprocessing 在关键路径上

2. **MFU 150%+** — 单张 H200 上不可能。这是 torch.compile 测量伪影，不是真实利用率。

3. **iter 600 处 Loss spike** (4.91 vs 之前 4.85 和之后 4.43) — 可能是坏 batch 或 LR scheduling 问题。如果恢复就不用担心。

4. **ckpt iter = 0** — checkpoint 保存了 model weights 但 `iter` 计数器未正确存储。这是 nanoGPT 的 bug/feature。

## ✅ 良好点

- Loss 持续下降 (950 steps 内 11 → 4)
- Val loss 紧密跟踪 train loss — 尚未过拟合
- 4.0 loss 的 model 已可用于基本生成
- 18GB checkpoint 保存正确

## 结论

21s/step × 剩余 9050 iters = **约 53 小时** 剩余。太慢了。数据 pipeline 可能是瓶颈。但 model 本身学习良好。如果你能修复速度 (也许用 `block_size=512`)，就能在几小时内完成而不是几天。🦞
