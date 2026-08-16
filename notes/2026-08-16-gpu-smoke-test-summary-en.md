---
audio: false
generated: true
image: false
lang: en
layout: post
title: GPU Smoke Test Summary
translated: false
type: note
---

Smoke run complete. ✅ Here's the summary:

## Results

| Test | Command | Result |
|------|---------|--------|
| Import sanity | `python3.12 -c "import sglang, torch"` | ✅ sglang dev63, torch 2.11+cu130, CUDA available |
| Unit test | `python3.12 test/registered/unit/configs/test_embedding_model_spec.py -f` | ✅ 6 tests passed |
| Registered CLI test | `python3.12 test/registered/unit/cli/test_serve_backends.py -f` | ✅ 12 tests passed |
| **GPU inference smoke** (Qwen2.5-1.5B-Instruct) | engine launch + `engine.generate()` | ✅ "The capital of France is" → **" Paris, which is at latitude 48.85..."** in ~4s |

## Issues found & fixed along the way

1. **Python env**: default `python3` is 3.14 (linuxbrew); use `/usr/bin/python3.12` (3.12.3, sglang installed in dev mode from `/mnt/data/sglang/python`).
2. **Kernel version mismatch**: repo requires `sglang-kernel >= 0.4.6.post1`, but 0.4.6.post1's only PyPI wheel ships **SM100-only binaries** (won't load on your RTX 4070/SM89, plus a torch ABI mismatch). Reverted to **0.4.5** (has sm90/sm89-compatible binaries) and run with:
   ```bash
   env SGLANG_SKIP_SGL_KERNEL_VERSION_CHECK=1
   ```
3. **Default test model** (`meta-llama/Llama-3.2-1B-Instruct`) is gated/uncached; use the locally cached `Qwen/Qwen2.5-1.5B-Instruct` instead.
4. **DeepSeek-V2-Lite OOMs** on the 12GB card; stick to ≤1.5B models for local smoke tests.

## Working smoke command

```bash
cd /mnt/data/sglang && env SGLANG_SKIP_SGL_KERNEL_VERSION_CHECK=1 HF_HUB_OFFLINE=1 \
  /usr/bin/python3.12 /tmp/smoke_sglang.py
```

Note: this repo checkout is ahead of what the released `sglang-kernel` wheels support on SM89, so full GPU CI suites (`run_suite.py --hw cuda ...`) won't work locally until a matching kernel wheel ships. CPU suites (`base-a-test-cpu`) and unit tests run fine.