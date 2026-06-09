---
audio: false
generated: true
image: false
lang: en
layout: post
title: Effects of MAX_JOBS=64 on Flash-Attention Build
translated: false
type: note
---

Question: What will happen if I set `MAX_JOBS=64` when compiling flash-attention on an AMD AI Developer Cloud MI300X instance?

Answer:

Setting `MAX_JOBS=64` increases the number of concurrent compilation tasks to 64. On your `snapshots-gpu-mi300x1-192gb-devcloud-atl1` instance, here’s what you can expect:

1. **CPU Saturation**:

   * The MI300X instance likely has fewer than 64 physical CPU cores (usually around 128 threads across 64 cores for the full MI300X system, but your snapshot might not expose all).
   * Setting `MAX_JOBS=64` can oversubscribe CPU threads. This may cause the OS scheduler to time-slice heavily between compilation jobs, reducing per-job efficiency.

2. **Memory Pressure**:

   * Each `hipcc` compilation process consumes RAM. With 32 jobs, you used ~32 GB RAM with 149 GB free. Doubling jobs may double RAM usage, possibly reaching 60–70 GB or more. Still safe for your 192 GB instance, but spikes may occur with large kernels.

3. **Disk I/O**:

   * Flash-attention generates many intermediate object files (`.o`). More jobs at once increase simultaneous disk writes, which can slow builds if the storage isn’t extremely fast.

4. **Diminishing Returns**:

   * You observed:

     * 16 jobs → ~48 objects/min
     * 32 jobs → ~93 objects/min (~2× speed-up, not 100% linear)
   * Going to 64 jobs may increase speed to ~120–130 objects/min, but you’re unlikely to double again due to CPU, memory, and I/O contention.

5. **Risk of Instability**:

   * Oversubscribing the build system may trigger occasional compiler failures (`FAILED`) due to temporary resource starvation or `hipcc` memory limits.
   * Monitoring `/tmp/flash_attn_build64.log` for errors will be essential.

6. **Practical Advice**:

   * If your goal is the fastest build, try 48 or 56 jobs first and monitor system load (`htop` or `nproc`) and memory usage.
   * Only push to 64 if CPU usage is not already near 100% and RAM usage is comfortably below ~150 GB.
   * Keep `GPU_ARCHS=gfx942` and ROCm paths unchanged—these are independent of `MAX_JOBS`.

**Summary:**

* You will likely get a modest speedup compared to 32 jobs, but not 2×.
* RAM and CPU usage will increase; disk I/O may become a bottleneck.
* Monitor for build failures; this is the main risk of `MAX_JOBS=64`.

---

If you want, I can calculate an **estimated object compilation rate and total build time** for `MAX_JOBS=64` based on your previous logs. This gives a more concrete expectation.
