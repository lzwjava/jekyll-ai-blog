---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fastest upload paths for China
translated: false
type: note
---

Here's the situation and options:

**Model:** 475MB model.safetensors + 3.4MB tokenizer = ~478MB total. Target: `lzwjava/sec-edgar-gpt-124m` on HuggingFace.

**Why it's slow from China:** HuggingFace CDN (Cloudflare) is throttled/blocked by some Chinese ISPs. Upload stalls mid-transfer. GCS to HF direct transfer also requires fast US-EU connectivity.

**Ranked options (best → worst):**

**Option 1: AMD Dev Cloud (Atlanta) as relay — FASTEST**
You have `ssh amd-cloud` (MI300X in Atlanta). US→HuggingFace is fast. Two sub-options:

  a) Rsync files from Mac to AMD, then upload to HF from AMD
  b) Download from GCS on AMD, then upload to HF

**Option 2: hf-mirror.com — China-friendly**
HuggingFace's official China mirror. `huggingface-cli` can be configured to use it.

**Option 3: Your DMIT proxy (LA)**
Route `huggingface-cli upload` through hysteria2/DMIT proxy via LA. US-located proxy should be fast to HF.

Let me try the fastest: upload directly from Mac using your DMIT proxy, since you already have it running:
