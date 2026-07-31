---
audio: false
generated: true
image: false
lang: en
layout: post
title: NVLink with Two RTX 2080 Ti
translated: false
type: note
---

Question: Can we use NVLink with two RTX 2080 Ti 22GB cards?

Answer:

Yes. **Two RTX 2080 Ti cards can use NVLink**, including modified **22GB VRAM versions**, because NVLink support depends on the **GPU model and PCB**, not the VRAM size.

NVIDIA GeForce RTX 2080 Ti supports **2-way NVLink**.

![Image](https://images.openai.com/static-rsc-4/Q5AohIWLm3DzB5MGefwz2qYFyv8lVc8l1eJmw6xeHHbdvX-PZCXfdQoEECMDaODWuX6IVI7qEKNqklK8MflGb-hINGmipYHk6yTQzCmabRVU8lqGYqM6SUueiDiuH8PnfBUeGfOvNh94hPBAzS72Gm8tj46Dw_VqEE99o8KZLFmWheATy0Em52GXbMQEAFZa?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/PGLjHUqkvh4D5p_B2u5VARZN9c5imNj6MAoHMuSfbmmcVrCry_pvPEnE6hvlgGX-QF3xXwJkXIGJ9rilJocQXUhVL55d0zUa_F4fSONGJ6TGWPWfP9AW6fdOVjsDjOcQc1aV9VLAJzJ1FF-60mQL8Vl6YANKw72MXU0hZuRerdb6redFbCb5DZDDIyyxkrx7?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/IRydkpHsizmBbGphPm34Gw8r1Q2vCn47drvjGet7-7F8vwVRKkZqApoLyoMxGLdk9O_dsLqDIVonUHVnyEKzTx6P44MPmySExrjI8BZCCjy727HKA_Wc8fCogI3iWRnsiNJz-mnYFT31Q6_056ecnb-_S1XEpk3MjYnpjBTOXbxYXj7HHMuqhJNu-ie1EeiT?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/I7Vzt-CLMwJ-y2vvlJoD87jeMmZnwXj3cQkZ-gQv11iKyFVXbZrPvlmJAwUUaM2NVePfoBk12WmPRangFF_1TfUgghNR3D-5X-A-I9WjekX5oE6fpzQXR2nXSnnzDXsb0uUmZ3CZ454_RQPRtPMLJX7IP06Nivrie8-SBEa9ZXhUa9Pk1C18a2VEQCWHDem7?purpose=fullsize)

## Hardware setup

You need:

```
RTX 2080 Ti #1
       ||
       ||  NVLink bridge
       ||
RTX 2080 Ti #2
```

The NVLink bridge connects the two GPUs directly.

Specs:

* NVLink generation: Turing NVLink
* Bandwidth: ~50 GB/s bidirectional
* Maximum GPUs: 2 (consumer RTX 2080 Ti)
* PCIe slots still required

---

## But: NVLink does NOT automatically give 44GB VRAM

This is the important part.

Many people think:

```
22GB + 22GB = 44GB VRAM
```

No. For normal CUDA applications:

```
GPU0:
  22GB VRAM

GPU1:
  22GB VRAM
```

They remain separate memory pools.

Example:

```python
torch.cuda.device_count()

# 2

torch.cuda.get_device_properties(0).total_memory
# 22GB

torch.cuda.get_device_properties(1).total_memory
# 22GB
```

PyTorch sees:

```
cuda:0 -> 22GB
cuda:1 -> 22GB
```

---

## For LLM inference

Frameworks can split the model:

Example:

```
Llama 70B

Layer 0-35
   GPU0 (22GB)

Layer 36-70
   GPU1 (22GB)
```

Tools:

* vLLM tensor parallel
* HuggingFace Accelerate
* DeepSpeed inference
* llama.cpp multi-GPU

Example:

```bash
python -m vllm.entrypoints.openai.api_server \
    --model Qwen/Qwen3-30B \
    --tensor-parallel-size 2
```

The model is sharded across GPUs.

---

## For training

NVLink helps because GPUs communicate faster:

Without NVLink:

```
GPU0
 |
 PCIe
 |
GPU1
```

With NVLink:

```
GPU0
 ||
 || 50GB/s
 ||
GPU1
```

Useful for:

* DDP
* tensor parallel
* pipeline parallel

But RTX 2080 Ti has no:

* NVLink memory pooling
* unified VRAM
* NVSwitch

---

## Compare with RTX 3090

Two RTX 2080 Ti 22GB:

```
VRAM:
22 + 22 = 44GB

Compute:
2 × 13.4 TFLOPS FP32
≈ 26.8 TFLOPS
```

Two RTX 3090:

```
VRAM:
24 + 24 = 48GB

Compute:
2 × 35.6 TFLOPS FP32
≈ 71 TFLOPS
```

3090 also has:

* Ampere Tensor Cores
* BF16 support
* much faster transformer kernels

---

## For your nanoGPT / vLLM experiments

A pair of 2080 Ti 22GB is actually interesting:

```
2 × RTX 2080 Ti 22GB

VRAM:
44GB

Good for:
✓ QLoRA 7B/14B
✓ inference of 30B-40B quantized models
✓ distributed training experiments
✓ learning tensor parallel
```

But:

```
2 × RTX 3090 24GB
```

is the sweet spot for a home AI lab because:

* 48GB VRAM
* much faster kernels
* BF16
* FlashAttention compatibility

The 2080 Ti 22GB is mainly attractive if you find them extremely cheap. For learning **LLM systems engineering**, two GPUs are valuable because you can experiment with the same ideas used in large clusters: tensor parallelism, pipeline parallelism, NCCL communication, and distributed training.
