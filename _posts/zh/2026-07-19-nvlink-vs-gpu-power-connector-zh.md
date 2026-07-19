---
audio: false
generated: true
image: false
lang: zh
layout: post
title: NVLink对比GPU电源连接器
translated: true
type: note
---

问题：NVLink在RTX 3090上如何物理连接？它是否与GPU电源接口（RTX 4070上的12针接口）有关？

答案：

不。**NVLink与GPU电源接口毫无关系。**

混淆源于两者都是“GPU顶部的微型接口”，但它们完全不同。

## RTX 4070 电源接口

RTX 4070 使用：

* **12VHPWR（12+4针）电源接口**（在许多型号上）

它看起来像：

```
PSU 线缆
    |
    v
[ 12VHPWR ]
+----------------+
| 电源输入      |
+----------------+

RTX 4070 PCB
```

用途：

```
PSU ---> GPU
```

它提供电力。

---

## RTX 3090 电源接口

大多数 RTX 3090 显卡使用：

```
8针 PCIe
8针 PCIe
```

或有时：

```
8针
8针
8针
```

示例：

```
PSU
 |
 +----8 针----+
              |
 +----8 针----+ ---> RTX 3090
```

RTX 3090 功耗：

* 典型约 350W
* 在功率限制下更高

因此它需要比 RTX 4070 更多的电源接口。

---

## RTX 3090 上的 NVLink 在哪里？

RTX 3090 在显卡顶部边缘有一个**独立的 NVLink 金手指接口**。

示例：

```
                 GPU 顶部

        NVLink 接口
              ||
              ||
  +-------------------------+
  |                         |
  |       RTX 3090          |
  |                         |
  +-------------------------+

        |             |
     8 针           8 针
```

NVLink 桥接器位于此处：

```
RTX 3090 #1

  [ NVLink 端口 ]
          ||
          ||
  [ NVLink 桥接器 ]
          ||
          ||
  [ NVLink 端口 ]

RTX 3090 #2
```

---

## 重要提示：NVLink 不是 PCIe 电源

存在三个独立的连接：

### 1. 电源

```
PSU
 |
8 针接口
 |
GPU
```

### 2. PCIe 接口

```
GPU
 |
PCIe 插槽
 |
主板
```

### 3. NVLink

```
GPU
 |
NVLink 桥接器
 |
GPU
```

它们服务于不同的目的。

---

## RTX 3090 AI 工作站示例

两块 RTX 3090：

```
             CPU
              |
        PCIe 主板
        /              \
       /                \
 RTX3090 #1          RTX3090 #2
    |                   |
 8针+8针           8针+8针
    |
    +==== NVLink ====+
```

你需要：

* 带有两个 x16 插槽（物理）的主板
* 足够的 PCIe 通道
* 大功率 PSU（850W-1200W）
* 足够的散热气流

---

## 另一个 AI 相关的注意事项

对于 LLM 训练，NVLink 带宽很重要：

RTX 3090：

* PCIe 4.0 x16：理论双向约 32 GB/s
* NVLink：双向约 112 GB/s

因此张量并行通信可以改善性能。

但现代框架：

* PyTorch DistributedDataParallel
* DeepSpeed ZeRO
* FSDP

通常也能很好地通过 PCIe 工作。

对于你的情况（本地 LLM 实验），RTX 3090 的主要吸引力仍然是：

```
24GB VRAM × 2 = 48GB 总容量
```

NVLink 是一个不错的优化，但并非购买它的主要原因。