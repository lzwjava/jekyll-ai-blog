---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 批次大小最佳点已找到
translated: true
type: note
---

**device_batch=32 works** — 正在运行。以下是总结：

### 批次大小对比

| | batch=16 | batch=32 | batch=128 |
|---|---|---|---|
| **VRAM** | 54 GB (38%) | **93 GB (65%)** | 139 GB 时 OOM |
| **Step time** | 4.1s | **7.8s** | — |
| **Tok/sec** | 129K | **135K** | — |
| **MFU** | 62% | **65%** | — |
| **Grad accum** | 16 | **16** | — |
| **Total batch** | 524K | **1M** | — |
| **Steps total** | 29,000 | **14,500** | — |
| **ETA** | ~33h | **~31h** | — |

**batch=32** 是最佳选择：
- 使用 93/144 GB (65%) — 有充足余量
- 更高吞吐量（135K vs 129K tok/s）
- 更高 MFU（65% vs 62%）
- 相同总 token 下步数减少一半，实际耗时相当（~31h）
- 1M token 批次带来更干净的梯度估计

注意：学习率由 nanochat 的代码**自动按 1.414×**（平方根规则）缩放。损失曲线与 batch=16 运行完全一致——一切正常。

对于后续的**收敛瓶颈**策略（约第 10,000/14,500 步），可通过 `--resume-from-step=10000` 并增加 `--device-batch-size=48`——这应使用约 125 GB，并在最终精调阶段进一步提升 MFU。