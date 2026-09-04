---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 航嘉电源P4与4+4 CPU接口
translated: true
type: note
---

**问题：** 在航嘉（Huntkey）Super 500W 电源上，“P4 线缆”（4-pin 连接器）是什么意思？旁边第二组 4-pin 接口又代表什么？

---

**答案：**

下面是对这两个连接器的清晰说明：

---

### 1. P4 线缆（4-pin CPU 电源连接器）

这个 4-pin ATX 连接器——正式名称为 **ATX12V P4 连接器**——是随着 2000 年 ATX12V 1.0 规范推出的标准化供电接口。它直接向主板的 CPU VRM（电压调节模块）提供 **+12V 直流电**，将高电流的 CPU 负载与主电源轨分离。

P4 线缆包含 **两根黑色线（地线）** 和 **两根黄色线（+12V 直流）**。这些线连接到主板上的一个 4-pin 接口。它是 Intel 和 AMD 主板都使用的标准电源连接器。

“P4”这个名称源于 Intel **Pentium 4** 时代，但现在已适用于所有现代 CPU。

---

### 2. “旁边”的第二组 4-pin——4+4（EPS12V）连接器

许多电源配备了一条 **8-pin EPS12V CPU 线缆，可拆分为两个 4-pin 连接器**。如果你的主板只有 4-pin CPU 插座，只需将两个半部分分开，插入其中一半即可。

因此，你在航嘉 Super 500W 上看到的是 **4+4 pin 设计**——两个 4-pin 部分并排卡在一起：

| 配置 | 使用场景 |
| --- | --- |
| **仅使用一个 4-pin 半部分** | 主板只有 4-pin CPU 电源插座（较旧或入门级主板） |
| **将两个部分卡在一起形成 8-pin** | 主板有 8-pin EPS CPU 电源插座（大多数现代主板） |

4+4 EPS12V 连接器的一半是另一半的镜像。引脚具有防呆设计（有些是方形，有些是切角/圆角），因此 **只有正确的一半才能在不强行插入的情况下适配 4-pin 主板插座**。

---

### 总结

- **P4 / 4-pin** = CPU 电源连接器，为 CPU 提供 +12V 电源。**必须插上**，否则 CPU 无法获得电力。
- **旁边的 4 个引脚** = **4+4 EPS12V** 连接器的另一半。将两个半部分卡在一起用于 **8-pin 插座**，或仅使用一半用于 **4-pin 插座**。
- 最佳做法是：将 4-pin 线缆插入 4-pin 接口，8-pin 线缆插入 8-pin 接口，而 4+4 线缆可适配任意一种接口。

---

**参考来源：**

- [What Is P4? – ComputerHope](https://www.computerhope.com/jargon/p/p4.htm)
- [All About PSU Cables and Connectors – PlayTool](https://www.playtool.com/pages/psuconnectors/connectors.html)
- [How to Connect a PSU to a 4-pin CPU Port – Corsair](https://help.corsair.com/hc/en-us/articles/360043469632-PSU-How-to-connect-a-PSU-to-a-4-pin-CPU-port)
- [ATX Compatibility Guide – PlayTool](http://www.playtool.com/pages/psucompat/compat.html)
