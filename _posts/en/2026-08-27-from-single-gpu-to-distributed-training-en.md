---
audio: false
generated: true
image: false
lang: en
layout: post
title: From Single GPU to Distributed Training
translated: false
type: note
---

Question: Your exploration path: moving from single-GPU LLM training to multi-GPU infra, DeepSpeed, inference systems, and GPU hardware — is this the right direction?

Answer:

Yes, your direction is quite natural. Actually your current position is interesting because you are sitting at the intersection of **three layers of AI engineering**:

```
model research
    ↓
training infrastructure
    ↓
hardware/system optimization
```

Most people only touch one layer.

You already did:

* train GPT-2 760M/1.3B scale models
* understand transformer basics
* run nanochat
* touch vLLM/KV cache
* build GPU environment
* debug CUDA/driver issues

The next step is not necessarily "buy more GPUs". It is understanding **why distributed training works**.

---

## 1. Two consumer GPUs: your intuition is correct

For example:

```
GPU0 RTX 4070
      |
    PCIe
      |
   CPU / chipset
      |
    PCIe
      |
GPU1 RTX 4070
```

The problem is communication.

A training step:

```
forward
  |
  v
loss
  |
backward
  |
gradient synchronization
  |
optimizer update
```

After backward:

GPU0 has:

```
gradients for all parameters
```

GPU1 has:

```
gradients for all parameters
```

They need to communicate:

```
GPU0 <-------> GPU1
```

On datacenter GPUs:

```
H100
 |
NVLink
 |
900 GB/s
```

Consumer PCIe:

```
PCIe 4.0 x16
~32 GB/s
```

Huge difference.

So for a 760M model, two consumer GPUs may not give 2x speed.

Sometimes:

```
1 GPU: 10 hours

2 GPU:
compute faster
communication slower

=> 6-8 hours
```

not:

```
5 hours
```

---

## 2. But you should still learn distributed training

Because the knowledge transfers.

The basic stack:

```
torch.distributed
        |
        v
DDP
        |
        v
DeepSpeed ZeRO
        |
        v
Megatron tensor parallel
        |
        v
large cluster training
```

DeepSpeed ZeRO is interesting because it attacks memory redundancy.

Normal data parallel:

GPU0:

```
weights
gradients
optimizer states
```

GPU1:

```
weights
gradients
optimizer states
```

Duplicate.

ZeRO:

GPU0:

```
weights A
optimizer A
```

GPU1:

```
weights B
optimizer B
```

The states are partitioned. ([DeepSpeed][1])

For your 1.3B model:

Adam memory:

```
parameters:
1.3B * 2 bytes(fp16)
≈2.6GB

gradients:
≈2.6GB

Adam states:
≈10GB+

total:
15GB+
```

A 16GB card is already tight.

Two GPUs + ZeRO makes experiments much easier.

---

## 3. Your next experiment should not be "train bigger"

I would do:

### Phase 1

Take your existing GPT-2 760M.

Run:

```
single GPU
vs
DDP 2 GPU
vs
DeepSpeed ZeRO-2
```

Measure:

```
tokens/sec
GPU utilization
communication overhead
memory
```

Make a table.

This is already a good engineering experiment.

---

## 4. The GPU hardware exploration actually fits

Many AI researchers avoid hardware.

But historically:

```
NVIDIA CUDA
        |
        |
AI explosion
```

The people who understand:

```
model
+
compiler
+
kernel
+
hardware
```

are rare.

For example:

FlashAttention is not just a math improvement.

Naive attention:

```
QK^T

store huge matrix

softmax

multiply V
```

Memory:

```
O(n^2)
```

FlashAttention:

```
load small blocks
compute
discard
```

Less HBM traffic.

The algorithm is designed around GPU memory hierarchy.

That is exactly the bridge:

```
Transformer
       |
       v
Attention kernel
       |
       v
CUDA
       |
       v
GPU architecture
```

---

## 5. vLLM / SGLang / KV cache is the right next layer

Training is only half.

Inference has another world.

Normal transformer generation:

token 1:

```
K,V
```

token 2:

recompute:

```
K1,V1
K2,V2
```

Wasteful.

KV cache:

store:

```
K1,V1
K2,V2
...
```

Then next token only computes:

```
new K,V
+
attention with cache
```

vLLM's PagedAttention idea is basically:

"virtual memory for KV cache".

Similar concepts:

```
OS virtual memory
        |
        v
GPU KV cache management
```

This is a beautiful area.

---

## 6. About ICML papers

Your concern is correct:

> one GPU, experiments slower

But many good papers are not about brute force.

Your advantage:

You can explore system + model.

Possible directions:

* efficient training
* small model scaling laws
* dataset quality
* inference optimization
* hardware-aware training
* agent evaluation

For example:

A 760M model is enough to study:

```
data
architecture
optimizer
tokenization
evaluation
```

You don't need 100B parameters.

---

## 7. Your current weakness is evaluation, not training

I think this sentence is important:

> 训练完了，大概用agent看看训练质量

This is where you can improve.

A model is not "done" after loss.

For example:

```
training loss
        |
        v
validation loss
        |
        v
benchmark
        |
        v
qualitative analysis
```

For code models:

```
HumanEval
MBPP
SWE-bench style tests
```

For language:

```
MMLU
ARC
HellaSwag
```

For your own models:

create your own eval:

```
100 coding questions
100 reasoning questions
100 Chinese/English questions
```

Then every experiment has a measurable output.

---

My view:

Your GPU exploration is not a distraction. It is probably your unique path.

Many people learn:

```
use API
fine tune
deploy
```

You are moving toward:

```
train model
understand kernels
understand GPU
build infra
```

That is closer to the Karpathy / systems engineer path.

The next practical milestone I would choose:

```
RTX 4070
        |
        v
GPT-2 760M
        |
        v
PyTorch DDP
        |
        v
DeepSpeed ZeRO-2
        |
        v
profile communication
        |
        v
write notes
```

One well-documented experiment here may be more valuable than ten random model trainings.

References:

* DeepSpeed ZeRO documentation ([DeepSpeed][1])
* DeepSpeed training API ([DeepSpeed][2])
* DeepSpeed pipeline/model parallel training overview ([deepspeed.ai][3])

[1]: https://deepspeed.readthedocs.io/en/stable/zero3.html?utm_source=chatgpt.com "ZeRO — DeepSpeed 0.19.2 documentation"
[2]: https://deepspeed.readthedocs.io/en/stable/training.html?utm_source=chatgpt.com "Training API — DeepSpeed 0.19.5 documentation"
[3]: https://www.deepspeed.ai/training/?utm_source=chatgpt.com "Training Overview and Features - DeepSpeed"
