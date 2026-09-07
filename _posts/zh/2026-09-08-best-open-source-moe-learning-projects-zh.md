---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 最佳开源MoE学习项目
translated: true
type: note
---

问题：**有哪些适合深入学习MoE的优秀开源项目？**

答案：如果你的目标不仅仅是*使用*MoE，而是理解**路由（router）→ 令牌分派（token dispatch）→ 专家计算（expert computation）→ 通信（communication）→ 专家并行（expert parallelism）→ CUDA效率**，我建议按以下顺序学习。

### 1. MegaBlocks — 最佳起点

MegaBlocks可能是我**最推荐的#1项目**。

[MegaBlocks GitHub](https://github.com/stanford-futuredata/megablocks?utm_source=chatgpt.com)

它使用块稀疏操作实现了高效的**无丢弃MoE（dropless MoE）**。重要的是，你可以看到从数学上的MoE：

```text
x
 │
 ▼
router
 │
 ├── expert 0
 ├── expert 1
 ├── expert 2
 └── ...
 │
 ▼
combine
```

过渡到实际能在GPU上高效映射的实现。

MegaBlocks特别解决了这个棘手的实际问题：

```text
tokens
   ↓
top-k routing
   ↓
每个专家分配的令牌数不固定（variable number of tokens per expert）
   ↓
??? 我如何在GPU上高效实现？
```

它使用块稀疏矩阵运算来避免令牌丢弃并提高GPU利用率。（[GitHub][1]）

**首先阅读以下部分：**

```text
megablocks/
    layers/
    ops/
    grouped_gemm/
```

其中 `grouped_gemm` / routing / permutation 代码特别有学习价值。

---

### 2. DeepSpeed-MoE — 理解专家并行（Expert Parallelism）的最佳选择

[DeepSpeed MoE GitHub](https://github.com/deepspeedai/DeepSpeed?utm_source=chatgpt.com)

DeepSpeed有一个显式的MoE实现：

```python
MoE(
    hidden_size=hidden_size,
    expert=expert,
    num_experts=8,
    ep_size=2,
    k=1,
)
```

其中有趣的参数是：

```text
ep_size
```

因为这会将你带入**专家并行（Expert Parallelism, EP）**。

例如：

```text
GPU0                 GPU1

expert 0             expert 4
expert 1             expert 5
expert 2             expert 6
expert 3             expert 7
```

令牌必须被路由到包含其所选专家的GPU：

```text
GPU0
 tokens
   │
   ├──────────────┐
   │              │
   ▼              ▼
local expert   GPU1 expert
                  │
                  ▼
              computation
                  │
   ◀──────────────┘
   │
   ▼
combine
```

此时MoE从单纯的神经网络架构问题变成了一个**分布式系统问题**。

DeepSpeed的实现公开了`TopKGate`、`MOELayer`、专家分组（expert groups）、容量因子（capacity factors）、令牌丢弃（token dropping）等。（[GitHub][2]）

其教程中还包含一个非常小的可运行MoE示例，在深入研究大型实现之前很有用。（[GitHub][3]）

---

### 3. DeepSeek-MoE — 理解现代MoE架构的最佳选择

[DeepSeek-MoE GitHub](https://github.com/deepseek-ai/DeepSeek-MoE?utm_source=chatgpt.com)

这个项目值得研究，因为DeepSeek并没有简单地采用：

```text
8 experts
top-2
```

他们的架构探索了**细粒度专家（fine-grained experts）**和**共享专家（shared experts）**。

概念上：

```text
                  ┌── shared expert
                  │
x → router ───────┼── expert 17
                  ├── expert 42
                  └── expert 91
```

这有助于理解为什么现代MoE越来越关注：

* 专家专业化（expert specialization）
* 共享专家（shared experts）
* 专家数量（number of experts）
* top-k
* 路由负载均衡（routing load balance）
* 辅助损失（auxiliary losses）
* 专家容量（expert capacity）
* 通信成本（communication cost）

该仓库包含了实际的模型/训练实现，而不仅仅是玩具实现。（[GitHub][4]）

---

### 4. Qwen3 — 最适合阅读的现代生产级模型

[Qwen3 GitHub](https://github.com/QwenLM/Qwen3/blob/main/docs/source/getting_started/concepts.md?ref=aiposthub.com&utm_source=chatgpt.com)

Qwen3有以下版本：

```text
Qwen3-30B-A3B
Qwen3-235B-A22B
```

命名本身就有教育意义：

```text
30B-A3B

30B       总参数量（total parameters）
3B        每个令牌激活的参数量（active parameters/token）
```

因此：

```text
        30B parameters
             │
             ▼
        ┌─────────┐
x ────► │ router  │
        └────┬────┘
             │ top-k
       ┌─────┴─────┐
       ▼           ▼
   expert A     expert B
       │           │
       └─────┬─────┘
             ▼
          output

~3B parameters actually participate
```

这正是MoE强大的根本经济原因：

> **大参数容量，却不必为每个令牌上的每个参数支付稠密模型的计算代价。**

Qwen3官方同时提供了稠密模型和MoE模型，包括30B-A3B和235B-A22B。（[GitHub][5]）

---

### 5. Megatron-Core MoE — 当你想要成为MoE训练工程师时的最佳选择

当你理解了上述内容后，可以进入Megatron-LM / Megatron-Core。

有趣的部分变成：

```text
数据并行（Data Parallelism）
        +
张量并行（Tensor Parallelism）
        +
流水线并行（Pipeline Parallelism）
        +
专家并行（Expert Parallelism）
        +
序列并行（Sequence Parallelism）
        +
分布式检查点（Distributed checkpointing）
```

尤其是：

```text
MoE Token Dispatcher
        ↓
All-to-All
        ↓
Grouped GEMM
        ↓
All-to-All
        ↓
Combine
```

这部分我建议你花大量时间学习。

此外，目前还有基于Megatron-Core的DeepSeek-V3、Qwen3和Mixtral的开放训练方案，包括H100/B200/GB200/GB300的配置。（[GitHub][6]）

---

## 我推荐的学习路径

鉴于你已经在进行PyTorch/CUDA/LLM训练，我不建议你从一个庞大的框架开始。

我建议你逐步构建以下内容：

```text
01_toy_moe.py
       ↓
02_topk_router.py
       ↓
03_load_balancing.py
       ↓
04_token_dispatch.py
       ↓
05_grouped_gemm.py
       ↓
06_distributed_experts.py
       ↓
07_all_to_all.py
       ↓
08_expert_parallel.py
       ↓
09_megablocks.py
       ↓
10_deepseek_moe.py
       ↓
11_megatron_moe.py
```

第一个版本可以是**大约100行的PyTorch代码**：

```python
class MoE(nn.Module):
    def __init__(self, dim, hidden, n_experts, k):
        self.router = nn.Linear(dim, n_experts)
        self.experts = nn.ModuleList([
            MLP(dim, hidden)
            for _ in range(n_experts)
        ])
        self.k = k

    def forward(self, x):
        # x: [tokens, dim]

        logits = self.router(x)
        weights, indices = logits.topk(self.k, dim=-1)

        weights = weights.softmax(dim=-1)

        y = torch.zeros_like(x)

        for e, expert in enumerate(self.experts):
            mask = (indices == e)

            # select tokens routed to expert e
            token_ids = mask.nonzero()[:, 0]

            if len(token_ids) == 0:
                continue

            out = expert(x[token_ids])

            # combine expert output
            ...
        
        return y
```

然后**真正的学习从你删除Python循环开始**。

你将：

```python
for expert in experts:
    expert(tokens)
```

替换为更接近：

```text
routing
   ↓
permutation
   ↓
[expert0 tokens]
[expert1 tokens]
[expert2 tokens]
...
   ↓
Grouped GEMM
   ↓
unpermutation
   ↓
weighted combine
```

然后分布专家：

```text
                  NETWORK

GPU0 ── tokens ── AllToAll ──► GPU1
 │                              │
 │                              ▼
 │                          experts 4-7
 │
 ▼
experts 0-3
 │
 └──────────── AllToAll ◄────────────┘
```

**这种渐进式学习会比单纯阅读MoE论文教会你更多。**

### 我的排名

| 项目               | 你学到的内容                                  | 难度 |
| ------------------ | --------------------------------------------- | ----: |
| **MegaBlocks**     | 高效MoE / 块稀疏 / Grouped GEMM              |   ⭐⭐⭐ |
| **DeepSpeed-MoE**  | Router + 专家并行（Expert Parallelism）        |   ⭐⭐⭐ |
| **DeepSeek-MoE**   | 现代MoE架构                                   |   ⭐⭐⭐ |
| **Qwen3**          | 真实生产级MoE模型                             |  ⭐⭐⭐⭐ |
| **Megatron-Core**  | 大规模分布式MoE                               | ⭐⭐⭐⭐⭐ |

如果你的目标具体是**MoE + CUDA + GPU系统**，我建议你花最多时间在**MegaBlocks → DeepSpeed-MoE → Megatron-Core**，而不是从Qwen/DeepSeek模型代码开始。

我也可以为你构建一个**最小化的200行MoE实现，并逐步将其转化为专家并行+All-to-All**，这将是一个非常实用的学习路径。

[1]: https://github.com/mistralai/megablocks-public?utm_source=chatgpt.com "GitHub - mistralai/megablocks-public · GitHub"
[2]: https://github.com/deepspeedai/DeepSpeed/blob/master/deepspeed/moe/layer.py?utm_source=chatgpt.com "DeepSpeed/deepspeed/moe/layer.py at master · deepspeedai/DeepSpeed · GitHub"
[3]: https://github.com/deepspeedai/DeepSpeed/blob/master/docs/_tutorials/mixture-of-experts.md?utm_source=chatgpt.com "DeepSpeed/docs/_tutorials/mixture-of-experts.md at master · deepspeedai/DeepSpeed · GitHub"
[4]: https://github.com/deepseek-ai/DeepSeek-MoE?utm_source=chatgpt.com "GitHub - deepseek-ai/DeepSeek-MoE: DeepSeekMoE: Towards Ultimate Expert Specialization in Mixture-of-Experts Language Models · GitHub"
[5]: https://github.com/maximisto/qwen3?utm_source=chatgpt.com "GitHub - maximisto/qwen3: Qwen3 is the large language model series developed by Qwen team, Alibaba Cloud. · GitHub"
[6]: https://github.com/yanring/Megatron-MoE-ModelZoo?utm_source=chatgpt.com "GitHub - yanring/Megatron-MoE-ModelZoo: Best practices for training DeepSeek, Mixtral, Qwen and other MoE models using Megatron Core. · GitHub"
