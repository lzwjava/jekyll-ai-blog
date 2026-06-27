---
audio: false
generated: true
image: false
lang: en
layout: post
title: Capable Hardware, Broken Toolchain
translated: false
type: note
---

Right.

The 4070's Ada silicon (sm_89) runs FP16/BF16 attention and matmul kernels without issue — it's the same architecture class that vLLM/SGLang target in production. Nothing at the hardware level is gating you.

The failure is purely in the toolchain layer: Triton's JIT lowers your kernel through `triton.compile` → LLVM → PTX → `ptxas` (CUDA 13.0's assembler) → SASS. A segfault there is a compiler crash, not a GPU fault. You can confirm which stage with:

```bash
TRITON_DEBUG=1 python -c "import torch; ..." 2>&1 | tail -40
# or capture the IR dumps
MLIR_ENABLE_DUMP=1 TRITON_KERNEL_DUMP=1 python your_script.py
```

If it dies before any SASS is emitted, it's Triton's MLIR/LLVM passes. If it dies in `ptxas`, it's the CUDA 13.0 assembler choking on Triton-generated PTX. Either way: software.

One caveat to "purely software" — Triton/CUDA version matrices are validated against datacenter SKUs (H100/A100) first. Consumer Ada gets less coverage, so you hit edge bugs the big iron doesn't. The hardware is capable; the *tested* support surface just lags for consumer cards. Functionally that's still a software-stack problem you fix by pinning versions, not a 4070 limitation.

Fastest paths to a working stack on the 4070:

```bash
# Option A: known-good CUDA 12.4 wheels, skip CUDA 13 entirely
pip install torch==2.5.1 --index-url https://download.pytorch.org/whl/cu124
pip install triton==3.1.0   # the 3.1.x line is stable on cu124 + Ada

# Option B: vLLM, which ships its own validated torch+triton+cuda pin
pip install vllm   # let it resolve the whole matrix for you
```

vLLM is the cleaner path precisely because it freezes a triton/torch/cuda combination that's been smoke-tested together, instead of you fighting pip's resolver to hold a downgrade that runtime version-checks will undo anyway.
