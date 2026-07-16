---
audio: false
generated: true
image: false
lang: en
layout: post
title: RX 6700 XT for AI Experiments
translated: false
type: note
---

Question: Intro to Radeon RX 6700 XT 12GB (RDNA2), especially for AI/GPU use.

Answer:

AMD Radeon RX 6700 XT is a **mid-range RDNA2 gaming GPU from 2021**. It is interesting today mainly because of the **12GB VRAM at low second-hand prices**. ([AMD][1])

![Image](https://images.openai.com/static-rsc-4/uqfwGc9FmLotS2eGklN8aE7wFb0903FJAXVjBNw3w78MgUF4-dpGkahN9No92ibvIcxrT9JOeJFZgZeRXzQjQHlgBQVDGc4gZLh8IrdIUDRATBoP7gDaALAlEw_4tdX3Ls2Vho3n8z_5cOLMGi-PO-960-NX9DX4EFuvojBqVKhlM7C9qIYkcVOWheljBvFK?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/LsWTcLgSl7waB4CP_z16klf8AB60wnMvWjCKu3cbQwrvkbgFiimr1vR2LW0oseJQrxZiIN2_jEEw65zZF3iqHVeG-ZA8voIPnBQSkOaqtEXAMMNUt9GDIb900nl_Onxr9kEG3BwAJqY9t9aTdIsUKvWFKaSxBkqXI5q-LVS6wLYfeaiLqDP2SnUxOa4paKup?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/p_7iLWvbkhCQ1u-hhcIbacVSW_sblGiCQ8ItJ4oTmCotz1Sg94yj-bJwHvo_SE9Evom-WOBkD8Biqiq2It7eDJp83gIZjydB7izxI1kgrbmO4Z4qVqKj28L6BlWV27urzVZoarVibyM312KGB1ZNp83bzw9zLkotHGr-q9hIsCfWf_63ewdlI-k5SxoV9W-g?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/eu-rFoI5eRR2vn4AnzFFXnV5F7gYxwLfaS8v-WN8IPhQS6L-V97tX6tut9kp2d0Unh4OL6RLkWzzy1UzaG7iYunRkPNT9o8WXC-RFHf8YpmBufthrfVrbhZu5lbazoRYVNR-YVSa2xBz0vaK7NKErgWu5hFQknN96J4PwqHDsR0MvMdw1EU57lmABi0HPjsN?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/yLWwyCNXrwgUwZXwwQsDdnh7Niz8X0oigxu8hVDMJNpNo2uR3Scr8kI6XTH1YzO-g2s4dMYTXGVWPWmRofvL9ZYAPZTnvq61kcSM90kjIxkV3nBGmEbeimmTbiKwoxX6CyYY6kc2eGiFIb0EZ2oJipYvjM1URDN76xEG4qnELqP8i7JnIJSk_CG8FQ3WuHwa?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/E2bYslRQcjAsGFohdpPUP5Ohhd99Mte0x-_P1DKYNlTQh8bJsO2A5Cc0-rcom33VlFYpTBkdwehhQdFlPQ5dSBNuouqrObbLbJ5Q2hIT_a9kTM8-Wh63G7wLjT4Kg41jU0D8BhuC47ZEmYTJKbYKBPiN7YP813DaCb78CavVL9_5PNB_UjA-2yYpB4Ee2Fz8?purpose=fullsize)

## Hardware specs

| Item              |   RX 6700 XT |
| ----------------- | -----------: |
| Architecture      |        RDNA2 |
| Chip              |      Navi 22 |
| Process           |          7nm |
| VRAM              |   12GB GDDR6 |
| Memory bus        |      192-bit |
| Bandwidth         |     384 GB/s |
| Infinity Cache    |         96MB |
| Compute Units     |           40 |
| Stream Processors |         2560 |
| FP32              | ~13.2 TFLOPS |
| Power             |        ~230W |
| PCIe              |     PCIe 4.0 |

([AMD][2])

It was designed as a **1440p gaming card**, positioned around RTX 3060 Ti / RTX 3070 class performance depending on workload. ([AMD][1])

---

## Compared with your RTX 4070

Your RTX 4070:

|              | RX 6700 XT | RTX 4070      |
| ------------ | ---------- | ------------- |
| VRAM         | 12GB       | 12GB          |
| Memory       | GDDR6      | GDDR6X        |
| Architecture | RDNA2      | Ada Lovelace  |
| AI ecosystem | Weak       | Excellent     |
| CUDA         | ❌          | ✅             |
| Tensor cores | ❌          | ✅             |
| FP16 AI      | OK-ish     | Much stronger |
| Power        | 230W       | 200W          |

For AI:

**RTX 4070 >>> RX 6700 XT**

because CUDA + Tensor cores + mature PyTorch support matter much more than VRAM size.

---

## For LLM / ROCm experiments

This is where RX 6700 XT becomes complicated.

### Good:

* 12GB VRAM
* Cheap
* Linux support
* Can run some OpenCL / ROCm experiments

### Bad:

RDNA2 consumer cards are not the sweet spot for ROCm.

The ROCm ecosystem is much better with:

* MI50
* MI100
* MI200
* MI300
* Radeon Pro VII

Your MI50 16GB is actually more interesting for ROCm than RX 6700 XT.

RX 6700 XT has similar VRAM:

```
RX 6700 XT
12GB GDDR6

MI50
16GB HBM2 ECC
```

but MI50 has:

* HBM2 bandwidth (~1TB/s class)
* ECC
* Instinct driver path

---

## Local LLM size

VRAM:

```
7B model
FP16:
7B × 2 bytes ≈ 14GB
```

so RX 6700 XT cannot comfortably load 7B FP16.

But:

```
7B Q4:
~4-5GB
```

works.

Examples:

```
Qwen2.5-7B-Q4
Llama-3.1-8B-Q4
Mistral-7B-Q4
```

should fit.

---

## Price evaluation

Your range:

```
¥1000-1500
```

is reasonable.

At:

### ¥1000

Good deal.

You get:

* 12GB VRAM
* gaming performance near RTX 3070 class
* cheap experiment card

### ¥1500

Less attractive.

Because used RTX 3060 12GB / RTX 3070 sometimes compete, and RTX gives CUDA.

---

## My ranking for AI experiments

For your use case:

```
RTX 4070 12GB
    |
    | much better
    v
RTX 3060 12GB
    |
    v
RX 6700 XT 12GB
    |
    v
RX 580 / older AMD
```

But for ROCm learning:

```
MI50 16GB
    >
Radeon Pro VII 16GB
    >
RX 6700 XT
```

---

## Verdict

RX 6700 XT 12GB:

* Gaming: ⭐⭐⭐⭐⭐
* Price/value: ⭐⭐⭐⭐
* LLM inference: ⭐⭐⭐
* ROCm learning: ⭐⭐
* Training: ⭐

For your situation (RTX 4070 + MI50 experiments), I would **not buy RX 6700 XT unless you find one around ¥1000**. It is mainly a cheap 12GB VRAM card, not a serious AI card.

References:

* AMD Radeon RX 6700 XT specifications ([AMD][2])
* AMD RX 6700 XT launch information ([AMD][1])

[1]: https://www.amd.com/en/newsroom/press-releases/2021-3-3-amd-unveils-amd-radeon-rx-6700-xt-graphics-card-d.html?utm_source=chatgpt.com "AMD Unveils AMD Radeon RX 6700 XT Graphics Card, Delivering Exceptional 1440p PC Gaming Experiences"
[2]: https://www.amd.com/en/products/graphics/desktops/radeon/6000-series/amd-radeon-rx-6700-xt.html?utm_source=chatgpt.com "Radeon™ RX 6700 XT Graphics Card"
