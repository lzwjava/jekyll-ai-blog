---
audio: false
generated: true
image: false
lang: en
layout: post
title: China Upload Bottleneck Analysis
translated: false
type: note
---

Test file cleaned up. Here's the summary:

```
Smoke test results (China → HuggingFace):

  Direct:        ~190 KB/s (3.4MB in 17.9s)
  Via proxy 7890: ~157 KB/s (10MB in 65s, with long stalls)

  475MB estimated: ~42-50 minutes, likely to stall mid-transfer
```

**Both routes are equally slow** — the bottleneck is China's international bandwidth, not the routing path. Proxy doesn't help.

**Your real options for model.safetensors:**

1. **Just run it overnight** — direct upload, no proxy needed. It'll be slow but if it doesn't stall, ~50 min. `hf upload` does support resumable behavior for large files (multipart upload). If it stalls, rerun the same command — it picks up where it left off:
   ```
   cd ~/projects/sec-edgar-gpt-124m
   hf upload lzwjava/sec-edgar-gpt-124m model.safetensors model.safetensors
   ```

2. **AMD Dev Cloud** — but uploading 475MB from China→Atlanta (scp) faces the same wall. Only worth it if you can get the file there via GCS (which is also stuck).

3. **Workstation (192.168.1.36)** — also in China, same problem. Timed out on SSH.

**Bottom line:** Option 1 is your best bet. Kick it off before bed, let it grind through. If it stalls, rerun — `hf upload` re-uploads the file. Want me to start it in background?
