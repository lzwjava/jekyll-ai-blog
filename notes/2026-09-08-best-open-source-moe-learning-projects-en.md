---
audio: false
generated: true
image: false
lang: en
layout: post
title: Best Open-Source MoE Learning Projects
translated: false
type: note
---

Question: **What are good open-source projects to learn MoE deeply?**

Answer: If your goal is not just *using* MoE but understanding **router → token dispatch → expert computation → communication → expert parallelism → CUDA efficiency**, I’d learn them in this order.

### 1. MegaBlocks — best starting point

MegaBlocks is probably my **#1 recommendation**.

[MegaBlocks GitHub](https://github.com/stanford-futuredata/megablocks?utm_source=chatgpt.com)

It implements efficient **dropless MoE** using block-sparse operations. The important thing is that you can see the transition from the mathematical MoE:

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

to something that actually maps efficiently onto GPUs.

MegaBlocks specifically addresses the ugly practical problem:

```text
tokens
   ↓
top-k routing
   ↓
variable number of tokens per expert
   ↓
??? how do I make this efficient on GPU?
```

It uses block-sparse matrix operations to avoid token dropping and improve GPU utilization. ([GitHub][1])

**Read these parts first:**

```text
megablocks/
    layers/
    ops/
    grouped_gemm/
```

The `grouped_gemm` / routing / permutation code is particularly educational.

---

### 2. DeepSpeed-MoE — best for understanding Expert Parallelism

[DeepSpeed MoE GitHub](https://github.com/deepspeedai/DeepSpeed?utm_source=chatgpt.com)

DeepSpeed has an explicit MoE implementation:

```python
MoE(
    hidden_size=hidden_size,
    expert=expert,
    num_experts=8,
    ep_size=2,
    k=1,
)
```

The interesting parameter is:

```text
ep_size
```

because this gets you into **Expert Parallelism (EP)**.

For example:

```text
GPU0                 GPU1

expert 0             expert 4
expert 1             expert 5
expert 2             expert 6
expert 3             expert 7
```

Tokens have to be routed to the GPU containing their selected expert:

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

That's where MoE becomes a **distributed systems problem**, not merely a neural-network architecture problem.

DeepSpeed's implementation exposes `TopKGate`, `MOELayer`, expert groups, capacity factors, token dropping, etc. ([GitHub][2])

Its tutorial also has a very small runnable MoE example, which is useful before diving into the large implementation. ([GitHub][3])

---

### 3. DeepSeek-MoE — best for understanding modern MoE architecture

[DeepSeek-MoE GitHub](https://github.com/deepseek-ai/DeepSeek-MoE?utm_source=chatgpt.com)

This is worth studying because DeepSeek didn't simply do:

```text
8 experts
top-2
```

Their architecture explores **fine-grained experts** and **shared experts**.

Conceptually:

```text
                  ┌── shared expert
                  │
x → router ───────┼── expert 17
                  ├── expert 42
                  └── expert 91
```

This is useful for understanding why modern MoEs increasingly care about:

* expert specialization
* shared experts
* number of experts
* top-k
* routing load balance
* auxiliary losses
* expert capacity
* communication cost

The repository contains the actual model/training implementation rather than just a toy implementation. ([GitHub][4])

---

### 4. Qwen3 — best modern production model to read

[Qwen3 GitHub](https://github.com/QwenLM/Qwen3/blob/main/docs/source/getting_started/concepts.md?ref=aiposthub.com&utm_source=chatgpt.com)

Qwen3 has:

```text
Qwen3-30B-A3B
Qwen3-235B-A22B
```

The naming itself is educational:

```text
30B-A3B

30B       total parameters
3B        active parameters/token
```

So:

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

That's the fundamental economic reason MoE is powerful:

> **Large parameter capacity without paying dense-model compute for every parameter on every token.**

Qwen3 officially includes both dense and MoE models, including 30B-A3B and 235B-A22B. ([GitHub][5])

---

### 5. Megatron-Core MoE — best when you want to become an MoE training engineer

Once you understand the above, go into Megatron-LM / Megatron-Core.

The interesting stuff becomes:

```text
Data Parallelism
        +
Tensor Parallelism
        +
Pipeline Parallelism
        +
Expert Parallelism
        +
Sequence Parallelism
        +
Distributed checkpointing
```

And especially:

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

That's the part I'd recommend you spend serious time on.

There are also current open recipes for DeepSeek-V3, Qwen3 and Mixtral using Megatron-Core, including configurations for H100/B200/GB200/GB300. ([GitHub][6])

---

## My recommended learning path

Given that you're already doing PyTorch/CUDA/LLM training, I wouldn't start with a giant framework.

I'd literally build these progressively:

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

The first version can be **~100 lines of PyTorch**:

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

Then the **real learning begins when you delete the Python loop**.

You replace:

```python
for expert in experts:
    expert(tokens)
```

with something closer to:

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

Then distribute the experts:

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

**That progression will teach you much more than reading an MoE paper alone.**

### My ranking

| Project           | What you learn                              | Difficulty |
| ----------------- | ------------------------------------------- | ---------: |
| **MegaBlocks**    | Efficient MoE / block sparse / grouped GEMM |        ⭐⭐⭐ |
| **DeepSpeed-MoE** | Router + Expert Parallelism                 |        ⭐⭐⭐ |
| **DeepSeek-MoE**  | Modern MoE architecture                     |        ⭐⭐⭐ |
| **Qwen3**         | Real production MoE model                   |       ⭐⭐⭐⭐ |
| **Megatron-Core** | Large-scale distributed MoE                 |      ⭐⭐⭐⭐⭐ |

If your goal is specifically **MoE + CUDA + GPU systems**, I'd spend the most time on **MegaBlocks → DeepSpeed-MoE → Megatron-Core**, rather than starting from Qwen/DeepSeek model code.

I can also build you a **minimal 200-line MoE implementation from scratch and progressively turn it into Expert Parallelism + All-to-All**, which would be a very good hands-on path for learning this.

[1]: https://github.com/mistralai/megablocks-public?utm_source=chatgpt.com "GitHub - mistralai/megablocks-public · GitHub"
[2]: https://github.com/deepspeedai/DeepSpeed/blob/master/deepspeed/moe/layer.py?utm_source=chatgpt.com "DeepSpeed/deepspeed/moe/layer.py at master · deepspeedai/DeepSpeed · GitHub"
[3]: https://github.com/deepspeedai/DeepSpeed/blob/master/docs/_tutorials/mixture-of-experts.md?utm_source=chatgpt.com "DeepSpeed/docs/_tutorials/mixture-of-experts.md at master · deepspeedai/DeepSpeed · GitHub"
[4]: https://github.com/deepseek-ai/DeepSeek-MoE?utm_source=chatgpt.com "GitHub - deepseek-ai/DeepSeek-MoE: DeepSeekMoE: Towards Ultimate Expert Specialization in Mixture-of-Experts Language Models · GitHub"
[5]: https://github.com/maximisto/qwen3?utm_source=chatgpt.com "GitHub - maximisto/qwen3: Qwen3 is the large language model series developed by Qwen team, Alibaba Cloud. · GitHub"
[6]: https://github.com/yanring/Megatron-MoE-ModelZoo?utm_source=chatgpt.com "GitHub - yanring/Megatron-MoE-ModelZoo: Best practices for training DeepSeek, Mixtral, Qwen and other MoE models using Megatron Core. · GitHub"