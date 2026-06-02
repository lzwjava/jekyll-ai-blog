---
audio: false
generated: true
image: false
lang: en
layout: post
model: openai/gpt-5
title: Fixing Hugging Face XetHub Proxy Issue
translated: false
type: note
---

Your logs show something very important:

**The failing connection is *not* going to HuggingFace directly.**
It is going to **[https://transfer.xethub.hf.co](https://transfer.xethub.hf.co)** — this is Hugging Face’s *XetHub* backend (Rust client `reqwest`), which the proxy you set **does NOT automatically intercept**.

This explains everything:

* You already set `HTTP_PROXY` for Python → fine
* But XetHub uses **rust reqwest**, not Python requests
* Rust reqwest **ignores system proxy variables unless you set HTTPS_PROXY lowercase variables**, or uses an explicit proxy config

So: **your Python environment is using proxy, but XetHub (the new HF storage provider) is NOT**.

That's why you see:

```
ConnectError("Connection refused")
```

and retries.

---

# Why this happens (short version)

Hugging Face recently migrated storage to **XetHub**, which uses a Rust client.
That client obeys:

* `https_proxy`
* `http_proxy`

but **not always** uppercase versions depending on build.

You set uppercase? → It may ignore them.

---

# Fix (works reliably in China)

## 1. Set BOTH lowercase and uppercase proxy variables

In your shell **before running NanoGPT**:

```bash
export http_proxy="http://127.0.0.1:7890"
export https_proxy="http://127.0.0.1:7890"

export HTTP_PROXY="http://127.0.0.1:7890"
export HTTPS_PROXY="http://127.0.0.1:7890"
```

Rust reqwest prefers lowercase
Python requests prefers uppercase
Setting both avoids issues.

Then run:

```bash
python data/openwebtext_10k/prepare.py
```

You should see proper download speed immediately.

---

# 2. Important if your proxy is SOCKS5

Rust reqwest **does not support socks5** unless compiled with optional features.
So if your proxy is socks5:// → it will fail.

You must switch to HTTP proxy port of your client, usually:

* Clash: 7890 (HTTP)
* V2RayN: 10809 (HTTP)

Use HTTP, not SOCKS.

---

# 3. How to test if Rust part is using proxy

Test via `curl`, **not Python**, because curl behaves similarly to Rust in proxy rules:

```bash
curl -I https://transfer.xethub.hf.co --proxy http://127.0.0.1:7890
```

If this works → Rust downloads will work too.

If it fails → your proxy cannot reach `xethub.hf.co` domain.

---

# 4. If you want to force Hugging Face to avoid XetHub

You can set env variable:

```bash
export HF_HUB_DISABLE_XETHUB=1
```

This forces old HuggingFace S3 backend instead of XetHub, much more proxy-friendly.

Then:

```bash
python data/openwebtext_10k/prepare.py
```

This is the most stable fix.

---

# Recommended solution (China-friendly)

For reliability:

```bash
export HF_HUB_DISABLE_XETHUB=1

export http_proxy="http://127.0.0.1:7890"
export https_proxy="http://127.0.0.1:7890"
export HTTP_PROXY="http://127.0.0.1:7890"
export HTTPS_PROXY="http://127.0.0.1:7890"

python data/openwebtext_10k/prepare.py
```

---

If you want, I can give you:

* A one-click bash script (`hf_proxy_on.sh`)
* A permanent `.bashrc` proxy setup
* Instructions to fully mirror OpenWebText locally to avoid future downloads

Just tell me.
