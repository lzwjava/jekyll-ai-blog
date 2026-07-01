---
audio: false
generated: true
image: false
lang: zh
layout: post
title: RunPod 停止与 DigitalOcean 销毁
translated: true
type: note
---

问题：对于 RunPod 而言，停止 Pod 是否比销毁 DigitalOcean 的 Droplet 更好？在 DigitalOcean 上，销毁前必须创建快照，而 RunPod 的恢复操作更简便？

回答：

是的，对于“暂停并稍后恢复”这一使用场景，**RunPod 的停止功能远比 DigitalOcean 的销毁功能更为便捷**。以下是详细的对比分析：

---

## RunPod：停止 vs 终止

RunPod 提供两种不同的操作：

| 操作 | 发生的情况 |
| --- | --- |
| **停止** | Pod 被暂停。GPU 计费停止。磁盘保持活动状态。`/workspace` 目录中的数据被保留。 |
| **终止** | 一切都被销毁。容器磁盘被永久清空。 |

如果仅停止 Pod，之后可以重新启动，存储在 `/workspace` 中的任何数据都将保留。RunPod 在 Pod 停止期间会收取**空闲磁盘费用**。

您截图中显示的正是这项空闲磁盘费用：**$0.006/hr（$0.13/天）** — 与保持 GPU 运行相比非常低廉。

存储在 `/workspace` 目录中的数据在 Pod 停止和重启后得以保留，但**在 Pod 终止时会被删除**。这非常适合存储需要在多个会话中访问的模型、数据集和检查点。

---

## DigitalOcean：销毁工作流

在 DigitalOcean 上，销毁 Droplet 是**永久且不可逆的**：

如果您打算销毁 Droplet 并希望获得最新的镜像，则必须**关闭 Droplet 并在销毁前立即创建快照**。

DigitalOcean 快照的费用为 **$0.06/GB/月**。如果您销毁 Droplet 并从快照创建新的实例，很可能**会丢失原有的 IP 地址**。

因此，DigitalOcean 的工作流程是：

1. 关闭 Droplet
2. 手动创建快照（消耗时间 + 存储费用）
3. 销毁 Droplet
4. 稍后，从快照**新建**一个 Droplet（新的 IP 地址，可能需要重新配置）

---

## 并排对比

| 特性 | RunPod 停止 | DigitalOcean 销毁 + 快照 |
| --- | --- | --- |
| **数据自动保留** | ✅ 是（`/workspace`） | ❌ 必须先手动快照 |
| **恢复速度** | ✅ 快速（同一 Pod 重启） | ❌ 缓慢（从快照新建 Droplet） |
| **IP / 环境保留** | ✅ 是 | ❌ 通常会丢失 IP |
| **需要额外手动步骤** | ❌ 无 | ✅ 必须手动创建快照 |
| **空闲成本** | ✅ 极低（仅磁盘约 $0.006/hr） | ✅ 为零（销毁后）+ 快照存储费 |
| **丢失数据风险** | 低（如果是停止，而非终止） | 较高（如果忘记创建快照） |

---

## 一个需要注意的细节

如果停止 Pod 但留下一个较大的容器磁盘，在该磁盘被删除之前，您仍需按**正常存储费率的双倍**支付费用。停止 Pod 并不会停止存储计量。

因此，对于长期的“冷存储”，最佳的 RunPod 策略是：

- 使用**网络卷**存储重要数据
- **终止** Pod（不仅仅是停止）以避免空闲磁盘的双倍计费
- 准备就绪时，将网络卷挂载到新的 Pod

您今天可以在一个 Pod 上训练模型，将检查点保存到已挂载的卷中，关闭 Pod 以节省费用，下周再将同一卷挂载到新的 Pod 上以恢复训练或进行推理。

---

## 总结

对于短期到中期的暂停（数小时到数天）：**RunPod 停止功能优势明显** — 无需快照、不会丢失 IP、无需手动操作、即时恢复、空闲成本极低。

对于长期暂停（数周/数月）：考虑使用 RunPod 的**网络卷 + 终止**组合，以避免持续的空闲磁盘成本，这仍然比 DigitalOcean 的销毁/快照工作流程更便捷。

参考文献：

- [RunPod 存储类型](https://docs.runpod.io/pods/storage/types)
- [RunPod 定价指南](https://flexprice.io/blog/runprod-pricing-guide-with-gpu-costs)
- [RunPod 网络卷博客](https://www.runpod.io/blog/network-volumes-on-runpod-secure-cloud)
- [DigitalOcean：销毁 Droplet 并保留快照](https://docs.digitalocean.com/support/how-can-i-destroy-my-droplets-while-maintaining-my-backups/)
- [DigitalOcean 快照成本](https://snapshooter.com/learn/digitalocean/backups)
