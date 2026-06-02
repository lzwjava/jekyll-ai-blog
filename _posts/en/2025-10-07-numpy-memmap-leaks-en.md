---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Fixing NumPy memmap Memory Leaks
translated: false
type: note
---

### What the Stack Overflow Post Says

The post discusses a common issue with NumPy's `np.memmap` when processing large datasets stored on disk. The original question describes iterating over a huge matrix (e.g., via shuffled indices) to read rows in chunks, but noticing that RAM and virtual memory usage steadily increases during the process, slowing down the system—even though each row is accessed only once. The asker wants to cap memory usage to just the current chunk and asks for alternatives like a generator-based iteration or direct file I/O (noting the latter is slower).

The linked answer (ID 61472122, accepted) pinpoints the "memory leak" as NumPy's memmap retaining the entire array in memory for caching, despite the read-only mode and single-pass access. It proposes two solutions:

1. **Recreate the memmap object per chunk**: Delete and reinitialize `np.memmap` for each batch or chunk. This prevents the full array from building up in RAM, keeping usage low (tied to chunk size). There's minor CPU overhead from recreation, but it's negligible. Example code:
   ```python:disable-run
   def process_chunks(data_filename, chunk_size=4096):
       for start in range(0, total_size, chunk_size):
           # Recreate memmap fresh each time
           data = np.memmap(data_filename, dtype=np.float32, mode='r', shape=full_shape)
           # Process only the current chunk
           chunk = data[start:start + chunk_size]
           # ... do work ...
           del data  # Explicitly discard
   ```

2. **Custom mmap with OS memory advice**: Access the underlying `mmap` object in the memmap and use Python 3.8+'s `madvise` (e.g., `MADV_DONTNEED` or `MADV_DONTDUMP`) to tell the OS to release unused pages. This is more low-level but avoids recreation overhead. It includes code snippets from NumPy's source for accessing the mmap.

The answer recommends profiling tools like `memory-profiler` to verify fixes.

### Why NanoGPT Uses This Approach

In the provided code from NanoGPT (a minimal GPT implementation for language model training), the recreation of `np.memmap` inside the `get_batch` function follows the first solution from that answer exactly—to sidestep the memory leak during repeated batch sampling from massive binary files (e.g., tokenized training data).

NanoGPT trains on huge datasets (like billions of tokens), so loading the full file into memory isn't feasible. Instead, it uses memmap for efficient disk access, but without recreation, memory would balloon over epochs as NumPy caches more and more of the file. By remapping fresh each batch (via the `if split == 'train': data = np.memmap(...)` lines), it ensures low, stable RAM usage—critical for long training runs on limited hardware like a single GPU. The comment explicitly credits the SO post for this "memory leak avoidance" trick. This keeps the data loader lightweight while enabling random sampling (`torch.randint`) for x/y input-target pairs.

[Stack Overflow: numpy memmap memory usage - want to iterate once](https://stackoverflow.com/questions/45132940/numpy-memmap-memory-usage-want-to-iterate-once/61472122#61472122)
```
