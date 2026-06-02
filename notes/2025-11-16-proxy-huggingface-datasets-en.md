---
audio: false
generated: true
image: false
lang: en
layout: post
model: openai/gpt-5
title: Using Proxy with Hugging Face Datasets
translated: false
type: note
---

Yes — `datasets` follows your **system / environment proxy settings**, but it does **not** have its own proxy configuration.
So you can absolutely make Hugging Face download datasets through a proxy when you’re in China.

Here’s how.

---

# How to make `load_dataset` use a proxy (China-friendly)

## 1. Set environment variables for HTTP/HTTPS proxy

`datasets` uses Python’s `requests` library internally.
`requests` automatically uses the standard proxy env variables:

### Linux / macOS

```bash
export HTTP_PROXY="http://127.0.0.1:7890"
export HTTPS_PROXY="http://127.0.0.1:7890"
```

If your proxy uses SOCKS5:

```bash
export HTTP_PROXY="socks5://127.0.0.1:1080"
export HTTPS_PROXY="socks5://127.0.0.1:1080"
```

### Windows (PowerShell)

```powershell
setx HTTP_PROXY "http://127.0.0.1:7890"
setx HTTPS_PROXY "http://127.0.0.1:7890"
```

Then reopen terminal.

---

## 2. If you’re running Python inside code (like Jupyter), set it inside Python

```python
import os

os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7890'
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'
```

This works reliably.

---

## 3. Confirm proxy is working

You can test with:

```python
import requests
print(requests.get("https://api.ipify.org?format=json").text)
```

If the IP is your proxy’s exit node, then the Hugging Face dataset downloads will also go through that proxy.

---

## 4. Hugging Face’s `huggingface_hub` also respects these variables

`datasets` internally uses `huggingface_hub`, and it **also** follows:

* `HTTP_PROXY`
* `HTTPS_PROXY`
* `http_proxy`
* `https_proxy`

So once env variables are set, both model and dataset downloads will use your proxy automatically.

---

# Notes about usage in China

* Hugging Face raw downloads often require a proxy because they host on US/Europe endpoints.
* If you see timeouts from `.zst` dataset files, this is normal without proxy.
* A global proxy (Clash, V2Ray, Qv2ray, etc.) makes everything smoother.

---

# If you want, I can show:

* How to ensure NanoGPT downloads datasets through your proxy
* How to cache the dataset locally to avoid future downloads
* How to mirror Hugging Face datasets locally in China (e.g., Tsinghua mirror workaround)

Just tell me what you need.
