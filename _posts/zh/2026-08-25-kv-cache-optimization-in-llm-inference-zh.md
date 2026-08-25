---
audio: false
generated: true
image: false
lang: zh
layout: post
title: LLM推理中的KV缓存优化
translated: true
type: note
---

问题：`nano-vLLM` 及类似的最小化 LLM 推理引擎中的 KV 缓存是如何工作的？

答案：核心思想是：

> **KV 缓存将自回归解码从"对每个 token 重新计算整个前缀的注意力"转变为"计算一次 K/V，追加它们，仅计算新 token 的 Q"。**

对于 transformer 层，给定 tokens (x_1,\ldots,x_t)：

[
Q = XW_Q,\quad K=XW_K,\quad V=XW_V
]

因果注意力为：

[
\text{Attention}(Q,K,V)
=======================

\text{softmax}\left(\frac{QK^T}{\sqrt{d}}\right)V
]

在生成过程中，假设我们已经生成了 1000 个 tokens，现在想要生成第 1001 个 token。

### 无 KV 缓存

实际上你做了：

```text
tokens[0:1001]
       ↓
embedding
       ↓
为所有 1001 个 tokens 计算 Q, K, V
       ↓
注意力
       ↓
下一个 token
```

然后对于 token 1002：

```text
tokens[0:1002]
       ↓
重新计算所有 1002 个 tokens 的 Q, K, V
```

所以你是在反复重新计算旧的 K/V。

### 有 KV 缓存

在 token 1001 时：

```text
旧的 KV 缓存：
K[0:1000], V[0:1000]

新的 token：
x1001
  ↓
Q1001, K1001, V1001
  ↓
追加 K1001, V1001
  ↓
attention(Q1001, K[0:1001], V[0:1001])
```

在 token 1002 时：

```text
Q1002
   │
   ├── K 缓存：K0 ... K1002
   └── V 缓存：V0 ... V1002
             ↓
          注意力
```

你每层只计算**一个新的 Q/K/V**。

---

## 1. nano-vLLM 实际缓存的内容

概念上，每个 transformer 层都有：

```python
k_cache[layer][position]
v_cache[layer][position]
```

对于一个标准的多头注意力模型：

```text
K 缓存
[layer]
   └── [sequence position]
          └── [KV head]
                 └── [head dimension]

V 缓存
[layer]
   └── [sequence position]
          └── [KV head]
                 └── [head dimension]
```

例如：

```python
k_cache.shape
# [num_layers, max_seq_len, num_kv_heads, head_dim]

v_cache.shape
# [num_layers, max_seq_len, num_kv_heads, head_dim]
```

在 `nano-vLLM` 中的具体布局可能有所不同，因为布局针对 CUDA 内核进行了高度优化，但这是概念模型。

---

# 2. 重要技巧：只有最新的 token 需要 Q

假设：

```text
prompt = "The capital of France is"
```

提示阶段称为**prefill**。

你同时处理所有 tokens：

```text
X
│
├── Q
├── K ───────────────→ KV 缓存
└── V ───────────────→ KV 缓存
```

对于：

```text
"The capital of France is"
```

你得到：

```text
K0 K1 K2 K3 K4
V0 V1 V2 V3 V4
```

并保存它们。

然后假设模型预测：

```text
Paris
```

现在你有：

```text
K0 K1 K2 K3 K4 K5
V0 V1 V2 V3 V4 V5
```

对于下一步生成，你不需要计算：

```text
Q0 Q1 Q2 Q3 Q4 Q5
K0 K1 K2 K3 K4 K5
V0 V1 V2 V3 V4 V5
```

你只需计算：

```text
Q6 K6 V6
```

然后：

```text
Q6
 │
 ├────────────── K0
 ├────────────── K1
 ├────────────── K2
 ├────────────── K3
 ├────────────── K4
 ├────────────── K5
 └────────────── K6
                  ↓
              softmax
                  ↓
             V0...V6
```

这就是基本的 KV 缓存算法。

---

# 3. 为什么这如此重要

没有缓存时，生成的工作量大约为：

[
O(T^2)
]

对于长度为 (T) 的序列，因为每个新 token 都会重复处理旧的前缀。

使用 KV 缓存时，生成的增量投影工作大约为：

[
O(T)
]

加上注意力扫描：

[
q_t K_{0:t}^T
]

对于每个生成的 token 是 (O(t))。

所以总的解码注意力工作仍然是：

[
\sum_{t=1}^{T} O(t) = O(T^2)
]

但**巨大的重复 K/V 投影和 transformer 计算消失了**。

这个区别很重要。

KV 缓存**并没有**神奇地使注意力本身随序列长度变为线性。它通过避免重新计算先前状态来大幅降低自回归解码的成本。

---

# 4. nano-vLLM 更有趣的问题：批处理请求

这是 `vLLM` 风格系统比简单 Hugging Face 实现有趣得多的地方。

想象：

```text
请求 A：
"The cat sat on"

请求 B：
"Once upon a time"

请求 C：
"Explain transformers"
```

它们的长度不同。

你不想要：

```text
GPU 内存
┌────────────────────────────┐
│ 请求 A KV                  │
│ 请求 B KV                  │
│ 请求 C KV                  │
│ 巨大的连续张量              │
└────────────────────────────┘
```

因为序列在不断增长。

相反，现代引擎使用**分页/块 KV 缓存**。

---

# 5. 分页 KV 缓存

想象虚拟内存。

不是：

```text
sequence
0 1 2 3 4 5 6 7 8 9 ...
```

需要一次巨大的连续分配，而是将其分成块：

```text
块 0：tokens  0-15
块 1：tokens 16-31
块 2：tokens 32-47
...
```

然后维护一个映射：

```text
请求 A
逻辑块 0 → 物理块 17
逻辑块 1 → 物理块 42
逻辑块 2 → 物理块  3

请求 B
逻辑块 0 → 物理块  8
逻辑块 1 → 物理块 19
```

因此 GPU 内存看起来更像：

```text
物理 KV 内存：

[块 0]
[块 1]
[块 2]
...
[块 17] ← A 的逻辑块 0
...
[块 42] ← A 的逻辑块 1
...
```

序列不关心它的块在物理上是否相邻。

这基本就是**KV 缓存的虚拟内存**。

---

# 6. 为什么这被称为 PagedAttention

原始的 vLLM 理念本质上是：

```text
虚拟 token 位置
        ↓
逻辑 KV 块
        ↓
块表
        ↓
物理 KV 块
        ↓
GPU 内存
```

例如：

```python
block_table = {
    request_A: [17, 42, 3],
    request_B: [8, 19],
}
```

注意力内核接收块映射并获取适当的 K/V 块。

这同时解决了几个问题：

* 变长序列
* 动态序列增长
* GPU 内存碎片
* 连续批处理
* KV 缓存共享
* 前缀缓存

---

# 7. GQA 大幅减小 KV 缓存

这是现代模型的另一个重要细节。

假设：

```text
num_attention_heads = 32
num_kv_heads       = 8
head_dim            = 128
```

对于标准 MHA：

```text
K：32 个头
V：32 个头
```

对于 GQA：

```text
Q：32 个头
K： 8 个头
V： 8 个头
```

每个 KV 头被 4 个 Q 头共享：

```text
Q0 Q1 Q2 Q3 → KV0
Q4 Q5 Q6 Q7 → KV1
...
```

所以 KV 内存减少了：

[
\frac{32}{8}=4\times
]

这对推理来说**至关重要**。

对于一个具有以下参数的模型：

```text
L = 32 层
H_kv = 8
D = 128
上下文 = 32K
数据类型 = FP16
```

一个序列的 KV 内存大约为：

[
2 \times L \times H_{kv} \times D \times T \times 2\text{ 字节}
]

结果为：

[
2 \times 32 \times 8 \times 128 \times 32768 \times 2
\approx 4\text{ GiB}
]

因此单个 32K 序列可能消耗 **约 4 GB 仅用于 KV 缓存**。

这就是为什么推理引擎如此关注 KV 内存。

---

# 8. Prefill 与 Decode

阅读 nano-vLLM 代码时，理解这个区别至关重要。

### Prefill

你有：

```text
prompt = 1000 个 tokens
```

执行：

```python
Q, K, V = model(prompt)
```

并填充：

```text
KV 缓存：
[0 ... 999]
```

这一步高度并行且计算密集。

### Decode

现在生成一个 token：

```text
1000 → 1001
1001 → 1002
1002 → 1003
...
```

每次迭代基本上执行：

```python
q, k, v = model(new_token)

cache.append(k, v)

logits = attention(
    q,
    cache.K,
    cache.V,
)
```

批处理维度可能包含许多请求：

```text
请求 A → token
请求 B → token
请求 C → token
请求 D → token
```

这就是连续批处理变得强大的地方。

---

# 9. 最小化实现

一个玩具 KV 缓存实际上可以是这样：

```python
class KVCache:
    def __init__(self, max_seq_len, n_kv_heads, head_dim):
        self.k = torch.empty(
            max_seq_len,
            n_kv_heads,
            head_dim,
            device="cuda",
        )

        self.v = torch.empty(
            max_seq_len,
            n_kv_heads,
            head_dim,
            device="cuda",
        )

    def update(self, pos, k, v):
        self.k[pos] = k
        self.v[pos] = v

    def get(self, end):
        return self.k[:end], self.v[:end]
```

然后解码：

```python
for pos in range(prompt_len, max_seq_len):

    q, k, v = model(
        input_ids[:, pos:pos+1]
    )

    cache.update(pos, k, v)

    K, V = cache.get(pos + 1)

    y = attention(q, K, V)

    next_token = sample(y)
```

这基本上就是概念核心。

真正的 `nano-vLLM` 实现增加了：

```text
块分配
块表
批处理请求
CUDA 内核
RoPE
GQA
内存管理
连续批处理
采样
```

但基本的状态机保持不变。

---

# 10. 真正重要的思维模型

将 KV 缓存视为**跨自回归时间的持久化中间激活**。

通常：

```text
t 时刻的 token
   ↓
transformer
   ↓
K, V
   ↓
丢弃
```

KV 缓存将其改变为：

```text
t 时刻的 token
   ↓
transformer
   ↓
K, V
   ↓
GPU 内存
   ↓
被每个未来 token 使用
```

因此模型的有效状态变为：

```text
Transformer 权重
        +
KV 缓存
        ↓
下一个 token 分布
```

**权重是静态的**，而 **KV 缓存是每个活动序列的动态状态**。

这也是为什么服务 LLM 与服务普通的无状态神经网络根本不同。

---

## 如果你阅读 nano-vLLM 源码

我会按以下顺序追踪这四个方面：

```text
1. 请求 / 调度器
       ↓
2. KV 缓存块分配
       ↓
3. Model.forward()
       ↓
4. 注意力内核
```

特别关注路径：

```text
请求
  → 块表
  → 槽位映射
  → k_cache / v_cache
  → attention()
```

一旦你理解了 **`block_table` + `slot_mapping` + K/V 张量布局**，nano-vLLM 的 KV 缓存实现就不再那么神秘。其余部分主要是让这个简单的算法在 GPU 上高效运行。
