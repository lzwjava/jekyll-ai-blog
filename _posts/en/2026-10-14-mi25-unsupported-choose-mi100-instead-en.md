---
audio: false
generated: true
image: false
lang: en
layout: post
title: "MI25 Unsupported: Choose MI100 Instead"
translated: false
type: note
---

### What about unofficial workarounds?

Some community projects and older software stacks may enable unsupported GPUs, but success with MI25 depends on the ROCm version and the individual application's kernels.

For the MI25, the GPU target is `gfx900`. AMD's official documentation explicitly marks it **unsupported** in both ROCm 6.1 and current documentation. [AMD ROCm](https://rocm.docs.amd.com/projects/install-on-linux/en/docs-6.1.5/reference/system-requirements.html?utm_source=chatgpt.com)

If you're buying a used card for AI, I'd prioritize:

| GPU | VRAM | ROCm outlook |
|---|---:|---|
| Instinct MI25 | 16GB | Officially unsupported |
| Instinct MI50 | 16GB/32GB | Legacy; current official support removed |
| Instinct MI100 | 32GB | Officially supported |
| Instinct MI210 | 64GB | Officially supported |

See AMD's [GPU compatibility documentation](https://rocm.docs.amd.com/en/latest/compatibility/compatibility-matrix.html).

**My advice:** If you find an MI25 for a very low price, treat it as a hardware/software hacking project, not a dependable ROCm accelerator. If you want an older AMD GPU for serious PyTorch experiments, the MI100 is a much safer choice.