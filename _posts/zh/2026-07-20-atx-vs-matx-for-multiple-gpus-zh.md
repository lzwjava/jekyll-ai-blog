---
audio: false
generated: true
image: false
lang: zh
layout: post
title: ATX与mATX多GPU对比
translated: true
type: note
---

问题：在使用多张GPU的情况下，什么是PCIe延长线，为什么人们推荐使用ATX主板而非mATX来安装两张或更多GPU？

答案：

**PCIe 延长线（PCIe riser cable / PCIe extension cable）** 是一种用于延长PCIe插槽的线缆，能将GPU从主板上移开。

正常情况下：

```
GPU
 |
 |  (直接连接)
 |
主板上的PCIe x16插槽
```

使用延长线后：

```
主板PCIe插槽
        |
        |
   PCIe延长线
        |
        |
      GPU
```

GPU不再需要直接物理安装在主板上方。

常见例子：

* 矿机
* AI多GPU服务器
* 小型机箱
* 配备大型GPU的工作站

典型的延长线包含：

```
PCIe x16主板适配器
        |
        |
 带状线缆
        |
        |
PCIe x16 GPU适配器
```

通常电气连接仅支持 **PCIe x1/x4/x8**，取决于延长线类型。许多矿用延长线使用PCIe x1，因为带宽对挖矿并不重要。

对于AI推理/训练，通常需要：

* PCIe x16物理插槽
* 尽可能保证每张GPU至少PCIe x8电气连接
* 使用高质量屏蔽延长线（如果采用延长方案）

---

## 为什么2张以上GPU推荐ATX而非mATX？

问题不仅在于“插槽数量”，还涉及：

1. **物理间距**
2. **PCIe通道**
3. **散热**

示例：

### mATX主板

```
CPU

PCIe x16
========
RTX 3090（3槽）

PCIe x4
====
被遮挡
```

一张RTX 3090 / 4090通常厚度为2.5~4个槽位。

安装第一张GPU后：

```
GPU
GPU散热器
GPU散热器
GPU散热器
```

它会覆盖下一个PCIe插槽。

因此即使主板提供：

```
PCIe x16
PCIe x16
```

物理上也没有空间。

---

ATX：

```
CPU

PCIe x16
========
（空余间距）

PCIe x16
========

PCIe x4
====
```

示例：

```
RTX3090
  |
  | 2槽间距
  |
RTX3090
```

两张卡都能获得良好散热。

---

## PCIe通道问题

消费级平台也存在限制。

示例：

### Intel i9-13900K

CPU PCIe：

```
CPU
 |
 +-- PCIe 5.0 x16
 |
 +-- PCIe 4.0 x4
```

因此主板厂商会进行拆分：

```
GPU1: x8
GPU2: x8
```

或：

```
GPU1: x16
GPU2: 芯片组 x4
```

具体取决于设计。

对于AI工作负载：

* LLM推理：
  * PCIe带宽影响较小
  * 多张GPU可正常工作

* 训练：
  * 梯度同步至关重要
  * PCIe带宽影响很大

---

## 多GPU配置示例

### 廉价AI工作站

```
ATX主板

RTX3090
PCIe x8

RTX3090
PCIe x8

128GB内存

850W~1200W电源
```

良好。

---

### 使用延长线的mATX

可行：

```
mATX

GPU1
 |
PCIe延长线

GPU2
 |
PCIe延长线
```

但存在：

* 气流更差
* 通道数更少
* 线缆问题更多
* 调试更困难

这在矿机中常见，对AI来说不太理想。

---

## 服务器/工作站主板解决了这些问题

对于4-8张GPU：

```
EPYC主板

CPU PCIe通道：

128通道

GPU1 x16
GPU2 x16
GPU3 x16
GPU4 x16
GPU5 x16
GPU6 x16
GPU7 x16
GPU8 x16
```

例如：

* AMD EPYC
* Intel Xeon W
* Xeon Scalable

这就是为什么AI服务器会使用技嘉G292-Z20、超微、华硕ESC系列等主板。

---

对于你的RTX 4070 / 可能的RTX3090多GPU实验：

* 2张GPU → 消费级ATX主板合理
* 3-4张GPU → 工作站/服务器主板更佳
* 8张GPU → EPYC + PCIe延长线/背板

PCIe延长线主要是一种**机械解决方案**，它们不会增加PCIe通道数量。实际带宽由主板和CPU决定。
