---
audio: false
generated: true
image: false
lang: zh
layout: post
title: DigitalOcean Droplet 按小时计费指南
translated: true
type: note
---

Question: DigitalOcean Droplets 是按月计费（即使我只使用几天）还是按小时计费？

Answer:

DigitalOcean **Droplets 是按小时计费的**，且设有**月度封顶价格**。这意味着：

* 您**只需为 Droplet 存在的小时数**付费 ⏱️
* 当费用**达到月度价格后将停止增加** 💰
* 如果您提前删除，**无需支付全月费用** ❌

### 运作机制

示例：一个标价为 **$24/month** 的 Droplet

* 每小时费率 ≈ $24 / ~730 小时 ≈ **$0.033/hour**
* 使用 10 小时 → 支付约 **$0.33**
* 使用 3 天 (72h) → 支付约 **$2.38**
* 使用整个月 → 封顶支付 **$24**

因此：

* 创建 → 按小时计费
* 删除 → 立即停止计费
* 运行整月 → 达到月度封顶

### 重要例外情况 ⚠️

某些项目**无论如何都是按月计算的**：

* Reserved IPs（未使用时）
* Snapshots 存储
* Block storage volumes
* Load balancers
* GPU droplets（仍按小时计费但价格较高）

但**普通的 Droplets 和 GPU droplets** 仍然是**基于小时计费**的。

### 针对您的使用场景（下载数据 → 开启 H100 → 删除）

您的思路是正确的：

* 开启廉价 Droplet → 下载 100GB 数据
* 删除
* 开启 H100 GPU → 训练
* 删除

您只需支付**实际使用的小时数**，而非全月费用。

这也是为什么人们会：

* 开启 GPU 运行 **2–6 小时** 🔥
* 训练
* 销毁

这非常具有成本效益。

经验法则：

* 正在运行 (Running) = 计费
* 已停止但未删除 (Stopped) = 仍在计费
* 已删除 (Deleted) = 停止计费
