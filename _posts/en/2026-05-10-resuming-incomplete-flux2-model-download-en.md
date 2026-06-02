---
audio: false
generated: true
image: false
lang: en
layout: post
title: Resuming Incomplete Flux.2 Model Download
translated: false
type: note
---

Here's the status:                                                                                                              │
│                                                                                                                                             │
│             **What's done:**                                                                                                                │
│             1. Created a Python 3.12 venv at /home/lzw/projects/flux2/.venv                                                                 │
│             2. Installed all dependencies (torch 2.8+cu129, transformers, safetensors, etc.)                                                │
│             3. Detected your GPU: RTX 4070 with 12GB VRAM -- perfect for FLUX.2 [klein] 4B                                                  │
│             4. First download attempt from huggingface.co was crawling at ~54 KB/s                                                          │
│             5. Switched to hf-mirror.com (HF_ENDPOINT=https://hf-mirror.com) -- got ~30 MB/s                                                │
│             6. The smaller safetensors file (778MB) finished downloading                                                                    │
│             7. The large safetensors file (4.41GB) was at ~74% and still downloading when I hit the iteration limit                         │
│                                                                                                                                             │
│             **Current state:**                                                                                                              │
│             The background download process (proc_567395c17054) is likely still running and downloading the remaining ~1.1GB of the 4.41GB  │
│ model file. After that, it will also need to download the text encoder (Mistral-Small-3.2-24B-Instruct-2506) and the autoencoder            │
│ (ae.safetensors), which are additional downloads.                                                                                           │
│                                                                                                                                             │
│             **To finish what I started, run this yourself:**                                                                                │
│             ```bash                                                                                                                         │
│             cd /home/lzw/projects/flux2                                                                                                     │
│             HF_ENDPOINT=https://hf-mirror.com .venv/bin/python scripts/cli.py                                                               │
│             ```                                                                                                                             │
│             Then pick option 1 (flux.2-klein-4b) when prompted. The partially downloaded model files will resume from cache. Once all       │
│ weights are downloaded, you'll get an interactive prompt where you can type any text prompt to generate images.                             │
│                                                                                                                                             │
│             **Key note:** The `HF_ENDPOINT=https://hf-mirror.com` flag is critical -- without it, downloads from huggingface.co are nearly  │
│ unusable from your network (~50 KB/s). With the mirror, you get ~30 MB/s.
