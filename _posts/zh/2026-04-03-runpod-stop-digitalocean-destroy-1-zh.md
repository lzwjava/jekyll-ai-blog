---
audio: false
generated: true
image: false
lang: zh
layout: post
title: RunPod停用与DigitalOcean销毁
translated: true
type: note
---

**问题：** 对于 RunPod 而言，停止一个 Pod 是否真的比 DigitalOcean 的销毁选项更好？使用 DigitalOcean 时，销毁前需要先创建快照，但在 RunPod 上，是否可以更轻松地恢复？

**回答：**

是的，在 RunPod 上停止一个 Pod 通常比在 DigitalOcean 上销毁一个 Droplet 更方便，但两者的权衡略有不同：

1. **RunPod 停止操作**：

   * 停止 Pod 会保留附加的卷/磁盘，因此您存储在上面的数据将保持完整。
   * 计算资源会被释放，因此在 Pod 停止期间您无需为 GPU/CPU 使用付费。
   * 您可以稍后重新启动 Pod，它将恢复至相同的环境和磁盘状态。
   * 只有实例 RAM 中的临时内存或任何未保存的数据会丢失。
   * 您需要继续支付少量闲置磁盘费用（0.006 美元/小时）。

2. **DigitalOcean 销毁操作**：

   * 销毁 Droplet 会完全删除虚拟机。所有未备份或未快照的数据都将丢失。
   * 如果您想保留状态，必须先创建一个快照，这是一个手动步骤，并且可能产生额外的存储成本。
   * 重新启动需要从快照创建新的 Droplet 或重新配置，这比简单地恢复一个已停止的 Pod 需要更多时间。

**结论：**

* 如果您的目标是 **暂停计算同时保持您的工作完好无损**，那么在 RunPod 上停止 Pod 比在 DigitalOcean 上销毁/重建更容易、更快捷。
* DigitalOcean 的销毁操作更为永久，因此如果您希望以后恢复，快照是必需的。

简而言之：**RunPod 停止 = 快速暂停/恢复，DigitalOcean 销毁 = 除非创建快照，否则操作永久生效。**
