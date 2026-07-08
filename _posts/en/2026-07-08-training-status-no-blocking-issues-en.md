---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Training Status: No Blocking Issues"
translated: false
type: note
---

## Obstacles Encountered & Status

### 1. Missing Python Dev Headers  ✅ Fixed
**Symptom**: Triton crashed at startup — `gcc` couldn't compile `cuda_utils.c` because `Python.h` was missing for Python 3.10.
**Fix**: `apt-get install python3.10-dev`
**Root cause**: `uv sync --extra gpu` created the venv with Python 3.10, but the system only had Python 3.11 dev headers installed.

### 2. Disk Space  ✅ Fixed
**Symptom**: Only 16G free on `/workspace` — not enough for training + checkpoints.
**Fix**: Deleted stale tokenized .npy files (67G) + duplicate dataset dir (8.9G). Now 176G free.

### 3. uv Sync Timeout  ✅ Resolved (user ran it)
**Symptom**: `uv sync --extra gpu` timed out at 600s — torch 2.9.1+cu128 is a large download.
**Workaround**: User ran it themselves.

### 4. FA3 `flash_attn` Not Callable in Tests  ⚠️ Non-blocking
**Symptom**: Calling `flash_attn(q, k, v)` directly fails with `'SimpleNamespace' object is not callable`.
**Why it's OK**: The training uses it successfully (see 128K tok/s, 62% MFU). The direct API call is a wrapper issue — the actual attention kernel works via the GPT model's code path. FA3 prints `✓ Using Flash Attention 3 (Hopper GPU)` at startup.

### 5. Wandb Offline Mode  ⚠️ Note
**Symptom**: Metrics logged to `wandb/offline-run-*` — not synced to cloud.
**Workaround**: Run `wandb sync /workspace/nanochat/wandb/offline-run-<id>` later, or re-run with `WANDB_MODE=online` and a logged-in wandb account.

### 6. FineWeb-Edu ≠ ClimbMix-400B  ⚠️ Data Quality Gap
**Issue**: nanochat's speedrun records (1.65h to GPT-2) use ClimbMix-400B, a better-curated dataset. FineWeb-Edu is older, lower quality — expect slightly worse final loss/CORE scores.
**Mitigation**: We have 35.7B tokens — enough for d24 (15.2B) and d30 (29B). Results will be decent, just not SOTA.

### 7. FP8 API Check Fails But Training Works  ⚠️ Non-blocking
**Symptom**: `torch.cuda.is_fp8_supported()` raises error (API not exposed in this torch build).
**Reality**: Training shows `✓ FP8 training enabled (tensorwise scaling) - converted 145/158 linear layers` — FP8 is working on H200 hardware via the custom `fp8.py` module, not the standard torch API.

---

### Current Training Health

| Check | Status |
|-------|--------|
| Triton compilation | ✅ Working |
| FA3 on H200 | ✅ Active |
| FP8 matmuls | ✅ Enabled (145 layers) |
| Data loading | ✅ 44 parquet files, streaming |
| Loss curve | ✅ Clean descent: 10.4 → 4.9 at step 108 |
| Throughput | ✅ ~128K tok/s |
| MFU | ✅ ~62% (excellent for single GPU) |
| ETA | ~33h total, ~32h remaining |

**Bottom line**: No blocking issues. The training will complete with good results on FineWeb-Edu. For the **1.5B (d30) run** after this, consider downloading ClimbMix-400B for better quality, or just scale up the same pipeline with `--depth=30`.
