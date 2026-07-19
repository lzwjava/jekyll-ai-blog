---
audio: false
generated: true
image: false
lang: zh
layout: post
title: DeepSpeed多GPU训练框架
translated: true
type: note
---

问题：什么是DeepSpeed？它是一个多GPU训练框架吗？

回答：

是的。**DeepSpeed是微软开发的分布式深度学习训练与推理优化框架**，主要旨在让**大模型能够在多个GPU（甚至数千个GPU）上进行训练**。

你可以把它看作是**PyTorch Distributed**之上的一层，用于解决从1个GPU扩展到多个GPU时遇到的各种问题：

* GPU内存限制
* 通信开销
* 优化器状态爆炸
* 检查点大小
* 训练吞吐量

核心理念：

```
PyTorch模型
      |
      v
DeepSpeed引擎
      |
      +-- ZeRO优化器
      +-- 分布式数据并行
      +-- 内存优化
      +-- 通信优化
      +-- CPU/NVMe卸载
      +-- 混合精度
```

---

## DeepSpeed存在的原因：内存爆炸

对于常规Adam训练，模型所需的内存远不止参数本身。

示例：FP16训练。

一个参数：

```
权重：              2字节 (fp16)
梯度：              2字节
Adam动量：          4字节 (fp32)
Adam方差：          4字节 (fp32)
主权重：            4字节 (fp32)

总计 ≈ 每参数16字节
```

一个70B参数的模型：

```
70B × 16字节

= 1.12 TB显存
```

即使是H100 80GB也无法训练它。

DeepSpeed ZeRO解决了这个问题。

---

## ZeRO（零冗余优化器）

常规的DistributedDataParallel：

```
GPU0：
 模型
 梯度
 优化器状态

GPU1：
 模型
 梯度
 优化器状态

GPU2：
 模型
 梯度
 优化器状态
```

每个GPU都存储全部内容。

非常浪费。

---

DeepSpeed ZeRO：

### ZeRO阶段1

分割优化器状态：

```
GPU0：
 优化器分片A

GPU1：
 优化器分片B

GPU2：
 优化器分片C
```

---

### ZeRO阶段2

同时分割梯度：

```
GPU0：
 优化器A
 梯度A

GPU1：
 优化器B
 梯度B
```

---

### ZeRO阶段3

参数也被分割：

```
GPU0：
 参数分片A

GPU1：
 参数分片B

GPU2：
 参数分片C
```

现在，大于单个GPU容量的模型也可以训练了。

---

示例：

```
70B模型

不使用ZeRO：

需要约1TB

使用ZeRO-3：

8个GPU × 80GB

可行
```

---

## DeepSpeed vs PyTorch DDP

简单的DDP：

```python
torchrun \
 --nproc_per_node=8 \
 train.py
```

每个GPU拥有完整模型。

适合：

* 7B模型
* 13B模型

---

DeepSpeed：

```bash
deepspeed train.py \
 --deepspeed ds_config.json
```

配合：

```json
{
 "zero_optimization": {
   "stage": 3
 }
}
```

适合：

* 70B+
* 万亿参数实验

---

## DeepSpeed不仅用于训练

它还具备：

### 1. 推理优化

示例：

一个70B模型：

```
FP16：

140GB显存
```

DeepSpeed推理可以：

* 分片权重
* 张量并行
* 优化内核

在以下配置上运行：

```
2 × A100 80GB
```

---

### 2. CPU/NVMe卸载

如果GPU内存不足：

```
GPU显存
   |
   |
CPU内存
   |
   |
NVMe固态硬盘
```

示例：

在消费级GPU上训练30B模型。

---

## 与其他框架比较

| 框架         | 主要用途                        |
| ------------ | ------------------------------- |
| PyTorch DDP  | 标准多GPU                       |
| DeepSpeed    | 大模型训练                      |
| FSDP         | PyTorch原生版ZeRO               |
| Megatron-LM  | 超大规模Transformer训练         |
| ColossalAI   | 类似目标                        |
| Accelerate   | HuggingFace启动器抽象层          |

---

## 针对你的硬件情况

针对你的RTX 4070/可能的RTX 3090配置：

### 单块RTX 4070 12GB

DeepSpeed帮助不大。

你受限于内存，但只有一块GPU。

更好的选择：

* 梯度检查点
* LoRA
* QLoRA
* 更小的批次
* Flash Attention

---

### 2块RTX 3090 24GB

DeepSpeed开始变得有用：

```
总共48GB显存
```

可行的操作：

* 13B全量微调
* 30B推理
* 使用ZeRO进行更大规模的训练

示例：

```
2 x 3090
        |
        v
DeepSpeed ZeRO-2/3
        |
        v
Qwen 14B微调
```

---

### 数据并行 vs 模型并行

重要区别：

**DDP：**

```
GPU0：整个模型
GPU1：整个模型

处理不同数据
```

**DeepSpeed ZeRO-3：**

```
GPU0：模型的一部分
GPU1：模型的一部分

同一个模型被分布式存储
```

这就是DeepSpeed对LLM至关重要的原因。

---

对于你的GPT-2 124M/760M训练实验，你可能不需要DeepSpeed。你的RTX 4070可以处理这些模型。当你进入**7B+全量训练或30B/70B微调**时，DeepSpeed才会变得有意义。
