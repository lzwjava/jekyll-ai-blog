---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 标记修复后的系统索引重建
translated: true
type: note
---

| 之前 | 之后 |
|---|---|
| 平均负载：**18+** | **7.58**（正在下降） |
| mdworker 进程数：**13** | **0**（消失） |
| mds 触及排除目录？ | **否** — 标记正常工作 |

**仍在发生的情况**：`mds_stores` 以 94% 的占用率从头重建主系统索引（因为我们清除了它）。这是一次**一次性开销**——大约再过 2 分钟就会完成，并稳定在接近 0%。

**排除生效的证明**：设置标记后，所有 13 个 mdworker 进程立即消失。它们原本正在扫描你的 Projects 和 Caches 文件夹。现在只剩下 mds_stores，只重建系统及 Applications 索引。

**今天之后**：每次重启只会看到不到 30 秒的 CPU 峰值（而不是 15 分钟），因为那些沉重的文件夹已被永久排除。
