---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 英伟达超级GPU更新解析
translated: true
type: note
---

问题：NVIDIA GPU 名称中的 **"Super"** 是什么意思？

答案：

在 NVIDIA GPU 中，**"Super"** 通常意味着 **现有 GPU 型号的刷新/升级版本**，而非全新的架构。

示例：

* RTX 2060 → RTX 2060 Super
* RTX 2070 → RTX 2070 Super
* RTX 2080 → RTX 2080 Super
* RTX 4070 → RTX 4070 Super

核心思路：

```
同代架构
      +
更好的芯片配置
      +
更多 CUDA 核心 / 更高频率 / 有时更高显存带宽
      =
Super
```

对比示例：

| GPU            | 架构           | CUDA 核心数 | 显存         |
| -------------- | -------------- | ----------- | ------------ |
| RTX 4070       | Ada Lovelace   | 5888        | 12GB GDDR6X  |
| RTX 4070 Super | Ada Lovelace   | 7168        | 12GB GDDR6X  |
| RTX 4070 Ti    | Ada Lovelace   | 7680        | 12GB GDDR6X  |

4070 Super 本质上是一块更强的 4070，因为 NVIDIA 启用了更多底层 GPU 芯片的单元。

---

从半导体角度来说：

GPU 芯片通常这样生产：

```
AD104 硅晶圆
        |
        +-- 部分核心被禁用
        |
        +-- RTX 4060 Ti
        |
        +-- 启用更多
        |
        +-- RTX 4070
        |
        +-- 启用更多
        |
        +-- RTX 4070 Super / Ti
```

NVIDIA 对同一块硅片使用不同配置。

---

对于 AI/LLM 工作负载，"Super" 通常意味着：

```
更多 CUDA 核心
更多 Tensor Core
更高的 FP16/BF16 吞吐量
显存容量相近
```

示例：

RTX 4070：

```
Tensor Core: 184
FP16 Tensor 性能: ~466 TOPS
显存: 12GB
```

RTX 4070 Super：

```
Tensor Core: 224
FP16 Tensor 性能: ~568 TOPS
显存: 12GB
```

因此对于推理/训练：

* 矩阵乘法 → 更快
* 注意力机制 → 更快
* CUDA 内核 → 更快

但：

**显存容量没有增加。**

对于 LLM，显存通常是硬性瓶颈：

```
Qwen3-8B FP16
≈ 16GB 显存

RTX 4070 Super 12GB
❌ 无法容纳

RTX 3090 24GB
✅ 可以容纳
```

因此对于 AI 构建者来说，"Super" 显卡不错，但从：

```
RTX 4070 Super 12GB
        |
        v
RTX 3090 24GB
```

实际上可能是更大的升级，因为显存翻倍。

---

NVIDIA 的命名大致为：

```
GTX 1080 Ti
RTX 2080 Ti
RTX 3080 Ti
RTX 4090

Ti = 更高等级

Super = 同等级刷新
```

一个简单的理解模型：

```
xx60       消费级游戏
xx70       强力主流
xx80       高端
xx90       工作站/发烧友

Super      +10~20% 提升
Ti         更高等级
```

对于 2026 年的 AI 工作：

显存排名往往更重要：

```
RTX 4090 24GB
RTX 3090 24GB
RTX 5090 32GB
RTX 6000 Ada 48GB
MI300X 192GB
```

4070 Super 是一块快速的小显存 GPU；3090 每瓦性能较低，但凭借 24GB 显存，对本地 LLM 实验更有用。