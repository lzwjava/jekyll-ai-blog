---
audio: false
generated: true
image: false
lang: en
layout: post
title: Slow Upload Fix Recommendations
translated: false
type: note
---

Here's the smoke test results:

```
config.json (831B)  →  1.7s  ✓
tokenizer.json (3.4MB) → 17.9s  ≈ 190 KB/s
```

**190 KB/s throughput from your current connection.** At that rate:

```
model.safetensors (475MB) → estimated ~42 minutes
```

And it will likely stall mid-transfer (like you saw with GCS).

**Recommendations (ranked):**

1. **hf-mirror.com** — China-optimized HuggingFace mirror. Try:
   ```
   HF_ENDPOINT=https://hf-mirror.com hf upload lzwjava/sec-edgar-gpt-124m model.safetensors model.safetensors
   ```

2. **DMIT proxy (LA)** — route through your hysteria2 proxy. The `hf` CLI respects `https_proxy`:
   ```
   https_proxy=http://127.0.0.1:<hysteria-port> hf upload lzwjava/sec-edgar-gpt-124m model.safetensors model.safetensors
   ```

3. **AMD Dev Cloud relay** — rsync to Atlanta, upload from there (US→HF is fast)

Want me to try option 1 (hf-mirror) or option 2 (DMIT proxy) as the actual upload? Or just kick off the 475MB upload on current connection and hope it doesn't stall?
