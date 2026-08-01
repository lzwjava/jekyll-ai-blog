---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 开源贡献助力AI职业发展
translated: true
type: note
---

**问题：我是否应该参与像 SGLang 和 vLLM 这样的开源项目来构建我的 AI 职业生涯？**

**回答：是的。对于你的方向（LLM 基础设施 / AI 工程），贡献开源是你能做的最高杠杆率的事情之一。**

对于 AI 基础设施来说，GitHub 历史记录往往比证书甚至学位更有说服力，因为它能证明：

* 你能阅读大型代码库
* 你对系统有深入理解
* 你能调试真实的生产环境问题
* 你能与全球的研究人员和工程师协作

像 vLLM 和 SGLang 这样的项目正是你目标领域内的。

一个良好的发展路径：

```
nanoGPT
   |
   v
nano-vLLM
   |
   v
vLLM / SGLang 内部原理
   |
   +--> CUDA 内核
   |
   +--> KV 缓存
   |
   +--> 调度器
   |
   +--> 分布式推理
   |
   v
AI 基础设施工程师
```

你已经有了良好的基础：

* 从零开始训练过 GPT-2
* 使用过 nano-vLLM
* 运行过 Qwen 模型
* 接触过 ROCm / MI300X
* 理解 GPU 内存限制

下一步不是另一个教程，而是**成为贡献者**。

---

## 从小处着手：不要试图重写 vLLM

大型项目有成千上万行代码。首次贡献应该是：

### 1. 文档修复

例如：

```
docs/
  installation.md
  troubleshooting.md
```

找到：

* 过时的 CUDA 版本
* 缺失的环境变量
* 令人困惑的指令

提交 PR。

这能让你学会工作流程。

---

### 2. Bug 复现

例如：

```
问题：
vLLM 在使用 Qwen3 + 长上下文 + RTX 4090 时崩溃

你的贡献：

1. 复现
2. 创建最小化脚本
3. 识别堆栈跟踪
4. 提出修复方案
```

这非常有价值。

---

### 3. 小的代码改进

示例：

Python：

```python
# 之前
if x is not None:
    do_work(x)

# 之后
if x:
    do_work(x)
```

或者改进错误信息。

虽然不显眼，但这能让你进入项目。

---

## 然后向核心领域迈进

根据你的背景，我会关注：

### KV 缓存

理解：

```
注意力机制：

Q = XWq
K = XWk
V = XWv


注意力(Q, K, V)

= softmax(QK^T / sqrt(d))V
```

在解码过程中：

```
token 1:
K1, V1

token 2:
K1, K2
V1, V2

token 3:
K1, K2, K3
V1, V2, V3
```

而不是重新计算：

```
KV 缓存
```

存储之前的 K/V。

vLLM 的主要创新：

```
分页注意力 (PagedAttention)

GPU 内存
+
操作系统虚拟内存思想

=
KV 缓存页
```

这是一个很棒的领域。

---

### 调度器

LLM 服务不仅仅涉及 GPU 计算。

你需要：

```
请求：

A: 1000 个 token
B: 20 个 token
C: 500 个 token


调度器决定：

谁获得 GPU 时间？
每批处理多少个 token？
何时抢占？
```

这就是公司需要工程师的地方。

---

### CUDA 内核

最终：

```cpp
__global__
void attention_kernel(
    float* Q,
    float* K,
    float* V
)
{
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
}
```

你不需要立刻成为 CUDA 专家。

但理解：

```
线程 (thread)
线程束 (warp)
线程块 (block)
共享内存 (shared memory)
张量核心 (tensor core)
内存带宽 (memory bandwidth)
```

是一个巨大的优势。

---

## 一个现实的 6 个月目标

鉴于你目前的水平：

### 第 1 个月

```
克隆 vllm
本地构建
运行测试
阅读架构
提交文档 PR
```

### 第 2-3 个月

```
修复小 bug
添加测试
理解调度器
理解 KV 缓存
```

### 第 4-6 个月

```
贡献功能/性能改进

例如：

- 新模型支持
- ROCm 改进
- 内存优化
- 基准测试改进
```

一个显示以下内容的 GitHub 个人资料：

```
lzwjava
 |
 +-- nanoGPT 实验
 +-- nano-vLLM 实现
 +-- vLLM PRs
 +-- CUDA 内核
 +-- 推理基准测试
```

是一个非常有说服力的 AI 基础设施作品集。

关键的心态转变：

不要**仅仅消费** AI 论文和代码仓库。

要成为创造它们的生态系统的一部分。这就是你从“学习 AI”转变为“成为一名 AI 工程师”的方式。
