---
audio: false
generated: true
image: false
lang: zh
layout: post
title: R47与电容邻近问题
translated: true
type: note
---

**问题：为什么 Quadro 410/401 GPU PCB 上的 R47 功率电感要放在电容旁边？**

简短回答：**因为 R47 和电容是一对电源滤波组件，它们的物理距离很重要。**

R47 不是电阻。在 GPU PCB 上，标记 **R47 通常表示一个 0.47 µH 的功率电感/扼流圈**，它是 VRM/DC-DC 电源路径的一部分。（[阿里巴巴电子][1]）

典型路径：

```
12V PCIe / 辅助电源
          |
          |
       MOSFET 开关
          |
          |
       R47 电感
          |
          |
     +----+----+
     |         |
   电容器      GPU 核心 / 显存供电轨
     |
    GND
```

电感与电容构成 **LC 低通滤波器**：

$$
V_{out} = \text{平滑后的直流电压}
$$

MOSFET 以数百 kHz 至 MHz 的频率快速开关。电感阻止电流突变：

$$
V_L = L \frac{di}{dt}
$$

电容吸收电压纹波：

$$
I_C = C\frac{dV}{dt}
$$

两者协同工作：

* **电感阻隔高频开关噪声**
* **电容储存能量并提供瞬态电流**
* GPU 获得稳定电压

这就是为什么你经常看到：

```
VRM MOSFET → R47 → 电容 → GPU
```

这些元件紧密排布在一起。（[Cadence PCB 资源][2]）

---

### 为什么要把电容紧挨着 R47 放置？

想象一下：

```
错误布局：

R47 -------------------- 电容 -------- GPU
        长走线
```

PCB 走线本身会变成一个不需要的电感。

在高频下：

```
走线电感 + 电容
```

会改变滤波器特性。

电容无法足够快地响应，因为电流需要经过额外的电感。

正确布局：

```
R47
 |
 |
电容
 |
GPU
```

小的回路面积 = 更低的寄生电感 = 更好的瞬态响应。基于这个原因，PCB 电源设计通常会尽量缩短电源元件之间的距离。（[AMD 文档][3]）

---

### 从 GPU 维修视角来看

当你看到：

```
[ MOSFET ] [ R47 ] [ 电容 ] [ GPU ]
```

你就可以解读出电源流动路径。

举例：

* MOSFET 烧毁 → 开关问题
* R47 开裂/断路 → GPU 供电轨断开
* 电容短路 → GPU 无法上电，可能触发电源保护
* 电容缺失 → 电压不稳定，负载下崩溃

维修时：

1. 测量 R47 两侧电压。

之前：

```
12V 侧
```

之后：

```
滤波后的 GPU 电压
```

2. 检查电容对地电阻。

R47 后端的电容如果短路，会将整个 GPU 供电轨拉低。

---

GPU PCB 设计的有趣之处在于，你几乎可以“读懂”工程师的思路：

* 大的灰色方块 = 大电流电感
* MLCC 集群 = 高频滤波
* MOSFET + 驱动 IC + 电感 = 一个 VRM 相位
* GPU 周围多相位 = 分散电流和热量

现代 GPU 供电本质上就是一个集成在计算芯片旁边的小型大电流开关电源。（[Cadence PCB 资源][4]）

你研究坏 GPU 的想法，实际上非常接近硬件工程师的学习方式：通过物理布局逆向推导电源树。你可以拿一块坏掉的 Quadro，追踪每一条 R47 → 电容 → MOSFET 路径，从而重构 VRM 设计。

[1]: https://electronics.alibaba.com/buyingguides/r47-motherboard-guide-what-it-really-is-when-to-care?utm_source=chatgpt.com "R47 主板指南：它到底是什么，何时需要关注"
[2]: https://resources.pcb.cadence.com/blog/whats-needed-to-get-to-ka-currents-on-a-pcb?utm_source=chatgpt.com "PCB 上实现 kA 级电流需要什么"
[3]: https://docs.amd.com/r/en-US/ug583-ultrascale-pcb-design/Capacitor-Placement-Background?utm_source=chatgpt.com "电容布局背景 - 电容布局背景 - UG583"
[4]: https://resources.pcb.cadence.com/pcb-design-blog/2019-what-is-a-vrm-and-why-does-my-cpu-gpu-need-one-2?utm_source=chatgpt.com "什么是 VRM，我的 CPU/GPU 为什么需要它？| 高级 PCB 设计博客 | Cadence"