---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 同步时分复用详解
translated: true
type: note
---

Question: What is **同步时分多路复用（Synchronous TDM, Synchronous Time-Division Multiplexing）**?

Answer:

**同步时分多路复用**是一种技术，它让**多个低速数据流通过轮流使用固定时隙的方式共享一条高速通信链路**。

![Image](https://images.openai.com/static-rsc-4/TBf4IvUxKLzd1irrBbNo-hyqbz8GdkEsxEwstey5oX_GsHMibfG1QBFFBRJex-oCJvFOzRACsaa3q-ckOnruGf_M7qpbJyJ10DWVzJRxUjHMzVkZEpF68jx-KjsHeB66j-NDHcD-5WgO-T8bijKgp5ETNNXhM3wdD7xsOHl_6bjFA6kCfYjoU1N8ESy_xUpg?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/QuUf3sULJA4PPOXyEQNDG8DFQjOQExHSgkYXg9EZVgzPCON1Cfc4NzR39Um2Kq1YAMtzft9XceLM2LrtsqyLfynLj-1s5uOlB5dpHyUI3ODqSXC1WqMYqvQ2mWER1Qs6hxkOdVu3XwvHIhQ82MTbr4lzpVqPcyJsBoy_d80J8WHF0FbpJOO8PP05UYMYL1f8?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/NfvsF1s4cuNFzJYirPhHF-dBCTpjKxdzyvVc3P5qFBWl8ChwVSWqsvjgPOx71D8vrPPjTl-tr-3BNSqIpc-YOy8Mc61yu6A3pK1BA-iKbIeSA1sdmaZCVFEhDTQf1NYd0OZeEBV6vypKiiW3RSquG0Yqma8rY6RsCThYOu5cTUqnSQeVinxYascA4KnjTrr4?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/UAkHOF5GUcuHDGcTEG4A-KU_f5Z9DAPRWs966cvZ4zUVuxDi-riNaxL3srr2U1gviZJ9rQnsg9SeUPs7gROxHmdIyhEgePOnWDwwVv91u1yEPaDuIOP7r-dbmU3RxSvQ355G1i7nYPfErr1q3uP5v_uqAMa3kpGQLRv7MLEom3i2lYI6z59Q6EEDCMIjq4Bm?purpose=fullsize)

### 1. 基本思想

假设我们有四条输入通道：

```text
通道 A ──┐
通道 B ──┤
通道 C ──┼──> [ 复用器 ] ──> 高速链路
通道 D ──┘
```

TDM 将时间划分为一个个小的**时隙**：

```text
时间 ─────────────────────────────────────>

| A | B | C | D | A | B | C | D | A | B | ...
```

每个通道在每个帧中获得**固定的位置**。

例如：

```text
帧 1: | A | B | C | D |
帧 2: | A | B | C | D |
帧 3: | A | B | C | D |
```

接收端知道：

> 时隙 1 → A
> 时隙 2 → B
> 时隙 3 → C
> 时隙 4 → D

因此它可以对合并后的数据流进行解复用。

---

### 2. 为什么称为“同步”？

因为发送端和接收端同步到相同的**时隙/帧结构**。

例如：

```text
             帧
       ┌─────────────────┐
       │ A │ B │ C │ D   │
       └─────────────────┘
         ↑   ↑   ↑   ↑
       固定  固定  固定  固定
       时隙  时隙  时隙  时隙
```

即使通道 C **没有数据要发送**，它的时隙通常仍然被保留：

```text
| A | B | -- | D | A | B | -- | D |
          ↑
       未使用
```

这是同步 TDM 的关键特征。

---

### 3. 与统计 TDM 的对比

这可能是考试中最重要的区别。

**同步 TDM：**

```text
| A | B | C | D | A | B | C | D |
```

每个通道都获得一个时隙，**无论它是否有数据**。

**统计 TDM：**

```text
| A | C | C | D | A | D | B | C |
```

时隙被动态分配给实际有数据的通道。

因此：

|                     | 同步 TDM                     | 统计 TDM                       |
| ------------------- | ---------------------------- | ------------------------------ |
| 时隙分配            | 固定                         | 动态                           |
| 空闲通道的时隙      | 通常浪费                     | 可被其他通道使用               |
| 效率                | 流量突发时较低               | 较高                           |
| 控制复杂度          | 简单                         | 更复杂                         |
| 同步需求            | 需要                         | 需要，此外还需要寻址/控制信息  |

---

### 4. 示例

假设有四条电话通道，每条通道产生：

```text
64 kb/s
```

使用同步 TDM：

```text
A = 64 kb/s
B = 64 kb/s
C = 64 kb/s
D = 64 kb/s
```

复用器将它们合并：

```text
64 + 64 + 64 + 64 = 256 kb/s
```

忽略帧/开销，输出链路大约需要：

```text
256 kb/s
```

传输看起来像：

```text
A1 B1 C1 D1 A2 B2 C2 D2 A3 B3 C3 D3 ...
```

在另一端：

```text
                    ┌──> A
高速数据流 ──┼──> B
                    ├──> C
                    └──> D
```

解复用器利用已知的时隙位置恢复每条通道。

---

### 5. 核心思维模型

可以把它想象成一个**轮询 CPU 调度器**：

```text
A → B → C → D → A → B → C → D → ...
```

只不过这里分配的并非 CPU 时间，而是**通信时间**。

因此一句话定义是：

> **同步时分多路复用将一条共享通信链路划分为固定、周期性重复的时隙，并为每个输入通道分配一个预定的时隙。**

需要记住的两个词是：

**固定时隙 + 周期性重复**。

下一步有用的内容是推导 **TDM 帧/时隙时长和比特率计算**，包括常见的中国网络考试题目。