---
audio: false
generated: true
image: false
lang: en
layout: post
title: Training Bottleneck Analysis
translated: false
type: note
---

Question: Why does each training iteration take ~21 seconds on an NVIDIA H200 GPU droplet with the given configuration?

Answer:

Training speed around **21 seconds per 1M-token batch** on an H200 (which has 141 GB memory and 24+ vCPUs) is far slower than expected. In typical benchmarks, an H200 can process thousands of samples per second – for example, 50 batches of 32 images (1,600 samples) ran in <1 s on an H200【23†L203-L205】 (≈19.6 ms per batch). The 21s per iteration we see indicates a **severe bottleneck** elsewhere. The primary culprits are likely the model compilation overhead and data pipeline, not raw GPU compute.

- **Compile & Warm‑up Overhead:** You enabled `torch.compile(True)`, so PyTorch’s Inductor compiler is fusing kernels. The first few iterations are much slower because Inductor is still tracing and compiling kernels. Indeed, the logs show a huge pause at iter 0 (compilation) and then slow steps for many iterations. According to NVIDIA/PyTorch sources, although most compilation happens at the first call, **“several additional warm-up passes are often required to reach peak performance”**【1†L169-L172】. In our case, those 24 background compile workers were still active deep into training, so the model wasn’t fully optimized yet. During this phase, even though the GPU reports 100% utilization and high power draw, it’s actually doing unoptimized work + compiling, so effective throughput is low. Once Inductor is done, step times should drop to ~1–2 sec on an H200 (a massive speedup).

- **Data Loading & Pipeline Bottleneck:** Another big issue is data I/O. The FineWeb data (10B tokens) appears to be streamed or loaded from text, not memory‑mapped binaries. Without multi-threaded loading, Python must read, tokenize, and batch on-the-fly. This can easily swamp the GPU. In fact, Hugging Face developers note that streaming FineWeb can be very slow and recommend using a `DataLoader` with `num_workers` and `prefetch_factor` to parallelize I/O【7†L50-L59】. A single-threaded loader will underutilize an H200 by starving it of data. The logs also show huge spikes when saving checkpoints (~60–90 s), suggesting I/O is a slow point. In practice, enabling `DataLoader(dataset, num_workers=4, prefetch_factor=2, pin_memory=True, batch_size=16)` (or whatever suits) can overlap loading and computation. Using the `prepare.py` step to convert raw text to `.bin` (memory‑mapped) would also speed things dramatically.

- **Other Factors:** Saving 18GB checkpoints took a minute or two (observed 84s at iter 250), which stalls the loop. Also, the “mfu 150%+” metric is an artifact of profiling – in reality you can’t exceed 100% GPU utilization. The fact we see 100% power (∼690W) means the GPU is busy – so the lag is not idle GPU but work (compilation + data feeding). Additionally, check if Python is using all CPU cores. If the droplet’s vCPUs are busy elsewhere (e.g. running other tasks or limited by Docker), that could delay data prep. Finally, ensure nothing like logging or console output is backpressuring the loop.

**Recommendations:**

- **Wait out the compile phase.** Monitor logs until step time drops from ~21s to a few seconds.
- **Add DataLoader workers:** Use `torch.utils.data.DataLoader` with multiple workers and a prefetch factor to speed data loading【7†L50-L59】.
- **Prepare data properly:** Convert FineWeb text to binary with `prepare.py` so the loader can `mmap` it. This avoids Python I/O overhead.
- **Pin memory:** Set `pin_memory=True` in DataLoader so that transfers to GPU can overlap with CPU data prep.
- **Profile CPU usage:** Use tools like `htop` or PyTorch’s profiler to see if Python is the bottleneck.
- **Reduce I/O during training:** Save checkpoints less frequently or to a faster storage (e.g. /dev/shm) to cut the ~80s save stalls.

In summary, **21 s/iter on an H200 indicates a data or compilation bottleneck, not the GPU’s compute limit.** By ensuring the model is fully compiled (warm-up) and the data pipeline is parallelized, step times should drop toward the sub-second range expected for this hardware【1†L169-L172】【23†L203-L205】.

References:

- TorchInductor (PyTorch 2.0+) compilation and warm-up behavior【1†L169-L172】【1†L184-L189】 (initial slowdown, then peak throughput).
- Hugging Face forum on FineWeb streaming: use `DataLoader`, multiple workers, prefetch to avoid slow I/O【7†L50-L59】.
- NVIDIA H200 performance example (50 batches of 32 in ~0.98 s)【23†L203-L205】 (illustrates expected GPU throughput).
