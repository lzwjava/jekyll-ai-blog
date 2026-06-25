---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 为什么你的MacBook充电慢
translated: true
type: note
---

让我来分析一下你的设置：

**你现有的设备：**
- **Baseus GaN3 Lite** — 一款氮化镓充电器，可能是30W-67W USB-C输出。这是一款质量不错的第三方充电器，并非劣质产品。
- **Romoss排插** — 1个输入，3个输出（USB集线器/分线器）
- **手机数据线**（很可能是USB-A转USB-C）—— 给MacBook充电

**瓶颈在于数据线和连接路径：**

如果你的连接方式是：**墙壁插座 → Baseus GaN3 Lite → Romoss → 手机数据线 → MacBook**

问题出在**手机数据线**上。原因如下：

- USB-A数据线**无法协商USB-C Power Delivery (PD)**，而这是MacBook所需要的
- USB-A转USB-C数据线最高只能提供**5V × 2.4A = 约12W**，无论充电器功率多大
- 你的MacBook官方充电器根据型号不同为**30W-140W**
- 在12W下，你的MacBook充电会**非常慢** — 可能每小时充10-15%，甚至在使用时电量还会下降

**需要检查的事项：**

1. **Baseus GaN3 Lite是否有USB-C接口？** 如果有，直接使用**USB-C转USB-C数据线**从充电器连接到MacBook — 完全跳过Romoss。这样你将获得30W以上的正常PD充电。

2. **如果必须使用Romoss**，检查它是否有USB-C输出接口（不仅仅是USB-A）。从那个接口使用USB-C转USB-C数据线。

3. **手机数据线才是真正的问题。** 即使是一条便宜的USB-C转USB-C数据线，在为笔记本电脑充电时也会比手机数据线表现好得多。

**总结：** 能用 — 你的MacBook不会损坏 — 但充电速度会慢得令人痛苦。如果你能找到任何一条USB-C转USB-C数据线，哪怕很便宜，直接插到Baseus充电器的USB-C接口上，跳过Romoss。仅此一项就能让你的充电速度提升3-5倍。