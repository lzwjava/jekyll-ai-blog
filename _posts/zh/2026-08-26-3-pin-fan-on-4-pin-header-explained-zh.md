---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 3针风扇接4针接口详解
translated: true
type: note
---

**问题：** 为什么技嘉 H81M-DS2 主板上的 CPU 风扇使用 3 针接口，这意味着什么？

**回答：**

首先需要澄清一点：根据技嘉官方 GA-H81M-DS2 用户手册，**该主板上的所有风扇接口实际上都是 4 针的**。因此，如果你的风扇插头只有 3 针，那是**风扇本身**的特性，而非主板的接口问题。

以下是这种情况发生的原因及其含义：

**为什么你的风扇可能只有 3 针：**

较旧或预算型 CPU 散热器通常配备 3 针连接器。标准的 3 针风扇连接器包含三根信号线：电源（+12V）、接地和测速/转速反馈线。主板通过改变电源引脚上的电压（通常在约 5V 到 12V 之间）来控制 3 针风扇的速度。

**它与 4 针（PWM）的区别：**

在 4 针接口上，速度通过 PWM（脉宽调制）信号控制——该独立信号精确指示风扇的转速，而风扇始终接收完整的 12V 电源。而在 3 针接口上，速度控制则通过改变电压实现。

两种风扇类型在物理上都兼容两种接口类型，因此 3 针风扇完全可以插入 4 针接口——第四个针脚只是闲置不用。

**将 3 针风扇插入 4 针接口时会发生什么：**

接口上的 PWM 引脚将不会被使用。除非你在 BIOS 中将其设置为 DC 模式（电压调节）来控制风扇，否则风扇很可能会一直以 100% 的速度运行。H81M-DS2 的 BIOS 确实提供了风扇速度控制设置，因此你可以将接口切换到 DC 模式以实现基本的转速调节。

**总结表：**

|          | 3 针风扇                 | 4 针风扇           |
| :------- | :----------------------- | :----------------- |
| 速度控制 | 电压（DC）               | PWM 信号           |
| 精确度   | 较低                     | 较高               |
| 兼容 4 针接口？ | ✅ 可以（第 4 针闲置） | ✅ 可以           |

---

**参考资料：**
- [技嘉 GA-H81M-DS2 用户手册 (ManualsLib)](https://www.manualslib.com/manual/577266/Gigabyte-Ga-H81m-Ds2.html?page=12)
- [CPU 风扇接口指南 — SunbeamTech](https://sunbeamtech.com/hardware-guides/cpu-fan-header-where-it-is-and-how-to-use-it/)
- [3 针与 4 针风扇区别 — ElectronicsHub](https://www.electronicshub.org/3-vs-4-pin-fans/)
- [3 针与 4 针兼容性 — PositionIsEverything](https://www.positioniseverything.net/can-i-use-4-pin-fans-on-3-pin-headers-or-vice-versa/)