---
audio: false
generated: true
image: false
lang: zh
layout: post
title: HBM更优，GDDR对消费者更便宜
translated: true
type: note
---

**问题：既然HBM2更好，为什么NVIDIA在消费级GPU上从HBM2退回到GDDR6/GDDR6X？**

**回答：**

简单来说：**HBM在技术上更优，但GDDR价格低得多，且更容易在消费级GPU上扩展。**

NVIDIA并非从HBM2“降级”至GDDR6X，而是进行了市场细分：

```
数据中心：
V100 → A100 → H100 → H200
       HBM2 → HBM2e → HBM3/HBM3e

消费级：
GTX/RTX Pascal → Turing → Ampere → Ada
              GDDR5 → GDDR6 → GDDR6X
```

两者优化目标不同。

## 1. HBM价格高昂

HBM需要：

```
GPU芯片
  |
硅中介层
  |
HBM堆叠
```

示例：

```
         HBM
       ||||||
    ===========
    中介层
    ===========
       GPU
```

GPU和内存成为一个先进封装体。

问题：

* 封装成本高
* 制造良率低
* 供应商有限
* PCB设计困难

对于一块599美元的RTX显卡，使用HBM会破坏其成本结构。

GDDR：

```
GPU ---- PCB ---- GDDR芯片
GPU ---- PCB ---- GDDR芯片
GPU ---- PCB ---- GDDR芯片
```

价格低得多。

---

## 2. 消费级工作负载对极高带宽需求较低

V100：

```
32GB HBM2
900 GB/s
```

设计用于：

```
矩阵乘法
大规模批量训练
科学计算
```

游戏GPU：

```
RTX 4070：
12GB GDDR6X
504 GB/s
```

同时还具备：

```
超大L2缓存
压缩技术
渲染优化
```

游戏不像训练那样需要持续传输大型张量。

---

## 3. NVIDIA在需要之处仍使用HBM

以H100为例：

```
H100 SXM：
80GB HBM3
3.35 TB/s 带宽
```

因为AI训练：

```
Transformer：

注意力：
Q @ K^T

MLP：
X @ W
```

本质上就是：

```
大规模矩阵乘法
+
内存搬运
```

带宽决定一切。

---

## 4. GDDR6X为何变得足够好

美光的GDDR6X采用PAM4信号：

传统方式：

```
0 → 1
两个电压级别
```

GDDR6X：

```
00
01
10
11

四个电压级别
```

每个时钟周期传输更多比特。

因此NVIDIA获得了：

```
GDDR6：
14-16 Gbps

GDDR6X：
19-24 Gbps
```

无需承担HBM的成本。

---

## 5. 有趣的AI视角

你对MI50/V100的观察其实没错：

旧款数据中心显卡有一个隐藏优势：

```
MI50：
16GB HBM2

V100：
16/32GB HBM2

RTX 4070：
12GB GDDR6X
```

对于某些AI工作负载：

```
显存容量
+
内存带宽
```

比游戏时代的TFLOPS更重要。

这就是为什么二手V100 32GB、MI50、P100等仍有市场。

但NVIDIA不在RTX显卡上使用HBM的原因很简单：

```
RTX客户：
“我想要599美元的GPU”

AI客户：
“我花30,000美元买H100”

不同的市场。
```

未来很可能是分化的架构：

* 消费级：GDDR7 + 更大的缓存
* AI/数据中心：HBM4/HBM5 + 庞大的内存池

HBM不会取代GDDR；它们针对不同的成本效益进行了优化。
