---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Mini-ITX 与 mATX 的区别
translated: true
type: note
---

问题：什么是Mini-ITX主板，它与mATX有何不同？

答案：

**外形尺寸：**
- Mini-ITX：170mm × 170mm（正方形）
- microATX（mATX）：244mm × 244mm（正方形，但更大）
- ATX：305mm × 244mm（供参考）

**实际差异：**

| | Mini-ITX | mATX |
|---|---|---|
| PCIe插槽 | 1个（x16，用于GPU） | 2-4个（通常1个x16 + 2-3个x1） |
| 内存插槽 | 2个（根据芯片组，最大约64-128GB） | 4个（最大约128-256GB） |
| 机箱尺寸 | 最小，适合SFF构建 | 小型到中塔 |
| 扩展性 | 除一个GPU插槽外无其他 | 可添加采集卡、额外网卡、HBA |
| 成本 | 按特性通常更贵（小众市场） | 更便宜，主流 |

**为何对你的用例（GPU/ML机器）重要：**

如果你要构建多GPU系统，或需要PCIe分叉用于NVMe/网络，mATX（或全尺寸ATX）是唯一明智的选择——Mini-ITX只提供一个x16插槽，仅此而已。Mini-ITX适用于单GPU推理机箱，且希望物理尺寸小（例如家庭服务器或边缘部署），或NAS。

另外注意：
- **VRM质量** — Mini-ITX主板通常在供电上有所缩减，因为目标是用在低功耗SFF构建上。如果你运行300W以上的GPU或高TDP CPU用于本地训练，请仔细检查VRM温度和评测。
- **M.2插槽** — Mini-ITX主板由于空间限制有时只有一个M.2插槽；mATX通常有两个或更多。
- **散热空间** — ITX机箱以紧凑著称，如果你要在家庭开发环境中塞入工作站GPU加大型散热器，这一点很重要。

对于你类似MI300X的家用设置或任何多GPU实验，mATX/ATX是实际的选择。ITX适用于“我想要这个东西很小，而且只需要一张卡”。