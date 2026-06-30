---
audio: false
generated: true
image: false
lang: en
layout: post
title: Three Independent Constraints Colliding
translated: false
type: note
---

The why comes down to three independent constraints colliding, not one.

**1. sglang's hard torch pin.** sglang 0.4.x doesn't loosely depend on torch — it pins to a specific build because it ships custom kernels (flashinfer, its own attention/sampling ops) compiled against a particular torch C++ ABI and CUDA version. Torch's C++ ABI (`libtorch`) is not stable across minor versions; a kernel `.so` built against 2.5.1's headers will hit symbol/ABI mismatches when loaded against 2.7.1, or vice versa. So "torch 2.5.1+cu124" wasn't a suggestion you could override — it was the version sglang's prebuilt wheels expected, and the planned combo simply wasn't the one sglang 0.4.x was actually built against.

**2. triton is pinned transitively by torch, not chosen freely.** Each torch release vendors a specific triton version it was tested/compiled against (torch hard-codes triton in its own dependency metadata):

- torch 2.5.x → triton 3.1.0
- torch 2.7.x → triton 3.3.x

triton is what compiles the fused kernels at runtime (the `@triton.jit` GPU codegen path used by `torch.compile`, flashinfer, and sglang's own ops). If triton's codegen, its PTX/ABI expectations, or its pointer-arithmetic semantics drift from what torch and the kernels assume, you get miscompiled kernels — which surface as **segfaults**, not clean Python exceptions, because the failure is in generated GPU/host code below the Python layer. So you can't mix-and-match: triton 3.3.1 belongs to the torch 2.7.x line, and forcing 3.1.0 under 2.7.1 (or 3.5/3.6 anywhere in this stack) breaks the contract.

**3. The CUDA tag (cu124 vs cu126) is the third axis.** The `+cu124` / `+cu126` suffix is which CUDA toolkit the torch wheel was built against. flashinfer/sglang prebuilt wheels are also tagged by CUDA version. cu124 torch + cu126-built sglang kernels = mismatched CUDA runtime symbols. They all have to agree.

**Why 3.3.1 specifically works:** It's the triton that ships with torch 2.7.1, so the torch↔triton ABI contract is satisfied by construction. And it predates the triton 3.5/3.6 line, which introduced codegen/IR changes that the flashinfer/sglang kernels in 0.4.x weren't built or tested against — those manifest as the segfaults you were avoiding. So 3.3.1 is the sweet spot: new enough to be the matched partner of the torch version sglang 0.4.x actually wants, old enough to stay inside the kernel compatibility window.

The mental model: **sglang picks torch, torch picks triton, the CUDA tag has to match all three.** You don't have three free variables — you have one (the sglang version), and everything else is determined. The original plan failed because it treated torch/triton/cuda as independently choosable when they're a single locked tuple defined by whatever sglang 0.4.x was compiled against.

If you want to verify the exact pins rather than trust the working combo empirically, the ground truth is in sglang's `pyproject.toml` / `setup.py` for the 0.4.x tag and torch's own `setup.py` triton pin — worth grepping those to confirm rather than rediscovering by segfault next upgrade.
