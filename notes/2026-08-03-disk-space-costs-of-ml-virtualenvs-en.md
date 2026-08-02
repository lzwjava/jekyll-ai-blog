---
audio: false
generated: true
image: false
lang: en
layout: post
title: Disk Space Costs of ML Virtualenvs
translated: false
type: note
---

Question: For AI/ML work specifically, will venvs eat a lot of disk space since torch is huge?

Answer: Yes — torch + CUDA is the actual size driver, not the venv mechanism. Numbers:

```bash
# torch with bundled CUDA libs
pip install torch  # ~2.5-3GB (CUDA 12.x wheels bundle cudnn, cublas, nccl etc)

# check what's actually eating space
du -sh $(python -c "import torch,os; print(os.path.dirname(torch.__file__))")
du -sh $(python -c "import torch,os; print(os.path.dirname(torch.__file__))")/lib/*.so*
```

Full stack for LLM work adds up fast:

| package | size |
| --- | --- |
| torch (cuda) | ~2.5-3GB |
| transformers | ~50-100MB |
| flash-attn (compiled) | ~500MB-1GB build artifacts |
| vllm | ~1-2GB (own torch + cuda deps) |
| deepspeed | ~200MB + compiled ops |
| datasets/tokenizers | ~50MB |

One venv for full fine-tuning stack: **4-8GB easy**. Ten project venvs, no dedup: **40-80GB gone**.

**What actually matters — dedup strategy:**

```bash
# 1. uv hardlinks across venvs from one cache — this is the single biggest win
uv venv .venv1 && uv pip install torch vllm
uv venv .venv2 && uv pip install torch transformers
# both venvs share underlying blobs, real disk usage ~1x not 2x
uv cache dir
du -sh $(uv cache dir)

# 2. CUDA-less torch build for CPU-only dev/testing venvs (way smaller)
pip install torch --index-url https://download.pytorch.org/whl/cpu
# ~200MB vs 3GB

# 3. Skip bundled CUDA, use system CUDA + separately installed cudnn
# (only worth it if you're already managing driver/toolkit versions manually)

# 4. Don't recompile flash-attn per venv — build once, reuse wheel
pip wheel flash-attn -w /tmp/wheels
# then in every venv: pip install /tmp/wheels/flash_attn-*.whl
```

For your MI300X setup specifically — ROCm torch builds are also multi-GB (~3-4GB), same story. `uv` + shared cache is the fix regardless of CUDA vs ROCm.

Real number to expect: with `uv` dedup, N venvs with the full LLM stack costs roughly **1x the base install (~5-8GB) + small deltas per venv**, not N×.

References:

- [PyTorch install matrix](https://pytorch.org/get-started/locally/)
- [uv cache/dedup docs](https://docs.astral.sh/uv/concepts/cache/)
