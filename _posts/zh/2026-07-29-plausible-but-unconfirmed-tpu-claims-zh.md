---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 可信但未经证实的TPU声明
translated: true
type: note
---

问题：关于谷歌“Frozen V2”TPU在芯片内集成SRAM并放弃台积电CoWoS用于Gemini的说法是否正确？

答案：

简短回答：**方向是合理的，但文章混合了已确认的事实、分析师的推测和部分夸张的措辞。**

核心观点：

* 谷歌确实在推动定制TPU架构以减少对NVIDIA GPU的依赖。
* 内存带宽和数据移动正成为AI加速器的主要瓶颈。
* 将更多SRAM靠近计算单元是一个真实的架构趋势。
* 但**“完全放弃CoWoS”和“SRAM直接集成到硅片内”并非公开确认的谷歌产品细节。**

让我们逐一分析。

---

## 1. 为什么片上SRAM很重要

现代AI加速器主要受限于：

```
HBM/DRAM
   |
   |  （巨大的延迟 + 能耗成本）
   v
GPU/TPU计算单元
```

最昂贵的部分是数据移动。

例如：

```
计算：
  矩阵乘法：便宜

内存移动：
  获取权重
  获取激活值
  写入中间结果
  昂贵
```

粗略的能耗层级：

```
寄存器        ~1 pJ
SRAM          ~5-20 pJ
HBM           ~100+ pJ
DDR           更高
```

因此，如果你能在TPU核心附近放置更多SRAM：

```
之前：

TPU核心 <---> HBM


之后：

+----------------------+
| TPU计算单元          |
|                      |
| SRAM缓存             |
|                      |
+----------------------+
```

你可以减少：

* 延迟
* 功耗
* 带宽压力

这正是公司探索以下方向的原因：

* SRAM缓存
* 3D堆叠
* 晶圆级计算
* 近内存计算

---

## 2. 但“没有CoWoS”是一个很大的说法

NVIDIA当前的AI GPU：

```
GPU芯片
 |
CoWoS中介层
 |
HBM堆叠
```

示例：

```
        HBM
         |
HBM -- 中介层 -- HBM
         |
       GPU芯片
```

CoWoS存在的原因是：

* HBM需要极宽的连接
* GPU芯片和HBM是不同工艺
* 制造良率更好

纯单片式方法：

```
+----------------+
| TPU            |
|                |
| SRAM           |
|                |
+----------------+
```

存在以下问题：

### 良率

大芯片更容易出现故障。

如果单个大芯片包含：

* 计算单元
* SRAM
* IO

一个缺陷就可能毁掉整个芯片。

### SRAM密度

SRAM占用大量硅面积。

示例：

1GB的SRAM缓存与逻辑单元相比非常庞大。

现代处理器通常使用：

```
CPU：
小容量SRAM缓存
+
大容量DRAM

AI：
需要巨大的内存带宽
```

---

## 3. 有趣的部分：推理 vs 训练

这种架构更适合**Gemini推理**，而非训练。

训练：

```
巨大模型
+
巨大优化器状态
+
巨大数据集
```

需要：

* HBM
* 网络
* 分布式集群

推理：

```
固定模型
重复查询
```

可以从以下方面受益：

* 定制化内存层次结构
* 固定权重
* 专用化

Gemini推理芯片可以是：

```
谷歌搜索
      |
      v
Gemini模型
      |
      v
Frozen TPU
      |
      v
高吞吐量推理
```

谷歌控制整个堆栈：

```
模型
 |
编译器
 |
TPU
 |
数据中心
```

这是他们最大的优势。

---

## 4. 与Taalas的对比

Taalas的方法更为极端。

他们基本上说：

```
传统方式：

芯片执行神经网络

Taalas方式：

芯片就是神经网络
```

权重变成硬件。

就像：

```
软件模型：

W1
W2
W3

↓

硅片布线
```

优点：

* 极快的推理速度
* 极低的功耗

缺点：

模型变化需要重新制造芯片。

这类似于ASIC与CPU的对比：

```
CPU：
通用

ASIC：
针对单一工作负载快10倍
但固定不变
```

---

## 5. 我的评估

我会给这篇文章打分：

| 说法                                 | 可信度 |
| ------------------------------------- | ---------- |
| 谷歌开发定制Gemini TPU               | 高       |
| 谷歌希望提高内存效率                 | 高       |
| SRAM更靠近计算单元是趋势             | 高       |
| Frozen V2按描述存在                  | 中/低    |
| 完全放弃CoWoS                        | 低        |
| TPU取代NVIDIA GPU                    | 过于强烈 |

真正的趋势可能是：

```
NVIDIA：
GPU + HBM + CoWoS

Google：
TPU + 定制内存层次结构

Amazon：
Trainium + Inferentia

Microsoft：
Maia

Meta：
MTIA
```

AI硬件的未来可能不是“GPU芯片突然消失”。

而是：

```
通用AI加速器
        |
        +-- NVIDIA GPU
        |
        +-- Google TPU
        |
        +-- Amazon Trainium
        |
        +-- ASIC推理芯片
        |
        +-- 晶圆级系统
```

谷歌有一个独特优势：**Gemini是他们的模型，TPU是他们的硅片，而谷歌拥有数据中心。** 这种垂直整合使他们能够采用激进的架构，而NVIDIA难以轻易复制，因为NVIDIA必须服务众多客户。

参考文献：

* Google TPU架构：[https://cloud.google.com/tpu/docs](https://cloud.google.com/tpu/docs)
* 台积电CoWoS封装：[https://www.tsmc.com/english/technology/cowos](https://www.tsmc.com/english/technology/cowos)
* NVIDIA Hopper架构：[https://www.nvidia.com/en-us/data-center/technologies/hopper-architecture/](https://www.nvidia.com/en-us/data-center/technologies/hopper-architecture/)
* Taalas AI硅片：[https://taalas.com/](https://taalas.com/)