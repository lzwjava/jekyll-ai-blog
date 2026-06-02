---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: CPU vs GPU Training Performance
translated: false
type: note
---

The low MFU (0.01%) during NanoGPT training on your laptop stems from the `--device=cpu` flag in your command, which forces the entire workload onto the CPU rather than leveraging any GPU acceleration. Here's a breakdown of why this happens and how it compares to your 4070 Ti setup:

### Key Reasons for Low MFU on Laptop

- **CPU vs. GPU Architecture Mismatch**: Transformers like the one in NanoGPT (even this tiny config: 4 layers, 128 embed dim, batch size 12) are heavily parallelizable matrix operations (e.g., attention, FFNs) that GPUs excel at via thousands of cores and high-bandwidth memory. CPUs, even modern laptop ones (yours is likely an Intel Alder Lake-P series based on the kernel/platform info), handle these sequentially or with limited parallelism. PyTorch on CPU uses optimized BLAS (e.g., OpenBLAS) but still achieves <1% of GPU FLOPs throughput for such models. MFU measures *utilization relative to theoretical peak FLOPs*, so CPU-bound runs naturally report tiny values like 0.01%—it's not "broken," just inefficient for this task.

- **No GPU Offload Here**: Your laptop's hardware (Intel UHD Graphics from Alder Lake-P) isn't CUDA-compatible, so PyTorch defaults to CPU without tweaks. The `get_gpu_info.py` output shows an integrated Intel iGPU mislabeled as "AMD" (likely a script bug in parsing `lspci`), but even if it were usable, standard PyTorch doesn't accelerate training on Intel/AMD iGPUs out-of-the-box. You'd need extras like Intel's oneAPI (via `torch.backends.mps` or extensions) or ROCm for AMD, but that's experimental and won't match NVIDIA perf.

- **Model/Workload Scale**: This is a micro-model on a small dataset (Shakespeare chars, block_size=64). On CPU, overhead from data loading, Python loops, and non-FLOP ops dominates, dragging MFU down further. Your max_iters=2000 and log_interval=1 mean frequent checkpoints/evals, amplifying CPU bottlenecks.

### Comparison to 4070 Ti (10% MFU)

- **Hardware Throughput Gap**: A 4070 Ti (RTX 40-series, ~29 TFLOPs FP16) can crunch this model at 10-20x the speed of a laptop CPU (~0.5-1 TFLOPs effective for ML). 10% MFU is solid for NanoGPT on a small model—it's not 100% because of kernel launch overhead, memory bandwidth limits, and non-ideal batch sizes. Scaling batch_size higher (e.g., 128+) or using FP16/bfloat16 could push it to 15-20%, but your config is conservative.

- **Implicit GPU Mode**: On the 4070 Ti setup, you're likely running with `--device=cuda` (default in NanoGPT if available), enabling full tensor parallelism and cuBLAS/cuDNN kernels. This alone boosts MFU by optimizing for the hardware.

| Aspect | Laptop (CPU) | 4070 Ti (GPU) |
|--------|--------------|---------------|
| **Device** | CPU (forced) | CUDA GPU |
| **Peak FLOPs** | ~0.5-1 TFLOPs (ML-tuned) | ~29 TFLOPs (FP16) |
| **MFU Achieved** | 0.01% (CPU overhead dominates) | 10% (parallelism shines) |
| **Train Time Estimate (2000 iters)** | 10-30+ mins (slow I/O) | <1 min (blazing) |
| **Bottlenecks** | Serial execution, RAM limits | Memory bandwidth, kernel efficiency |

### Quick Fixes to Improve Laptop Training

- **Switch to GPU if Possible**: If you have access to the 4070 Ti remotely (e.g., via SSH + `torchrun`), just run there. For local Intel iGPU, try:

  ```
  pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu  # Ensure CPU fallback
  # Or for Intel oneAPI (experimental):
  conda install intel-extension-for-pytorch -c intel
  ```

  Then test `--device=cuda` (it'll error) or use `device='xpu'` with IPEX enabled. Expect 1-5% MFU at best—still not great.

- **Optimize CPU Run**:
  - Increase `batch_size` to 24-48 if RAM allows (your Ubuntu 24.04 setup has plenty with glibc2.39).
  - Add `--compile=True` (PyTorch 2.0+ dynamo for CPU speedups, ~20-50% faster).
  - Use `num_workers=4` in dataloader for I/O parallelism.
  - Run with `taskset -c 0-7` to pin to performance cores (check with `lscpu`).

- **Benchmark It**: Rerun with `--device=cuda` on the 4070 Ti machine for a direct apples-to-apples (should hit ~10% MFU). If you share the exact NanoGPT repo/version, I can suggest config tweaks.

This is expected behavior—CPUs aren't for prod ML training. If it's still off, paste the full train log for deeper debugging!
