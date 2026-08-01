---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Taalas 产品概览
translated: true
type: note
---

## Taalas 一句话总结

**Taalas 正在制造一种 ASIC，将 AI 模型本身"编译到硅片中"——他们不是让 LLM 软件在通用 GPU 上运行，而是为特定模型创建定制芯片。** ([Taalas][1])

不妨这样理解：

```
传统 GPU：

Llama 权重
      |
      v
CUDA 内核
      |
      v
NVIDIA GPU
      |
      v
输出文本


Taalas：

Llama 权重 + 架构
      |
      v
定制 ASIC 硅片
      |
      v
输出文本
```

这更接近于**将神经网络直接"烧录"到硬件中**。

---

## 产品：Taalas HC1

他们的首款产品是 **HC1 技术演示器**。它运行：

*   模型：Llama 3.1 8B
*   工艺：台积电 6nm
*   芯片尺寸：815 mm²
*   晶体管：约 530 亿
*   服务器功耗：2.5 kW

([Taalas][1])

有趣的地方在于：

> 权重不像 GPU 推理那样存储在 HBM/DDR 中。

取而代之的是：

```
GPU 推理：

HBM
 |
 | 加载权重
 v
张量核心
 |
 v
下一个 token


Taalas：

硅逻辑门
 |
 v
矩阵乘法
 |
 v
下一个 token
```

芯片成为了模型的物理实现。

---

## 为何速度极快？

LLM 推理的当前瓶颈：

```
GPU 计算速度很快

但是...

数据搬运是主要限制

HBM ---> GPU ---> SRAM ---> 张量核心
```

每次生成 token 都需要：

1.  加载权重
2.  计算注意力
3.  计算 MLP
4.  写入输出
5.  重复

大量能量消耗在数据搬运上。

Taalas 试图消除这一点：

```
权重
   |
   v
已内置于芯片

无 HBM 带宽问题
无 PCIe 流量
无 CUDA 调度开销
```

这与以下技术类似：

*   TPU 专用化
*   Groq LPU
*   Cerebras 晶圆级引擎

但更为极致。

---

## 宣称的性能

针对 Llama 3.1 8B：

*   根据 Taalas 的测量，**每个用户约 17,000 tokens/秒**。([Taalas][1])

对比常规体验：

```
RTX 4090：
约 50-150 tok/s

H100：
数百 tok/s

快速推理系统：
1000+ tok/s

Taalas：
17000 tok/s
```

响应几乎变得即时。

([heise.de][2])

---

## 巨大的权衡

缺点显而易见：

GPU：

```
下载：

Llama
Qwen
DeepSeek
Mistral
...

可以运行任何模型
```

Taalas 芯片：

```
这块硅片 = Llama 3.1 8B

无法神奇地变成：

Qwen3-235B
DeepSeek-V3
GPT-5
```

需要一次新的流片。

所以：

|                        | GPU      | Taalas ASIC             |
| ---------------------- | -------- | ----------------------- |
| 灵活性                 | ⭐⭐⭐⭐⭐    | ⭐                       |
| 速度                   | ⭐⭐⭐      | ⭐⭐⭐⭐⭐                   |
| 每 token 成本          | 好       | 潜在极优                |
| 新模型支持             | 即时     | 需要重新设计芯片        |
| 编程                   | CUDA     | 硬件特定                |

---

## 为何这个想法有趣

AI 产业正从：

```
一个巨大的通用加速器
        |
        v
NVIDIA GPU
```

转向：

```
不同的工作负载
        |
        +-- 训练 GPU
        |
        +-- 推理 ASIC
        |
        +-- 语音 ASIC
        |
        +-- 智能体 ASIC
        |
        +-- 边缘 AI 芯片
```

Taalas 押注某些 AI 工作负载会足够稳定，以至于**硬件专用化将胜出**。

---

## 与 vLLM / CUDA 学习的关联

对于正在学习 vLLM/CUDA 的人：

Taalas 几乎是"优化的最终极限"。

常规路径：

```
PyTorch
 |
CUDA 内核
 |
FlashAttention
 |
TensorRT
 |
定制 GPU 内核
 |
ASIC
 |
Taalas
```

你都在优化同一个计算图，只是越来越接近物理层面。

核心问题：

> "我们如何避免搬运比特？"

这也是以下技术背后的同一个问题：

*   FlashAttention
*   KV 缓存优化
*   GPU 内存层级
*   TPU 脉动阵列
*   Taalas ASIC

---

我的看法：Taalas 是一个非常重要的实验。它可能不会取代 NVIDIA GPU，因为前沿模型变化太快。但对于**拥有巨量推理请求的固定模型**（语音助手、客户服务、搜索排序、嵌入式 AI），模型专用硅片可能会是一个巨大的市场。([Forbes][3])

参考资料：

*   Taalas 产品：([Taalas][1])
*   Forbes 对 Taalas HC1 的分析：([Forbes][4])
*   Heise 对 HC1 架构的概述：([heise.de][2])

[1]: https://taalas.com/products/ "Products | Taalas"
[2]: https://www.heise.de/en/news/AI-inference-cast-in-silicon-Taalas-announces-HC1-chip-11185112.html?utm_source=chatgpt.com "AI inference cast in silicon: Taalas announces HC1 chip | heise online"
[3]: https://www.forbes.com/sites/karlfreund/2026/02/19/taalas-launches-hardcore-chip-with-insane-ai-inference-performance/?ss=enterprisetech&utm_source=chatgpt.com "Taalas Launches Hardcore Chip With ‘Insane’ AI Inference Performance"
[4]: https://www.forbes.com/sites/karlfreund/2026/02/19/taalas-launches-hardcore-chip-with-insane-ai-inference-performance/?utm_source=chatgpt.com "Taalas Launches Hardcore Chip With ‘Insane’ AI Inference Performance"