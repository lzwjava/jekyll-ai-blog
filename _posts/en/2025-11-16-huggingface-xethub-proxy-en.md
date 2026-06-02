---
audio: false
generated: true
image: false
lang: en
layout: post
model: openai/gpt-5
title: Configuring Hugging Face XetHub Proxy
translated: false
type: note
---

Yes — **Rust reqwest absolutely supports an explicit proxy configuration**, and Hugging Face’s XetHub client (written in Rust) allows this too.
BUT: Hugging Face does **not expose** a Python API for you to pass proxy settings directly.
Instead, XetHub relies on **environment variables** that reqwest automatically reads.

So the explicit proxy config for reqwest looks like this:

---

# ✔ How reqwest detects proxies (official)

Reqwest automatically uses the following **environment variables**:

* `https_proxy`
* `http_proxy`
* `all_proxy`

Lowercase is the important part.
Reqwest **ignores** uppercase variables (`HTTPS_PROXY`) unless a certain feature flag is enabled at compile time.

**Hugging Face XetHub uses the default reqwest → lowercase only.**

This means:

```
export https_proxy="http://127.0.0.1:7890"
export http_proxy="http://127.0.0.1:7890"
```

is the only guaranteed working explicit proxy config for XetHub.

---

# ✔ How HuggingFace XetHub loads proxy config

When Python runs `load_dataset`, it triggers a Rust binary that:

1. Looks for lowercase proxy env vars
2. Rewrites URLs
3. Opens connections through reqwest
4. Downloads file chunks from `https://transfer.xethub.hf.co`

If those env vars aren’t set, or reachable → connection refused.

---

# ✔ Manually forcing reqwest to use proxy (reference code)

Just to show what reqwest would do internally:

```rust
let proxy = reqwest::Proxy::https("http://127.0.0.1:7890")?;
let client = reqwest::Client::builder()
    .proxy(proxy)
    .build()?;
```

Hugging Face's XetHub client *does something equivalent*, but triggered by env vars.

---

# ✔ Full explicit proxy config that always works with reqwest (HF compatible)

Run **all** of these:

```bash
export http_proxy="http://127.0.0.1:7890"
export https_proxy="http://127.0.0.1:7890"
export all_proxy="http://127.0.0.1:7890"
```

Use `http` proxy, not `socks5`, because:

* reqwest’s socks support is optional
* XetHub client binary was not compiled with it for HF

So socks may silently fail.

---

# ✔ Verify that your proxy is being used

Try:

```bash
env | grep proxy
```

If you see lowercase → good.

Then:

```bash
curl -I https://transfer.xethub.hf.co --proxy http://127.0.0.1:7890
```

If curl succeeds → reqwest will succeed.

---

# Summary

* Hugging Face datasets sometimes download via **XetHub** (Rust reqwest client)
* Reqwest only respects **lowercase** proxy vars by default
* You must set them explicitly
* Use **HTTP** proxy, not SOCKS
* `HF_HUB_DISABLE_XETHUB=1` can bypass reqwest entirely if needed

---

If you want, I can prepare a:

* one-command “HF proxy fix” script
* persistent config for your `.bashrc`
* auto-detection to confirm if reqwest is using proxy

Just let me know.
