---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 基于存储大小的快照成本
translated: true
type: note
---

问题：在 AMD Developer Cloud 中，大小为 132.77 GB 的 droplet 快照每月费用约为 6 美元。这个费用与其大小有关吗？

回答：

是的，droplet 快照的费用直接与其存储大小相关。在 AMD Developer Cloud、DigitalOcean 或 AWS 等云服务中，快照定价通常基于**存储的数据量**，而非计算资源使用情况。以下是详细说明：

1. **快照大小**
   * 你的 droplet 快照大小为 **132.77 GB**。
   * 云提供商通常按每 GB 每月收取固定存储费率。

2. **费用计算示例**
   * 假设快照价格为 **每 GB 每月 0.045 美元**（开发者云中常见费率），则每月费用为：
     \[
     132.77 \, \text{GB} \times 0.045 \, \text{USD/GB} \approx 5.97 \, \text{USD}
     \]
   * 这与您观察到的约 6 美元/月相符。

3. **其他因素**
   * 价格可能因区域（在您的案例中为 ATL1）、存储类型（SSD 与 HDD）以及任何额外的冗余或备份选项而略有差异。
   * 快照本质上是 droplet 的定点副本，因此 droplet 数据越多，快照越大，存储成本越高。

**结论：** 约 6 美元/月的费用主要源于**快照的大小（132.77 GB）**，并且费用与存储空间成正比。

参考：

* [DigitalOcean Droplet Snapshot Pricing](https://www.digitalocean.com/pricing/)
* [Understanding Cloud Snapshot Costs](https://www.cloudzero.com/blog/cloud-snapshot-costs)