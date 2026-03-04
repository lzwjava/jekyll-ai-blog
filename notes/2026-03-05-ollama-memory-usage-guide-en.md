---
audio: false
generated: true
image: false
lang: en
layout: post
title: Ollama Memory Usage Explained
translated: false
type: note
---

Question: Why does `ollama run qwen3.5:9b` show only 159 MB memory usage, which seems very small?

Answer: 

**The 159 MB figure you're seeing is not the actual memory used by the model — it's likely just the resident memory (RES) of the main Ollama server process itself, or a misleading partial reading from a tool like Activity Monitor / `top` / `htop` that doesn't account for how modern LLM runners handle memory.**

On Apple Silicon Macs (M2/M3), Ollama uses **memory-mapped files** and **unified memory** very efficiently. This means:

- The ~6.6 GB quantized model file (Q4_K_M for qwen3.5:9b) is mapped directly from disk into memory.
- The OS treats most of this as **file-backed memory** (cached / inactive / compressed), so it often doesn't show up fully in "App Memory" or simple process RES columns.
- When you actually send a prompt and inference starts, the real usage jumps — typically to **~8–12 GB total system memory** (including KV cache, overhead, and context).
- Tools like Activity Monitor frequently under-report this initially because the memory is "shared" / "compressed" or shown under "Cached Files" instead of the Ollama process directly.
- The Ollama server process stays small (~100–300 MB) when idle or just holding the API open; the heavy lifting happens in GPU-accelerated Metal buffers or shared memory pools that macOS doesn't always attribute clearly to one process.

### Typical Real Memory Usage for qwen3.5:9b on Mac M2/M3 (March 2026)
- Model file on disk: **6.6 GB**
- Loaded + short context inference: **~8–10 GB** unified memory used (most on GPU side via Metal)
- With longer context (e.g. 8k–16k tokens): **10–14 GB** depending on exact setup
- On a 16 GB Mac: Runs comfortably, but leaves less headroom for other apps
- On 24 GB+ Mac: Feels very smooth, often 40–70+ tokens/second

### Why It Looks So Small at First
- Before any prompt: Model may not be fully loaded yet (Ollama lazy-loads or unloads after inactivity to save resources).
- `ps`, `top`, or Activity Monitor's "Memory" tab for the `ollama` process often shows only **~150–300 MB** because the bulk is in:
  - Metal GPU buffers (not always listed per-process)
  - mmap'd model weights (counted as file cache)
  - Compressed / swapped memory
- Run `ollama ps` after starting inference — it shows a more accurate "SIZE" column (often 8–12 GB for this model).
- Use Activity Monitor → Memory tab → look at "Memory Used" total system increase, or enable "GPU" view to see Metal usage spike.

In short: **159 MB is normal for the idle server process**. The model is actually using several GB when active — that's expected and efficient on Apple Silicon. If you're seeing poor performance or errors, check total system memory pressure instead of just the process size.

References:  
- [Ollama qwen3.5:9b model page (6.6 GB Q4_K_M)](https://ollama.com/library/qwen3.5:9b)
- [Stack Overflow: Why doesn't Ollama use MORE RAM? (memory mapping explanation)](https://stackoverflow.com/questions/78068285/why-doesnt-ollama-use-more-ram)
- [GitHub Ollama issues on memory reporting (file cache & under-reporting)](https://github.com/ollama/ollama/issues/2496)
- [Local LLM guides on Apple Silicon unified memory behavior](https://localllm.in/blog/ollama-vram-requirements-for-local-llms)