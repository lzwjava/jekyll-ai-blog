---
audio: false
generated: true
image: false
lang: en
layout: post
title: Huawei Ascend 950 AI Chip Overview
translated: false
type: note
---

Question: Intro to Huawei 950 chip GPU

Answer:

Assuming you mean **Huawei Ascend 950** (昇腾 950), it is Huawei's next-generation AI accelerator/GPU-like chip in the Ascend AI processor family. It is **not a traditional GPU** like NVIDIA H100/B200; it is an **AI accelerator (NPU)** designed primarily for large-scale AI training and inference.

![Image](https://images.openai.com/static-rsc-4/ekY9WvsC7aEC_j5uOBe0gcaDjs39bz8g9vLIJIRDRG2V1_LU6PZAPT32P3BbKGvOCsBbfdu0Jin4fUao9mPZ5QocA1DvAshX9AtGHvUrkrUGen_8QZfuEWZ5aOUDhzqo10BY4aZO7PadI8JW9zFfla7G_5lgnGxe_wiPjJw3qBTPz3FEnQb-ocVNhrXu4uBD?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/cyirqFu2y0GaHwqwG2JBAve-VsGxEQ1ot20CEt_TC2sWrGO5VYdUY4ylxI90lJtQxAgHl4LMFzk5tSAaakkSMAjG_dEzaLhRMsZik7SUic2ckIBz9kLAwYwkQ2RllvfGrC9PCSWs0BRUy4YdeDdXwJJAZ9i3OoKYd7SMYdJ0s-krC9CzwBv1WNWbm5q9Aatg?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/tLLhIY0240X3gCkCI3othkoCEpGVp5nyOwAHlVvaWo6TF0egGXuDPFjnaTIES77v6DssHSAUSmiHYOvrvC9S_Xikgkky-T3mvkEhWTpQhwxp7hyED3JPdyp1ndEJWnFg4mrY4ynkbiZyzcjv-CCaHxNPiVwQ074R0kp0q-pMLbDyJ9cy-tIXpNRJNbuH-KWW?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/OHQWQENl_um9yekiH6rK0jQuCtfsUH9kSI9Lrh2lPO8ub14ISxZJf45UNIvuV7lJ9cUs23fITfzI33i5Zya-LJeW3gdwm65702xCCbRfS3N0rdxHpKJ0bR2IGu_9Iwiahep0J5f3IY9G6WOZoTrfH8BAfaJ5aiX5xbxcw9fgHOhqspgfw6hQ_uftVRgO8wbD?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/ZHd9VcS34VFUP4e_KildWkbz-Z_3ZH61ayjeNpUftoQ3R4x_lV-sKtOuBV64IrDGnsYWn1DjamdhapxE2VbMk2xnNFdr-KfzbKQPyCDwTFizUyOsPqtgzO4mMv9S6n-0FgXH53yLaMGijUNhaT9rF-R2kxupIgRoPfjphYUWmm3UCfcE8R5lm0Nml82A6zBN?purpose=fullsize)

## 1. Where Ascend 950 fits

Huawei's AI chip roadmap:

```
Ascend 310
   |
   | edge inference
   |
Ascend 910
   |
   | training / data center AI accelerator
   |
Ascend 910B / 910C
   |
   | domestic alternative to NVIDIA A100/H100 class
   |
Ascend 950
   |
   | next generation AI accelerator
```

The Ascend family is part of Huawei's:

* **Ascend chips** → compute
* **CANN (Compute Architecture for Neural Networks)** → software stack
* **MindSpore** → AI framework
* **Atlas servers** → hardware systems

Comparable ecosystem:

| NVIDIA               | Huawei                        |
| -------------------- | ----------------------------- |
| GPU                  | Ascend NPU                    |
| CUDA                 | CANN                          |
| cuDNN                | Ascend libraries              |
| PyTorch CUDA backend | PyTorch Ascend NPU backend    |
| TensorRT             | MindSpore / CANN optimization |

---

## 2. GPU vs Ascend NPU architecture

A simplified GPU:

```
CPU
 |
PCIe/NVLink
 |
GPU
 |
+----------------+
| CUDA cores     |
| Tensor Cores   |
| SRAM/L2        |
| HBM            |
+----------------+
```

Ascend:

```
CPU
 |
PCIe / HCCS
 |
Ascend NPU
 |
+----------------+
| AI Core        |
| Cube Engine    |
| Vector Engine  |
| AI Memory      |
| HBM            |
+----------------+
```

The key difference:

* NVIDIA designs a **general parallel processor**
* Huawei designs a **tensor computing machine**

For LLM workloads:

```
Transformer:

Q,K,V projection
       |
       v
   Matrix Multiply
       |
       v
   Attention
       |
       v
   FFN

```

Most compute is:

```
C = A × B
```

So Huawei optimizes:

```
Matrix multiplication
+
memory bandwidth
+
communication
```

---

## 3. Why Ascend 950 matters

The AI accelerator race is no longer only FLOPS.

The bottlenecks:

```
Training LLM:

40% compute
60%:

- HBM bandwidth
- memory capacity
- interconnect
- compiler efficiency
```

A chip needs:

### Compute

Example:

```
BF16 Tensor:

1000 TFLOPS
```

### Memory

```
HBM:

3 TB/s+
```

### Scale-out

```
8 GPUs/NPU

↓

hundreds/thousands of chips
```

The real competition:

```
NVIDIA B200
        vs
Huawei Ascend 950
        vs
AMD MI350
        vs
Google TPU
```

---

## 4. Ascend software stack

The hardest part is not silicon.

NVIDIA advantage:

```
CUDA
 |
cuBLAS
 |
cuDNN
 |
TensorRT
 |
PyTorch
 |
millions developers
```

Huawei stack:

```
MindSpore
 |
PyTorch-NPU
 |
CANN
 |
Ascend hardware
```

The compiler is critical.

For example:

PyTorch:

```python
x = torch.matmul(a, b)
```

CUDA path:

```
PyTorch
 |
ATen
 |
cuBLAS
 |
Tensor Core
```

Ascend:

```
PyTorch
 |
torch_npu
 |
CANN compiler
 |
Cube Engine
```

---

## 5. Relation to NVIDIA H100

Approximate positioning:

| Chip               | Position                |
| ------------------ | ----------------------- |
| NVIDIA H100        | 2023 frontier           |
| NVIDIA H200        | HBM capacity upgrade    |
| NVIDIA B200        | 2025 frontier           |
| AMD MI300X         | H100 competitor         |
| Huawei Ascend 910C | domestic AI accelerator |
| Huawei Ascend 950  | future generation       |

Ascend 950's goal is not to beat NVIDIA globally in software ecosystem. The goal is:

1. Reduce dependence on CUDA/NVIDIA
2. Build China's AI infrastructure stack
3. Provide enough performance for:

   * DeepSeek-style training
   * enterprise inference
   * government/cloud AI

---

## 6. The important engineering lesson

For LLM:

A chip is not just:

```
TOPS/FLOPS
```

The real stack:

```
AI Model
 |
PyTorch/JAX
 |
Compiler
 |
Kernel library
 |
Runtime
 |
Interconnect
 |
Memory system
 |
Silicon
```

NVIDIA dominates because CUDA owns the whole stack.

Huawei's challenge is similar to AMD ROCm:

```
Hardware is only 30%.
Software ecosystem is 70%.
```

For someone doing LLM training, the interesting comparison is probably:

```
Ascend 950
vs
AMD MI300X / MI350
vs
NVIDIA Blackwell
```

because all three are fighting the same bottleneck: **HBM + distributed Transformer training efficiency**.

References:

* Huawei Ascend AI computing platform: [https://www.hiascend.com/](https://www.hiascend.com/)
* Huawei CANN architecture: [https://www.hiascend.com/software/cann](https://www.hiascend.com/software/cann)
* NVIDIA Blackwell architecture: [https://www.nvidia.com/en-us/data-center/technologies/blackwell-architecture/](https://www.nvidia.com/en-us/data-center/technologies/blackwell-architecture/)
* AMD Instinct accelerators: [https://www.amd.com/en/products/accelerators/instinct.html](https://www.amd.com/en/products/accelerators/instinct.html)
