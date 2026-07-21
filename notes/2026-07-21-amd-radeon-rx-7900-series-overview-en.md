---
audio: false
generated: true
image: false
lang: en
layout: post
title: AMD Radeon RX 7900 Series Overview
translated: false
type: note
---

Question: Intro to AMD Radeon RX 7900 series cards.

Answer:

![Image](https://images.openai.com/static-rsc-4/L_TDlUdg5rpbIpgXgWDTDIECgUbrFgGqGEMvPj9G1HSOFC62QtioyLwHnREZY84PHpkNfKdCKSzF3dq7cPt8jZZCJt54ujHItgnvH8q3i7hgeMyfjOdeIE6r6l79e4a3NQJ8mXiDicwJroatwJyJ4wQy0Ak7iozQdnrtDPDRcZPpuU6GYhNhQEhD5SnIKcK7?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/yXOZ1Z-FH_fk1ZMFr1fS8d0om-lB8gWDQA7puOhtfKRE51zGz8yngynQFKeXejR5YO14TMx1I404vU1bRussDjHmf7CWRepBLin0h0DM18BTcpW4CnI0a_VyqMLs2Bo0Z0VmZ0jqMXamriaWKZTeYPaXmcaFHLjwNpHsU0ypReW9TgiNkoYFDBv0XL6WPAru?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/p7iETk3hnNdohtlDOcZRrJND4D9gsvT_btBRWz0CMJR7uhokxa3ETE8Vkpvvkmd0RXsW-g2JSgIEbfaHNJlpjTn6m0tIXIZV-C6M_ta2P-6NN_boivJsvPridn9n70j8oGvsqpZmn28fZnnLCi6ddzrscJLMkbTLOq7g32MRrpGmjSm_u-2FVaTD5QIrXWyY?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/HLzBYOAjU7slWI8dvEwq8UoRFAi7FArHVsl5OsLNsiVT5QzozYEukoew2U3m1YtMS5LlDpjc4cPvDifpbALGuJZT2eaCklRh_hDK2N8pDoW-N1IjMzwSdXrZfPKaWfiJfkePMUrUGAgcvk5Yqk9zVzwK9HUkFHuwxSOb4sQo7fITQcLyFCdHyHu3-SNG3yZw?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/DbFr7gARWS5khW-6UA5qUClJFxA3Y9O4PludM1g0JIAU-DaStalu2zO73TWEvu_eqkZd1dywzOtJapyJtQmgrF-dpoLoRqAvntVqEVCug5ohruWnEaCeg0BkIN2d73vq2cJmT1dNzd5LeYwtY7u2HvG7bq6swoYBrTGqL__1kYoAfqBQ4rz2V7R-oyqMI3eK?purpose=fullsize)

The **AMD Radeon RX 7900 series** is AMD's high-end consumer GPU family based on the **RDNA 3 architecture**, launched in late 2022. The main models are:

* AMD Radeon RX 7900 XTX — flagship
* AMD Radeon RX 7900 XT — slightly cut-down version
* AMD Radeon RX 7900 GRE — lower-cost variant

## Hardware specs

| Model             | RX 7900 XTX |  RX 7900 XT |
| ----------------- | ----------: | ----------: |
| Architecture      |      RDNA 3 |      RDNA 3 |
| Compute Units     |          96 |          84 |
| Stream Processors |        6144 |        5376 |
| VRAM              | 24 GB GDDR6 | 20 GB GDDR6 |
| Memory Bus        |     384-bit |     320-bit |
| Infinity Cache    |       96 MB |       80 MB |
| TBP               |       ~355W |       ~315W |
| FP32 Compute      |  ~61 TFLOPS |  ~52 TFLOPS |

The interesting part:

**RX 7900 XTX has 24GB VRAM**, which is more than RTX 4080 (16GB) and comparable to RTX 3090 (24GB).

---

## Architecture: RDNA 3

Unlike NVIDIA's monolithic GPUs, AMD moved to a chiplet design:

```
          Navi 31 GPU

        +-------------+
        | Graphics    |
        | Compute Die |
        +-------------+
          |   |   |
     +----+---+---+----+
     |    |   |        |
    MCD  MCD MCD ...  MCD

   Memory Cache Dies
```

The GPU contains:

* **GCD (Graphics Compute Die)**

  * shader cores
  * ray tracing units
  * AI acceleration
* **MCD (Memory Cache Dies)**

  * Infinity Cache
  * memory controllers

This is similar to AMD CPU chiplets.

---

## AI / LLM usage

For AI workloads, RX 7900 XTX is interesting because:

### Pros

### 1. Large VRAM

24GB VRAM allows:

* Llama 3 8B FP16
* Qwen 14B FP16
* 30B+ quantized models
* Stable Diffusion / image models

Example:

```
Qwen2.5-14B FP16

14B params × 2 bytes
≈ 28GB

Need quantization

Q4:
14B × 0.5 byte
≈ 7GB

Fits easily
```

---

### 2. Good memory bandwidth

RX 7900 XTX:

```
VRAM bandwidth:
≈ 960 GB/s
```

Very close to:

```
RTX 3090:
936 GB/s
```

For LLM inference, memory bandwidth matters a lot.

Approximate token generation:

```
tokens/sec ≈ memory bandwidth / model size
```

---

## ROCm support

The important difference vs NVIDIA:

NVIDIA:

```
PyTorch
  |
CUDA
  |
RTX GPU
```

AMD:

```
PyTorch
  |
ROCm
  |
Radeon GPU
```

RX 7900 supports ROCm, but consumer Radeon support has historically lagged behind Instinct GPUs.

For example:

Good:

* PyTorch
* Llama.cpp
* Ollama
* ComfyUI
* Stable Diffusion

Less smooth:

* FlashAttention
* vLLM
* Triton kernels
* custom CUDA extensions

NVIDIA ecosystem is still much stronger.

---

## Comparison with NVIDIA cards

### RX 7900 XTX vs RTX 4090

|              | RX 7900 XTX | RTX 4090  |
| ------------ | ----------- | --------- |
| VRAM         | 24GB        | 24GB      |
| Memory       | GDDR6       | GDDR6X    |
| FP32         | 61 TF       | 82 TF     |
| Tensor cores | No          | Yes       |
| CUDA         | No          | Yes       |
| AI ecosystem | weaker      | strongest |

For gaming:

```
7900 XTX ≈ RTX 4080
```

For AI:

```
RTX 4090 >>> RX 7900 XTX
```

because CUDA + Tensor cores dominate.

---

## Compared with RTX 3090 for AI

Interesting comparison:

|              | RX 7900 XTX | RTX 3090  |
| ------------ | ----------- | --------- |
| VRAM         | 24GB        | 24GB      |
| Bandwidth    | 960GB/s     | 936GB/s   |
| FP16         | good        | excellent |
| CUDA         | ❌           | ✅         |
| Tensor cores | ❌           | ✅         |
| Used price   | cheaper     | higher    |

For pure memory capacity:

```
7900 XTX ≈ RTX 3090
```

For LLM engineering:

```
RTX 3090 wins
```

because:

* vLLM works better
* FlashAttention works better
* more pretrained CUDA kernels
* easier multi-GPU

---

## Multi-GPU possibility

7900 XTX has:

```
PCIe 4.0 x16
24GB VRAM
```

You can build:

```
2 × RX 7900 XTX

48GB VRAM total
```

or:

```
4 × RX 7900 XTX

96GB VRAM
```

But software scaling is harder than NVIDIA.

For example:

```
NVIDIA:
2×3090
 -> vLLM tensor parallel
 -> easy

AMD:
2×7900
 -> possible
 -> more debugging
```

---

## Price/performance in 2026 used market

A used RX 7900 XTX can be attractive if:

* you mainly do local inference
* you use llama.cpp / Ollama
* you need VRAM cheaply
* you don't need CUDA

Typical value:

```
24GB VRAM
+
~1TB/s bandwidth
+
low used price
```

makes it a "poor man's 4090" in memory terms.

---

For your use case (training GPT-2, running Qwen/Llama agents, experimenting with local LLMs), I would rank:

```
RTX 3090 24GB
    >
RX 7900 XTX 24GB
    >
RTX 4070 12GB
```

The RX 7900 XTX is a very capable hardware card, but the AI software ecosystem is the limiting factor. It is more attractive for **inference + experimentation** than for **serious LLM training/fine-tuning**.
