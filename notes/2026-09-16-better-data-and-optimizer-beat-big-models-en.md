---
audio: false
generated: true
image: false
lang: en
layout: post
title: Better data and optimizer beat big models
translated: false
type: note
---

Question: **How did Hugo Vergnes train `little-lm`, and why did it beat nanochat and GPT-2 despite costing only ~$1k?**

Answer:

The key is **not one magic architecture trick**. It is basically:

> **better data + aggressive optimizer + better LR schedule + modern architecture + brutal GPU utilization.**

Hugo trained a **3.848B decoder-only model from scratch** on **65.3B tokens**, using **8× B200 for 43h**, costing **$998**, and got **0.384 CORE**. His comparison is GPT-2 1.5B = 0.2565 and nanochat d32 ≈1B = 0.310. ([Hugo Vergnes][1])

![Image](https://images.openai.com/static-rsc-4/4gumHJTx4wSPc1CLSVQdr3evptuk-LQ2fQaDhoGk08OjSCXTnjEs5G-VkBzgPU5bmuTWCe-VlXNwJz0JHOQyhiy0oKXnhPlS9OLS9fE_E7CC7seBVLnidKIvsL-OiwWHkLRxmGmN-l62KUGrd-zXZLomcgnHOCQpncRW8-kHTkPCdvkPE6Ae_cmjhuMZqXWT?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/EoUedrrHBPEbU8iZUD0A95GEb3Mctc0FLS9Y57eSWBVV-Hib5ms3jjpJyC6ahgKD4edOfOMLkHCMjXZlX8TmiEKaSJHfTM5RsnRyZ0ScngPP16Ce0D2WYfP9ccuKsD8TsWxEIXYocVW-fVdD7XltcVRd_8sf1z3d3XkCPe_gw_jPzxUIEURePJsmIVEmzoZ2?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/h6V2ERw5OAv_ML07r1KRGDSGE4gq_xhB7wHwi4aMZWv1oyVGugKXYmfkKYKihL_YFs3yO0eB1NUQI85RsnON9bfPNYzrArINohGKZ-Sa8NEsM3J6-gap3wi59Tlsady2u4MWeB8RPWELz_PLca_VxLyR34hVc6BzhCDfyyP0_TlQ7_E0p7kQ1OJRE3BCxcdH?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/zzuPoN2u_1Z8waWRwdsV46xjfW9HEplonJCl5r-dp5vMFfXnKBRWg6OvrTb9Spp24C0NaYSThUGxKD1l2rBnbAQ3Z_vd3PcELKArbzpeH6ItRVMHst_MK8ybv-rxzn_iCbj9-aN2PtTDI7K-QwJARCbYSwubrK3KKOqXM8NRsxj-shcxokY-CUuAw2iKSdOM?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/O9ljkHoYYtvuMxrH9mSpjs1Ykmm9O2RgtR_BFHXOguoPJpE9ZXwsq93zz877s8XIqQJ6EqE2pVxMG3r61tpRPiaoyebb01ciVU65oo7RzXUI50MDQjJY_aVTtYHmBEeYee8jmHNVWbjQVoWHJqPEieiBicWh5DEOuc1FgDw7uHCXGmpcMHT45RwZsv_Jbjgh?purpose=fullsize)

### 1. The first attempt actually sucked

This is probably the most interesting part.

He initially trained:

```text
858M params
FineWeb-Edu
16.4B tokens
1× A100
2048 context
AdamW
lr = 2.5e-4
cosine → 0
```

Result:

```text
PIQA = 60.45%
```

while **GPT-2 124M ≈ 63%**.

So a model ~7× larger was worse. ([Hugo Vergnes][1])

The loss curve exposed the problem: cosine decay reached almost zero too early, so the final ~30% of compute was basically wasted.

That led to the important changes.

---

## 2. The recipe that actually worked

### Architecture

His final model is roughly:

```yaml
model:
  params: 3.848B
  layers: 28
  vocab: 50_304
  context: 2048

  norm: RMSNorm
  positional: RoPE

  attention:
    type: GQA
    q_heads: 24
    kv_heads: 8
    qk_norm: true

  mlp:
    activation: relu_squared

  logits:
    softcap: true

  residual:
    learnable_layer_scalars: true

  value_embeddings:
    tables: 14
```

The unusual part is **value embeddings**.

They add about:

```text
721M parameters
≈ 19% of the model
```

but are basically lookup operations, so they add parameters/memory without proportionally adding FLOPs. ([Hugo Vergnes][1])

The interesting ablation:

```text
+ value embeddings
→ +0.46% loss improvement
→ +3.2% CORE
```

at essentially identical throughput. ([Hugo Vergnes][2])

So this is a very good **compute-to-parameter trade** when training is FLOP-bound.

---

# 3. The biggest optimizer change: Muon

Instead of:

```python
AdamW(all_parameters)
```

he uses:

```python
Muon(matrix_parameters)
AdamW(other_parameters)
```

Conceptually:

```python
for p in matrix_params:
    p ← Muon(p)

for p in vectors_and_scalars:
    p ← AdamW(p)
```

Why?

AdamW maintains first/second moments for every parameter. Muon instead performs an approximate orthogonalization of the update for matrix parameters.

Very roughly:

$$
W_{t+1}=W_t-\eta\,\mathrm{Muon}(G_t)
$$

where Muon applies Newton-Schulz-style orthogonalization to the gradient/update.

The important empirical observation wasn't "Muon is cheaper per step".

It **isn't**.

Hugo measured roughly **25% overhead per optimizer step** in a shallow-accumulation test. But with gradient accumulation, that overhead became only ~4% of total runtime, while convergence improved enough to make the whole run substantially faster. ([Hugo Vergnes][1])

That's the important engineering lesson:

> **Optimize cost per unit of loss reduction, not tokens/sec in isolation.**

---

# 4. The LR schedule was surprisingly important

Initial attempt:

```text
warmup 5%
cosine decay → 0
```

Bad.

Final:

```text
5% warmup
↓
flat / high LR
↓
linear cooldown
↓
5% of peak LR
```

So approximately:

```python
if step < warmup:
    lr = peak * step / warmup

elif step < cooldown_start:
    lr = peak

else:
    lr = peak * linear_decay(
        step,
        cooldown_start,
        total_steps,
        final=0.05,
    )
```

Why this matters:

With cosine → 0, the model effectively says:

> "I'm done learning."

while there is still a huge amount of useful data left.

The final run's eval loss was **still falling at the final step**. ([Hugo Vergnes][1])

That's a huge difference from the failed 858M run.

---

# 5. Data: ClimbMix > FineWeb-Edu

This was another major jump.

The failed run used:

```text
FineWeb-Edu
```

The successful run switched to:

```text
ClimbMix
```

Hugo describes this as a **"tremendous jump in convergence speed."** ([Hugo Vergnes][1])

And this is important when comparing against GPT-2.

GPT-2 wasn't trained on modern curated training data. Its WebText corpus was roughly 40GB assembled from highly upvoted Reddit-linked webpages. ([Wikipedia][3])

So saying:

> "3.8B > 1.5B"

isn't really the interesting result.

The interesting result is:

> **2026 data + architecture + optimizer + training infrastructure make a ~$1k single-node experiment vastly more compute-efficient than a 2019 frontier recipe.**

---

# 6. FP8 was a huge throughput multiplier

He trained using FP8 for the GEMMs:

```text
forward GEMM → FP8
backward GEMM → FP8
backward GEMM → FP8
```

with dynamic tensor-wise scaling.

Then:

```text
vocab:
50,257 → 50,304
```

because 50,304 is divisible by 64 and maps better onto tensor-core hardware.

The combination produced roughly:

```text
+33% throughput
```

mostly from FP8. ([Hugo Vergnes][1])

He also used fused linear cross entropy so the enormous:

$$
[B,T,V]
$$

logit tensor doesn't need to be materialized in full.

That's exactly the kind of optimization that matters when you're personally paying the GPU bill.

---

# 7. The final throughput was crazy

The final run:

```text
8 × B200
~480k tokens/sec
57.3B tokens
~33h
```

and the 2048-context rerun:

```text
65.3B tokens
43h
$998
CORE = 0.384
```

GPU utilization:

```text
92% SM activity
40% SM occupancy
```

The low occupancy wasn't necessarily bad. The workload was dominated by large GEMMs, where register/tile utilization can matter more than maximizing occupancy. ([Hugo Vergnes][1])

He estimates approximately:

```text
1.047 PFLOP/s sustained / B200
~25% MFU vs Blackwell dense FP8 peak
```

and importantly:

> **DDP was enough.**

No FSDP/ZeRO/sharded optimizer was required at 3.8B on one node. ([Hugo Vergnes][1])

---

# 8. Why did it beat nanochat?

This is where the comparison gets interesting.

Hugo's table:

| Model        |     Params |    Tokens | Hardware    |     Cost |       CORE |
| ------------ | ---------: | --------: | ----------- | -------: | ---------: |
| GPT-2        |       1.5B |         — | —           |        — | **0.2565** |
| nanochat d26 |      ~561M |     11.2B | 8× H100     |        — | **~0.258** |
| nanochat d32 |        ~1B |         — | 8× H100     |   ~$1000 |  **0.310** |
| little-lm    | **3.848B** | **65.3B** | **8× B200** | **$998** |  **0.384** |

([Hugo Vergnes][1])

So **"surpass nanochat" is not a mysterious leap**.

He spent the same ~$1k budget on:

```text
~4× parameters vs nanochat d32
~65×10^9 training tokens
modern data
Muon
better LR schedule
FP8
modern Llama-style architecture
B200 instead of H100
```

The hardware economics matter enormously.

---

# 9. The real formula

I'd summarize Hugo's result as:

$$
\boxed{
\text{quality}
\approx
f(
\text{data quality},
\text{tokens},
\text{params},
\text{optimizer},
\text{architecture},
\text{compute efficiency}
)
}
$$

But the practical optimization target is:

$$
\boxed{
\frac{\Delta \text{quality}}
{\$}
}
$$

rather than:

$$
\frac{\text{tokens/sec}}{\$}
$$

or simply:

$$
\text{parameter count}
$$

His failed 858M experiment demonstrates this perfectly.

---

## The part I'd copy if you wanted to reproduce it

Given your MI300X experience, I'd reduce the recipe to:

```yaml
model:
  size: ~3B
  architecture: llama-ish
  norm: rmsnorm
  position: rope
  attention: GQA
  qk_norm: true
  mlp: relu2
  value_embeddings: true

data:
  dataset: ClimbMix
  tokens: 50-70B

optimizer:
  matrix: muon
  vector: adamw

schedule:
  warmup: 5%
  hold: ~45%
  linear_cooldown: ~50%
  final_lr: 5% peak

precision:
  compute: fp8
  master_weights: bf16

systems:
  vocab_padding: 64
  fused_linear_ce: true
  local_data_shards: true
  DDP: true
```

Then **don't blindly copy the 3.8B recipe**.

I'd run a controlled 300M–1B sweep first:

```text
                  A          B          C
optimizer       AdamW      Muon       Muon
schedule        cosine     cosine     trapezoid
data            FW-Edu     ClimbMix   ClimbMix
architecture    baseline   baseline   final
```

and measure:

```text
loss / 1B tokens
CORE / 1B tokens
tokens/sec
$/CORE improvement
```

That tells you *which* ingredient actually buys the improvement on your hardware/data, instead of spending $1k reproducing someone else's optimum.

One particularly important caveat: Hugo explicitly says he **did not ablate peak LR, QK-norm, or GQA ratio**, and some of the final recipe was inherited from nanochat rather than independently established at this scale. So this is a very good empirical recipe, not a proof that every component is necessary. ([Hugo Vergnes][1])

References:

* [Hugo Vergnes — Training a 3.8B LLM to 0.384 CORE for $998](https://hugovergnes.github.io/little-lm-3-8b/?utm_source=chatgpt.com)
* [Hugo Vergnes — little-lm project page](https://hugovergnes.github.io/projects/little-lm/?utm_source=chatgpt.com)
* [GPT-2 paper / Language Models are Unsupervised Multitask Learners](https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf?utm_source=chatgpt.com)

I can also turn this into a **minimal `little-lm`-style PyTorch training stack and derive the exact parameter/FLOP budget for a 1B or 3.8B model on your MI300X cluster**.

[1]: https://hugovergnes.github.io/little-lm-3-8b/ "Training a 3.8B LLM to 0.384 CORE for $998 | Hugo Vergnes"
[2]: https://hugovergnes.github.io/projects/little-lm/ "little-lm | Hugo Vergnes"
[3]: https://en.wikipedia.org/wiki/GPT-2?utm_source=chatgpt.com "GPT-2"
