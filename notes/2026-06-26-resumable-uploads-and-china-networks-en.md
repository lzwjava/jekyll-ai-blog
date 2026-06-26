---
audio: false
generated: true
image: false
lang: en
layout: post
title: Resumable Uploads and China Networks
translated: false
type: note
---

Two different issues here:

**1. `hf upload` — resumable? Yes, partially.**

`hf upload-large-folder` is explicitly designed for resumable uploads (it uses a local cache to track progress). For a single 475MB file, `hf upload` internally uses multipart upload via `huggingface_hub` — but if it stalls, it doesn't cleanly resume from where it left off on retry.

**2. Why SCP also stalls — this is a China network issue, not a tool issue.**

SCP is a single long-lived TCP stream. China's GFW + ISP traffic shaping (especially China Telecom) aggressively throttles long-lived international connections. The connection doesn't "fail" — it just slows to near-zero and eventually times out. Both SCP and `hf upload` hit the same wall: **sustained international bandwidth is rate-limited.**

**The real solution: use a resumable protocol + a good route.**

rsync with resume is better than SCP:
```
rsync -avz --progress --partial model.safetensors amd-cloud:~/
```
`--partial` keeps partially transferred files so it resumes on retry. But even rsync will be slow through the same pipe.

**What actually works from China:**

1. **hf-mirror.com** — China-optimized HF endpoint, designed for this exact problem:
   ```
   HF_ENDPOINT=https://hf-mirror.com hf upload lzwjava/sec-edgar-gpt-124m model.safetensors model.safetensors
   ```

2. **DMIT proxy (LA)** — your hysteria2 proxy has better international routing than raw China Telecom:
   ```
   https_proxy=http://127.0.0.1:<port> hf upload lzwjava/sec-edgar-gpt-124m model.safetensors model.safetensors
   ```

3. **GCS → HF** — you already uploaded to GCS. From a US machine (AMD Dev Cloud), pull from GCS and push to HF. Both are US-based, so it's fast:
   ```
   # on AMD Dev Cloud
   gsutil cp gs://lzwjava1/sec-edgar-gpt-124m/model.safetensors .
   hf upload lzwjava/sec-edgar-gpt-124m model.safetensors model.safetensors
   ```

Want me to try option 1 (hf-mirror) right now?
