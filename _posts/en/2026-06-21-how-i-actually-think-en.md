---
audio: false
generated: true
image: false
lang: en
layout: post
title: How I Actually Think
translated: false
type: note
---

**Question:** How do you think? (Asking about my reasoning/thinking process)

**Answer:**

Honestly, the summary you shared is a better answer to this than anything I could say abstractly — so let me reflect on what your debugging process already demonstrates, then add what I actually do.

---

## What Your Debugging Shows (and What It Names)

Your postmortem is a textbook example of **systems thinking from first principles**:

1. **Symptom → mechanism → root cause** — you didn't stop at "the machine crashed." You traced TCP handshake failure → sshd starvation → OOM → why OOM (Python list int overhead × 16 workers × file size). That's 4 layers deep.

2. **Back-of-envelope math before touching code** — `369M tokens × 28 bytes/int × 16 workers ≈ 160 GB` on a 62 GB machine. That single calculation explains everything. Most engineers skip this.

3. **Identify the real bottleneck** — "no benefit from parallelism when the bottleneck is memory, not CPU." This is Amdahl's Law applied correctly. Parallelism only helps the constrained resource.

4. **Solution matches the constraint** — streaming reads → constant memory footprint. Numpy uint16 → 56× smaller than Python int. Pre-allocated buffer → no GC pressure.

---

## How I Actually Think

**Decomposition first.** Break the problem into its smallest independent parts. For your case: (a) why did SSH fail, (b) why did the process OOM, (c) why did imap hang silently. Three independent threads.

**Work backward from invariants.** What *must* be true? Memory used ≤ available memory. That invariant was violated — find where.

**Quantify before diagnosing.** "A lot of memory" is useless. "369M × 28 bytes × 16 = 165 GB on a 62 GB machine" is actionable.

**Silent failure modes are the hardest bugs.** `pool.imap()` hanging with no error is worse than a crash. I try to always ask: *what does this look like when it fails silently?* Add timeouts, heartbeats, or progress output before you need them.

**Fix at the right abstraction layer.** You didn't tune GC or add swap. You eliminated the root allocation pattern entirely — streaming instead of bulk load, numpy instead of Python lists. That's the right layer.

---

## The Meta-Principle

Your fix reduced peak RAM from ~160 GB to ~600 MB — a **270× reduction** — without sacrificing throughput (5.7M tok/s is solid). That's only possible if you understood *why* the original was expensive, not just *that* it was expensive.

That's the difference between fixing symptoms and fixing causes. Your postmortem shows you already think this way. The next level is doing it *before* the crash — mentally running the workload at scale before submitting it. You almost had it: the script probably looked fine for small files.

**Pre-flight checklist for memory-intensive jobs:**

```python
# Before submitting any batch job, estimate peak memory:
rows_per_file = 4_000_000       # check with pq.read_metadata()
files_in_flight = num_workers
bytes_per_token_python = 28     # sys.getsizeof(int())
tokens_per_row = 90             # estimate

peak_gb = rows_per_file * files_in_flight * bytes_per_token_python * tokens_per_row / 1e9
print(f"Estimated peak RAM: {peak_gb:.1f} GB")
# If > 0.5 * available_ram: redesign before running
```

Run this before every new tokenization/ETL script. It takes 30 seconds and prevents a reboot.
