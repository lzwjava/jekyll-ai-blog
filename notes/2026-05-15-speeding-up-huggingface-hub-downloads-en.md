---
audio: false
generated: true
image: false
lang: en
layout: post
title: Speeding up HuggingFace Hub Downloads
translated: false
type: note
---

The slowness is HuggingFace Hub's default single-stream download from their CDN — nothing wrong with your setup. A few options to speed it up:

**1. Use `hf_transfer` (parallel chunks, usually 5–10× faster):**
```
pip install hf_transfer
HF_HUB_ENABLE_HF_TRANSFER=1 python3.11 sample.py --init_from=gpt2-medium ...
```

**2. Pre-download once with the CLI, then sample.py uses the cache:**
```
huggingface-cli download gpt2-medium
```

**3. If you're in a region where huggingface.co is slow (e.g., China), use the mirror:**
```
HF_ENDPOINT=https://hf-mirror.com python3.11 sample.py --init_from=gpt2-medium ...
```

The file lives in `~/.cache/huggingface/hub/` after the first download, so subsequent runs won't re-download. Which region are you in? That'll tell us if the mirror is worth trying.