---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 'FreeToken: 缓存感知的MoE卸载'
translated: true
type: note
---

问题：FreeToken 的核心思想基本上是**多级缓存 + 卸载**吗？

回答：

是的，这是核心直觉，但更精确地说：

**FreeToken = 智能多级内存管理 + 面向 MoE 推理的自适应卸载。**

它不仅仅是“当 GPU 显存不足时把部分权重放到 RAM 里”。关键之处在于**决定什么内容应该放在哪里、以及何时放置**。

可以像计算机架构工程师那样思考。

---

## 传统视角

GPU 的显存有限：

```
GPU VRAM (快速, 小容量)
        |
        |
PCIe
        |
        |
CPU RAM (慢速, 大容量)
        |
        |
SSD (极慢, 巨大)
```

一个简单的系统：

```
加载模型
    |
    v
如果 GPU 显存满：
    将其他所有内容卸载到 CPU
```

问题：

MoE 路由是动态的。

示例：

```
Token 1:
路由器 -> Expert 3, Expert 8

Token 2:
路由器 -> Expert 50, Expert 71

Token 3:
路由器 -> Expert 3, Expert 8
```

如果你不断移动：

```
CPU RAM -> GPU
GPU -> CPU
```

PCIe 就会成为瓶颈。

---

## FreeToken 的思路

将内存视为一个层次结构：

```
                热

        GPU VRAM cache
              |
              |
        CPU RAM cache
              |
              |
        SSD storage

                冷
```

类似于 CPU 缓存：

```
CPU

L1 cache  <-- 非常快
L2 cache
L3 cache
RAM
SSD
```

问题变成了：

> 哪些专家值得占用昂贵的 GPU 空间？

---

## 示例

假设一个 400B 参数的 MoE 模型：

```
专家:

E1
E2
E3
...
E128
```

但针对你的工作负载：

```
大多数 token 使用:

E7   40%
E21  25%
E50  15%

其他很少使用
```

那么：

GPU:

```
E7
E21
E50
```

CPU:

```
E1-E128 剩余部分
```

当路由器请求：

```
需要 E7
```

快速：

```
GPU 缓存命中
```

当：

```
需要 E99
```

取回：

```
CPU -> GPU
```

---

## 更深层的联系

这基本上就是**将 LLM 推理视为操作系统问题**。

模型巨大：

```
模型 = 虚拟内存空间
```

硬件：

```
VRAM = 缓存
RAM = 内存
SSD = 磁盘
```

推理引擎变成：

```
             路由器

               |
               v

       内存管理器

       /      |       \

    VRAM     RAM     SSD
```

---

## 为什么这对消费级 GPU 很重要

以前：

```
需要 80GB 显存的 GPU
才能运行 70B+ 模型
```

有了更好的系统后：

```
24GB GPU
+
128GB RAM
+
智能缓存

可以运行更大的模型
```

速度达不到数据中心级别，但它改变了可及性。

---

对于构建本地 LLM 系统的人来说，重要的层次逐渐变成：

```
1. 模型架构
   (Transformer, MoE)

2. 量化
   (FP16 -> INT8 -> INT4)

3. KV 缓存优化

4. 权重缓存 / 专家缓存
   (FreeToken 风格)

5. 内核优化
   (FlashAttention, CUDA kernels)

6. 硬件拓扑
   (PCIe, NVLink, 内存带宽)
```

FreeToken 主要针对**#4：模型权重移动与缓存**，尤其是针对 MoE。这与 CPU 缓存设计理念相同：**最快的存储器就是你避免访问的那一个。**
