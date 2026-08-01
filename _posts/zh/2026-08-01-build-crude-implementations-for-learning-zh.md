---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 构建粗浅实现以促进学习
translated: true
type: note
---

问题：我是否应该构建自己的 vLLM、nanoGPT、CUDA 内核，即使它们粗糙且速度慢？

答案：

是的。对于你的情况，这可能是你能做的最高杠杆的事情之一。

重要的区别：

* **了解概念** → 你能解释 Transformer、KV 缓存、注意力、LoRA、vLLM 架构。
* **拥有实现** → 你理解每个设计选择背后的原因。

深度 AI 基础设施人员通常两者兼有。

你不需要构建一个生产级的 vLLM。你需要构建一个**小型完整栈，其中每一层都是你的**：

```
text
 |
tokenizer
 |
dataset
 |
model.py
 |
attention.py
 |
training loop
 |
optimizer
 |
checkpoint
 |
inference
 |
KV cache
 |
continuous batching
 |
CUDA kernel
```

一个粗糙的实现比阅读 100 篇论文学到的更多。

例如：

### 1. nanoGPT 级别

你已经训练了 GPT-2 124M。下一步：

实现你自己的：

```python
class CausalSelfAttention(nn.Module):
    def forward(self, x):
        qkv = self.c_attn(x)
        q, k, v = qkv.split(self.n_embd, dim=2)

        att = q @ k.transpose(-2,-1)
        att = att / math.sqrt(q.size(-1))

        mask = torch.tril(torch.ones(T,T))
        att = att.masked_fill(mask == 0, -inf)

        att = softmax(att)

        return att @ v
```

然后思考：

* 为什么会有 FlashAttention？
* 为什么内存成为瓶颈？
* 为什么 O(N²) 的注意力会带来问题？
* 为什么 KV 缓存改变了推理的复杂度？

---

### 2. 迷你 vLLM

一个小型 vLLM 是一个绝佳的项目。

开始：

```python
while True:
    request = queue.pop()

    tokens = model.generate(
        input_ids,
        kv_cache
    )

    yield tokens
```

然后添加：

**分页 KV 缓存**

不再使用：

```
request A
[###########........]

request B
[#####.............]
```

而是使用块：

```
GPU memory:

block 0 -> request A
block 1 -> request B
block 2 -> request A
block 3 -> request C
```

这教会了你为什么 vLLM 改变了服务方式。

---

### 3. CUDA 内核

不要从 FlashAttention 开始。

从一些不光彩的东西开始：

Python：

```python
C = A @ B
```

然后 CUDA：

```cuda
__global__
void matmul(float *A,float *B,float *C)
{
    int row = blockIdx.y * blockDim.y + threadIdx.y;
    int col = blockIdx.x * blockDim.x + threadIdx.x;

    float sum=0;

    for(int k=0;k<N;k++)
        sum += A[row*N+k]*B[k*N+col];

    C[row*N+col]=sum;
}
```

它会比 PyTorch 慢。

这没关系。

然后你会学到：

* 全局内存
* 共享内存
* warp
* occupancy
* tensor cores
* CUDA graph

---

你当前的背景实际上很适合这条路径：

* Java/后端 → 分布式系统直觉
* Kubernetes/云 → 服务知识
* GPT-2 训练 → 模型理解
* nano-vLLM → 推理理解
* GPU 实验 → 硬件直觉

缺失的不是智力。而是**花在实现原语上的时间**。

一个不错的 6 个月目标：

```
Month 1:
  nanoGPT 重写

Month 2:
  迷你 vLLM 推理引擎

Month 3:
  CUDA 扩展

Month 4:
  分布式训练玩具版本

Month 5:
  LoRA + RLHF 管线

Month 6:
  向 vLLM / llama.cpp / PyTorch 生态贡献 PR
```

关于 AI 基础设施有趣的一点是，那些看起来“不迷茫”的人通常只是积累了 5-10 年的伤疤：

* “为什么我的内核慢？”
* “为什么 NCCL 挂起？”
* “为什么 batch size 2 时 OOM？”
* “为什么 GPU 利用率只有 40%？”

构建丑陋的版本会创造这些伤疤。

一个自制的慢速 vLLM 以 5 tokens/s 运行，比运行一个完美的以 200 tokens/s 的 vLLM 教给你的更多。

对于瞄准 AI 基础设施的人来说，“我构建了一个小型 vLLM 和 CUDA 内核”比“我读过 vLLM 论文”是一个更强的信号。