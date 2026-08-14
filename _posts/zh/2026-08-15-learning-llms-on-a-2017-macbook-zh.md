---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在2017款MacBook上学习LLMs
translated: true
type: note
---

问题：如果这台2017款MacBook Pro是你唯一的机器，你该如何认真学LLM/PyTorch？

答案：**实际上，完全可以——只要你把“学习机制”和“运行大模型”分开。**

你的机器用来训练很弱，但作为**CPU开发和实验机器**来说，它非常出色：

* 2核/4线程 i5-7360U
* 15 GB 内存
* Iris Plus 640——**对现代PyTorch GPU训练没有帮助**
* ~228 GB 固态硬盘
* Linux/Ubuntu
* Python 3.13

关键在于：**不要试图让这台笔记本成为你的GPU集群，而要把它变成你的实验室。**

### 1. 从本地基础开始学PyTorch

从极小的张量和模型开始。

```bash
python3 -m venv ~/venvs/torch
source ~/venvs/torch/bin/activate

pip install torch torchvision torchaudio
```

然后：

```python
import torch

x = torch.randn(4, 8)
W = torch.randn(8, 16, requires_grad=True)

y = x @ W
loss = y.pow(2).mean()

loss.backward()

print(y.shape)
print(W.grad.shape)
```

你几乎可以在这里学到所有PyTorch的基本机制：

```text
Tensor
  ↓
matmul
  ↓
forward
  ↓
loss
  ↓
autograd
  ↓
backward
  ↓
gradient
  ↓
optimizer
  ↓
parameter update
```

计算量很小，CPU完全够用。

---

### 2. 构建一个小型Transformer

这台机器完全能训练类似这样的模型：

```text
vocab       10K
context     256
layers      4
hidden      256
heads       4
parameters  ~10–20M
```

例如，实现：

```python
class CausalSelfAttention(nn.Module):
    ...
    
class MLP(nn.Module):
    ...
    
class TransformerBlock(nn.Module):
    ...
    
class GPT(nn.Module):
    ...
```

然后在小型语料上训练。

你不需要H100来理解：

```text
token
 ↓
embedding
 ↓
Q K V
 ↓
attention
 ↓
residual
 ↓
LayerNorm
 ↓
MLP
 ↓
residual
 ↓
logits
 ↓
cross entropy
```

事实上，**慢机器反而对教学有帮助**，因为你必须理解每个操作在做什么，而不是直接把7B模型扔给GPU。

---

### 3. 渐进式扩大规模，训练GPT-2风格模型

我会采用这样的递进模式：

```text
1M       parameters
  ↓
5M
  ↓
10M
  ↓
50M
  ↓
100M
```

前三个在你的笔记本上完全可行。

例如：

```bash
git clone https://github.com/karpathy/nanoGPT
cd nanoGPT

python train.py \
    --dataset=shakespeare \
    --n_layer=4 \
    --n_head=4 \
    --n_embd=256 \
    --block_size=256 \
    --batch_size=8
```

重点不是跑出好的基准。

重点在于能够检查：

```python
logits.shape
loss
tokens/sec
memory
gradient norms
parameter count
```

并且准确理解计算消耗在哪里。

---

### 4. 你可以重现Transformer的重要数学原理

你的笔记本足以实验以下内容：

**Attention**

```python
scores = Q @ K.transpose(-2, -1)
scores /= math.sqrt(d_k)

attn = torch.softmax(scores, dim=-1)

out = attn @ V
```

然后研究：

```text
当d_k变化时会发生什么？
当序列长度加倍时会发生什么？
为什么除以sqrt(d_k)？
因果掩码到底做了什么？
softmax对信息做了什么？
```

你可以直接打印出矩阵。

这比直接运行以下代码更有教育意义：

```python
model.generate(...)
```

---

### 5. 通过小型受控实验学习LLM内部机制

例如，研究KV缓存。

先从：

```text
Q = x_q W_Q
K = x W_K
V = x W_V

Attention(Q,K,V)
```

然后实现：

```text
prefill
   ↓
K_cache, V_cache
   ↓
decode token 1
   ↓
append K,V
   ↓
decode token 2
   ↓
append K,V
```

你可以测量：

```text
sequence length
↓
KV-cache memory
↓
attention computation
↓
decode latency
```

笔记本不需要快。

你在研究**算法本身**。

---

### 6. 对于大模型，把笔记本当作控制平面

这是重要的架构：

```text
                    你的MacBook
                 Ubuntu / Python / Git
                         │
             ┌───────────┴───────────┐
             │                       │
        本地 CPU                  远程 GPU
             │                       │
       1–50M 模型              7B/14B/70B
       小型数据集              LoRA/QLoRA
       调试                    训练
       性能分析                推理
```

SSH到GPU机器：

```bash
ssh <USER>@<GPU_HOST>
```

然后：

```bash
rsync -av ./project/ <USER>@<GPU_HOST>:~/project/
```

或者直接用Git：

```bash
git push
ssh <GPU_HOST>
git pull
```

这实际上是一种**非常好的专业工作流程**。

你的笔记本不需要拥有GPU。

---

### 7. 不要在本地安装巨型模型

不要做这种事：

```text
Qwen3-235B
DeepSeek-V3
Llama 405B
```

在这台机器上。

应该：

```text
笔记本
  ↓
小型模型 / 玩具模型

云GPU
  ↓
7B / 14B / 32B

大型集群
  ↓
70B+
```

对于推理，你可以偶尔在本地使用**小型量化模型**，但15GB内存意味着你应该考虑大约**1B–7B级别的模型**，具体取决于量化方式和上下文长度。

---

### 8. 你可以在没有CUDA的情况下学习CUDA概念

你的Iris Plus 640不是有用的CUDA设备。

没关系。

先理解抽象概念：

```text
CPU
 ├── cores
 ├── cache
 └── RAM

GPU
 ├── many parallel execution units
 ├── HBM/VRAM
 └── massive memory bandwidth
```

然后理解为什么：

```python
x @ W
```

在GPU上快那么多。

最终你可以把完全相同的PyTorch程序从：

```python
device = "cpu"
```

改成：

```python
device = "cuda"
```

在远程GPU上运行。

这样性能差异就变得**有意义**了，因为你已经理解了计算本身。

---

### 9. 我在这台笔记本上实际会研究的内容

一个非常扎实的递进路线：

```text
第1周
│
├── PyTorch Tensor
├── autograd
├── nn.Module
├── optimizer
└── training loop

第2周
│
├── linear regression
├── MLP
├── CNN
└── embeddings

第3周
│
├── attention
├── multi-head attention
├── causal mask
└── positional encoding

第4周
│
├── Transformer block
├── GPT
├── tokenizer
└── cross entropy

第5周
│
├── train tiny GPT
├── inspect loss
├── inspect activations
└── inspect gradients

第6周
│
├── KV cache
├── RoPE
├── RMSNorm
├── GQA/MQA
└── FlashAttention concept

第7周+
│
├── LoRA
├── QLoRA
├── distributed training concepts
├── quantization
└── inference engines
```

然后使用远程GPU进行：

```text
Qwen
Llama
DeepSeek
MoE
LoRA
RLHF/DPO
distributed training
```

---

### 10. 最重要的事

你笔记本的局限性实际上可以迫使你采取正确的学习策略：

**不要为了模型大小而优化，要为理解而优化。**

一个2000万参数的Transformer，你理解其中每一个张量：

```text
[B,T]
 ↓
[B,T,C]
 ↓
Q,K,V
 ↓
[B,H,T,D]
 ↓
QKᵀ
 ↓
[B,H,T,T]
 ↓
softmax
 ↓
attention @ V
 ↓
MLP
 ↓
logits
 ↓
cross entropy
 ↓
backward
```

比下载一个32B模型然后运行`ollama run`要有教育意义得多。

而一旦你理解了那个2000万参数的模型，7B模型基本上就是**同样的数学 + 更多的计算 + 围绕内存/带宽/分布的工程问题**。

所以，是的：**仅凭这台MacBook，你就可以学习PyTorch以及现代LLM几乎所有数学/核心架构基础。** 只有当实验受限于计算时，你才需要租用/远程GPU。

参考资料：

* [PyTorch](https://pytorch.org/?utm_source=chatgpt.com)
* [nanoGPT — Andrej Karpathy](https://github.com/karpathy/nanoGPT?utm_source=chatgpt.com)
* [Attention Is All You Need](https://arxiv.org/abs/1706.03762?utm_source=chatgpt.com)
