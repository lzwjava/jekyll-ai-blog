---
audio: false
generated: true
image: false
lang: en
layout: post
title: Per-Step Logging Impact on Training
translated: false
type: note
---

**Question:** In nanochat, does the per-step logging (the `step ... | loss ... | tok/sec ...` print) slow down or otherwise affect training?

**Answer:**

Short version: it does not affect training dynamics at all (loss, gradients, convergence are untouched — logging is read-only), and its throughput cost is ~0.01–0.1% per step. At your `dt ≈ 1170ms`, it's noise.

Break down what that log line actually costs, from the code in `scripts/base_train.py`:

**1. The `print` itself: microseconds.** Writing ~150 chars to a buffered stdout is ~10–50µs. Against a 1170ms step, that's 0.003%. (Caveat: if stdout is a blocking slow pipe — e.g. an ssh session with a laggy terminal, or `tee` to NFS — prints can block. Redirect to a local file if paranoid: `python -m scripts.base_train > train.log 2>&1`.)

**2. `loss.item()` / the EMA bookkeeping: one GPU→CPU sync per step.** This is the only "real" cost. `.item()` forces the CPU to wait for the GPU to finish the step before reading the scalar back. But nanochat already does this deliberately — it defines `synchronize = torch.cuda.synchronize` and syncs each step to get an accurate `dt` for the timing/MFU math. The cost of a sync isn't the sync itself (~µs); it's the lost ability to overlap CPU work (next-batch prep, optimizer host-side logic) with the GPU. With a prefetching dataloader and 1.17s steps, this overlap loss is well under 1ms/step.

**3. wandb logging:** buffered and async, negligible. With `--run dummy` it's a `DummyWandb()` no-op anyway.

What *does* eat wall-clock time (but still doesn't change training dynamics) are the periodic heavyweight operations, not the per-step print: val bpb eval every 250 steps, CORE metric every 2000 steps, sampling every 2000 steps, and checkpoint saves. Those pause training for seconds-to-minutes each time. If you want a faster run on your hardware, that's where to cut (`--eval-every -1 --core-metric-every -1 --sample-every -1`), not the logging.

If you want to verify empirically, gate the log and A/B it:

```python
# in the training loop
LOG_EVERY = 10
if step % LOG_EVERY == 0 and master_process:
    lossf = smooth_train_loss  # already computed
    print0(f"step {step:05d} | loss: {lossf:.6f} | dt: {dt*1000:.2f}ms | tok/sec: {tok_per_sec:,}")
```

Run 200 steps with `LOG_EVERY=1` vs `LOG_EVERY=10000` and compare mean `dt`. You'll see they're statistically indistinguishable. (One thing to *avoid* if you ever modify the loop: calling `.item()` on intermediate tensors *inside* the gradient-accumulation micro-step loop — that inserts a sync per micro-batch and can genuinely hurt when steps are short.)

Side note on your log: `bf16_mfu: 0.00` means `get_peak_flops()` didn't recognize your GPU's name, so `gpu_peak_flops` falls back to something that zeroes out the MFU calculation — on CPU/MPS it's explicitly set to `float('inf')` because "MFU not meaningful", and unknown CUDA devices hit a similar path. The lookup table is tuned for H100/A100-class names; on your MI300X (ROCm reports a different device name string) or RTX 4070 you'd need to add an entry in `nanochat/common.py:get_peak_flops` with your card's peak BF16 FLOPS (MI300X: ~1307 TFLOPS dense BF16; RTX 4070: ~29 TFLOPS BF16 non-sparse) to get a real MFU number. The `pq`/`rg` fields in your log (prefetch queue / ragged batch stats from the dataloader) aren't in current master's format string, so you're on a fork or different commit — same conclusion applies though.

**References:**

- [nanochat scripts/base_train.py](https://github.com/karpathy/nanochat/blob/master/scripts/base_train.py)
- [nanochat run1000.sh — reference step timings on 8×H100](https://github.com/karpathy/nanochat/blob/master/run1000.sh)
- [DeepWiki: nanochat base pretraining — MFU formula and logged metrics](https://deepwiki.com/karpathy/nanochat/3-base-model-pretraining)
