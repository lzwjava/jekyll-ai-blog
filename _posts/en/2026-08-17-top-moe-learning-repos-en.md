---
audio: false
generated: true
image: false
lang: en
layout: post
title: Top MoE Learning Repos
translated: false
type: note
---

Question: **What are good open-source projects to learn Mixture-of-Experts (MoE) deeply?**

Answer: If your goal is **understanding MoE internals + actually implementing/training it**, I would not start with a giant framework. I'd go in this order:

### 1. DeepSeek-MoE — best for understanding modern MoE architecture

[deepseek-ai/DeepSeek-MoE](https://github.com/deepseek-ai/DeepSeek-MoE?utm_source=chatgpt.com)

This is probably the most interesting one for you.

DeepSeek-MoE introduces two important ideas:

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

The released model is **16.4B total parameters**, while only a fraction of parameters are activated per token. Their implementation also includes fine-tuning code. ([GitHub][1])

I would read the model implementation while keeping this mental model:

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

Then ask: **how do we make this fast when `tokens -> experts -> tokens` happens across 8/64/256 GPUs?**

That's where the real MoE engineering starts.

---

### 2. MegaBlocks — best project for learning the systems side

[databricks/megablocks](https://github.com/databricks/megablocks?utm_source=chatgpt.com)

If DeepSeek-MoE teaches you **what modern MoE looks like**, MegaBlocks teaches you **why implementing it efficiently is hard**.

Its central idea is:

```text
Dense MLP
   ↓
Router
   ↓
tokens → experts
   ↓
???
```

The naïve implementation suffers from irregular token counts per expert.

MegaBlocks reformulates the computation as **block-sparse operations**, allowing **dropless MoE** without the traditional `capacity_factor` token-dropping mechanism. ([GitHub][2])

This is exactly the kind of code I'd study line-by-line:

[MegaBlocks moe.py](https://github.com/databricks/megablocks/blob/main/megablocks/layers/moe.py?utm_source=chatgpt.com)

Pay particular attention to:

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

That's the **forward pass you actually want to understand**.

---

### 3. Tutel — best for understanding Expert Parallelism

[Microsoft Tutel](https://github.com/microsoft/Tutel?utm_source=chatgpt.com)

Tutel is especially useful once you understand the single-GPU version.

It deals with:

```text
GPU 0              GPU 1
expert 0           expert 1
expert 2           expert 3
   ↑                   ↑
   └──── All-to-All ───┘
```

Tutel supports CUDA and ROCm and has implementations involving dropless MoE, MegaBlocks-style computation, expert parallelism, and communication optimization. ([GitHub][3])

For someone interested in **LLM inference/training infrastructure**, this is extremely valuable.

---

### 4. DeepSpeed-MoE — easiest conceptual distributed implementation

[DeepSpeed MoE tutorial](https://www.deepspeed.ai/tutorials/mixture-of-experts/?utm_source=chatgpt.com)

DeepSpeed exposes an explicit MoE layer:

```python
deepspeed.moe.layer.MoE(
    hidden_size=hidden_size,
    expert=expert,
    num_experts=8,
    ep_size=8,
    k=2,
)
```

The interesting parameter here is:

```text
ep_size
```

which gets you into **Expert Parallelism (EP)**. DeepSpeed's MoE implementation supports multiple forms of parallelism, including expert parallelism. ([DeepSpeed][4])

Good project for understanding:

```text
Data Parallelism
Tensor Parallelism
Expert Parallelism
Pipeline Parallelism
```

and how they interact.

---

### 5. Hugging Face Mixtral — best simple "real LLM MoE"

[Hugging Face Mixtral implementation](https://github.com/huggingface/transformers/blob/main/docs/source/en/model_doc/mixtral.md?utm_source=chatgpt.com)

Mixtral 8×7B is a great reference because the architecture is relatively easy to understand:

```text
8 experts
top-2 routing

45B total parameters
≈14B active computation/token
```

The Hugging Face implementation documents the architecture and exposes the `MixtralModel` / `MixtralForCausalLM` implementation. ([GitHub][5])

I'd start here if you want to modify a real LLM rather than first dealing with distributed infrastructure.

---

## My recommended learning path

Given that you're already working on LLM infrastructure, I'd literally do this:

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

And before touching any framework, implement this yourself:

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

Then benchmark:

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

The key conceptual progression is:

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

And once you understand the last three, **modern DeepSeek/Qwen/Kimi-style MoE systems become much easier to read**.

### If you only pick 3

**1. DeepSeek-MoE** → understand modern architecture
**2. MegaBlocks** → understand efficient MoE kernels/dispatch
**3. Tutel** → understand distributed Expert Parallelism

That's probably the highest-value path for you.

[1]: https://github.com/deepseek-ai/DeepSeek-MoE?utm_source=chatgpt.com "GitHub - deepseek-ai/DeepSeek-MoE: DeepSeekMoE: Towards Ultimate Expert Specialization in Mixture-of-Experts Language Models · GitHub"
[2]: https://github.com/databricks/megablocks?utm_source=chatgpt.com "GitHub - databricks/megablocks · GitHub"
[3]: https://github.com/microsoft/Tutel?utm_source=chatgpt.com "GitHub - microsoft/Tutel: Tutel MoE: Optimized Mixture-of-Experts Library, Support GptOss/DeepSeek/Kimi-K2/Qwen3 using FP8/NVFP4/MXFP4 · GitHub"
[4]: https://deepspeed.readthedocs.io/en/latest/moe.html?utm_source=chatgpt.com "Mixture of Experts (DeepSpeed MoE) — DeepSpeed 0.19.3 documentation"
[5]: https://github.com/huggingface/transformers/blob/main/docs/source/en/model_doc/mixtral.md?utm_source=chatgpt.com "transformers/docs/source/en/model_doc/mixtral.md at main · huggingface/transformers · GitHub"
