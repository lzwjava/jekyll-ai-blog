---
audio: false
generated: true
image: false
lang: en
layout: post
title: Acpx Plugin Setup Guide
translated: false
type: note
---

**Question:** How to configure the acpx (browser control) plugin on this bridge?

**Answer:**

The **acpx** plugin is the browser control / automation bridge used by OpenClaw (and several similar local AI agent frameworks) to give the agent real browser capabilities.

Here are the most common ways to configure/install/enable the **acpx** browser plugin, depending on your exact setup:

### 1. Quick recommended method (most users — OpenClaw CLI / bridge)

```bash
# Make sure you already have OpenClaw installed & updated
pip install --upgrade openclaw

# Install & register the acpx browser plugin (this downloads a small chromium + extension)
openclaw plugin install acpx

# Alternative longer name people sometimes use:
openclaw plugin install browser-acpx
```

After installation you usually see:

```
Plugin 'acpx' installed successfully.
Browser profile 'openclaw' created.
```

Then restart your OpenClaw bridge / server:

```bash
# If you're running the default bridge
openclaw bridge restart

# or if you run it manually / in docker / systemd
# just restart the process that runs openclaw bridge
```

### 2. Manual / advanced installation (when auto-install fails or you want custom profile)

```bash
# 1. Install playwright browsers (acpx uses playwright under the hood)
pip install playwright
playwright install chromium --with-deps

# 2. Install the acpx plugin explicitly from git (latest / bleeding edge)
pip install git+https://github.com/openclaw/acpx.git

# 3. Create / register the managed profile
acpx profile create --name openclaw --theme orange

# 4. Tell OpenClaw to use it (usually automatic, but you can force it)
openclaw config set browser.backend acpx
openclaw config set browser.profile openclaw
```

### 3. If you want to connect to your **real existing browser** instead (Extension Relay mode)

1. Install the **OpenClaw Browser Relay** extension
   → Chrome Web Store: search "OpenClaw Browser Relay" or go directly to
   <https://chromewebstore.google.com/detail/openclaw-browser-relay/……>

2. Enable developer mode in Chrome → load unpacked → point to the folder if you cloned it manually

3. In the extension popup → click "Copy WebSocket URL" (it looks like `ws://127.0.0.1:9222/devtools/browser/xxxx-xxxx`)

4. Paste that URL into your OpenClaw bridge config or when asked:

```bash
openclaw config set browser.backend acpx-relay
openclaw config set browser.websocket ws://127.0.0.1:9222/devtools/browser/……
```

**Important notes**

- Most people get good results with the **managed isolated profile** (`openclaw` profile) — it's safer and avoids messing with your personal logins.
- The **relay mode** is more powerful (uses your real cookies/sessions), but also more risky — only use it if you fully trust what the agent is doing.
- After configuring acpx, test it with a simple command like:
  `openclaw "open google.com and tell me what the Google logo says"`

If you're still getting "acpx plugin not configured" after these steps, share:

- which exact OpenClaw version you're running (`openclaw --version`)
- whether you're using docker / pip / binary
- the full error message when starting the bridge

That will help narrow it down faster.

**References:**

- [OpenClaw Browser Tools Documentation](https://docs.openclaw.ai/tools/browser)
- [ACPX GitHub Repository](https://github.com/openclaw/acpx)
- [OpenClaw Plugin Installation Guide](https://docs.openclaw.ai/setup/plugins)
