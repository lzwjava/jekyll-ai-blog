---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 通过动手迭代学习vLLM
translated: true
type: note
---

**问题：为什么学习 vLLM / inference 需要像 nanoGPT 训练一样的迭代循环？**

**回答：**

是的，完全正确。让 nanoGPT 变得易懂的**实验循环**，正是理解 vLLM、nano-vLLM 和推理系统的正确方法。

区别在于：

* nanoGPT → 你学到了**模型如何学习**
* nano-vLLM → 你学到了**模型如何高效运行**

但方法论是相同的：

```
假设
   ↓
改变一个变量
   ↓
运行实验
   ↓
打印日志 / 检查张量 / 测量
   ↓
建立心智模型
   ↓
重复
```

这基本上也是 Karpathy 学习系统的方式。

---

对于 nanoGPT，你的循环是：

```
model.py
   |
   | print(loss)
   | print(tokens)
   | print(attention)
   | modify architecture
   |
train
   |
观察行为
```

运行 13 个小模型后，你的大脑积累了：

* loss 曲线长什么样
* 过拟合行为
* 欠训练行为
* 数据集质量的影响
* 参数缩放
* 上下文长度的影响
* 优化器行为

你没有“阅读 transformer 理论”；你构建了一个内部模拟器。

---

对于 vLLM 也是如此，但变量不同。

一个 transformer 的前向传播：

```
tokens
  |
embedding
  |
attention
  |
MLP
  |
logits
  |
sampling
  |
下一个 token
```

vLLM 增加了服务层：

```
HTTP 请求
      |
 tokenizer
      |
 scheduler
      |
 KV cache manager
      |
 GPU 执行
      |
 sampling
      |
 流式输出 tokens
```

你需要观察：

### 1. 不同的输入长度

示例：

```
Prompt A:
"hello"

Prompt B:
10000 tokens 的文档
```

观察：

* prefill 延迟
* 内存使用
* KV cache 增长

你会开始理解：

“啊，长 prompt 的成本和生成成本不一样。”

---

### 2. 不同的生成长度

示例：

```
输入:
解释 transformer

max_tokens=20

vs

max_tokens=2000
```

观察：

* 解码速度
* tokens/sec
* GPU 利用率

你会发现：

```
prefill = 计算密集

decoder = 内存带宽密集
```

---

### 3. 不同的模型

运行：

```
Qwen3-8B
Llama-8B
Mistral-7B
```

相同的服务器。

观察：

```
模型大小
      |
      v
VRAM
      |
      v
KV cache 容量
      |
      v
batch size
      |
      v
吞吐量
```

然后 vLLM 架构就变得直观了。

---

### 4. 改变调度器参数

例如：

```
max_num_seqs
max_model_len
gpu_memory_utilization
```

运行：

```
10 个用户
50 个用户
100 个用户
```

观察：

```
延迟
吞吐量
OOM
```

你会理解为什么 vLLM 发明了 PagedAttention。

---

关键实验：

运行一个小型 nano-vLLM。

类似这样：

```
nano-vllm/
 ├── engine.py
 ├── scheduler.py
 ├── attention.py
 ├── kv_cache.py
 └── sampler.py
```

添加日志：

```python
print(
    "request",
    request_id,
    "prompt_len",
    len(tokens),
)

print(
    "kv blocks",
    len(kv_cache.blocks)
)

print(
    "batch size",
    len(active_requests)
)
```

然后发送：

```
请求 1:
短 prompt

请求 2:
长 prompt

请求 3:
代码生成
```

观察调度器。

当你看到：

```
Request A:
tokens 0-4096

KV blocks:
[1][2][3][4]

Request B:
tokens 0-512

KV blocks:
[5]
```

PagedAttention 就不再只是一个论文概念。

它变成了你亲眼目睹发生的事情。

---

你之前的 nanoGPT 学习模式实际上更接近科研工程师的工作方式：

不是：

```
读论文
记公式
实现
```

而是：

```
实现
搞坏它
测量它
做出错误假设
修正心智模型
```

对于 vLLM，我会遵循同样的递进：

```
Step 1:
llama.cpp inference

Step 2:
naive PyTorch generate()

Step 3:
批量处理多个请求

Step 4:
添加 KV cache

Step 5:
continuous batching

Step 6:
PagedAttention

Step 7:
CUDA kernel optimization
```

每一步都应该是“小模型实验”。

通常最大的飞跃是在你实现 **continuous batching + KV cache management** 的时候。这就是推理系统开始变得不同于普通 ML 代码的地方。你不再思考“一个输入 → 一个输出”，而是开始思考“GPU 时间调度器管理多个 token 流”。