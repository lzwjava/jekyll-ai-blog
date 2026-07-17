---
audio: false
generated: true
image: false
lang: en
layout: post
title: NVIDIA L4 GPU Overview
translated: false
type: note
---

Question: What's NVIDIA L4 GPU?

Answer:

NVIDIA L4 is a **low-power datacenter inference GPU** based on the **Ada Lovelace architecture** (same generation as RTX 40 series), designed mainly for **AI inference, video processing, and cloud workloads**, not large-scale training.

![Image](https://images.openai.com/static-rsc-4/S-fImIhGt-Cjj46vXR4rYJRG0aAKn1-r0NFNh2s4yWggwSL1g_lmTA0RlUsX0kz5pYIZLNZChn2RCiXkElTUVvY31bagQYeHFw8_8lHXjk5gj843Q4V740zWy8tmUT2DjcP0Bi0LYuDmWGELY-ZTHwZdheS-N_G6MuUVdqlD8afXEUy5Jpb2QC1jJJ_zwKoC?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/rM0l1u72mZUroI8B0wXYrUZiVqY4VOfNKhl2cLt912oGpp9ZIgR8V8fzOAic6H7XBvekUZlQS5VQzDwPcj_dU1V5mQdvltJAnVX6cXQGoKOSH8io0XLRgVu851IfrcJ6PpCNqpQgtmo0ARikBme3pdqOk6Cu8vpWNJllSKwUEtY4QM2RNzEcZA5bT_m_cHv9?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/mGVGYaU-TvegiPaWqZpGm2LXatOAgiY-l1qDiExOY-cyLO44BRixm1Gw1W7ArRzx2z3qlqJ-CvB4DnVC_EdvzR4Pxjw_E3Ts_Jcjxc5f14op3EZ4C55gq7FNBkzaxFuVhHh7y4z8PxHMlbwqe1Jt3OYVH9m6emQ6HyK3aE5i0_4p8q0AbJ8pnGawRT-P4GdB?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/0BWMw_DjhLMJeOCf1mrrxmKDipJkzIQzY2ZWyZxDEDYwCn-SZLcnmra1Y9nQhcUCEmCyHyNUxLZMPSBlsrZKv0_Ze4mN6q1TL6oNrjAE-_e7s9H1dymgbKnYrBuzKSxRI_sy46PcymAc8HZQs6O1E5H8aH14vd6ti-nk7O8juHw-oWVcEpeal3ILPaGpBDcp?purpose=fullsize)

Key specs:

|                  | NVIDIA L4                   |
| ---------------- | --------------------------- |
| Architecture     | Ada Lovelace                |
| GPU die          | AD104                       |
| VRAM             | **24GB GDDR6**              |
| Memory bandwidth | ~300 GB/s                   |
| Tensor cores     | 4th gen                     |
| CUDA cores       | 7,424                       |
| FP32             | ~30 TFLOPS                  |
| FP16 Tensor      | ~242 TFLOPS (with sparsity) |
| Power            | **72W**                     |
| Form factor      | Passive single-slot PCIe    |
| PCIe             | Gen4 x16                    |

### Positioning

Think of the L4 as:

```
RTX 4070       -> consumer AI / gaming
RTX 4090       -> consumer high-performance inference
L4             -> cloud inference server
A10            -> older datacenter inference
A100/H100      -> training + large inference
```

The L4 is basically a **server version of an RTX 4060/4070-class Ada GPU**, optimized for:

* low power
* density
* 24/7 operation
* many GPUs per server

---

### AI inference capability

24GB VRAM makes it useful for:

* Llama 3 8B
* Qwen 7B/14B
* Mistral 7B
* embedding models
* rerankers
* image generation (smaller models)

Example:

```
Qwen2.5-14B FP16
14B * 2 bytes ≈ 28GB
```

does not fit.

But:

```
Qwen2.5-14B INT8
14B * 1 byte ≈ 14GB
```

fits easily.

With vLLM:

```bash
vllm serve Qwen/Qwen2.5-14B-Instruct \
    --quantization awq \
    --gpu-memory-utilization 0.9
```

L4 can serve many concurrent users.

---

### Compared with your RTX 4070

|              | RTX 4070    | L4                 |
| ------------ | ----------- | ------------------ |
| VRAM         | 12GB GDDR6X | **24GB GDDR6 ECC** |
| Architecture | Ada         | Ada                |
| Power        | 200W        | **72W**            |
| Cooling      | active fan  | passive            |
| FP32         | ~29 TFLOPS  | ~30 TFLOPS         |
| AI inference | good        | better for server  |
| Training     | better      | limited            |

Interesting point: raw compute is almost identical.

The L4's advantage is:

```
RTX 4070:
  fast desktop GPU

L4:
  same generation GPU +
  2x VRAM +
  ECC +
  low power +
  datacenter drivers
```

---

### Compared with MI50 (your ROCm experiment)

|              | NVIDIA L4  | AMD MI50    |
| ------------ | ---------- | ----------- |
| Year         | 2023       | 2018        |
| VRAM         | 24GB GDDR6 | 16GB HBM2   |
| Bandwidth    | 300GB/s    | 1TB/s       |
| FP32         | 30 TFLOPS  | 13.4 TFLOPS |
| AI ecosystem | CUDA       | ROCm        |
| Power        | 72W        | 300W        |

MI50 has amazing memory bandwidth, but L4 wins for modern LLM inference because CUDA + TensorRT/vLLM ecosystem is much stronger.

---

### Price perspective

Typical second-hand / cloud value:

* L4 cloud rental: often around **$0.40–1/hour**
* Used L4 card: roughly **$1,000–2,000+ USD** depending on market

For hobby LLM work, a used RTX 3090 (24GB VRAM) is usually better value:

```
RTX 3090:
  24GB VRAM
  ~350W
  cheap used

L4:
  24GB VRAM
  72W
  expensive
```

For a datacenter:

```
100 servers × L4
vs
100 servers × RTX3090

L4 wins because electricity + density + reliability.
```

For your use case (training GPT-style models, ROCm experiments, local LLM infra), L4 is interesting mainly because it gives **24GB VRAM in a very efficient package**, but a used RTX 3090/4090 or A6000 is usually a better experimental GPU.
