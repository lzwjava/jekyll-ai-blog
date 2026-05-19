---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AMD GPU 实例：关闭仍计费
translated: true
type: note
---

问题：如果我的 AMD Developer Cloud GPU Droplet 被关机（电源关闭），是否仍然会产生费用？

回答：

**是的 — 关掉电源并不会停止计费。**

即使 droplet 处于关机状态，你仍然会被收费。要完全停止计费，你必须从仪表盘中 **Destroy** 该 droplet，而不仅仅是关机。

---

### 原因

这是标准的云提供商行为（AMD Developer Cloud 运行在 DigitalOcean 基础设施上）。当 droplet 仅仅是“电源关闭”或“关机”时，底层资源——MI300X GPU、存储和保留 IP——仍然分配给你。你支付的是**资源预留**费用，而不仅仅是活跃计算时间。

---

### 你应该怎么做

| 操作 | 是否仍然计费？ |
|---|---|
| 关机 / 关闭电源 | ✅ 是的，仍然计费 |
| **Destroy Droplet** | ❌ 不再收费 |
| 先创建 Snapshot，然后 Destroy | ❌ 无计算费用（仅少量存储费用） |

---

### 建议

- 如果你**彻底不再使用** → 立即从仪表盘中 **Destroy** 该 droplet。
- 如果你**以后还要恢复** → 先创建 **Snapshot**，然后 Destroy。需要时可以从 Snapshot 恢复。
- 按 **$1.99/小时** 计算，一个关机的 droplet 过夜将不必要地花费约 **$47/天**。

前往你的 [AMD Developer Cloud dashboard](https://devcloud.amd.com/gpus) → 选择该 droplet → 选择 **Destroy** 以完全停止所有计费。