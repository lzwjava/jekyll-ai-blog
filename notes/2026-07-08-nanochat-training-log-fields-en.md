---
audio: false
generated: true
image: false
lang: en
layout: post
title: NanoChat Training Log Fields
translated: false
type: note
---

Question: What do the fields in this nanochat training log line mean — `h: 1 pq: 0 rg: 278 | total time: 25.36m | eta: 1951.3m step 00383/29000 (1.32%) | loss: 3.369286 | lrm: 1.00 | dt: 4052.93ms | tok/sec: 129,360 | bf16_mfu: 62.46 | epoch: 1 pq: 0 rg: 279 | total time: 25.43m | eta: 1951.2m`?

Answer:

That's two consecutive `print0` lines from `base_train.py` glued together in your terminal — the leading `h: 1` is just the tail-end of `epoch: 1` from the *previous* line, truncated by terminal wrap. The actual format string, straight from `scripts/base_train.py`:

```python
epoch = f"{dataloader_state_dict['epoch']} pq: {dataloader_state_dict['pq_idx']} rg: {dataloader_state_dict['rg_idx']}"
print0(f"step {step:05d}/{num_iterations:05d} ({pct_done:.2f}%) "
       f"| loss: {debiased_smooth_loss:.6f} | lrm: {lrm:.2f} "
       f"| dt: {dt*1000:.2f}ms | tok/sec: {tok_per_sec:,} "
       f"| bf16_mfu: {mfu:.2f} | epoch: {epoch} "
       f"| total time: {total_training_time/60:.2f}m{eta_str}")
```

Field by field, using your line:

- **`step 00383/29000 (1.32%)`** — current optimizer step / total planned steps. `383/29000 = 1.32%` checks out.
- **`loss: 3.369286`** — `debiased_smooth_loss`, an EMA-smoothed cross-entropy loss with bias correction (Adam-style debiasing so early steps aren't artificially low). Not the raw per-step loss.
- **`lrm: 1.00`** — LR multiplier from the WSD (warmup-stable-decay) schedule, not the raw LR. At `1.00` you're in the flat "stable" phase, before the decay tail kicks in near the end of training.
- **`dt: 4052.93ms`** — wall-clock time for this step. On MI300X this includes the fwd+bwd+Muon/AdamW step.
- **`tok/sec: 129,360`** — throughput = `B*T*ddp_world_size/dt`. Back-solving: tokens/step ≈ `129360 * 4.05293 ≈ 524,350` tokens. If you're running depth=20 (`d=1280`) with `T=2048` and single-GPU (`ddp_world_size=1`), that implies `B ≈ 256`.
- **`bf16_mfu: 62.46`** — Model FLOPs Utilization: `100 * flops_per_sec / (gpu_peak_flops * ddp_world_size)`. Worth double-checking `get_peak_flops()` in `nanochat/common.py` — it hardcodes peak FLOPs tables per GPU (H100/A100/etc.), and I'd bet **MI300X isn't in that table**, meaning your 62.46% could be computed against a wrong/default peak-FLOPs constant. Grep for `get_peak_flops` and confirm it has an MI300X (CDNA3, ~1.3 PFLOPs bf16 dense) entry before trusting this number for real MFU comparisons.
- **`epoch: 1 pq: 0 rg: 279`** — dataloader resume state, not just "epoch number":
  - `epoch` — full passes over the shuffled shard set (`epoch=1` means first pass).
  - `pq_idx` — index of the current **parquet shard file** (each ~100MB / ~0.25M chars, per the FineWeb-EDU repackaging in `dev/repackage_data_reference.py`).
  - `rg_idx` — index of the current **row group** within that parquet file (`row_group_size = 1024` docs/group).
  This triple is exactly what `save_checkpoint` persists so a crashed/resumed run picks up mid-shard instead of restarting the epoch.
- **`total time: 25.43m`** and **`eta: 1951.2m`** — `total_training_time` only starts accumulating after step 10 (warmup steps excluded from the average), and `eta = (num_iterations - step) * avg_time_per_step`. Diff between the two lines: `25.43 - 25.36 = 0.07m ≈ 4.2s`, which matches `dt=4052.93ms` for the single step in between — so the loop is behaving consistently, no stalls.

One data-pipeline signal worth noting: `rg_idx` went `278 → 279` for one step — i.e. you're burning almost exactly one row group (1024 packed docs) per optimizer step at your current batch size. At `eta: 1951.2m` (~32.5 hours) for the full 29,000-step run, you'll cycle through a *lot* of row groups — worth confirming your local shard cache (`~/.cache/nanochat`) has enough shards downloaded that you're not going to stall on network I/O for parquet fetches mid-run on the AMD Dev Cloud box.

References:

- [nanochat/scripts/base_train.py](https://github.com/karpathy/nanochat/blob/master/scripts/base_train.py)
- [nanochat/nanochat/dataloader.py](https://github.com/karpathy/nanochat/blob/master/nanochat/dataloader.py)
- [nanochat/dev/repackage_data_reference.py](https://github.com/karpathy/nanochat/blob/master/dev/repackage_data_reference.py)
- [Introducing nanochat (Karpathy discussion #1)](https://github.com/karpathy/nanochat/discussions/1)
