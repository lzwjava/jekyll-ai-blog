---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 第一节运行顺畅
translated: true
type: note
---

复查 session `1` — 仍在正常运行，进展正常：

## 状态 @ 16:30（之前为 14:58）

| 指标 | 现在 | 上次检查 |
| --- | --- | --- |
| Progress | **step 614 / 3712 (16.54%)** | 544 (14.63%) |
| Loss | ~2.97–3.11（最近 6 个 step 的范围） | ~2.96 |
| Speed | ~13,000–13,600 tok/s, 77–81 s/step | ~14,000 tok/s, 75 s/step |
| MFU | 91.5–96.5% | ~99.1% |
| ETA | ~3,890 min ≈ **64.8 h ≈ 2.7 天**（完成约 10月8日） | ~3,955 min |
| GPU | 100% 利用率，11.32/12.28 GB，56°C，158 W | 60°C，164 W |
| Process | PID 3976056 存活，已运行 13h31m，100% CPU | — |

**Checkpoints** (`base_checkpoints/d18/`): 已保存 step 250 + step 500；下一个在 **step 750**（约 2.9 小时后，≈今天 19:25）。

**一个小观察：** 吞吐量略有下降（~13.0–13.6k tok/s，MFU 91–96%，而之前稳定在 14k / 99%），偶尔出现 80 秒的 step。GPU 仍保持在 100%，温度正常，所以这看起来像是微小波动（数据加载 / 频率调整），不是问题 — 但值得留意。如果持续下滑，ETA 会稍微拉长。

没有错误，没有停滞 — 一切正常。
