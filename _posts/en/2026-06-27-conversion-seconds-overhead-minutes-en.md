---
audio: false
generated: true
image: false
lang: en
layout: post
title: Conversion Seconds, Overhead Minutes
translated: false
type: note
---

For converting a 124M model checkpoint (~600MB) to HuggingFace format, the bottleneck is almost entirely the `scp` transfer and disk I/O — not compute. The actual conversion is trivial.

Breakdown:

**scp transfer (600MB over LAN):** On a typical gigabit LAN (~110 MB/s real throughput), 600MB takes ~5-6 seconds. On WiFi (~20-40 MB/s), it's ~15-30 seconds. But your script transfers the tiny `convert_local.py`, not the checkpoint — the 600MB `ckpt.pt` already lives on `192.168.1.36`. So no network cost for the model.

**`torch.load` (600MB from disk):** ~2-5 seconds on SSD, longer on spinning disk or if memory-constrained.

**Conversion (key renaming, `.float().clone()`):** You're upcasting fp16→fp32, so the in-memory model doubles to ~1.2GB. Pure CPU tensor copies — ~1-3 seconds.

**Saving safetensors (~1.2GB fp32 output):** This is the real cost. fp32 doubles the on-disk size vs fp16. Writing ~500MB-1.2GB to `/tmp` (often tmpfs/RAM-backed) is ~3-10 seconds.

**Total: ~15-30 seconds of real work.**

Your `04m41s` elapsed time is misleading — that's wall-clock including SSH session setup, Python interpreter + torch import (torch import alone is 3-8s cold), and likely the terminal waiting/idle. The `weights_only=False` load also has pickle overhead.

If it's genuinely taking minutes on the conversion itself, the likely culprits:

- **Disk is slow** (HDD not SSD on the workstation) — check with `iostat -x 1`
- **`/tmp` is not tmpfs** and you're writing fp32 to a slow disk
- **Memory pressure** — 1.2GB fp32 model + torch overhead on a constrained box causes swapping

One optimization: skip the fp32 upcast unless you need it. HF GPT-2 runs fine in fp16/bf16, halving your write size:

```python
# instead of .float().clone(), keep bf16:
state_dict[k] = state_dict[k].to(torch.bfloat16).clone()
```

And set `"dtype": "bfloat16"` in config. That cuts safetensors write time roughly in half.

To actually measure where the time goes:

```bash
ssh lzw@192.168.1.36 "PYTHONUNBUFFERED=1 python3 -X importtime /tmp/convert_local.py 2>&1 | tail -20"
```

Or just wrap the phases:

```python
import time
t = time.time()
ckpt = torch.load(CKPT_PATH, map_location="cpu", weights_only=False)
print(f"load: {time.time()-t:.1f}s", flush=True)
```

Bottom line: a 124M/600MB conversion should be well under a minute of actual compute. If you're seeing 4-5 minutes, it's import + SSH + slow disk overhead, not the model size.
