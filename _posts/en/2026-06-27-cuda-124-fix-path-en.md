---
audio: false
generated: true
image: false
lang: en
layout: post
title: CUDA 12.4 Fix Path
translated: false
type: note
---

Here's the analysis:

```
Current stack on workstation:
  Driver:   580.126.20  (supports CUDA 12.0–13.0)
  torch:    2.11.0+cu130
  triton:   3.6.0
  sglang:   0.5.9
  Python:   3.11 (no pip in venv)
  GPU:      RTX 4070 (sm_89, Ada Lovelace)
```

The problem chain: `torch 2.11.0` pins `triton>=3.5`, and Triton 3.5/3.6 JIT crashes on CUDA 13.0 + sm_89. You can't downgrade triton without --no-deps, and even then torch may runtime-reject it.

Three fix paths, ranked:

```
1. CLEANEST — Fresh venv with CUDA 12.4 wheels:
   Driver 580.x is backward-compatible with CUDA 12.x.
   torch 2.5.1+cu124 + triton 3.1.0 = known-good on Ada.
   sglang 0.4.x works with that combo.

2. FASTEST — Drop vLLM into existing venv:
   pip install vllm — it bundles its own validated stack.
   But may conflict with existing sglang deps.

3. RISKY — --no-deps triton pin:
   pip install --no-deps triton==3.4.0
   Torch may runtime-reject it. Fragile.
```

Option 1 is the most reliable. Want me to set up the fresh venv with cu124 wheels on the workstation?
