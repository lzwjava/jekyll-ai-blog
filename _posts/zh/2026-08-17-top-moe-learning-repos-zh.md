---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 顶级MoE学习仓库
translated: true
type: note
---

**有哪些好的开源项目可以深入学习 Mixture-of-Experts（MoE）？**

回答：如果你的目标是**理解 MoE 内部原理 + 真正实现/训练它**，我不会一开始就上手一个大而全的框架。我会按这个顺序来：

### 1. DeepSeek-MoE —— 理解现代 MoE 架构的最佳项目

[deepseek-ai/DeepSeek-MoE](https://github.com/deepseek-ai/DeepSeek-MoE?utm_source=chatgpt.com)

这可能是你最感兴趣的一个。

DeepSeek-MoE 提出了两个重要思路：

```text
normal MoE
    ↓
many relatively large experts

DeepSeekMoE
    ↓
fine-grained experts
+
shared experts
```

该模型总参数量为 **16.4B**，但每个 token 只激活其中一小部分参数。其实现还包含微调代码。([GitHub][1])

我会带着下面这个心智模型去阅读模型实现：

```python
x                         # [tokens, hidden]

router_logits = router(x) # [tokens, num_experts]

probs, ids = topk(
    softmax(router_logits),
    k=top_k
)

for expert in selected_experts:
    y += weight * expert(x)

y = shared_experts(x) + y
```

然后问：当 `tokens -> experts -> tokens` 要在 8/64/256 张 GPU 上发生时，我们如何让它变快？

这才是真正 MoE 工程开始的地方。

---

### 2. MegaBlocks —— 学习系统层面的最佳项目

[databricks/megablocks](https://github.com/databricks/megablocks?utm_source=chatgpt.com)

如果说 DeepSeek-MoE 让你看到**现代 MoE 长什么样**，MegaBlocks 则让你理解**为什么高效实现它很困难**。

它的核心思想是：

```text
Dense MLP
   ↓
Router
   ↓
tokens → experts
   ↓
???
```

朴素的实现会面临每个专家处理的 token 数量不均衡的问题。

MegaBlocks 将计算重新表述为 **block-sparse 运算**，从而在没有传统 `capacity_factor` token 丢弃机制的情况下实现 **dropless MoE**。([GitHub][2])

这正是我会逐行研读的代码：

[MegaBlocks moe.py](https://github.com/databricks/megablocks/blob/main/megablocks/layers/moe.py?utm_source=chatgpt.com)

请特别注意：

```text
router
  ↓
top-k
  ↓
token permutation
  ↓
expert computation
  ↓
unpermutation
  ↓
combine
```

这就是你真正需要理解的**前向传播**过程。

---

### 3. Tutel —— 理解专家并行（Expert Parallelism）的最佳项目

[Microsoft Tutel](https://github.com/microsoft/Tutel?utm_source=chatgpt.com)

当你理解了单 GPU 版本后，Tutel 会特别有用。

它处理的是：

```text
GPU 0              GPU 1
expert 0           expert 1
expert 2           expert 3
   ↑                   ↑
   └──── All-to-All ───┘
```

Tutel 支持 CUDA 和 ROCm，并包含涉及 dropless MoE、MegaBlocks 风格计算、专家并行和通信优化的实现。([GitHub][3])

对于对 **LLM 推理/训练基础设施**感兴趣的人来说，这极具价值。

---

### 4. DeepSpeed-MoE —— 最容易理解其概念的分布式实现

[DeepSpeed MoE 教程](https://www.deepspeed.ai/tutorials/mixture-of-experts/?utm_source=chatgpt.com)

DeepSpeed 提供了一个显式的 MoE 层：

```python
deepspeed.moe.layer.MoE(
    hidden_size=hidden_size,
    expert=expert,
    num_experts=8,
    ep_size=8,
    k=2,
)
```

这里值得关注的参数是：

```text
ep_size
```

它会带你进入 **Expert Parallelism（专家并行，EP）**。DeepSpeed 的 MoE 实现支持多种并行形式，包括专家并行。([DeepSpeed][4])

适合用来理解以下内容：

```text
Data Parallelism
Tensor Parallelism
Expert Parallelism
Pipeline Parallelism
```

以及它们之间如何相互配合。

---

### 5. Hugging Face Mixtral —— 最简单易懂的“真实 LLM MoE”

[Hugging Face Mixtral 实现](https://github.com/huggingface/transformers/blob/main/docs/source/en/model_doc/mixtral.md?utm_source=chatgpt.com)

Mixtral 8×7B 是一个很好的参考，因为它的架构相对容易理解：

```text
8 experts
top-2 routing

45B total parameters
≈14B active computation/token
```

Hugging Face 的实现对该架构做了说明，并提供了 `MixtralModel` / `MixtralForCausalLM` 实现。([GitHub][5])

如果你想修改一个真实 LLM，而不是先处理分布式基础设施，可以从这里开始。

---

## 我推荐的学习路径

既然你已经在做 LLM 基础设施，我会按下面这条路来走：

```text
                 MoE
                  │
          ┌───────┴────────┐
          ↓                ↓
      Architecture       Systems
          │                │
          ↓                ↓
     Mixtral          MegaBlocks
          │                │
          ↓                ↓
   DeepSeek-MoE          Tutel
          │                │
          └───────┬────────┘
                  ↓
             DeepSpeed
                  │
                  ↓
          Expert Parallelism
                  │
                  ↓
           All-to-All / NCCL
```

并且在接触任何框架之前，先自己实现一遍：

```python
class MoE(nn.Module):
    def __init__(self, d_model, d_ff, n_experts, top_k):
        ...
    
    def forward(self, x):
        # x: [B, T, D]

        logits = self.router(x)

        weights, indices = torch.topk(
            logits.softmax(-1),
            self.top_k,
            dim=-1,
        )

        # dispatch
        # expert FFNs
        # combine

        return y
```

然后做基准测试：

```text
Dense FFN
vs
MoE top-1
vs
MoE top-2
vs
MoE dropless
vs
MoE + expert parallelism
```

关键的概念递进是：

```text
MoE is NOT primarily "many FFNs".

MoE is:

routing
  +
dispatch
  +
expert computation
  +
combine
  +
load balancing
  +
distributed communication
```

一旦你理解了最后三点，**现代 DeepSeek/Qwen/Kimi 风格的 MoE 系统**读起来就会容易得多。

### 如果只选 3 个

**1. DeepSeek-MoE** → 理解现代架构
**2. MegaBlocks** → 理解高效的 MoE 内核/dispatch
**3. Tutel** → 理解分布式专家并行

这大概就是对你价值最高的学习路径。

[1]: https://github.com/deepseek-ai/DeepSeek-MoE?utm_source=chatgpt.com "GitHub - deepseek-ai/DeepSeek-MoE: DeepSeekMoE: Towards Ultimate Expert Specialization in Mixture-of-Experts Language Models · GitHub"
[2]: https://github.com/databricks/megablocks?utm_source=chatgpt.com "GitHub - databricks/megablocks · GitHub"
[3]: https://github.com/microsoft/Tutel?utm_source=chatgpt.com "GitHub - microsoft/Tutel: Tutel MoE: Optimized Mixture-of-Experts Library, Support GptOss/DeepSeek/Kimi-K2/Qwen3 using FP8/NVFP4/MXFP4 · GitHub"
[4]: https://deepspeed.readthedocs.io/en/latest/moe.html?utm_source=chatgpt.com "Mixture of Experts (DeepSpeed MoE) — DeepSpeed 0.19.3 documentation"
[5]: https://github.com/huggingface/transformers/blob/main/docs/source/en/model_doc/mixtral.md?utm_source=chatgpt.com "transformers/docs/source/en/model_doc/mixtral.md at main · huggingface/transformers · GitHub"
