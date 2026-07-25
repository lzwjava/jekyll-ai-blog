---
audio: false
generated: true
image: false
lang: en
layout: post
title: Torch Compile Fails for FLUX
translated: false
type: note
---

![Cat HD](cat_hd.png)

Here's the summary of what happened and what we learned:

---

## 🔍 What went wrong with `torch.compile`

| Approach | Result | Time |
| ---------- | -------- | ------ |
| ❌ `pipe.to('cuda')` — all to GPU | **OOM** (54 GB > 48 GB VRAM) | — |
| ❌ `enable_model_cpu_offload` — 1024×1024 | **OOM** (transformer + activations too big) | — |
| ✅ `enable_sequential_cpu_offload` — 512×512 | **Works** | **60.3s** |
| ❌ `torch.compile` with `max-autotune` | **Timeout** (>5 min compiling kernels) | — |
| ❌ `torch.compile` with `reduce-overhead` | **Stuck** (lazy compilation on first forward, 32 workers, minutes) | — |
| ✅ `enable_sequential_cpu_offload` — 1024×1024 | **Works** (APEX cached this time) | **37.2s** 🚀 |

### Key takeaways

1. **`torch.compile` is not worth it for FLUX** — the compilation overhead (minutes) far exceeds the generation time (37s) for a 4-step run
2. **Sequential CPU offload is the magic bullet** — keeps VRAM under 48 GB by moving individual submodules to GPU one at a time
3. **Attention slicing** reduces activation memory enough for 1024×1024
4. **1024×1024 is faster than 512×512** on the 2nd run because APEX kernels are cached (0.22s vs 20s compilation)

### Final working recipe

```python
pipe = FluxPipeline.from_pretrained('/root/FLUX.1-schnell', torch_dtype=torch.bfloat16)
pipe.enable_sequential_cpu_offload()
pipe.enable_attention_slicing()

image = pipe("prompt", num_inference_steps=4, width=1024, height=1024).images[0]
# → ~37s per 4-step image on AMD Radeon 48 GB
```
