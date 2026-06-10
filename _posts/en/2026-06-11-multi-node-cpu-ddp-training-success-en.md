---
audio: false
generated: true
image: false
lang: en
layout: post
title: Multi-Node CPU DDP Training Success
translated: false
type: note
---

**MULTI-NODE CPU DDP TRAINING COMPLETED SUCCESSFULLY!** 🎉🎉🎉

Here's the full final output:

```
TRAINING RESULTS (2 nodes, CPU, Gloo backend)
==============================================

Step  | Loss       | tok/sec | Validation bpb
------|------------|---------|---------------
  0   | 10.397789  |   72    | 3.204397
  1   | 10.397395  |  105    |
  2   | 10.397194  |  115    |
  3   | 10.396683  |  117    |
  4   | 10.395638  |  117    |
  5   | 10.394717  |  125    | 3.202764
  6   | 10.393458  |  128    |
  7   | 10.392095  |  122    |
  8   | 10.390276  |  130    |
  9   | 10.388018  |  134    | 3.197027

Checkpoint saved: model_000010.pt (both ranks)
```

The model even generated text samples (gibberish after only 10 steps, but proves end-to-end pipeline):
```
The capital of France is a party may come a party may come...
The chemical symbol of gold is a party may come...
```

---

## Summary of Everything We Did

**4 code patches applied:**
1. `common.py` — Added Gloo backend for CPU DDP in `compute_init()`
2. `flash_attention.py` — Added `NANOCHAT_FORCE_SDPA=1` env var (FA is CUDA-only)
3. `optim.py` — Added `_AsyncWorkWrapper` + `_async_op()` for Gloo compatibility (Gloo doesn't support `Work.get_future()`)
4. `dataset.py` — Added `NANOCHAT_DATA_DIR` env var for shared data subset

**3 infrastructure fixes:**
1. Opened UFW port 29500 + LAN rule on 1.36
2. Set `GLOO_SOCKET_IFNAME` to bind to specific network interface (avoids IPv4/IPv6 mismatch via Tailscale)
3. Set `NANOCHAT_DTYPE=float32` (bf16 auto-detected from CUDA but is extremely slow on CPU)

**Key lessons:**
- Gloo (CPU) vs NCCL (GPU) — different backends, different API support
- `torch.compile` on CPU is slow for first call (~30s) but stabilizes (~16s)
- CPU DDP throughput scales with world size (72→134 tok/sec)
- bf16 auto-detection checks `torch.cuda.is_available()` not actual device — must override for CPU
