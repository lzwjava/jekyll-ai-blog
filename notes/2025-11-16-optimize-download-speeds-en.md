---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Optimize Hugging Face Download Speeds
translated: false
type: note
---

Your current download is hitting Hugging Face's main endpoint (`huggingface.co`), which is hosted primarily in Europe/US data centers. Routing through your Taiwan proxy from Guangzhou adds similar latency issues as before: ~200–300ms round-trip, plus potential throttling on large files (this Parquet is ~500MB–1GB per shard). The 302 redirect you're seeing is likely to a CloudFront CDN edge, but it might not be the optimal one for Asia, leading to slowdowns (e.g., 1–5 MB/s).

To match the 20–60 MB/s speeds from the Wikimedia downloads, use these tweaks—prioritizing Asia-friendly options. All keep your Clash/TW proxy setup.

### 1. **Switch to HF Mirror (Fastest for China/Taiwan—Recommended)**
   HF Mirror (`hf-mirror.com`) is a community-run CDN optimized for East Asia (proxied through domestic CN networks like Tsinghua). It mirrors all HF datasets exactly, including FineWeb Parquet files. From TW proxy, expect 30–80 MB/s.

   Update your script:
   ```bash
   #!/bin/bash
   # wget_fineweb_1.sh (updated for speed)
   mkdir -p fineweb_test_dump
   cd fineweb_test_dump
   echo "Downloading FineWeb shard via HF Mirror (faster for Asia)..."

   # Replace huggingface.co with hf-mirror.com
   wget -c "https://hf-mirror.com/datasets/HuggingFaceFW/fineweb/resolve/main/data/CC-MAIN-2013-20/000_00000.parquet?download=true"

   echo "Done! Shard size: ~500MB–1GB"
   echo "For more shards, loop over e.g., 000_00001.parquet, etc."
   echo "To load in Python: from datasets import load_dataset; ds = load_dataset('HuggingFaceFW/fineweb', name='CC-MAIN-2013-20', split='train', streaming=True)"
   ```

   Run it: `./scripts/train/wget_fineweb_1.sh`
   - If the mirror lags (rare), fall back to the official: `https://huggingface.co/datasets/...` (but add the speed tip in #2).

### 2. **Boost with hf_transfer (For Any HF Download—100x Faster on Resumable)**
   Hugging Face's official Rust tool for parallel/multi-threaded downloads. It auto-retries, uses more connections, and hits >500 MB/s on good links. Works with `wget` indirectly or directly via Python (if your script uses `huggingface_hub`).

   Install (one-time, via pip—your env has it):
   ```bash
   pip install hf_transfer
   export HF_HUB_ENABLE_HF_TRANSFER=1
   ```

   Then re-run your original script. It accelerates the underlying `wget` calls to HF URLs.
   - Pro tip: For full dataset streaming (no full download), use Python in your pipeline:
     ```python
     from datasets import load_dataset
     import os
     os.environ['HF_HUB_ENABLE_HF_TRANSFER'] = '1'  # Enable before import
     ds = load_dataset("HuggingFaceFW/fineweb", name="CC-MAIN-2013-20", split="train", streaming=True)
     for example in ds.take(1000):  # Stream/process on-the-fly
         print(example)
     ```
     This pulls shards lazily via the mirror if you set `HF_ENDPOINT=https://hf-mirror.com`.

### 3. **Clash Rule Tweak (If Allowed—Ultra-Fast Domestic)**
   If your proxy config lets you bypass for HF (or route to HK/SG nodes), add a rule for `huggingface.co` / `hf-mirror.com` to go direct/domestic. In `clash.yaml`:
   ```
   rules:
     - DOMAIN-SUFFIX,hf-mirror.com,DIRECT  # Or your CN mirror node
     - DOMAIN-SUFFIX,huggingface.co,DIRECT
   ```
   Restart Clash, then download. Pairs with #1 for 50–100+ MB/s via Tsinghua mirrors.

### Why This Matches Wikimedia Speeds
- Wikimedia: Redirector auto-picked Asia (Japan/KR/SG) → low latency.
- HF: Default is EU/US → high latency; mirror + transfer flips it to Asia-optimized.

Test one shard first—if still slow, check `curl -I https://hf-mirror.com/...` for headers (should show Asia CDN). For the full 15T FineWeb, stream via `datasets` lib to avoid 100s of GB downloads. Hit me if speeds don't jump!
