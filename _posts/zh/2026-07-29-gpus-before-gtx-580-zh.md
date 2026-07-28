---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GTX 580之前的GPU
translated: true
type: note
---

问题：在NVIDIA GTX 580之前存在哪些GPU？

答案：

在 **NVIDIA GeForce GTX 580（2010年）** 之前，GPU领域主要专注于图形处理以及早期的CUDA计算。GTX 580是NVIDIA **Fermi** 架构的巅峰之作，但它之前还有几个重要的架构世代。

![Image](https://images.openai.com/static-rsc-4/DmevK_vQrcZm9CTO35MiBcb1OWw-i8jWLUkcOC3zc5j4texXDGCX6TLOcI-ssnOoju_cU2oOsl-7J11SFwnVL94C8New4QvG43cG4bkWFAYzeY_AfyhjBcq5hEjfpj-yJS5scNkTON5rzArq2sqvOTjN0wzUfqvhAjTGq9X5MuaBRvJq_vdRUZnp-YlA8fbE?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/Q2SGf2fm382wjq2wWxSBxbpVJzrAiZdsptDRJzSEf3lDOS06MHHR3wSWY0t6ujKbslh5LA9TE5EbiiABB2S519OsduYzXzRDVOsvZKlOpQ4O8hLETqW_9Y6LNJWksjM8LRkHrm5T9-SLcXL2P-dRzSZRjvEjTZaQb2YLi7RO0hZUQz9HteiWSia8e8MKcRRq?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/S5f6FzwbzO72SG3Djl4n9ye6Hmmn8oy3XEYnluw_d-tf6PNklYX6YnjtFhpPiEJ5n5TUMOfbGTDkH1GknzBWV8kU3glDrgaUcyWfhRO6w3cocJMpvhNxBIp3ReJLJ0jlKk9BhH9r2-DRe2u6QZ_9mXuAsbyzNnmuILH4nwFgRMq-_GZBA8jH9dSAhZqQctXi?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/KiiQuOzE7Pb2hWVcRES3fD80a1sk7hzeaBZGaVFC4v_oT9tLeJ1gSVre5uOqRcfM03vH739S8TqyPYyzRsrONArvH21cxqUuSFfM76tLFOFtqXcNCEXpvrqEG0ZBeGQXSiD1l6bOc0KXUefyXsnPSLc20hdlPeDgxlzUg8LTzsg8gws8ccJsuhuGEJX0M9dz?purpose=fullsize)

## GTX 580 之前的 NVIDIA GPU 时间线

| 年份 | GPU              | 架构          | CUDA 核心数 | 显存    | 重要性                        |
| ---- | ---------------- | ------------- | ----------: | ------: | ----------------------------- |
| 2006 | GeForce 8800 GTX | Tesla         |         128 |   768MB | 首个CUDA时代的GPU             |
| 2008 | GeForce GTX 280  | Tesla         |         240 |     1GB | 早期 GPGPU                    |
| 2009 | GeForce GTX 285  | Tesla 刷新版  |         240 |     1GB | 流行的计算卡                  |
| 2010 | GTX 480          | Fermi         |         480 |   1.5GB | 首个真正用于CUDA计算的GPU     |
| 2010 | **GTX 580**      | Fermi 刷新版  |         512 |   1.5GB | AlexNet 时代的 GPU            |

---

## 重要的那一款：GeForce 8800 GTX（2006年）

NVIDIA GeForce 8800 GTX 是一款具有历史意义的GPU。

为什么？

在此之前：

```
GPU = 固定功能图形管线
```

在 G80 架构之后：

```
GPU = 可编程并行处理器
```

NVIDIA 引入了：

* CUDA（2007年）
* 统一着色器架构
* 通用 GPU 计算（GPGPU）

许多研究人员开始问：

> “我们能否在这个大规模并行芯片上运行神经网络？”

---

## 迈向深度学习的GPU演进

### 1. 前CUDA时代（2006年之前）

GPU 主要是：

```
CPU
 |
 +-- GPU
      |
      +-- 三角形
      +-- 像素
      +-- 着色器
```

编程非常困难。

---

### 2. CUDA 时代开启（2006-2010年）

示例：

GTX 280：

```
240 个 CUDA 核心

每个核心：
    小型浮点运算单元

并行：
    数千个线程
```

研究人员可以编写：

```cpp
kernel<<<blocks, threads>>>(data);
```

并运行科学计算负载。

---

### 3. Fermi 架构世代（2010年）

GTX 480 / GTX 580 的设计更接近计算加速器：

```
Fermi GPU

SM
 |
 +-- CUDA 核心
 +-- 共享内存
 +-- L1 缓存
 +-- 双精度单元
```

这更接近今天的人工智能 GPU。

---

## 早期深度学习是否使用了 GTX 280/285？

是的。

在 AlexNet 之前，包括 Hinton 实验室在内的团队已经在尝试使用 GPU。

示例：

* 神经网络的 CUDA 实现
* GPU 加速的卷积
* 受限玻尔兹曼机（RBM）

Hinton 团队在 2009–2011 年左右使用 GPU 使深度学习变得实用。

但 AlexNet 是那个时刻：

```
GPU + CNN + 大规模数据集 + ReLU
=
现代深度学习
```

---

## 与你的 RTX 4070 的有趣对比

你的 RTX 4070：

```
Ada Lovelace
2023 年

5888 个 CUDA 核心
12GB 显存
~29 TFLOPS FP32
```

GTX 580：

```
Fermi
2010 年

512 个 CUDA 核心
1.5GB 显存
~1.5 TFLOPS FP32
```

RTX 4070 大致是：

* FP32 计算性能约 20 倍
* 显存 8 倍
* 内存效率大幅提升
* 专为 AI 设计的 Tensor Core

今天一块消费级 RTX 4070 远远超过整个 AlexNet 训练设置。

令人惊讶的不是 AlexNet 使用了弱硬件——而是他们在其他人之前发现了正确的缩放定律：

```
更多数据
+ 更大的神经网络
+ GPU
+ 更好的优化
=
深度学习革命
```
