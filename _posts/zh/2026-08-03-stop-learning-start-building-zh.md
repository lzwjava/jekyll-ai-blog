---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 停止学习，开始构建
translated: true
type: note
---

问题：根据我当前的AI工程路线，现在应该做什么？

答案：

鉴于你目前的状况——你已经从零训练了GPT-2，玩过nano-vLLM/vLLM、CUDA/ROCm、MI300X、本地GPU、代理，并且正在构建AI产品——最高杠杆的举动**不是更多的随机学习**。而是将你零散的实验转化为可见的AI工程作品集。

我建议未来3-6个月这样聚焦：

## 1. 选择一个“深度工程山峰”：LLM推理栈

你的方向应该是：

```
Transformer基础
        ↓
nanoGPT
        ↓
nano-vLLM
        ↓
vLLM / SGLang贡献
        ↓
CUDA内核 / GPU优化
        ↓
AI基础设施工程师
```

你已经接触了很多片段。现在深入下去。

具体操作：

```bash
git clone https://github.com/vllm-project/vllm
git clone https://github.com/sgl-project/sglang
```

阅读：

* attention实现
* KV缓存
* paged attention
* continuous batching
* tensor parallelism
* CUDA内核

然后提交小的PR：

* 文档改进
* 基准测试
* 错误修复
* ROCm支持
* 性能测试

目标不仅仅是知识。目标是：

> “我的GitHub显示我改进了被数百万AI用户使用的基础设施。”

这与“我又训练了一个玩具模型”是不同的信号。

---

## 2. 构建你自己的“迷你AI基础设施栈”

你拥有足够的硬件。

示例项目：

```
lzw-ai-runtime

model
 |
transformer.py
 |
attention.py
 |
kv_cache.py
 |
scheduler.py
 |
cuda_kernel.cu
 |
benchmark.py
```

从粗糙开始。

类似这样：

```python
while requests:
    batch = scheduler.next_batch()

    logits = model.forward(
        input_ids,
        kv_cache
    )

    next_token = sample(logits)

    update_kv_cache()
```

然后添加：

* 批处理
* 流式输出
* OpenAI兼容API
* 量化
* 推测解码

这会成为你的个人vLLM。

---

## 3. 发布一切

你已经有优势：

你的博客有流量。

将实验转化为工程文章：

示例：

```
How I trained GPT-2 124M on RTX 4070

Building nano-vLLM from scratch

Understanding PagedAttention by implementing it

CUDA Matrix Multiplication: from naive kernel to Tensor Core

Running LLM inference on AMD ROCm
```

AI社区看重：

```
构建者 + 解释 + 代码
```

远胜过证书。

---

## 4. 不要在通用AI应用上花费太多时间

代理很有趣，但护城河正在向下移动。

成千上万的人能构建：

```
LangChain + GPT API + UI
```

但能解释以下问题的人少得多：

```
为什么vLLM能实现更高吞吐量？

KV缓存内存布局如何工作？

FlashAttention如何减少HBM流量？
```

你之前关于GPU/内存的问题实际上正指向正确的方向。

---

## 5. 硬件方向

你的RTX 4070足够了。

现在不要通过购买GPU来优化。

一个好的学习设置：

```
RTX 4070
+
偶尔使用云上的MI300X / H100
+
AMD ROCm实验
```

学习：

```
CUDA
HIP
Triton
CUTLASS
FlashAttention
```

未来的AI栈是：

```
模型
   ↓
推理引擎
   ↓
编译器
   ↓
GPU内核
   ↓
ASIC硬件
```

你自然地朝着底层前进。

---

## 6. 职业定位

你最强的故事不是：

> “我正在学习AI。”

你的故事是：

> “我是一名软件工程师，从零构建模型，实现推理引擎，优化GPU工作负载，并为开源AI基础设施做出贡献。”

这是一个罕见的形象。

---

我建议立即开始接下来7天：

```
第1-2天：
阅读vLLM架构

第3天：
实现简单的paged KV缓存

第4天：
与朴素KV缓存进行基准测试

第5天：
写博客文章

第6-7天：
提交PR / 分享项目
```

下一步不是另一个教程。

而是交付一些能让人们说：

> “这个人端到端地理解AI栈。”
