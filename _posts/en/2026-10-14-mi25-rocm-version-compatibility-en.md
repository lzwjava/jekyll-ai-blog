---
audio: false
generated: true
image: false
lang: en
layout: post
title: MI25 ROCm Version Compatibility
translated: false
type: note
---

For the **MI25 16GB**, the practical answer is:

| ROCm version | MI25 (`gfx900`) status |
| --- | --- |
| ROCm 4.x | Historically officially supported |
| ROCm 5.x | Official support dropped |
| ROCm 6.0–6.2 | Not officially supported; community workarounds may work |
| ROCm 6.3 | Community reports indicate some configurations work |
| ROCm 6.4+ | Not officially supported; compatibility depends on community builds and patches |
| ROCm 10.1 | Not officially supported |

Sources: [Arch Linux Wiki — MI25](https://wiki.archlinux.org/title/AMD_Radeon_Instinct_MI25) and [AMD's current GPU support matrix](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html). [wiki.archlinux.org](https://wiki.archlinux.org/title/AMD_Radeon_Instinct_MI25?utm_source=chatgpt.com)

### My recommendation

If you find a very cheap MI25, you could experiment with **ROCm 6.3 and a compatible PyTorch build**, but don't assume that every operation will work.

For example, some applications may run while others fail because their precompiled GPU kernels don't include `gfx900`.

If your goal is to experiment with LLM inference, test the exact combination of GPU, ROCm, PyTorch, and inference software before investing in multiple cards.
