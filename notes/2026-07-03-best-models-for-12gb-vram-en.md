---
audio: false
generated: true
image: false
lang: en
layout: post
title: Best Models for 12GB VRAM
translated: false
type: note
---

Short answer: **none of them.** Even the most aggressive quant (TQ1_0 at ~158 GB) is 13× your VRAM and 2× your combined system RAM + VRAM.

The previous reply has it right — your RTX 4070 12 GB cannot run a 743B-parameter model at any quantization. Period.

**What you *can* run on that GPU:**

The MoE sweet spot for 12 GB VRAM + system RAM offload is models in the **80–110B total** / **10–15B active** range. Your best options right now:

| Model | Total params | Active | Q4_K_M size | Your speed (est.) |
|---|---|---|---|---|
| GLM-4.5-Air (UD-Q3_K_XL) | 106B | 12B | ~50 GB | 8–15 tok/s with offload |
| Qwen3-30B-A3B | 30B | 3B | ~18 GB | 30–50 tok/s, fits mostly in VRAM |
| DeepSeek-V3-Lite | ~68B | ~8B | ~35 GB | 15–25 tok/s with offload |

The GLM-4.5-Air with `--n-cpu-moe` (attention + shared expert on GPU, routed experts in system RAM) is the closest GLM-family model that'll actually run on your hardware. The Qwen3-30B-A3B is smaller but much faster since most of it stays on the GPU.

**So what should you actually download?**

```bash
# Pick one:
huggingface-cli download unsloth/GLM-4.5-Air-GGUF --include "*UD-Q3_K_XL*" --local-dir ~/models
# or
huggingface-cli download unsloth/Qwen3-30B-A3B-GGUF --include "*Q4_K_M*" --local-dir ~/models
```

Don't waste bandwidth on GLM-5.2 — it needs a datacenter GPU (MI300X, H100) even at 1–2 bits.