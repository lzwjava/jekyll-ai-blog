---
audio: false
generated: true
image: false
lang: en
layout: post
model: openai/gpt-5
title: Fixing Slow Hugging Face Downloads
translated: false
type: note
---

This is a common issue when downloading huge HF datasets through a proxy. The combination of:

* Many multi-hundred-MB files
* Python `requests` / `huggingface_hub`
* A local HTTP proxy (especially Clash, V2Ray, or tun2socks)

often results in extremely slow throughput or connection resets.

Below are the most useful fixes.

---

## 1. **Best Fix: Use `hf_transfer`**

Hugging Face has an accelerated downloader that gives **10×–50× faster** speeds and is more stable.

Install:

```bash
pip install hf_transfer
export HF_HUB_ENABLE_HF_TRANSFER=1
```

Run your command again.

This alone usually fixes slow downloads through proxies.

---

## 2. Use `aria2c` with Hugging Face CLI (fastest for huge files)

If you download manually:

```bash
pip install huggingface_hub[cli]
sudo apt install aria2
```

Then download:

```bash
huggingface-cli download --repo-type dataset openwebtext --local-dir ./openwebtext --local-dir-use-symlinks False
```

HF CLI automatically uses aria2, which handles:

* parallel connections
* resume
* unstable proxies

much better than `requests`.

---

## 3. Fix for local proxy slowness: use system-wide SOCKS instead of HTTP

If you're using something like:

```
HTTP_PROXY=http://127.0.0.1:7890
HTTPS_PROXY=http://127.0.0.1:7890
```

Switch to SOCKS5 if your proxy supports it:

```bash
export ALL_PROXY=socks5://127.0.0.1:7891
```

SOCKS is **much more stable** for large file streaming.

---

## 4. Disable proxy for large files

If your raw network is OK but proxy is slowing down:

```bash
unset HTTP_PROXY
unset HTTPS_PROXY
unset ALL_PROXY
```

Then retry. Some HF servers are fast even without proxy depending on region.

---

## 5. Use HF mirror (Chinese mainland / TW sometimes slow)

You can force CDN:

```bash
export HF_ENDPOINT=https://hf-mirror.com
```

Then run again.
This dramatically improves speeds for some regions.

---

## 6. Resume interrupted downloads

HF datasets are cached here:

```
~/.cache/huggingface/datasets/
```

If any file was partially downloaded, HF resumes automatically — no need to start from zero.

---

## 7. If still slow: avoid the full dataset, use a small slice

OpenWebText is >40GB.
You can load only a small part:

```python
from datasets import load_dataset
ds = load_dataset("openwebtext", split="train[:1%]")
```

---

## Quick recommendation

Fastest + easiest:

```bash
pip install hf_transfer
export HF_HUB_ENABLE_HF_TRANSFER=1
python data/openwebtext_10k/prepare.py
```

You should immediately see download speeds jump.

---

If you want, I can show you how to modify your `prepare.py` to use a completely custom downloader with retry/backoff and parallel fetching, so your pipeline always downloads fast and never stalls.
