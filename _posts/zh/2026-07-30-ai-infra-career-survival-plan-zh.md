---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AI基础设施职业生存计划
translated: true
type: note
---

问题：**鉴于我的情况（AI infra转型，无正式学历，房贷900k CNY，明天从银行外包离职），我该如何生存并规划我的职业生涯？**

回答：

首先：**不要把自己当作一个新手AI工程师。** 你的处境很特殊。

你拥有：

* 11年engineering经验
* backend/distributed systems经验
* cloud/Linux/Kubernetes
* 真实的LLM训练经验：
  * 从零开始的GPT-2 124M
  * nanoGPT/nanochat实验
  * vLLM探索
  * GPU调试
  * CUDA/ROCm接触
* 之前交付过产品

问题不在于能力。问题在于**市场信号**。

学历是HR的过滤器。它不是AI infra的核心要求。

但是背负着900k CNY房贷，你不能做出不切实际的“辞职全部去研究AI”的举动。你需要一个**双轨策略**。

---

## 1. 接下来的3个月：生存模式

你的优先级：

**现金流 > 完美的AI工作**

不要耗尽缓冲期。

你的目标：

* 保持收入：月薪20k-40k RMB
* 每个月向AI infra靠近一步

可能的路径：

### 路径A：AI Infrastructure Engineer（最佳）

职位：

* LLM Platform Engineer
* Inference Engineer
* ML Infrastructure Engineer
* AI Backend Engineer
* Agent Infrastructure Engineer

你已有的backend背景很匹配。

陈述：

> “Backend engineer转型到LLM infra。构建并训练了GPT模型，部署了推理系统，优化了GPU工作负载。”

而不是：

> “我没有学历，想学AI。”

---

### 路径B：AI咨询/外包

你已经有了优势。

很多公司需要：

* RAG系统
* 私有LLM部署
* agent工作流
* 内部AI工具

一个小公司可能支付：

* 每个项目30k-80k RMB

你的工程背景在这里很有价值。

---

### 路径C：保持一个过渡工作

一个错误的做法是：

```
bank contractor
     |
     v
unemployed
     |
     v
study AI 6 months
     |
     v
job hunting
```

房贷使这变得危险。

更好的做法：

```
bank contractor
      |
      +---- freelance AI projects
      |
      +---- AI infra portfolio
      |
      v
AI infra job
```

---

# 2. 你的AI infra路线图

不要再学习更多的模型了。

你理论上已经知道得足够多了。

现在构建生产环境的证据。

## 第1个月

构建：

### 项目1：Mini vLLM clone

实现：

```
prompt
 |
tokenizer
 |
KV cache
 |
continuous batching
 |
scheduler
 |
CUDA kernel
 |
generation
```

即使是玩具版本。

仓库：

```
github.com/lzwjava/my-vllm
```

README：

```
Implemented:
- PagedAttention
- KV cache management
- batching scheduler
- tensor parallel inference
```

这代表了AI infra。

---

## 第2个月

构建：

### 生产级LLM serving stack

示例：

```
Client
 |
FastAPI
 |
Ray
 |
vLLM
 |
NVIDIA GPU
 |
Prometheus
 |
Grafana
```

添加：

* autoscaling
* monitoring
* latency benchmark

测量：

```
tokens/sec
TTFT
GPU utilization
memory usage
```

---

## 第3个月

向上游贡献。

目标：

* vLLM
* llama.cpp
* PyTorch
* Triton

即使是很小的PR。

一个合并的PR可以取代学历信号。

---

# 3. 学历问题

现实情况：

大公司：

```
Google
Meta
OpenAI
Anthropic
NVIDIA
```

通常使用学历过滤器。

但AI infra生态系统不同。

很多团队关心的是：

```
你能让GPU更便宜吗？
你能提高throughput吗？
你能debug CUDA吗？
你能部署模型吗？
```

你的优势：

大多数拥有学历的人做不到你已经做过的事情。

一个拥有CS PhD但没有生产经验的人可能不知道：

```
nvidia-smi故障
CUDA不匹配
flash-attn构建
distributed training
Linux内核问题
```

但你知道。

---

# 4. 背负900k CNY房贷的财务计划

假设：

房贷：

900k RMB

不要首先优化最大薪水。

优化：

```
生存概率
```

你的层级：

## 第1层

稳定收入：

月薪20k+

↓

## 第2层

AI转型

↓

## 第3层

月薪30k-50k AI infra

↓

## 第4层

咨询/创业

---

避免：

* 购买更多GPU硬件
* 花6个月只读论文
* 追逐PhD-level理论
* 没有收入就辞职

你已经拥有足够的算力。

你的RTX 4070足够用于portfolio工作。

---

# 5. 你的故事很重要

你的背景实际上是一个有力的founder/engineer故事：

```
自学成才的程序员
 |
mobile/backend engineer
 |
built products
 |
学习deep learning
 |
本地训练GPT模型
 |
构建AI infra
```

这更接近：

* Karpathy风格
* 独立researcher-engineer

而不是传统的研究生。

利用它。

---

# 6. 我推荐接下来的12个月

```
2026年8月-9月

获得收入过渡
+
构建类似vLLM的项目


2026年10月-12月

申请：
- AI infra engineer
- LLM平台工程师
- AI backend engineer

贡献OSS


2027年

选择：

A：
Senior AI infra engineer

或

B：
AI咨询公司

或

C：
AI startup
```

---

明天的关键决定不是“我应该离开银行工作吗？”

关键问题是：

**离职后，你还有多少个月的缓冲期？**

计算：

```
现金储蓄 / 每月家庭支出
```

如果缓冲期小于6个月：

在转型的同时立即获得收入。

如果缓冲期大于12个月：

你可以积极构建AI infra portfolio。

鉴于你的房贷，我个人建议优化为**收入 + AI转型同步进行**，而不是纯粹的探索。你已经过了初级阶段；下一步是将你的AI能力转化为市场证明。
