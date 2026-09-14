---
audio: false
generated: true
image: false
lang: en
layout: post
title: Tesla M40 vs P100 Comparison
translated: false
type: note
---

Question: How does the Tesla M40 compare, and will it work in your B150M + i5-6500?

Answer: **Yes, it will work electrically, but for your use case I would choose the P100 over the M40 unless the M40 is substantially cheaper.**

### M40 specs

The Tesla M40 is a **Maxwell** compute card:

|                    |       Tesla M40 |      Tesla P100 |
| ------------------ | --------------: | --------------: |
| Architecture       |       Maxwell 2 |          Pascal |
| CUDA cores         |           3,072 |           3,584 |
| VRAM               | **24 GB GDDR5** |   12/16 GB HBM2 |
| Memory bandwidth   |        288 GB/s |    **732 GB/s** |
| FP32               |       ~7 TFLOPS | **~9.3 TFLOPS** |
| PCIe               |         3.0 x16 |         3.0 x16 |
| Power              |       **250 W** |           250 W |
| Cooling            |     **Passive** |         Passive |
| Compute capability |         **5.2** |         **6.0** |

NVIDIA's M40 datasheet confirms 24 GB GDDR5, PCIe 3.0 x16, 250 W, and passive cooling. ([NVIDIA Images][1])

### Your B150M + i5-6500

**Compatible.**

Your B150M board has a PCIe 3.0 x16 slot, and the M40 is PCIe 3.0 x16. B150 also supports 6th-gen Core CPUs such as your i5-6500. ([MSI USA][2])

So:

```text
i5-6500
   │
B150M
   │ PCIe 3.0 x16
   ▼
Tesla M40
   │
   └── 24 GB GDDR5
```

No special motherboard is required.

### ⚠️ Cooling is exactly the same problem as P100

The M40 is **passively cooled**.

That means:

```text
M40 heatsink
████████████████
████████████████  ← NO GPU FAN
████████████████
       ↑
   needs airflow
```

And it's a **250 W** card.

You really want a high-airflow setup with a fan blowing directly through the heatsink. In a normal desktop case, I'd consider adding a **120 mm/140 mm fan mounted immediately in front of the M40**.

### The interesting part: 24 GB vs 16 GB

If you're considering these specifically for **LLMs**, the M40's 24 GB is attractive.

For example:

```text
7B FP16:
7B × 2 bytes ≈ 14 GB
```

So 24 GB gives you considerably more room for model weights + KV cache than a 16 GB P100.

But the M40 is **much older** and has compute capability **5.2**, which creates significant modern CUDA/software compatibility issues.

The P100's `sm_60` is much nicer for modern CUDA workloads.

### My ranking

For an LLM/CUDA machine:

```text
P100 16GB
  > M40 24GB
```

**unless the M40 is very cheap and you specifically need 24 GB.**

If you're choosing between something like:

```text
M40 24GB  → $80
P100 16GB → $100
```

I'd take the **P100**.

If it's:

```text
M40 24GB  → $50
P100 16GB → $150
```

then the **M40 becomes interesting** purely because of the 24 GB VRAM.

One more thing: **M40 has no display output and is passive**, so treat it as a headless CUDA accelerator, not a gaming GPU.

If you give me the **prices you're seeing for M40 / P100 / P40**, I can rank them specifically for **LLM inference per dollar**.

[1]: https://images.nvidia.com/content/tesla/pdf/78071_Tesla_M40_24GB_Print_Datasheet_LR.PDF?utm_source=chatgpt.com "Data Sheet: Quadro M6000"
[2]: https://us.msi.com/Motherboard/B150M-PRO-VDH/Specification?utm_source=chatgpt.com "Specification B150M PRO-VDH | MSI USA"
