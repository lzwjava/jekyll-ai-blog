---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Fix OOM Killer in FineWeb Script
translated: false
type: note
---

The "Killed" message without any Python traceback means the Linux OOM (Out-of-Memory) killer terminated the process. This happens in the `data/fineweb/prepare.py` script because it tries to load your entire ~15 GB concatenated text file (`train_fineweb.txt`) into RAM at once with something like `open(...).read()` before tokenizing.

Even though FineWeb-Edu is designed for streaming (the official downloader uses Hugging Face `datasets` and processes shard-by-shard in ~100M token chunks without ever loading everything into memory), the nanoGPT fineweb folder has a custom local-file path that is not memory-efficient for large files.

### Quick Fixes (pick one)

1. **Best & Recommended: Use the official streaming FineWeb-Edu downloader instead of your local files**
   Don't use the nanoGPT `data/fineweb/prepare.py` at all.
   Use Karpathy's newer script made exactly for FineWeb-Edu 10B tokens (or larger):

   ```bash
   # From the nanoGPT root (or anywhere)
   wget https://raw.githubusercontent.com/karpathy/build-nanogpt/master/fineweb.py
   python fineweb.py
   ```

   This downloads and tokenizes FineWeb-Edu sample-10BT (10 billion tokens, ~15-20 GB raw) in streaming fashion using `datasets.load_dataset(..., streaming=True)` and multiprocessing. It never loads the full dataset into RAM and produces the exact same `.bin` shards nanoGPT expects in a folder like `edu_fineweb10B/`.
   It runs fine on machines with 32-64 GB RAM (or even less if you reduce `num_proc_load_dataset` and `num_proc` in the script).

   For the full 100B or 1T versions, just change `remote_name = "sample-10BT"` to `"100BT"` or whatever you need.

2. **If you really want to keep your 10 local parquet → txt file**
   Modify `data/fineweb/prepare.py` to process the text in chunks instead of loading it all:

   Open the script and replace the big `with open(local_file, 'r', encoding='utf-8') as f: data = f.read()` block with something like this:

   ```python
   from tqdm import tqdm
   import tiktoken
   enc = tiktoken.get_encoding("gpt2")

   chunk_size = 1_000_000  # characters per chunk, adjust if needed
   tokens = []
   with open(local_file, "r", encoding="utf-8") as f:
       while True:
           chunk = f.read(chunk_size)
           if not chunk:
               break
           tokens.extend(enc.encode_ordinary(chunk))  # or enc.encode(chunk)
           print(f"Tokenized so far: {len(tokens)/1e6:.1f}M tokens")
   tokens = np.array(tokens, dtype=np.uint16)
   ```

   This keeps peak RAM under ~10-15 GB even for your 15 GB file.

3. **Hardware workarounds (temporary, not ideal)**
   - Add a lot of swap (e.g., 64-128 GB swap file). It will be extremely slow once it starts swapping, but it may finish.
     ```bash
     sudo fallocate -l 64G /swapfile
     sudo chmod 600 /swapfile
     sudo mkswap /swapfile
     sudo swapon /swapfile
     ```
   - Run on a machine/instance with ≥64 GB RAM (e.g., AWS r6i.4xlarge or bigger).

### Summary
Just run the official `fineweb.py` from build-nanogpt — it's the cleanest solution and what everyone uses for FineWeb now. Your concatenated 15 GB txt file is the problem, not FineWeb itself.

[Official FineWeb-Edu downloader script](https://raw.githubusercontent.com/karpathy/build-nanogpt/master/fineweb.py)
[FineWeb-Edu dataset page](https://huggingface.co/datasets/HuggingFaceFW/fineweb-edu)
