---
audio: false
generated: true
image: false
lang: en
layout: post
title: Upload large model file options
translated: false
type: note
---

Done. Here's the status:

```
Uploaded ✓
  config.json (831B)
  generation_config.json (202B)
  tokenizer_config.json (286B)
  tokenizer.json (3.4MB)
  README.md (2.1KB)
  .gitattributes (50B)

Still pending — upload yourself:
  model.safetensors (475MB)
```

Your repo: https://huggingface.co/lzwjava/sec-edgar-gpt-124m

For `model.safetensors`, pick your fastest path:

```
# Option 1: hf-mirror.com (China-optimized)
HF_ENDPOINT=https://hf-mirror.com hf upload lzwjava/sec-edgar-gpt-124m model.safetensors model.safetensors

# Option 2: via DMIT proxy
https_proxy=http://127.0.0.1:<port> hf upload lzwjava/sec-edgar-gpt-124m model.safetensors model.safetensors

# Option 3: upload to AMD Dev Cloud, upload from there
scp model.safetensors amd-cloud:~/
ssh amd-cloud 'hf upload lzwjava/sec-edgar-gpt-124m ~/model.safetensors model.safetensors'
```
