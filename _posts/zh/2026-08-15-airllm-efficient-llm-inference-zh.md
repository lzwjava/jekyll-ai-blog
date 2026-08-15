---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AirLLM：高效的LLM推理
translated: true
type: note
---

## 问题：AirLLM 简介

## 答案

AirLLM 是一个开源项目，它通过一种称为**逐层卸载（layer-wise offloading）**的技术，允许在**有限的 GPU 显存**上运行**非常大的语言模型（LLM）**。

核心思想：

> 不是一次性将整个模型加载到显存/内存中，而是只加载当前前向传播所需的层。

例如：

* 一个 70B 参数的 FP16 模型：

[
70B \times 2\ bytes \approx 140GB
]

通常需要：

* A100 80GB × 2
* H100
* 多 GPU 配置

使用 AirLLM：

```
GPU 显存
 |
 |  层 0  ---> 计算
 |  层 1  ---> 计算
 |  层 2  ---> 计算
 |
CPU 内存 / 磁盘
 |
 |  其余层
```

只有少数几个 transformer 块留在 GPU 上。

---

## 架构

常规 transformer 推理：

```
输入 tokens

    |
    v

Embedding

    |
    v

Transformer 块 1
Transformer 块 2
Transformer 块 3
...
Transformer 块 N

    |
    v

LM Head

    |
    v

下一个 token
```

传统推理：

```
GPU:

Embedding
Block1
Block2
...
Block80
LM Head
```

AirLLM：

```
GPU:

Block1
   |
计算
   |
移除

Block2
   |
计算
   |
移除

Block3
...
```

伪代码：

```python
for layer in model.layers:
    layer.to("cuda")

    hidden = layer(hidden)

    layer.to("cpu")
```

---

## 为什么有效

Transformer 层大多是独立的顺序函数：

[
h_{i+1}=f_i(h_i)
]

你不需要同时拥有所有层。

在推理过程中：

```
第 i 层需要：
    当前隐藏状态
    第 i 层权重

第 i+1 层需要：
    输出隐藏状态
    第 i+1 层权重
```

前面层的权重不再需要。

---

## 示例

不使用 AirLLM：

```
Llama-70B

FP16：

140GB 权重

需要：
- A100 80GB x2
```

使用 AirLLM：

```
RTX 4090 24GB

+
系统内存

可以运行
Llama-70B
```

权衡：

|                | 常规推理         | AirLLM          |
| -------------- | ---------------- | --------------- |
| 速度           | 快               | 慢              |
| 显存           | 巨大             | 小              |
| 实现           | 简单             | 较复杂          |
| 使用场景       | 生产环境         | 个人/本地       |

---

## 安装

典型方式：

```bash
pip install airllm
```

示例：

```python
from airllm import AutoModel

model = AutoModel.from_pretrained(
    "meta-llama/Llama-2-70b-hf"
)

output = model.generate(
    ["Explain transformers"]
)
```

---

## 与其他技术的对比

### 1. 量化（Quantization）

示例：

```
FP16：
140GB

INT8：
70GB

4-bit：
35GB
```

量化减少：

[
\text{权重精度}
]

AirLLM 减少：

[
\text{内存驻留}
]

它们可以结合：

```
AirLLM
+
4-bit 量化
+
CPU 卸载
```

---

### 2. llama.cpp

llama.cpp：

```
GGUF 模型

CPU/GPU 混合推理
量化
优化的内核
```

在消费级机器上通常快得多。

示例：

```
Qwen-72B-Q4

llama.cpp
RTX 4090
~每秒几个 token
```

AirLLM：

```
相同模型

内存效率更高
但更慢
```

---

### 3. DeepSpeed ZeRO-Inference

DeepSpeed：

设计用于：

* 集群
* 多 GPU
* 生产服务

AirLLM：

* 单台开发机
* 实验

---

## 局限性

### 1. 生成速度慢

因为每个 token 都需要反复移动层：

```
CPU 内存
   |
PCIe
   |
GPU
```

PCIe 带宽成为瓶颈。

示例：

GPU 计算：

```
100 TFLOPS
```

PCIe 传输：

```
~20-30 GB/s
```

大量时间花费在移动权重上。

---

### 2. 不适合聊天服务

不好：

```
100 个用户
+
AirLLM
```

适合：

```
一位研究人员
一个巨型模型
一台机器
```

---

## 与你的配置的关系

对于你的 RTX 4070 12GB：

可能：

```
RTX 4070 12GB

+
64GB/128GB 内存

AirLLM

70B 模型推理
```

但速度很可能很差。

今天更好的选择：

### 本地实验

```
Qwen3-30B-A3B
Qwen3-32B
DeepSeek-R1-Distill-Qwen-32B

4-bit GGUF

llama.cpp
```

你的 12GB 显存更适合：

```
7B-14B：
快速

30B：
可能

70B：
AirLLM / CPU 卸载
```

---

## 历史意义

AirLLM 在 2023 年左右变得流行，因为它展示了：

> “内存容量，而非计算能力，是普及巨型 LLM 的第一道障碍。”

它是更广泛趋势的早期例子：

```
巨型模型
      |
      v
内存优化

- 量化
- 剪枝
- 卸载
- KV 缓存压缩
- MoE
- MLA
```

现代系统如 vLLM、llama.cpp、TensorRT-LLM 和 DeepSpeed 更侧重于吞吐量，但同样的根本问题依然存在：**如何将越来越大的模型适配到有限的硬件中**。

参考资料：

* AirLLM GitHub： [https://github.com/lyogavin/airllm](https://github.com/lyogavin/airllm)
* llama.cpp： [https://github.com/ggml-org/llama.cpp](https://github.com/ggml-org/llama.cpp)
* DeepSpeed： [https://github.com/microsoft/DeepSpeed](https://github.com/microsoft/DeepSpeed)
* vLLM： [https://github.com/vllm-project/vllm](https://github.com/vllm-project/vllm)
