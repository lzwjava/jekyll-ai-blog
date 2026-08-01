---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 为vLLM和SGLang做贡献
translated: true
type: note
---

**问题：我是否应该在未来几个月内为 SGLang 和 vLLM 等开源项目做出贡献？**

**回答：是的。针对你当前的方向，这可能是你能做的最具杠杆效应的事情之一。**

基于你的背景：

* 你已经训练过 GPT-2/nanoGPT 模型。
* 你接触过 ROCm、MI300X、CUDA、vLLM、nano-vLLM。
* 你的目标是 AI 基础设施 / LLM 工程岗位。
* 你缺乏传统的计算机科学学位，因此**公开的能力证明非常重要**。

为 vLLM 和 SGLang 这样的项目做贡献，比再拿一张证书或完成一门课程能提供更有力的证据。

原因很简单：

一家招聘 AI 基础设施工程师的公司会问：

> "这个人能理解一个大型分布式机器学习系统并改进它吗？"

一个被合并的 PR 比简历上的一行文字更能回答这个问题。

---

## 适合你的好目标

### 1. 从 vLLM 开始

不要立即尝试重写 CUDA 内核。

首先理解整个栈：

```
API server
    |
engine
    |
scheduler
    |
worker
    |
model executor
    |
attention backend
    |
CUDA kernels
```

你的初期贡献可以是：

* 文档修复
* Bug 复现
* 测试
* 性能基准测试
* 调度器的小改进
* ROCm 兼容性
* AMD GPU 支持

鉴于你对 AMD MI300X/ROCm 的兴趣，这其实是一个细分领域。

---

### 2. SGLang 也非常有趣

SGLang 主要关注：

* 结构化生成
* 服务效率
* RadixAttention
* KV 缓存管理
* 推测解码

你已经探索过 KV 缓存和推理内部机制，因此这与你的学习路径相匹配。

---

## 一个现实的三个月计划

### 第 1 个月：成为一个用户

在本地运行所有内容。

示例：

```bash
git clone https://github.com/vllm-project/vllm
cd vllm

pip install -e .

python examples/offline_inference/basic.py
```

然后追踪流程：

```
request
 -> scheduler
 -> sequence groups
 -> KV cache allocation
 -> attention
 -> logits
```

写下笔记。

---

### 第 2 个月：选择一个子系统

例如：

KV 缓存。

理解：

```
tokens
 |
attention
 |
K,V tensors

K = [num_layers, heads, seq_len, head_dim]
V = [num_layers, heads, seq_len, head_dim]
```

然后研究：

* PagedAttention
* block manager
* memory allocation

做出一个小改进。

---

### 第 3 个月：提交 PR

好的初学 PR 示例：

```
Fix ROCm build issue
Add benchmark
Improve error message
Add test case
Optimize small bottleneck
Update documentation
```

目标不是为了出名。

目标：

```
GitHub profile:
    vLLM PR #xxxxx
    SGLang PR #xxxxx
    CUDA benchmark repo
    nano-vLLM implementation
```

这能改变工程师对你的评价。

---

## 一个可能的个人项目组合

我认为你最强的作品集应该是：

```
1. nanoGPT
    |
    v
2. nano-vLLM
    |
    v
3. contribute to vLLM/SGLang
    |
    v
4. build an AMD ROCm inference demo
```

这讲述了一个连贯的故事：

> "我理解训练、推理、内核和部署。"

很少有工程师能解释整个流水线。

---

一个警告：

不要花 6 个月只读代码。

循环应该是：

```
read 20%
modify 30%
break things 30%
submit 20%
```

大型开源系统是通过动手接触来学习的。

对你而言，未来几个月内一个被合并的 vLLM/SGLang PR 很可能比另一门 AI 课程更有价值。
