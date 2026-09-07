---
audio: false
generated: true
image: false
lang: zh
layout: post
title: LLM工程师学习路线图
translated: true
type: note
---

## 问题：给我一个严肃的学习AI/LLM工程的计划

## 回答：

鉴于你当前的水平，**不要遵循初学者“学习AI”的课程**。你已经接触过PyTorch、CUDA/GPU、GPT训练、vLLM、KV缓存和分布式训练。

我会将你接下来**12个月的目标**定为：

> **成为能够理解、修改、训练、优化并部署LLM的工程师，涵盖从CUDA内核→分布式训练→模型架构→推理系统的全过程。**

关键在于通过**逐步构建更大规模的系统**来学习，而不是收集课程。

### 路线图

```text
                 AI / LLM Engineer
                        │
        ┌───────────────┼────────────────┐
        ↓               ↓                ↓
    MODEL/ML         TRAINING          SYSTEMS
        │               │                │
 Transformer       PyTorch DDP       CUDA
 MoE               FSDP/ZeRO         Triton
 Attention         TP/PP             NCCL
 MTP               Checkpointing     FlashAttention
 RL/Post-training  Scaling laws      GPU memory
        │               │                │
        └───────────────┼────────────────┘
                        ↓
                    INFERENCE
                        │
               KV Cache / PagedAttention
               Continuous batching
               Quantization
               Speculative decoding
               vLLM / SGLang
                        ↓
                 FRONTIER RESEARCH
                        │
             MoE / MLA / MTP / FP4
             distributed inference
             training efficiency
```

---

# 阶段 0 — 1周：巩固基础

不要在这里花费数月。

你应该能够凭记忆推导出以下内容：

### Transformer

```text
X
 ↓
Q = XWq
K = XWk
V = XWv
 ↓
Attention(Q,K,V)
    = softmax(QKᵀ / √d)V
 ↓
O projection
 ↓
MLP / MoE
 ↓
residual
 ↓
LayerNorm/RMSNorm
```

然后理解：

* BPE/分词
* embeddings
* 位置编码 / RoPE
* MHA
* MQA
* GQA
* RMSNorm
* SwiGLU
* 残差连接
* logits
* 交叉熵
* 自回归训练
* teacher forcing

但**所有内容都要亲自动手实现**。

你的最低项目：

```bash
nano transformer.py
```

实现：

```python
class Attention(nn.Module):
    ...

class MLP(nn.Module):
    ...

class TransformerBlock(nn.Module):
    ...

class GPT(nn.Module):
    ...
```

然后在一个小型语料库上训练它。

你已有的GPT-2从零实现意味着这部分对你来说应该非常快。

---

# 阶段 1 — 2-3周：深入理解GPT

以**nanoGPT → nanochat**作为主要课程。

Karpathy目前的GitHub项目非常适合这个目的：`nanoGPT`、`nanochat`、`llm.c`、`llama2.c`、`micrograd`和`microgpt`都明确围绕最小化实现设计。([GitHub][1])

[Karpathy的GitHub](https://github.com/karpathy?utm_source=chatgpt.com)

不要仅仅运行nanochat。

按以下顺序阅读：

```text
tokenizer
   ↓
dataset
   ↓
model
   ↓
forward()
   ↓
loss
   ↓
backward()
   ↓
optimizer
   ↓
distributed training
   ↓
checkpoint
   ↓
inference
   ↓
serving
```

当前的nanochat项目实际上建议按照训练流程阅读代码，从分布式设置和分词器实现开始。

### 你的任务

修改nanochat。

例如：

```text
实验1：
    修改RoPE

实验2：
    修改RMSNorm

实验3：
    修改attention实现

实验4：
    添加GQA

实验5：
    添加不同的激活函数

实验6：
    修改分词器词表

实验7：
    修改优化器

实验8：
    修改学习率调度
```

每个实验都应产生：

```text
git commit
训练日志
验证损失
tokens/sec
GPU内存
简短笔记解释结果
```

这是你从**LLM用户 → LLM工程师**的转变方式。

---

# 阶段 2 — 1个月：GPU + CUDA

鉴于你的兴趣，我会在这里投入大量时间。

你不需要立即成为CUDA编译器工程师。

你需要理解：

```text
Python
 ↓
PyTorch
 ↓
ATen
 ↓
CUDA kernel
 ↓
GPU SM
 ↓
Tensor Core
 ↓
HBM
```

学习：

### GPU架构

```text
SM
├── CUDA cores
├── Tensor cores
├── registers
├── shared memory
└── L1 cache

GPU
├── SM
├── SM
├── SM
└── ...

        ↓

       HBM
```

理解：

* occupancy
* warps
* threads
* blocks
* registers
* shared memory
* coalesced memory access
* memory bandwidth
* arithmetic intensity
* Tensor Cores
* FP32 / BF16 / FP16 / FP8 / FP4
* GEMM

然后编写CUDA代码。

从以下开始：

```cpp
vector_add.cu
```

然后：

```text
matmul
 ↓
tiled matmul
 ↓
softmax
 ↓
layernorm
 ↓
attention
```

重要的问题变成：

> **为什么这个内核慢？**

而不是：

> 如何调用这个PyTorch API？

---

# 阶段 3 — 1个月：实现FlashAttention

这应该是你的一个重要里程碑。

从以下开始：

```python
Q @ K.T
softmax()
@ V
```

然后理解朴素实现为何会具体化：

```text
QKᵀ
```

这在内存中是：

```text
O(N²)
```

然后推导出分块注意力。

基本思想：

```text
HBM
 ↓
加载Q/K/V块
 ↓
SRAM/共享内存
 ↓
计算
 ↓
不具体化完整的注意力矩阵
 ↓
写出输出
```

然后实现一个简化的CUDA版本。

之后阅读真实实现。

这将使后续主题如：

* FlashInfer
* FlashAttention
* MLA
* PagedAttention
* attention backends

变得容易得多。

---

# 阶段 4 — 1个月：分布式训练

现在学习如何从单GPU变成8 → 64 → 1000个GPU。

顺序：

```text
single GPU
    ↓
DDP
    ↓
FSDP
    ↓
Tensor Parallel
    ↓
Pipeline Parallel
    ↓
3D parallelism
```

PyTorch当前的分布式堆栈明确涵盖了DDP、FSDP2、Tensor Parallel、DeviceMesh、RPC及相关分布式机制。([PyTorch Documentation][2])

从DDP开始：

```bash
torchrun \
  --nproc_per_node=8 \
  train.py
```

准确理解发生了什么：

```text
GPU 0                    GPU 1

forward                  forward
   ↓                        ↓
loss                     loss
   ↓                        ↓
backward                 backward
   ↓                        ↓
gradient ───── NCCL ───── gradient
             all-reduce
                 ↓
          synchronized grads
```

然后是FSDP。

重要的区别：

```text
DDP:

GPU0: 完整模型
GPU1: 完整模型
GPU2: 完整模型
GPU3: 完整模型


FSDP:

GPU0: 分片
GPU1: 分片
GPU2: 分片
GPU3: 分片
```

FSDP对参数、梯度和优化器状态进行分片，在计算时使用all-gather，在梯度时使用reduce-scatter。([PyTorch Documentation][3])

然后自行实现：

```text
8 GPU GPT训练
```

---

# 阶段 5 — 1个月：LLM推理

你已经开始了这个领域。要更深入。

学习：

```text
prefill
decode
KV cache
continuous batching
PagedAttention
prefix caching
chunked prefill
quantization
speculative decoding
```

思维模型：

```text
Prompt
  │
  ▼
PREFILL
  │
  ├── 计算所有token
  └── 创建KV cache
          │
          ▼
       DECODE
          │
       token 1
          │
       token 2
          │
       token 3
          │
          ...
```

然后理解为什么推理通常受**内存带宽/KV缓存**限制，而不仅仅是FLOP限制。

然后阅读vLLM源码。

当前的vLLM拥有一个庞大的推理堆栈，围绕PagedAttention、continuous batching、prefix caching、chunked prefill、quantization、CUDA/HIP graphs、优化的attention/GEMM/MoE内核以及speculative decoding。([vLLM][4])

你的项目：

```text
mini-vllm/
    scheduler.py
    kv_cache.py
    block_manager.py
    attention.py
    worker.py
    engine.py
```

实现：

```text
request queue
     ↓
scheduler
     ↓
KV cache manager
     ↓
batch
     ↓
model forward
     ↓
sample
     ↓
return token
```

之后你会对vLLM有更深刻的理解。

---

# 阶段 6 — 1个月：MoE

这应该是你的下一个主要架构项目。

你最近问过关于学习MoE的问题。我认为这**正是你现在正确的方向**。

从以下开始：

```text
Dense FFN

x
│
▼
W1
│
activation
│
▼
W2
│
▼
output
```

然后：

```text
MoE

             ┌── Expert 1
             ├── Expert 2
x → Router ──┼── Expert 3
             ├── Expert 4
             └── Expert N
```

学习：

* top-k routing
* expert capacity
* auxiliary loss
* load balancing
* expert parallelism
* all-to-all communication
* token dispatch
* token combine
* expert parallel + tensor parallel
* MoE inference

然后实现：

```python
class MoE(nn.Module):
    def forward(self, x):
        scores = self.router(x)
        experts = topk(scores)

        ...
```

然后进行基准测试：

```text
Dense 7B
vs
MoE 8x1B
```

比较：

```text
FLOPs
active parameters
total parameters
tokens/sec
memory
communication
quality
```

这让你理解为什么现代LLM架构越来越像一个**分布式系统问题**。

---

# 阶段 7 — 1-2个月：后训练

只有在理解预训练之后，才应深入这里。

学习：

```text
SFT
 ↓
Preference data
 ↓
Reward modeling
 ↓
DPO
 ↓
RL
 ↓
GRPO / PPO-like methods
 ↓
reasoning models
```

理解数学目标。

对于SFT：

```text
L = -Σ log pθ(y_t | x, y_<t)
```

对于DPO，理解以下之间的关系：

```text
policy
reference model
chosen response
rejected response
```

不要从记忆框架开始。

在PyTorch中实现一个最小化版本。

---

# 阶段 8 — 1-2个月：现代LLM架构

然后开始积极阅读论文和源码。

优先级：

### 架构

```text
Transformer
RoPE
GQA
MoE
MLA
MTP
Long context
```

### 效率

```text
FlashAttention
PagedAttention
Quantization
FP8
FP4/NVFP4
Speculative decoding
MTP
```

### 训练

```text
Scaling laws
Data mixture
Data quality
Distributed training
Checkpointing
Fault tolerance
```

### 系统

```text
CUDA
Triton
CUTLASS
NCCL
PyTorch compiler
vLLM
SGLang
```

---

# 你的12个月项目序列

我会严格按顺序把这些放在GitHub上：

```text
01-micrograd
02-microgpt
03-tiny-transformer
04-gpt-from-scratch
05-gpt-pretraining
06-cuda-matmul
07-cuda-attention
08-flash-attention
09-ddp-training
10-fsdp-training
11-tensor-parallel-gpt
12-mini-vllm
13-moe
14-moe-distributed
15-speculative-decoding
16-mtp
17-quantization
18-llm-post-training
19-research-project
```

这个作品集比以下内容有价值得多：

```text
10个证书
50门课程
300篇已收藏的论文
```

---

# 我会采用的每周计划

如果你每周能投入约20小时：

```text
周一
  2小时论文/源码阅读
  1小时数学

周二
  3小时实现

周三
  3小时CUDA/PyTorch内部机制

周四
  3小时实现

周五
  2小时基准测试/性能分析

周六
  5小时正式项目

周日
  1小时写笔记
```

比例大致应为：

```text
70%编码
20%阅读
10%理论
```

对你来说，**不是**：

```text
70%课程
20%视频
10%编码
```

---

# 最重要的学习循环

对于每项新技术：

```text
阅读
 ↓
实现
 ↓
基准测试
 ↓
破坏它
 ↓
性能分析
 ↓
阅读源码
 ↓
修改
 ↓
再次基准测试
```

例如，不要通过观看视频来学习KV缓存。

自己构建：

```python
# 朴素版
generate(prompt)

# 缓存版
generate_with_kv_cache(prompt)
```

然后测量：

```text
tokens/sec
GPU内存
prefill延迟
decode延迟
```

然后破坏实现。

然后修复它。

**这才是真正的LLM工程。**

---

# 我特别为你推荐优先关注的内容

我**不会**在以下方面花费大量时间：

```text
❌ 经典机器学习
❌ sklearn
❌ 基础CNN
❌ 通用AI课程
❌ 提示工程
❌ RAG教程
❌ LangChain教程
❌ “AI Agent 101”
```

你最有价值的路径是：

```text
                 你
                  │
          Transformer内部机制
                  │
          CUDA / GPU架构
                  │
        分布式训练
                  │
             MoE / MTP
                  │
          推理系统
                  │
         量化 / 内核
                  │
          后训练 / RL
                  │
             研究
```

而你已有的硬件经验实际上是一个优势：**GPU内存、PCIe、CUDA故障、多GPU拓扑、显存限制、内核性能、模型卸载都不是次要话题——它们才是实际的工程约束。**

对于分布式训练，学习DDP → FSDP2 → TP，而不是直接跳入一个庞大的框架；PyTorch的当前文档正好提供了这一进展。([PyTorch Documentation][2])

### 你接下来的30天

如果我是你，我会这样做：

```text
第1周
  nanochat源码
  Transformer内部机制
  分词器
  训练循环

第2周
  修改nanochat
  实现GQA
  实现RoPE变体
  基准测试

第3周
  CUDA
  分块GEMM
  softmax
  LayerNorm
  性能分析

第4周
  FlashAttention
  KV缓存
  阅读vLLM注意力实现
```

然后：

```text
第2个月 → DDP + FSDP + NCCL
第3个月 → Tensor Parallel + Pipeline Parallel
第4个月 → MoE
第5个月 → MoE分布式
第6个月 → vLLM / 推理
第7个月 → CUDA/Triton内核
第8个月 → 量化 + FP8/FP4
第9个月 → 投机解码 + MTP
第10个月 → SFT/DPO/RL
第11个月 → 复现一篇近期论文
第12个月 → 你自己的研究/优化项目
```

最终目标不是了解每一种LLM技术。

而是能够看到一篇论文说：

> “我们引入了一种新的注意力/MoE/训练优化方法”

然后在几天内**理解数学、找到相关代码、实现最小版本、运行实验、在GPU上进行性能分析，并解释它是否真的有效。**

这就是我建议你瞄准的水平。

我也可以将其转化为一个**具体的6个月逐仓库课程**，明确说明要克隆哪些GitHub项目、阅读哪些文件，以及每周应该实现哪些代码。

[1]: https://github.com/karpathy?utm_source=chatgpt.com "karpathy (Andrej) · GitHub"
[2]: https://docs.pytorch.org/tutorials/distributed.html?utm_source=chatgpt.com "Distributed — PyTorch Tutorials 2.14.0+cu130 documentation"
[3]: https://docs.pytorch.org/tutorials/intermediate/FSDP1_tutorial.html?utm_source=chatgpt.com "Getting Started with Fully Sharded Data Parallel(FSDP) — PyTorch Tutorials 2.14.0+cu130 documentation"
[4]: https://docs.vllm.ai/en/stable/?utm_source=chatgpt.com "vLLM"