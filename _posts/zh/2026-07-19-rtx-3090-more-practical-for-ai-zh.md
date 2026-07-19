---
audio: false
generated: true
image: false
lang: zh
layout: post
title: RTX 3090 更适用于AI
translated: true
type: note
---

问题：根据你的AI研究方向（Kimi验证、模型架构实验、MoE、本地推理、老旧GPU集群），你应该购买二手RX 7900 XT还是RTX 3090？

回答：

基于你的目标，**RTX 3090仍然是更实用的研究GPU**，尽管ROCm/开源AMD方案很有吸引力。

你的想法正确：因为H100/A100级别的GPU价格昂贵，二手市场才是个体研究者可以发挥的地方。但对于AI实验来说，**软件生态比硬件参数更重要**。

下面从你的使用场景进行对比。

|                          | RTX 3090 24GB       | RX 7900 XT 20GB  |
| ------------------------ | ------------------- | ---------------- |
| 显存                     | ✅ 24GB GDDR6X       | 20GB GDDR6       |
| CUDA                     | ✅ 行业标准         | ❌ 无CUDA         |
| ROCm                     | ❌                   | ✅                |
| PyTorch 支持             | ⭐⭐⭐⭐⭐               | ⭐⭐⭐              |
| vLLM                     | ⭐⭐⭐⭐⭐               | ⭐⭐               |
| llama.cpp                | ⭐⭐⭐⭐⭐               | ⭐⭐⭐⭐             |
| 训练小型LLM              | ✅ 优秀             | ⚠️ 可能可行       |
| 微调                     | ✅ LoRA/QLoRA       | ⚠️ 更多障碍       |
| 多卡实验                 | ✅ 成熟             | ⚠️ 困难           |
| 二手价格                 | 较高               | 较低              |
| 研究可复现性             | ✅                  | ⚠️                |

---

## 你的实验更适合NVIDIA

你的清单：

### 1. 验证Kimi Thinking Machine

你可能需要：

* 复现推理行为
* 运行基准测试
* 比较推理轨迹
* 测试scaling

大多数开源实现假设：

```bash
pip install torch
pip install transformers
pip install vllm
```

CUDA路径：

```
PyTorch
  |
CUDA
  |
NVIDIA GPU
```

是默认的。

使用AMD时：

```
PyTorch
  |
ROCm
  |
AMD GPU
```

虽然可用，但很多论文的仓库会出问题，因为：

* CUDA内核
* FlashAttention版本
* Triton内核
* 自定义算子

例如：

```python
import flash_attn
```

在NVIDIA上运行顺畅。

在AMD上，你可能要花几天时间修复构建问题。

---

### 2. 移植前沿实验室的技巧

在这方面NVIDIA优势巨大。

现代LLM研究栈：

```
Transformers
Accelerate
DeepSpeed
FSDP
FlashAttention
Triton
vLLM
SGLang
Megatron
```

大多数CI测试都在NVIDIA上进行。

例如：

```bash
torchrun \
 --nproc_per_node=2 \
 train.py
```

在NVIDIA上：

正常运行。

在AMD上：

可能不行。

---

### 3. MoE实验

实际上这一点非常重要。

MoE需要：

* 内存管理
* 通信
* 专家并行

示例：

```
                 router
                   |
        +----------+----------+
        |          |          |
     Expert1    Expert2    Expert3
```

小型MoE：

```
Qwen-MoE风格
8个专家
top-2路由
```

你的RTX 3090：

```
24GB显存
```

非常宝贵。

RX7900XT：

```
20GB显存
```

已经少了4GB。

对于LLM来说，显存为王。

---

### 4. 本地模型 + 老旧GPU组合

这很有趣。

你提到了：

> 探索老旧显卡拼凑方案

在这方面NVIDIA有巨大优势。

示例：

```
3090 24GB
+
3090 24GB

=48GB显存
```

配合：

```bash
CUDA_VISIBLE_DEVICES=0,1
```

很多框架能理解这种配置。

AMD多卡：

虽然可行，但经过实战检验的程度低得多。

---

### 5. 注意力机制演变

你的目标：

```
Transformer
 |
FlashAttention
 |
MQA
 |
GQA
 |
Sliding Window Attention
 |
Linear Attention
 |
RWKV
 |
Mamba
```

你可能会克隆很多仓库。

概率：

```
仓库立即可运行：

RTX3090: 90%

RX7900XT: 50-70%
```

---

## 什么时候RX7900XT实际上有意思

AMD并非糟糕的选择。

如果你的研究目标是：

“开源硬件/软件能否取代CUDA？”

例如：

* ROCm贡献
* 内核优化
* llama.cpp HIP后端
* GPU编程

那么RX7900XT会很有趣。

但你现在的研究方向更像：

> AI研究员 / 模型构建者

而不是：

> GPU编译器工程师

---

## 价格很重要

如果：

```
RTX3090:
8000-10000 CNY

RX7900XT:
3000-4000 CNY
```

那么计算结果会改变。

3090卖10k CNY不划算。

在大约：

```
3500-4500 CNY
```

的价位，二手RTX3090非常有吸引力。

因为：

```
24GB显存
+
CUDA生态
+
Tensor Core
+
成熟工具链
```

很难被替代。

---

## 我对你的推荐排序

根据你的背景：

* 在RTX4070上训练过GPT-2 124M
* 对nanoGPT感兴趣
* MoE
* 注意力机制研究
* 本地LLM
* 复现论文

我的排序是：

### 方案1（最佳）

```
RTX3090 24GB
+
你的RTX4070 12GB
```

使用方式：

* 3090用于训练
* 4070用于推理/测试

非常实用。

---

### 方案2

```
2 x RTX3090
```

“穷人的AI实验室”：

```
48GB显存
```

你可以探索：

* 7B微调
* 14B量化
* MoE原型

---

### 方案3

```
RX7900XT
```

仅当：

* 价格低很多
* 你特别想体验ROCm

---

我的结论：

对于**你的AI研究方向组合**，我会购买：

> **RTX 3090 24GB 优先。**

ROCm在智力上很吸引人，但几乎所有前沿LLM实验都在CUDA上进行。你以后可以用更便宜的AMD卡学习ROCm；你当前的瓶颈不是FLOPS，而是**显存 + 生态兼容性**。

你理想的个人AI实验室配置：

```
RTX3090 24GB
        |
        +-- nanoGPT
        +-- QLoRA
        +-- MoE toy models
        +-- attention experiments
        +-- vLLM/SGLang

RTX4070 12GB
        |
        +-- inference
        +-- agents
        +-- daily development
```

这更接近一个小型研究实验室的配置。
