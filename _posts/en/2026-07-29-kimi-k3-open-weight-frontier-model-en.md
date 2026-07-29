---
audio: false
generated: true
image: false
lang: en
layout: post
title: Kimi-K3 Open-Weight Frontier Model
translated: false
type: note
---

Question: What is `moonshotai/Kimi-K3` on Hugging Face?

Answer:

Moonshot AI's **Kimi-K3** is their latest **open-weight frontier large language model** released on Hugging Face. It is basically Moonshot's answer to models like GPT-5-class systems and Claude-class models, but with downloadable weights. ([Hugging Face][1])

The important part is not just "2.8 trillion parameters" — the architecture is what makes it interesting. ([Hugging Face][1])

## 1. Architecture

```
Kimi K3

2.8T total parameters
        |
        v
Mixture-of-Experts (MoE)
        |
        +-- 896 experts
        |
        +-- each token activates only 16 experts
        |
        v
~104B active parameters/token
```

So it is not like a dense 2.8T model.

A dense model:

```
token
 |
all 2.8T parameters run
 |
huge compute
```

K3:

```
token
 |
router
 |
choose 16 / 896 experts
 |
only ~104B parameters execute
```

This is the same scaling idea used by models like Mixtral, DeepSeek MoE, etc. ([Hugging Face][1])

---

## 2. Key specs

From the model card: ([Hugging Face][1])

| Item          | Kimi K3                          |
| ------------- | -------------------------------- |
| Architecture  | MoE                              |
| Total params  | 2.8T                             |
| Active params | 104B                             |
| Experts       | 896                              |
| Experts/token | 16                               |
| Context       | 1,048,576 tokens                 |
| Vision        | Yes                              |
| Layers        | 93                               |
| Attention     | Kimi Delta Attention + Gated MLA |
| Weight format | MXFP4                            |
| Vocabulary    | 160K                             |

---

## 3. Why Kimi Delta Attention (KDA) matters

The normal Transformer attention:

[
Attention(Q,K,V)=softmax(\frac{QK^T}{\sqrt d})V
]

has:

```
sequence length N

memory:
O(N²)
```

For million-token context:

```
1,000,000 tokens

attention matrix:
1e12 entries
```

Impossible.

Kimi introduces **Kimi Delta Attention**, trying to make long-context processing cheaper by compressing attention state. ([Hugging Face][1])

Conceptually:

Traditional:

```
token1 token2 token3 ... token1000000

every token attends every token
```

KDA:

```
token stream
    |
compressed memory state
    |
retrieve relevant history
```

Similar direction to:

* recurrent memory
* linear attention
* state-space models (Mamba style)

but integrated into a Transformer architecture.

---

## 4. Why people are excited

The big shift:

Before:

```
Frontier model
=
OpenAI / Anthropic / Google
=
closed weights
```

Now:

```
Frontier-level capability
+
downloadable weights
+
self hosting
```

K3 joins the trend:

* DeepSeek R1
* Qwen series
* Llama series
* Kimi K3

where researchers can inspect, modify, quantize, and deploy locally. ([GitHub][2])

---

## 5. Can your RTX 4070 run it?

Short answer: **no, not normally.**

Your RTX 4070:

```
VRAM: 12GB
```

K3 checkpoint:

```
~1.5TB+
```

The full model is split into many safetensor shards. ([Hugging Face][3])

But because it is MoE, clever systems can partially load experts:

```
CPU RAM
 |
model weights
 |
GPU
 |
active experts
```

Possible experiments:

* CPU offload
* quantized MXFP4
* distributed inference
* expert streaming

Community experiments have already shown unusual low-GPU deployments because only selected experts are active. ([Reddit][4])

For practical local inference:

```
RTX 4070 12GB
    |
    +-- Qwen3-8B
    +-- Qwen3-14B quantized
    +-- Llama 70B via CPU offload (slow)

Kimi K3
    |
    +-- server cluster
    +-- many GPUs
```

---

## 6. Why this matters for AI engineers

For someone learning vLLM / inference stack, K3 is actually a very good architecture study case.

You can learn:

### MoE routing

```
hidden state
      |
      v
router()
      |
      +--> expert 13
      +--> expert 201
      +--> expert 777
```

### Expert parallelism

```
GPU0:
 expert 0-100

GPU1:
 expert 101-200

GPU2:
 expert 201-300
```

### KV cache pressure

1M context makes:

```
KV cache
+
attention memory
+
paging
```

the main bottleneck.

This is exactly the problem vLLM is solving.

---

My take: Kimi K3 is less interesting because "2.8T" and more because it is a **MoE + long-context + agent-oriented architecture**. It represents the direction where future frontier models may look like:

```
huge sparse model
+
cheap active compute
+
persistent memory
+
tool agents
+
local/private deployment
```

which is very aligned with the inference engineering work you are currently studying.

References:

* [Kimi-K3 Hugging Face Model Card](https://huggingface.co/moonshotai/Kimi-K3/blob/main/README.md?utm_source=chatgpt.com)
* [MoonshotAI Kimi-K3 GitHub](https://github.com/MoonshotAI/Kimi-K3?utm_source=chatgpt.com)
* [Kimi K3 Technical Report (arXiv)](https://arxiv.org/abs/2607.24653?utm_source=chatgpt.com)

[1]: https://huggingface.co/moonshotai/Kimi-K3/blob/main/README.md?utm_source=chatgpt.com "README.md · moonshotai/Kimi-K3 at main"
[2]: https://github.com/MoonshotAI/Kimi-K3?utm_source=chatgpt.com "GitHub - MoonshotAI/Kimi-K3: Open Frontier Intelligence · GitHub"
[3]: https://huggingface.co/moonshotai/Kimi-K3/blob/main/model-00022-of-000096.safetensors?utm_source=chatgpt.com "model-00022-of-000096.safetensors · moonshotai/Kimi-K3 at main"
[4]: https://www.reddit.com/r/LocalLLM/comments/1v8sy23/ran_moonshots_28tparameter_kimi_k3_on_a_gpuless/?utm_source=chatgpt.com "Ran Moonshot's 2.8T-parameter Kimi K3 on a GPU-less mini-PC, one day after release"
