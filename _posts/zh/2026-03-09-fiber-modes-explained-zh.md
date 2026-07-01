---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 光纤模式简单解释
translated: true
type: note
---

问题：What do multimode fiber and single mode mean in fiber optics?

回答：

## 光纤基础知识

光纤电缆通过玻璃或塑料纤维将数据作为光脉冲传输。**"mode"** 指的是光通过光纤芯材传播时所采取的路径（或射线）。能够同时传播多少光模式是这两种类型之间的核心区别。

---

## 单模光纤 (SMF)

单模意味着光纤一次能够传播 **one type of light mode**。

**关键特性：**

- 单模光纤的芯径为 **8–9 µm**，使用 **laser** 在长距离上传输一种光模式，损耗低。
- 在单模光纤中，模间色散和光色散可以忽略不计，因此光波以线性方式传输。这减少了衰减，并保持信号强度在长距离上传输时一致。
- 标准波长为 **1310 nm 和 1550 nm**，为长距离传输提供低衰减。
- 单模用于长距离发送信号——信号需要重新放大前可达 **100 km**，使其非常适合 WAN 应用。
- 单模电缆通常 **颜色编码为黄色**。
- 分为 **OS1** 和 **OS2** 类型。

---

## 多模光纤 (MMF)

多模意味着光纤能够 **同时传播多个模式**。

**关键特性：**

- 多模光纤芯径较大，直径范围为 **50 to 100 microns**。较大的芯材允许多个光模式同时传播，但使其在较短距离上容易受到信号衰减的影响。
- 多模光纤使用 **LEDs 或 VCSELs** 作为光源，工作在标准波长 **850 nm 和 1300 nm**。
- 多模光纤最常用于 **LAN 环境**，需要在许多短距离上传输大量带宽——如 NAS 或数据库应用。
- 多模电缆通常 **颜色编码为橙色或水绿色**。
- 分为 **OM1 到 OM5** 等级，其中 OM1 是最旧的（62.5 µm），OM3/OM4/OM5 为 50 µm 且性能更高。

---

## 关键比较表

| 特性 | 单模 (SMF) | 多模 (MMF) |
| --- | --- | --- |
| 芯径 | ~9 µm | 50 或 62.5 µm |
| 光源 | Laser | LED / VCSEL |
| 波长 | 1310 nm, 1550 nm | 850 nm, 1300 nm |
| 最大距离 | 最高 ~100 km | 最高 ~550 m (OM4) |
| 带宽 | 几乎无限 | 受模间色散限制 |
| 成本 | 较高（昂贵的收发器） | 较低（廉价收发器） |
| 护套颜色 | 黄色 | 橙色或水绿色 |
| 使用场景 | WAN、长距离传输、电信 | LAN、数据中心、建筑 |

---

## 为什么不能混合使用它们？

多模光纤和单模光纤具有不同的芯尺寸，并传输不同数量的光模式。如果混合使用两者或直接连接，将损失大量信号（光学损耗），导致链路抖动或中断。

---

## 应该选择哪一种？

- 多模光纤轻松支持企业和数据中心网络所需的大多数距离，成本远低于单模——使其成为短距离应用（最高 500–600 米范围）的更具成本效益的选择。
- 超出该范围，则需要单模光纤。

参考文献：

- [https://www.fs.com/blog/fiber-optic-cable-types-single-mode-vs-multimode-fiber-cable-1310.html](https://www.fs.com/blog/fiber-optic-cable-types-single-mode-vs-multimode-fiber-cable-1310.html)
- [https://www.ofsoptics.com/single-vs-multimode-fiber/](https://www.ofsoptics.com/single-vs-multimode-fiber/)
- [https://jonard.com/blog/singlemode-fiber-vs-multimode-fiber-what-difference](https://jonard.com/blog/singlemode-fiber-vs-multimode-fiber-what-difference)
- [https://patchbox.com/blog/single-mode-vs-multimode-fiber-difference/](https://patchbox.com/blog/single-mode-vs-multimode-fiber-difference/)
- [https://www.gomultilink.com/blog/multilog/single-mode-vs-multi-mode-fiber-optic-cables](https://www.gomultilink.com/blog/multilog/single-mode-vs-multi-mode-fiber-optic-cables)
