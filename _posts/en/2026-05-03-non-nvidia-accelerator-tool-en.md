---
audio: false
generated: true
image: false
lang: en
layout: post
title: Explaining a Non-NVIDIA Accelerator Tool
translated: false
type: note
---

Question: What is this card shown in the `nvidia-smi`-like output, and how should it be explained?

Answer:

What you’re looking at is **not an NVIDIA GPU**, even though the interface looks similar to `nvidia-smi`. This is a **different accelerator ecosystem** that mimics NVIDIA tooling for familiarity.

Let’s break it down clearly.

---

## 1. What is “PPU” here?

* **PPU = Processing Unit (custom accelerator)**
* It’s analogous to a GPU, but **not from NVIDIA**
* The tool `ppu-smi` (shown as `PPU-SMI`) is a **drop-in replacement for `nvidia-smi`**

👉 Think of it like:

* NVIDIA → GPU + `nvidia-smi`
* This system → PPU + `ppu-smi`

---

## 2. The specific card: `PPU-ZW810E`

This is the model of the accelerator:

* **PPU-ZW810E**
* Likely a **datacenter AI training/inference chip**
* Comparable to:

  * NVIDIA A100 / H100
  * or Huawei Ascend 910 (very similar ecosystem style)

---

## 3. Key specs from your screenshot

### Memory

```
2MiB / 97920MiB
```

* Total memory ≈ **97 GB**
* That’s very large → clearly **AI training-class hardware**

👉 Comparable to:

* A100: 40GB / 80GB
* H100: 80GB
* This: **~97GB**

---

### Power

```
62W / 400W
```

* Max power: **400W**
* Current usage: **62W (idle)**

---

### Utilization

```
PPU-Util: 0%
```

* No workload running

---

### Temperature

```
24°C
```

* Idle / cool

---

### Processes

```
No running processes found
```

* Nothing is using the accelerator right now

---

## 4. What is “HGGC”?

```
HGGC Version: 13.0
```

This is the **software stack / runtime**, similar to:

* NVIDIA → CUDA
* This system → **HGGC (custom compute platform)**

👉 It likely includes:

* compiler
* runtime
* distributed training support

---

## 5. Why does it look like `nvidia-smi`?

Because many AI platforms intentionally copy NVIDIA’s interface:

* same columns:

  * memory usage
  * utilization
  * power
* same workflow:

  * check status
  * monitor jobs

👉 This lowers the learning curve for engineers.

---

## 6. What system is this likely from?

The “PAI DSW” in your terminal suggests:

* **PAI = Platform for AI (Alibaba Cloud)**
* DSW = Data Science Workshop

So this is probably:

👉 A **cloud AI instance using non-NVIDIA accelerators**

---

## 7. Simple mental model

You can think of this as:

```
PPU ≈ GPU
PPU-SMI ≈ nvidia-smi
HGGC ≈ CUDA
ZW810E ≈ A100/H100-class chip
```

---

## 8. Why 97GB memory matters

This is important for LLM work:

* Large models (like 70B+) need huge VRAM
* 97GB allows:

  * bigger batch sizes
  * larger context
  * fewer devices needed

---

## 9. Bottom line

This is:

👉 A **high-end AI accelerator (non-NVIDIA)**
👉 With ~97GB VRAM
👉 Running on a CUDA-like ecosystem (HGGC)
👉 Managed using a `nvidia-smi`-style tool

---

If you want, I can help you:

* compare this card vs A100 / H100 in real performance
* or show how to actually run LLMs on this PPU system
* or explain why OpenClaw might be consuming so many tokens on it