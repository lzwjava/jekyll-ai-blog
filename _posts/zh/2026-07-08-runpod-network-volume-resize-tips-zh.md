---
audio: false
generated: true
image: false
lang: zh
layout: post
title: RunPod网络卷调整大小提示
translated: true
type: note
---

问题：在RunPod的“编辑网络卷”对话框中，我看到一个现有的200 GB卷正在扩展+100 GB，总量达到300 GB，计费为$0.14/GB/月（总计$42/月，之前为$28/月）。关于这种情况，我需要了解什么？

回答：

$0.14/GB/月的费率确认你使用的是RunPod的**高性能网络卷**层级，而非标准层级。供参考：

| 层级 | 费率（前1TB） | 备注 |
| --- | --- | --- |
| 标准网络卷 | $0.05–$0.07/GB/月 | 基于Ceph，广泛可用 |
| **高性能网络卷** | **$0.14/GB/月** | 基于NVMe，目前限于蒙特利尔数据中心 |

你的计算正确：300 GB × $0.14 = $42/月，之前为200 GB × $0.14 = $28/月 — 增加100 GB多出$14/月。

此次调整在操作上需要注意的事项：

**1. 调整仅支持扩容。** RunPod网络卷可以扩展，但无法就地缩小。如果过度配置，唯一的缩小方式是创建一个新的较小卷并迁移数据（使用rsync/rclone），然后删除旧卷。不要“以防万一”而多填数值——这是一条单向递增之路。

**2. 调整前需先卸载。** 网络卷在进行调整操作时通常不能处于被Pod挂载的状态——请确保使用该卷的Pod已停止，否则仪表盘或API中的调整调用可能会被拒绝或进入队列。

**3. 计费按小时而非按秒。** 与计算资源不同：容器和卷磁盘按秒计费，而网络卷按小时计费。因此，一旦你提交300 GB的配置，无论你在该小时内的哪个时间点进行调整，你都要支付完整下一个小时块的费用。

**4. 此处不适用停止Pod的陷阱**——停止时翻倍的惩罚是针对**容器/卷磁盘**（$0.10 → $0.20/GB）的，而非网络卷。网络卷的费率无论挂载、卸载还是Pod停止都保持不变——这正是网络卷相对于本地磁盘的核心优势。

**5. 考虑到你的工作负载（MI300X训练任务、检查点密集的MoE工作）**——如果这300 GB用于存储DeepSeek-v4 MoE检查点或nanochat中间产物，那么高性能层级的NVMe支持在训练期间进行持续读写是正确的选择。如果只是用于运行间数据集的冷存储，那你为不需要的吞吐量付出了两倍的价格——在非蒙特利尔区域使用标准网络卷以$0.07/GB计算，同样的300 GB仅需$21/月。

通过RunPod API快速检查你所实际支付的层级：

```bash
curl -s https://api.runpod.io/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <RUNPOD_API_KEY>" \
  -d '{"query": "query { myself { networkVolumes { id name size dataCenterId } } }"}' \
  | python3 -m json.tool
```

这会返回`dataCenterId`——如果它不是蒙特利尔区域的ID但你仍被收费$0.14，建议提交支持工单，因为该层级本应是地理限制的。

参考链接：

- [Pricing - Runpod Documentation](https://docs.runpod.io/pods/pricing)
- [Understanding Runpod Pricing: A Clear Guide to Costs and Options | Hivenet](https://compute.hivenet.com/post/runpod-pricing-complete-guide-to-gpu-cloud-costs)
- [GPU Cloud Pricing | Runpod](https://www.runpod.io/pricing)
