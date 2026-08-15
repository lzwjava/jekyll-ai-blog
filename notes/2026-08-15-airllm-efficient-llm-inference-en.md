---
audio: false
generated: true
image: false
lang: en
layout: post
title: "AirLLM: Efficient LLM Inference"
translated: false
type: note
---

## Question: Intro to AirLLM

## Answer

AirLLM is an open-source project that allows running **very large language models (LLMs) on limited GPU memory** by using a technique called **layer-wise offloading**.

The core idea:

> Instead of loading the entire model into VRAM/RAM at once, load only the layers needed for the current forward pass.

For example:

* A 70B parameter model in FP16:

[
70B \times 2\ bytes \approx 140GB
]

Normally requires:

* A100 80GB × 2
* H100
* multi-GPU setup

With AirLLM:

```
GPU VRAM
 |
 |  layer 0  ---> compute
 |  layer 1  ---> compute
 |  layer 2  ---> compute
 |
CPU RAM / disk
 |
 |  remaining layers
```

Only a few transformer blocks stay on GPU.

---

## Architecture

A normal transformer inference:

```
input tokens

    |
    v

Embedding

    |
    v

Transformer block 1
Transformer block 2
Transformer block 3
...
Transformer block N

    |
    v

LM Head

    |
    v

next token
```

Traditional inference:

```
GPU:

Embedding
Block1
Block2
...
Block80
LM Head
```

AirLLM:

```
GPU:

Block1
   |
compute
   |
remove

Block2
   |
compute
   |
remove

Block3
...
```

Pseudo code:

```python
for layer in model.layers:
    layer.to("cuda")

    hidden = layer(hidden)

    layer.to("cpu")
```

---

## Why it works

Transformer layers are mostly independent sequential functions:

[
h_{i+1}=f_i(h_i)
]

You don't need all layers simultaneously.

During inference:

```
Layer i needs:
    current hidden state
    layer i weights

Layer i+1 needs:
    output hidden state
    layer i+1 weights
```

Previous layers' weights are no longer needed.

---

## Example

Without AirLLM:

```
Llama-70B

FP16:

140GB weights

Need:
- A100 80GB x2
```

With AirLLM:

```
RTX 4090 24GB

+
system RAM

can run
Llama-70B
```

The tradeoff:

|                | Normal inference | AirLLM         |
| -------------- | ---------------- | -------------- |
| Speed          | Fast             | Slow           |
| VRAM           | Huge             | Small          |
| Implementation | Simple           | More complex   |
| Use case       | Production       | Personal/local |

---

## Installation

Typical:

```bash
pip install airllm
```

Example:

```python
from airllm import AutoModel

model = AutoModel.from_pretrained(
    "meta-llama/Llama-2-70b-hf"
)

output = model.generate(
    ["Explain transformers"]
)
```

---

## Comparison with other techniques

### 1. Quantization

Example:

```
FP16:
140GB

INT8:
70GB

4-bit:
35GB
```

Quantization reduces:

[
\text{weight precision}
]

AirLLM reduces:

[
\text{memory residency}
]

They can combine:

```
AirLLM
+
4-bit quantization
+
CPU offload
```

---

### 2. llama.cpp

llama.cpp:

```
GGUF model

CPU/GPU hybrid inference
quantization
optimized kernels
```

Usually much faster for consumer machines.

Example:

```
Qwen-72B-Q4

llama.cpp
RTX 4090
~few tokens/sec
```

AirLLM:

```
same model

more memory efficient
but slower
```

---

### 3. DeepSpeed ZeRO-Inference

DeepSpeed:

Designed for:

* clusters
* multi-GPU
* production serving

AirLLM:

* single developer machine
* experimentation

---

## Limitations

### 1. Slow generation

Because every token requires repeatedly moving layers:

```
CPU RAM
   |
PCIe
   |
GPU
```

PCIe bandwidth becomes bottleneck.

Example:

GPU compute:

```
100 TFLOPS
```

PCIe transfer:

```
~20-30 GB/s
```

You spend lots of time moving weights.

---

### 2. Not ideal for chat serving

Bad:

```
100 users
+
AirLLM
```

Good:

```
one researcher
one giant model
one machine
```

---

## Relation to your setup

For your RTX 4070 12GB:

Possible:

```
RTX 4070 12GB

+
64GB/128GB RAM

AirLLM

70B model inference
```

But speed will likely be poor.

Better options today:

### For local experiments

```
Qwen3-30B-A3B
Qwen3-32B
DeepSeek-R1-Distill-Qwen-32B

4-bit GGUF

llama.cpp
```

Your 12GB VRAM is much better matched to:

```
7B-14B:
fast

30B:
possible

70B:
AirLLM / CPU offload
```

---

## Historical importance

AirLLM became popular around 2023 because it demonstrated:

> "Memory capacity, not compute, is the first barrier to democratizing giant LLMs."

It was an early example of the broader trend:

```
Huge model
      |
      v
memory optimization

- quantization
- pruning
- offloading
- KV cache compression
- MoE
- MLA
```

Modern systems such as vLLM, llama.cpp, TensorRT-LLM, and DeepSpeed focus more on throughput, but the same fundamental problem remains: **how to fit increasingly large models into limited hardware**.

References:

* AirLLM GitHub: [https://github.com/lyogavin/airllm](https://github.com/lyogavin/airllm)
* llama.cpp: [https://github.com/ggml-org/llama.cpp](https://github.com/ggml-org/llama.cpp)
* DeepSpeed: [https://github.com/microsoft/DeepSpeed](https://github.com/microsoft/DeepSpeed)
* vLLM: [https://github.com/vllm-project/vllm](https://github.com/vllm-project/vllm)
