---
audio: false
generated: true
image: false
lang: en
layout: post
title: Blackwell Consumer Compute Capability
translated: false
type: note
---

Question: What does SM120 mean?

Answer:

`sm_120` = compute capability **12.0** = **Blackwell consumer GPUs** (RTX 50xx series — 5090, 5080, etc.).

Same encoding as before: `SM<major><minor>` → `sm_120` = 12.0.

The Blackwell generation splits into two arch numbers, same consumer/datacenter pattern you saw with Ampere:

- `sm_100` → 10.0 → Blackwell **datacenter** (B100, B200, GB200)
- `sm_120` → 12.0 → Blackwell **consumer** (RTX 5090/5080/5070, RTX PRO 6000)

Note the jump skips 11.x entirely — NVIDIA reserved 10.x for the datacenter die (GB100) and bumped consumer to 12.x rather than using a minor version like they did with Ampere (`sm_80` vs `sm_86`). The two Blackwell dies are different enough silicon that they got separate major versions.

What `sm_120` adds over `sm_89` (your Ada 4070):

- **5th-gen Tensor Cores** with `fp4` (NVFP4) and `fp6` support — sub-byte quantized inference. This is the headline feature for LLM serving.
- **2nd-gen Transformer Engine** with finer-grained fp8/fp4 scaling.
- Updated `tcgen05` Tensor Core MMA instructions (the datacenter `sm_100` gets the full tensor-memory async path; `sm_120` gets a consumer subset).

Practical gotcha for you: **PyTorch/CUDA toolkit version matters.** `sm_120` needs **CUDA 12.8+** and a recent PyTorch build (2.7+). Older wheels compiled with `TORCH_CUDA_ARCH_LIST` topping out at `9.0` will fail or fall back to slow PTX JIT on a 5090. If you ever rent a 5090 box:

```bash
nvidia-smi --query-gpu=compute_cap --format=csv,noheader   # → 12.0
python -c "import torch; print(torch.cuda.get_device_capability())"  # (12, 0)
# make sure: torch.version.cuda >= '12.8'
```

For your stack, the `fp4` support is the interesting part — it's what makes Blackwell attractive for cheap local inference of large quantized models, vs your 4070 which caps at `fp8` Tensor Core ops (and even fp8 is limited on Ada consumer).
