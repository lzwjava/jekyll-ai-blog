---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 不关机创建实例快照
translated: true
type: note
---

**问题：** 对于 AMD Dev Cloud 和 DigitalOcean — 能否在不先关闭实例的情况下为运行中的实例创建快照？

**回答：**

这两个平台的行为不同：

## DigitalOcean

**不能 — 你需要先关机才能获得一致的快照。**

DigitalOcean 确实支持“在线快照”（运行中创建快照），但他们明确警告这可能导致**文件系统状态不一致/损坏**——本质上是一种崩溃一致性快照，而非应用一致性快照。对于任何有状态的工作负载（数据库、正在进行且打开文件的训练任务），关机才是安全路径。

其文档建议：

```
# 在快照前先正常关机
doctl compute droplet-action power-off <droplet-id> --wait
doctl compute droplet-action snapshot <droplet-id> --snapshot-name "my-snapshot"
```

DigitalOcean 的在线快照本质上是“尽力而为”的——适用于无状态机器，对活跃工作负载有风险。

## AMD Dev Cloud

位于 `devcloud.amd.com/images/snapshots` 的快照页面是针对其环境的。AMD Dev Cloud 实例（尤其是计费约 $2/小时的 MI300X 节点）通常是**临时计算节点**，其中：

- 快照/镜像是从**已停止或空闲的实例状态**捕获的
- UI 可能允许你在运行中的实例上发起快照，但底层编排系统（很可能是 OpenStack 或类似的云底层）通常会短暂地暂停或挂起 VM

建议检查实际的 UI 行为——如果运行中“创建快照”按钮是灰色的，那就是答案。如果可点击，充其量也只是崩溃一致性的。

## 结论

| 平台 | 支持在线快照？ | 对 ML 工作负载安全吗？ |
| --- | --- | --- |
| DigitalOcean | 技术上可以，但有风险 | 先关机 |
| AMD Dev Cloud | 取决于 UI，很可能需要停止 | 先停止实例 |

**针对你的用例的实操建议：** 在训练中途对 AMD Dev Cloud 实例创建快照之前，请先明确地保存模型权重检查点（它们应该已在磁盘上），然后干净地停止实例再创建快照。快照用于保存环境和依赖，而非检查点状态。
