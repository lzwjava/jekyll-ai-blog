---
audio: false
generated: true
image: false
lang: en
layout: post
title: Tesla P100 vs M60 for AI
translated: false
type: note
---

Question: Compare NVIDIA Tesla M60 vs Tesla P100 for AI workloads.

Answer:

Short version: **Tesla P100 is much faster for AI/compute. Tesla M60 is basically a virtualization/display GPU with two old Maxwell chips.** For LLM training/inference, P100 wins by a large margin.

NVIDIA Tesla M60 vs NVIDIA Tesla P100

|                  | Tesla M60          | Tesla P100      |
| ---------------- | ------------------ | --------------- |
| Architecture     | Maxwell (2015)     | Pascal (2016)   |
| GPU cores        | 2 × GM204          | 1 × GP100       |
| CUDA cores       | 2048 × 2 = 4096    | 3584            |
| VRAM             | 16GB GDDR5 (2×8GB) | 16GB HBM2       |
| Memory bandwidth | ~320 GB/s          | **732 GB/s**    |
| FP32 compute     | ~9 TFLOPS          | **9.3 TFLOPS**  |
| FP16 compute     | weak               | **18.7 TFLOPS** |
| Memory ECC       | Yes                | Yes             |
| Power            | ~300W              | 250W            |
| Cooling          | Passive            | Passive         |
| AI usefulness    | Low                | Much better     |

Sources: NVIDIA lists Tesla P100 PCIe at 3584 CUDA cores, 9.3 TFLOPS FP32, 18.7 TFLOPS FP16, and 16GB HBM2 with 732GB/s bandwidth. ([NVIDIA Images][1])

---

## 1. The biggest difference: memory

AI workloads are often **memory-bandwidth limited**.

Transformer inference:

```
tokens/sec ≈ memory bandwidth / model size
```

A 7B model FP16:

```
7B params × 2 bytes ≈ 14GB
```

You constantly stream weights.

M60:

```
320 GB/s
```

P100:

```
732 GB/s
```

P100 has more than **2× bandwidth**.

For LLM inference, this matters more than raw FLOPS.

---

## 2. Tensor / FP16 performance

Neither card has Tensor Cores.

But:

M60:

```
Maxwell
FP16 is basically not useful
```

P100:

```
Pascal
FP16 optimized
18.7 TFLOPS
```

P100 was literally designed for deep learning and HPC. ([NVIDIA][2])

---

## 3. For LLMs

Example:

### Qwen / Llama 7B quantized

Both have 16GB.

Could run:

```
7B Q4
~4-5GB
```

But speed:

Tesla M60:

```
slow decode
maybe 5-10 tok/s
```

Tesla P100:

```
maybe 15-30 tok/s
```

(depends heavily on software/kernel)

Community experiments also show P100 remains surprisingly useful for cheap LLM inference because of HBM2 bandwidth. ([Reddit][3])

---

## 4. Training / fine-tuning

P100 wins.

Example LoRA:

```
Llama 7B
4-bit QLoRA
```

M60:

* possible
* painful
* old CUDA
* slower

P100:

* reasonable
* better bandwidth
* ECC
* CUDA support

But important:

Neither supports:

```
BF16 Tensor Core training
```

You need:

* V100
* A100
* RTX 30/40 series
* H100

for modern efficient training.

---

## 5. Multi-GPU

M60 is interesting because:

```
M60 = two GPUs on one board
```

Linux sees:

```
GPU0 8GB
GPU1 8GB
```

not:

```
16GB unified
```

So you cannot run a 16GB model on one M60 GPU.

P100:

```
one GPU
16GB HBM2
```

Much simpler.

---

## 6. Price/value (used market)

Typical used prices:

### Tesla M60

~$50-100

Good for:

* virtualization
* CUDA learning
* cheap GPU experiments

### Tesla P100 16GB

~$100-200

Better for:

* PyTorch
* CUDA experiments
* small LLM inference
* HPC

---

## My ranking for an AI home lab

```
RTX 3090 24GB
        |
        | huge gap
        |
RTX 4070 12GB
        |
Tesla P100 16GB
        |
Tesla M60 16GB
```

For your use case (training GPT-style models, agents, local LLMs):

I would choose:

1. **RTX 3090 24GB** → best cheap AI card
2. **Tesla P100 16GB HBM2** → fun cheap AI accelerator
3. **Tesla M60** → only if extremely cheap (<$80)

The P100 is a "mini old A100 ancestor"; the M60 is more like a "server GTX 980 with ECC". ([developer.nvidia.com][4])

[1]: https://images.nvidia.com/content/tesla/pdf/nvidia-tesla-p100-PCIe-datasheet.pdf?utm_source=chatgpt.com "NVIDIA
® TESLA
® P100
GPU ACCELERATOR
World’s mo"
[2]: https://www.nvidia.com/en-au/data-center/tesla-p100/?utm_source=chatgpt.com "Tesla P100 Data Center Accelerator | NVIDIA"
[3]: https://www.reddit.com/r/MachineLearning/comments/193t4w8?utm_source=chatgpt.com "[D] Anyone Tried a Tesla P100 for Fine-Tuning LLMs?"
[4]: https://developer.nvidia.com/blog/inside-pascal/?utm_source=chatgpt.com "Inside Pascal: NVIDIA’s Newest Computing Platform | NVIDIA Technical Blog"
