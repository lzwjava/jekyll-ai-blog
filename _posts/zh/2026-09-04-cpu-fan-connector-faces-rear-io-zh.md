---
audio: false
generated: true
image: false
lang: zh
layout: post
title: CPU风扇接口朝向后部I/O
translated: true
type: note
---

**问题：** 在华硕 H81M-K 主板上安装 CPU 散热器/风扇时，风扇接口应朝向哪个方向——PCIe 插槽、内存插槽、USB 接口还是其他位置？

**回答：**

根据华硕 H81M-K 的官方布局，以下是需要了解的信息：

**CPU_FAN 接口位置**

根据 H81M-K 主板布局，`CPU_FAN` 接口位于主板的**左上角区域**，靠近 ATX12V 电源接口，位于 LGA1150 CPU 插座上方——因此它最靠近主板的**后部 I/O 侧**（带有视频/USB 接口的一侧）。

**风扇接口应朝向哪个方向？**

大多数英特尔原装散热器（推针式）的风扇连接线较短。由于 `CPU_FAN` 位于**左上角**（靠近后部 I/O 面板 / ATX12V 电源接口），因此您应：

- **将风扇的线缆朝向左上角 / 后部 I/O 侧**——这里正是 `CPU_FAN` 接口所在位置。
- 这意味着接口通常朝向**远离 PCIe 插槽**（位于底部）、**远离内存/DIMM 插槽**（位于 CPU 右侧）以及**远离内部 USB 接口**（位于右下角区域）。

**H81M-K 视觉方向总结：**

| 主板边缘 | 此处有什么 |
|---|---|
| 顶部（后部 I/O） | CPU_FAN 接口 ← **线缆朝向此处** |
| 右侧 | DDR3 内存插槽 |
| 底部 | PCIe x16 插槽、USB 接口、SATA |
| 左侧 | ATX 24-pin 电源 |

**实用提示：** 对于英特尔推针式散热器，线缆固定在风扇的某一角。在按下推针之前，先旋转整个散热器/风扇组件，使线缆角最靠近 `CPU_FAN` 接口，然后锁定推针。CPU_FAN 接口支持最大 1A（12W）的 CPU 风扇，只有 4-pin CPU 风扇支持华硕 Fan Xpert 功能。

**参考资料：**
- [ASUS H81M-K 用户手册 – 主板布局 (ManualsLib)](https://www.manualslib.com/manual/565354/Asus-H81m-K.html)
- [ASUS H81M-K – 风扇接口第 24 页 (ManualsLib)](https://www.manualslib.com/manual/565354/Asus-H81m-K.html?page=24)
- [H81M-K 布局内容 – ManualOwl](https://www.manualowl.com/m/Asus/H81M-K/Manual/372249?page=12)