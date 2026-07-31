---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Nano-vLLM 的下一步
translated: true
type: note
---

问题：学习了 nano-vLLM 之后，下一步应该学什么？

答案：

鉴于你的学习轨迹（从零训练 GPT-2、nanochat、nano-vLLM、vLLM 实验、GPU 调试），**最有价值的下一步并不是另一个玩具项目**。你应该深入一层，将完整的 LLM 服务/训练栈连接起来。

一个合理的路径：

```
nano-vllm
    |
    v
vLLM 内部原理
    |
    +--> PagedAttention
    +--> KV cache 管理器
    +--> CUDA 内核
    +--> 连续批处理
    |
    v
分布式推理
    |
    +--> Tensor Parallel
    +--> Pipeline Parallel
    +--> Expert Parallel (MoE)
    |
    v
训练系统
    |
    +--> DeepSpeed
    +--> Megatron-LM
    +--> FSDP
    |
    v
生产级 AI 基础设施
    |
    +--> Kubernetes
    +--> GPU 调度
    +--> 可观测性
```

## 1. 阅读真实的 vLLM 源码

学完 nano-vLLM 后，转向：

vLLM

重点关注文件：

```
vllm/
├── engine/
│   ├── llm_engine.py
│   └── async_llm_engine.py
│
├── worker/
│   ├── worker.py
│
├── attention/
│   ├── backend.py
│
├── core/
│   ├── block_manager.py
│   └── scheduler.py
```

理解前向路径：

```
HTTP 请求
      |
      v
AsyncLLMEngine
      |
      v
Scheduler
      |
      +---- 等待队列
      |
      +---- 运行队列
      |
      v
KV Cache 分配
      |
      v
Model forward()
      |
      v
Sampler
      |
      v
Token 响应
```

关键洞察：

LLM 服务主要是一个**内存管理问题**，而不是计算问题。

---

## 2. 自己实现 PagedAttention

这可能是最有价值的练习。

普通的 KV cache：

```
Request A:
[0][1][2][3][4][5]

Request B:
[0][1][2][3]
```

问题：

不同请求有不同的长度。

内存碎片。

PagedAttention：

```
GPU KV 内存：

Block 0 -> A token 0-15
Block 1 -> B token 0-15
Block 2 -> A token 16-31
Block 3 -> C token 0-15
```

类似于操作系统虚拟内存：

```
虚拟地址
        |
        v
页表
        |
        v
物理 GPU 内存
```

这就是你的系统背景变得有价值的地方。

---

## 3. 学习 CUDA 内核

你不需要成为 CUDA 研究员，但要理解：

* 内存合并
* 共享内存
* warp
* occupancy
* tensor cores

例子：

朴素的 attention：

```python
scores = Q @ K.T
weights = softmax(scores)
out = weights @ V
```

内存：

```
Q
K
scores   <-- 巨大
weights  <-- 巨大
V
```

FlashAttention：

```
Q,K,V
 |
 v
SRAM 中的 tiles
 |
 v
输出
```

没有巨大的 attention 矩阵。

阅读：

FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness

---

## 4. 构建一个迷你分布式推理引擎

使用你的 GPU。

例子：

```
RTX 4070 12GB
        |
        |
Tensor Parallel
        |
        |
RTX 3060 12GB
```

拆分：

```
Linear layer:

Y = XW

W:

GPU0:
W0

GPU1:
W1


Y = concat(
      XW0,
      XW1
)
```

学习：

* NCCL
* torch.distributed
* tensor parallel

---

## 5. 学习训练基础设施

你已经训练过 GPT-2。下一步：

使用以下方式训练一个小模型：

* FSDP
* DeepSpeed ZeRO
* Megatron

理解：

### 数据并行

```
GPU0:
模型副本
batch 0


GPU1:
模型副本
batch 1


梯度同步
```

### 张量并行

```
层跨 GPU 拆分
```

### 流水线并行

```
GPU0:
layers 0-10

GPU1:
layers 11-20
```

---

## 6. 构建一个 AI 基础设施组合项目

比如：

```
mini-vllm
+
分布式服务
+
Kubernetes 部署
+
指标仪表板
```

架构：

```
             Client
               |
               v
        FastAPI Gateway
               |
               v
          Scheduler
               |
       +-------+-------+
       |               |
    GPU Worker     GPU Worker
       |               |
       +-------+-------+
               |
            NCCL
```

部署：

```
docker-compose
      |
      v
k8s
      |
      v
GPU 集群
```

这更接近真实的 AI 基础设施岗位。

---

## 推荐的 3 个月路线图

### 第一个月

```
nano-vllm
    |
    v
vLLM 源码
    |
    v
PagedAttention 实现
```

可交付成果：

GitHub 仓库：

```
mini-vllm-paged-attention
```

---

### 第二个月

```
CUDA
FlashAttention
Triton
```

实现：

* layernorm 内核
* softmax 内核
* attention 内核

---

### 第三个月

```
分布式推理
+
Kubernetes GPU 服务
```

部署：

```
Qwen3-8B
或
Llama-3.1-8B
```

附带：

* tensor parallel
* 指标
* 自动扩缩

---

对于你的背景，最有力的定位是：

> "后端工程师，理解 LLM 内部原理，从零训练过模型，实现过推理引擎，并能操作 GPU 集群。"

这种组合很少见。nano-vLLM 是很好的第一步；下一步是 **vLLM 内部原理 + CUDA/Triton + 分布式系统**。