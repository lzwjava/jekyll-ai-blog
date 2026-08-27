---
audio: false
generated: true
image: false
lang: en
layout: post
title: "GLM-5.3-Flash: 320B MoE, 18B Active"
translated: false
type: note
---

## Question: Intro to zai-org/GLM-5.3-Flash

## Answer

Z.ai's **GLM-5.3-Flash** is a new generation **Mixture-of-Experts (MoE) multimodal large language model** in the GLM-5 family. The key idea is:

> **320B total parameters, only ~18B active parameters → frontier-level capability with much lower inference cost.** ([Hugging Face][1])

Think of it as a Chinese counterpart to models like GPT-5-class reasoning models, Claude Opus-class coding models, etc., but optimized heavily for efficient serving.

---

## 1. Architecture

The important architecture changes:

### 1. MoE sparse activation

Instead of:

```
Transformer layer

all 100B+ parameters participate
          ↓
huge compute cost
```

GLM-5.3-Flash:

```
320B parameters stored

token
 |
router
 |
 +--> expert A  \
 +--> expert B   ---> only ~18B activated
 +--> expert C  /
```

So:

* memory requirement ≈ full model size
* compute requirement ≈ 18B model

This is the same general direction as:

* Mixtral
* DeepSeek-V3
* Qwen MoE models

---

### 2. Hybrid attention

The paper/model card mentions a hybrid architecture:

* sparse attention
* linear attention

The problem:

Normal Transformer attention:

$$
Attention(Q,K,V)=softmax(\frac{QK^T}{\sqrt d})V
$$

Complexity:

$$
O(n^2)
$$

where `n` = context length.

At 100k+ tokens, KV cache becomes huge.

GLM-5.3-Flash tries to combine:

```
short-range precise attention
+
long-range efficient linear attention
```

to reduce long-context serving cost. ([Hugging Face][1])

---

### 3. mHC (Manifold-Constrained Hyper-Connections)

Another interesting part.

Normal residual:

```
x
 |
Layer
 |
x + Layer(x)
```

mHC changes the residual pathway to allow richer information routing while keeping training stable.

The intuition:

Instead of one highway:

```
hidden state
     |
     v
  transformer
     |
     v
 hidden state
```

you have multiple learned communication paths.

This is similar to asking:

"Can we scale depth without the optimization problems of huge transformers?"

---

## 2. Multimodal

GLM-5.3-Flash is the first GLM-5 series model designed as **natively multimodal**. It can process:

* text
* images
* reasoning tasks
* coding tasks
* agents

The Hugging Face implementation supports image-text inputs through `AutoProcessor` and multimodal generation. ([Hugging Face][2])

---

## 3. Model size

Hugging Face lists:

```
GLM-5.3-Flash

~321B parameters
FP8 weights
MIT license
Chinese + English
```

([Hugging Face][3])

Memory estimation:

### BF16

$$
321B \times 2 bytes
$$

≈

```
642 GB VRAM
```

before KV cache.

### FP8

$$
321B \times 1 byte
$$

≈

```
321 GB VRAM
```

So realistic deployment:

```
4x H100 80GB
8x A100 80GB
MI300X cluster
```

or aggressive quantization/offload.

---

## 4. Why "Flash"?

Not because of Flash Attention only.

The philosophy:

```
big model
+
small active compute
+
optimized attention
+
cheap serving
```

Similar to:

```
DeepSeek-V3:
671B total
37B active

GLM-5.3-Flash:
320B total
18B active
```

The goal:

> "Near frontier intelligence at a fraction of inference cost."

---

## 5. Running locally

Example with vLLM:

```bash
pip install vllm

vllm serve zai-org/GLM-5.3-Flash
```

It exposes OpenAI-compatible API:

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="EMPTY"
)

response = client.chat.completions.create(
    model="zai-org/GLM-5.3-Flash",
    messages=[
        {
          "role":"user",
          "content":"Explain CUDA kernel optimization"
        }
    ]
)

print(response.choices[0].message.content)
```

([Hugging Face][2])

---

## 6. For your hardware experiments

Given your setup:

* RTX 4070 12GB
* local Qwen/vLLM experiments
* GPT-2 training
* interest in distributed inference

This model is interesting because it demonstrates the future direction:

```
Old scaling:

bigger dense model
       |
       v
more GPUs


New scaling:

huge sparse model
       |
       +--> MoE
       +--> quantization
       +--> offload
       +--> smarter attention
```

The bottleneck moves from:

> "Can we train a bigger model?"

to:

> "Can we route, cache, compress, and serve a huge model efficiently?"

That connects directly to your previous experiments with:

* multi-GPU
* offload
* KV cache
* local inference
* GPU hardware repair

because future AI infrastructure is increasingly about **systems engineering**, not only model architecture.

---

References:

* [GLM-5.3-Flash on Hugging Face](https://huggingface.co/zai-org/GLM-5.3-Flash?utm_source=chatgpt.com)
* [GLM-5.3-Flash README](https://huggingface.co/zai-org/GLM-5.3-Flash/blob/main/README.md?utm_source=chatgpt.com)
* [GLM-5.3-Flash-BF16 model card](https://huggingface.co/zai-org/GLM-5.3-Flash-BF16?utm_source=chatgpt.com)

[1]: https://huggingface.co/zai-org/GLM-5.3-Flash-BF16?utm_source=chatgpt.com "zai-org/GLM-5.3-Flash-BF16 · Hugging Face"
[2]: https://huggingface.co/zai-org/GLM-5.3-Flash/blob/main/README.md?utm_source=chatgpt.com "README.md · zai-org/GLM-5.3-Flash at main"
[3]: https://huggingface.co/zai-org/GLM-5.3-Flash?utm_source=chatgpt.com "zai-org/GLM-5.3-Flash · Hugging Face"
