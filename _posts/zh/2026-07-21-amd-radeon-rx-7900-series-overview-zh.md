---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AMD Radeon RX 7900 系列概览
translated: true
type: note
---

**问题：AMD Radeon RX 7900 系列显卡简介**

**答案：**

![Image](https://images.openai.com/static-rsc-4/L_TDlUdg5rpbIpgXgWDTDIECgUbrFgGqGEMvPj9G1HSOFC62QtioyLwHnREZY84PHpkNfKdCKSzF3dq7cPt8jZZCJt54ujHItgnvH8q3i7hgeMyfjOdeIE6r6l79e4a3NQJ8mXiDicwJroatwJyJ4wQy0Ak7iozQdnrtDPDRcZPpuU6GYhNhQEhD5SnIKcK7?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/yXOZ1Z-FH_fk1ZMFr1fS8d0om-lB8gWDQA7puOhtfKRE51zGz8yngynQFKeXejR5YO14TMx1I404vU1bRussDjHmf7CWRepBLin0h0DM18BTcpW4CnI0a_VyqMLs2Bo0Z0VmZ0jqMXamriaWKZTeYPaXmcaFHLjwNpHsU0ypReW9TgiNkoYFDBv0XL6WPAru?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/p7iETk3hnNdohtlDOcZRrJND4D9gsvT_btBRWz0CMJR7uhokxa3ETE8Vkpvvkmd0RXsW-g2JSgIEbfaHNJlpjTn6m0tIXIZV-C6M_ta2P-6NN_boivJsvPridn9n70j8oGvsqpZmn28fZnnLCi6ddzrscJLMkbTLOq7g32MRrpGmjSm_u-2FVaTD5QIrXWyY?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/HLzBYOAjU7slWI8dvEwq8UoRFAi7FArHVsl5OsLNsiVT5QzozYEukoew2U3m1YtMS5LlDpjc4cPvDifpbALGuJZT2eaCklRh_hDK2N8pDoW-N1IjMzwSdXrZfPKaWfiJfkePMUrUGAgcvk5Yqk9zVzwK9HUkFHuwxSOb4sQo7fITQcLyFCdHyHu3-SNG3yZw?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/DbFr7gARWS5khW-6UA5qUClJFxA3Y9O4PludM1g0JIAU-DaStalu2zO73TWEvu_eqkZd1dywzOtJapyJtQmgrF-dpoLoRqAvntVqEVCug5ohruWnEaCeg0BkIN2d73vq2cJmT1dNzd5LeYwtY7u2HvG7bq6swoYBrTGqL__1kYoAfqBQ4rz2V7R-oyqMI3eK?purpose=fullsize)

**AMD Radeon RX 7900 系列**是AMD基于**RDNA 3 架构**的高端消费级 GPU 家族，于 2022 年底推出。主要型号包括：

* AMD Radeon RX 7900 XTX — 旗舰型号
* AMD Radeon RX 7900 XT — 略微精简的版本
* AMD Radeon RX 7900 GRE — 低成本变体

## 硬件规格

| 型号 | RX 7900 XTX | RX 7900 XT |
| :--- | :--- | :--- |
| 架构 | RDNA 3 | RDNA 3 |
| 计算单元 | 96 | 84 |
| 流处理器 | 6144 | 5376 |
| 显存 | 24 GB GDDR6 | 20 GB GDDR6 |
| 显存位宽 | 384位 | 320位 |
| Infinity Cache | 96 MB | 80 MB |
| TBP（典型板卡功耗） | ~355W | ~315W |
| FP32 算力 | ~61 TFLOPS | ~52 TFLOPS |

值得注意的点：

**RX 7900 XTX 拥有 24GB 显存**，超过了 RTX 4080（16GB），与 RTX 3090（24GB）相当。

---

## 架构：RDNA 3

与NVIDIA的单片式GPU不同，AMD转向了芯片组设计：

```
          Navi 31 GPU

        +-------------+
        | 图形        |
        | 计算芯片    |
        +-------------+
          |   |   |
     +----+---+---+----+
     |    |   |        |
    MCD  MCD MCD ...  MCD

   内存缓存芯片
```

该GPU包含：

* **GCD（图形计算芯片）**

  * 着色器核心
  * 光线追踪单元
  * AI 加速
* **MCD（内存缓存芯片）**

  * Infinity Cache
  * 内存控制器

这与AMD的CPU芯片组设计类似。

---

## AI / LLM 应用

对于 AI 工作负载，RX 7900 XTX 因其以下特点而值得关注：

### 优势

### 1. 大容量显存

24GB 显存支持：

* Llama 3 8B FP16
* Qwen 14B FP16
* 300亿+参数的量化模型
* Stable Diffusion / 图像模型

示例：

```
Qwen2.5-14B FP16

140亿参数 × 2字节
≈ 28GB

需要量化

Q4：
140亿 × 0.5字节
≈ 7GB

轻松适配
```

---

### 2. 良好的显存带宽

RX 7900 XTX：

```
显存带宽：
≈ 960 GB/s
```

非常接近：

```
RTX 3090：
936 GB/s
```

对于 LLM 推理而言，显存带宽至关重要。

近似 Token 生成速率：

```
tokens/秒 ≈ 显存带宽 / 模型大小
```

---

## ROCm 支持

与NVIDIA相比的关键区别：

NVIDIA：

```
PyTorch
  |
CUDA
  |
RTX GPU
```

AMD：

```
PyTorch
  |
ROCm
  |
Radeon GPU
```

RX 7900 支持 ROCm，但消费级 Radeon 的支持历来落后于 Instinct GPU。

例如：

良好支持：

* PyTorch
* Llama.cpp
* Ollama
* ComfyUI
* Stable Diffusion

支持欠佳：

* FlashAttention
* vLLM
* Triton kernels
* 自定义 CUDA 扩展

NVIDIA 生态系统仍然强大得多。

---

## 与 NVIDIA 显卡对比

### RX 7900 XTX 对比 RTX 4090

| | RX 7900 XTX | RTX 4090 |
| :--- | :--- | :--- |
| 显存 | 24GB | 24GB |
| 显存类型 | GDDR6 | GDDR6X |
| FP32 算力 | 61 TF | 82 TF |
| Tensor Core | 无 | 有 |
| CUDA | 无 | 有 |
| AI 生态系统 | 较弱 | 最强 |

对于游戏：

```
7900 XTX ≈ RTX 4080
```

对于 AI：

```
RTX 4090 >>> RX 7900 XTX
```

因为 CUDA + Tensor Core 占据主导地位。

---

## AI 场景下与 RTX 3090 对比

有趣的对比：

| | RX 7900 XTX | RTX 3090 |
| :--- | :--- | :--- |
| 显存 | 24GB | 24GB |
| 带宽 | 960GB/s | 936GB/s |
| FP16 | 好 | 优秀 |
| CUDA | ❌ | ✅ |
| Tensor Core | ❌ | ✅ |
| 二手价格 | 更低 | 更高 |

仅就显存容量而言：

```
7900 XTX ≈ RTX 3090
```

针对 LLM 工程：

```
RTX 3090 胜出
```

因为：

* vLLM 运行更好
* FlashAttention 运行更好
* 预训练的 CUDA 内核更多
* 多 GPU 配置更简便

---

## 多 GPU 可能性

7900 XTX 拥有：

```
PCIe 4.0 x16
24GB 显存
```

你可以构建：

```
2 × RX 7900 XTX

总计 48GB 显存
```

或者：

```
4 × RX 7900 XTX

总计 96GB 显存
```

但软件层面的扩展比 NVIDIA 更困难。

例如：

```
NVIDIA：
2×3090
 -> vLLM 张量并行
 -> 简单

AMD：
2×7900
 -> 可能
 -> 更多调试工作
```

---

## 2026 年二手市场价格/性能

一块二手的 RX 7900 XTX 可能颇具吸引力，如果：

* 你主要进行本地推理
* 你使用 llama.cpp / Ollama
* 你希望廉价获得大显存
* 你不需要 CUDA

典型价值：

```
24GB 显存
+
~1TB/s 带宽
+
低价二手
```

使其在显存方面成为“穷人的 4090”。

---

针对你的用例（训练 GPT-2、运行 Qwen/Llama 智能体、实验本地 LLM），我的排名如下：

```
RTX 3090 24GB
    >
RX 7900 XTX 24GB
    >
RTX 4070 12GB
```

RX 7900 XTX 是一款非常强大的硬件显卡，但 AI 软件生态系统是限制因素。它对于**推理 + 实验**的吸引力大于**严肃的 LLM 训练/微调**。