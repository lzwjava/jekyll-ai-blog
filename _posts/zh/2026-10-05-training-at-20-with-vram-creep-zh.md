---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 20%显存蠕变训练
translated: true
type: note
---

19:33 重新检查 —— 仍在运行，刚刚超过 20%：

## Status @ 19:33 (was 16:30)

| Metric | Now | Last check |
|---|---|---|
| Progress | **step 749 / 3712 (20.18%)** | 614 (16.54%) |
| Loss | ~2.79–3.04 | ~2.97–3.11 |
| Speed | ~12.9–13.8k tok/s, 76–81 s/step, MFU 91–99% | ~13.0–13.6k |
| ETA | ~3,741 min ≈ **62.4 h ≈ 2.6 days** (finish ~Oct 8) | ~3,890 min |
| GPU | 100% util, **11.68/12.28 GB (95.1%)**, 56°C, 145 W, 2835 MHz | 11.32 GB |
| Process | PID 3976056 alive, 16h35m elapsed, 100% CPU | — |

**Checkpoints:** 仍然只有 step 250 + 500 —— 你实际上正*处于* step 749，因此 step-750 的保存文件（`model_000500` → `*_000750`，~6.8 GB）应该正在写入。

**两件需要注意的事情：**
1. **VRAM 逐渐爬升**：11.36 → 11.32 → **11.68 GB**（92% → 95%）。轻微增长符合碎片化模式 —— 这强化了之前的建议：在 step-2000 评估之前添加 `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True`。
2. **吞吐量略有波动**：MFU 在 91–99% 之间跳动（之前稳定在 ~99%），steps 在 76–81 s 之间变化。没什么大问题 —— GPU 频率保持高位（2835 MHz），温度较低。

Step 2000 评估（上一次运行的 OOM 点）现在大约还有 27 小时，大约在 **10 月 6 日 ~22:30**。