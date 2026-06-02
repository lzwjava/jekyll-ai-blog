---
audio: false
generated: true
image: false
lang: en
layout: post
title: MacBook Air M2 AI Engineering Guide
translated: false
type: note
---

Here's what your MacBook Air M2 (16 GB unified memory) looks like right now:

**Memory: critically tight**

- 48% free reported — but 6 GB is compressed (the OS is working hard to keep things running)
- 145 MB swap used (you're already overflowing to disk)
- 54 GB free disk — enough buffer for now
- WeChat 265 MB, WebKit tabs ~250 MB each, Github Desktop 236 MB, Python 188 MB, Zed 144 MB

This is an M2 with **unified memory** — there's no separate VRAM. The GPU shares the same 16 GB as everything else. When you run ML workloads here, you're competing with WeChat and Chrome.

---

## Optimizations for AI Engineering on This Machine

**1. Quantization — GGUF 4-bit for everyday inference**

llama.cpp with Metal backend is the baseline:

```bash
# Install llama.cpp with Metal support
brew install llama.cpp
llama-cli -m model.Q4_K_M.gguf -n 256 --mlock
```

For 7B models at Q4_K_M: ~4.5 GB RAM. Leaves ~11 GB for system.
Q8_0: better quality, ~7 GB — still workable if you close other apps.

**2. MLX — The real platform for M2**

MLX is Apple's native framework. It leverages the unified memory intelligently and can use the ANE (Neural Engine) which is separate bandwidth:

```bash
pip install mlx mlx-lm
```

For inference AND fine-tuning on 16 GB, MLX is by far the best option:

```python
from mlx_lm import load, generate
model, tokenizer = load("mlx-community/Llama-3.2-3B-4bit")
```

**3. Stop using swap — close the heavy hitters**

| Process | Memory | Fix |
|---|---|---|
| WeChat | 265 MB | Close if not needed |
| WebKit tabs | 250 MB × N | Close excess tabs |
| GitHub Desktop | 236 MB | CLI git saves 200+ MB |
| Zend (Zed) | 144 MB | Already lean |

Replace GitHub Desktop with `gh` CLI. Safari heavy tabs → close or suspend.

**4. ML training — don't**

The 16 GB M2 with no discrete GPU VRAM is not a training machine. Use it for:

- Inference (MLX 4-bit, 3B - 8B models)
- Embeddings generation (MLX)
- Agent orchestration (API calls to OpenRouter, your RTX 4070, AMD cloud)
- Eval + data engineering scripts

Reserve actual training for:

- 192.168.1.36 (RTX 4070 12 GB) — LoRA/QLoRA, nanoGPT
- AMD MI300X cloud (192 GB HBM3) — full fine-tuning, large GRPO runs

**5. Memory monitoring toolkit**

```bash
# Quick check
memory_pressure | grep "free percentage"
vm_stat | head -1
sysctl vm.swapusage

# Watch GPU pressure
sudo powermetrics --samplers gpu_power -n 1 -i 2000
```

**6. For your workflow (AI engineer, API-first, agent builder)**

Your actual workflow doesn't need local GPU at all — you route to OpenRouter, RTX 4070, and AMD cloud. On this MacBook:

- The terminal + editor + browser IS the workflow
- MLX for quick local inference/embeddings
- Close WeChat + excess Safari/Chrome tabs → reclaim 1+ GB immediately
- That frees the 6 GB compression overhead — the system stops swapping

Want me to set up any of that — close memory hogs, kill swap, or set up your ideal AI development stack on this machine?
