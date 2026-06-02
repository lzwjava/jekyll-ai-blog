---
audio: false
generated: true
image: false
lang: en
layout: post
model: openai/gpt-5
title: Fixing Proxy for HuggingFace Download
translated: false
type: note
---

Yes — it **can** use your proxy, but from the output you pasted, **your proxy is NOT being used right now**.
That’s why the download is stuck at **17.6 bytes/s** — classic symptom of direct China-to-HF connection.

Let me show you **how to confirm** and **how to fix** it.

---

# 1. Why your current run is *not* using the proxy

The line:

```
78.0/630M [00:16<9947:51:33, 17.6B/s]
```

is clear: if a proper proxy (Clash, V2Ray, Shadowsocks) were active via `HTTP_PROXY` / `HTTPS_PROXY`, you'd see speeds like:

* hundreds of KB/s
* or several MB/s
* not ~17 bytes/s

So the Python process isn't picking up any proxy environment.

---

# 2. CHECK if your proxy environment variables exist

In the exact same terminal where you run:

```
python data/openwebtext_10k/prepare.py
```

Run:

```bash
echo $HTTP_PROXY
echo $HTTPS_PROXY
```

If nothing prints → they are not set, so HuggingFace cannot use them.

---

# 3. FIX: set proxy for that terminal session

Example for Clash running on 7890:

```bash
export HTTP_PROXY="http://127.0.0.1:7890"
export HTTPS_PROXY="http://127.0.0.1:7890"
```

If you use SOCKS5 (e.g. Shadowsocks):

```bash
export HTTP_PROXY="socks5://127.0.0.1:1080"
export HTTPS_PROXY="socks5://127.0.0.1:1080"
```

**Then run again:**

```bash
python data/openwebtext_10k/prepare.py
```

Now your speed should jump dramatically.

---

# 4. Additional check inside Python

Add these lines at the top of `prepare.py` just to test:

```python
import os
print("HTTP_PROXY:", os.getenv("HTTP_PROXY"))
print("HTTPS_PROXY:", os.getenv("HTTPS_PROXY"))
```

If they print `None` → your shell did not pass them → fix your env.

---

# 5. Optional: verify with `requests` before loading dataset

Run:

```python
import requests
print(requests.get("https://api.ipify.org?format=json", timeout=5).text)
```

* If the returned IP is from your VPN/proxy → good.
* If it is your home ISP IP → proxy not used.

---

# 6. Important detail: HuggingFace uses **HTTP**, not SOCKS**, unless you use pysocks

If your proxy is SOCKS5, some Python installations don’t work with it unless `PySocks` is installed:

```bash
pip install pysocks
```

Then SOCKS proxies work normally.

---

# 7. Summary

✔ HuggingFace *will* use proxy
✔ But only if environment variables are set
✘ Your logs show your proxy is NOT active
✔ Solution: set proxy env vars in the same shell

---

If you want, I can:

* Adjust your shell config (`.bashrc` or `.zshrc`) to always use proxy
* Make a “proxy-on” / “proxy-off” script
* Patch your NanoGPT `prepare.py` to enforce proxies inside Python

Tell me which direction you prefer.
