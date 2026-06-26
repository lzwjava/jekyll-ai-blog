---
audio: false
generated: true
image: false
lang: en
layout: post
title: Upload Pipeline Almost Complete
translated: false
type: note
---

## Current Status

### The Model
- **Workstation** (`lzw@192.168.1.36`): 47k-step checkpoint converted to HF format at `/tmp/sec-edgar-gpt-124m-hf/` (652MB)
- **RunPod**: Running the old 20k-step model → garbage output

### Upload Pipeline (in progress)
```
Workstation → SCP → Relay (47.86.12.246) → HuggingFace Hub
```
- Background SCP running now: 652MB model.safetensors from workstation → relay
- Relay has 31GB free disk, can reach HuggingFace
- Small files (config, tokenizer) still need uploading too

### After Upload Completes
1. Install `huggingface-hub` on relay
2. Upload all files to `lzwjava/sec-edgar-gpt-124m`
3. On RunPod: `huggingface-cli download lzwjava/sec-edgar-gpt-124m --local-dir /workspace/model/hf-model`
4. Restart server.py

### What You'll See
```
Before (20k steps): "ivableivableignedignedivable..."
After  (47k steps): "The Company has a $2.2 million revolving credit facility..."
```

Waiting for the SCP to finish — I'll continue as soon as it completes.
