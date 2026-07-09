---
audio: false
generated: true
image: false
lang: en
layout: post
title: Claude Code Proxy Transient Error Diagnosis
translated: false
type: note
---

Claude Code is working right now — the third-party proxy server is reachable and the auth token is valid. The error you hit was likely transient.

Here's the full diagnosis:

---

**Root Cause: transient failure of the third-party API proxy**

Your Claude Code `settings.json` points to a non-official endpoint:

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "https://claude2.sssaicode.com/api",
    "ANTHROPIC_AUTH_TOKEN": "sk-sss...0443"
  }
}
```

This is a third-party proxy that gives access to Claude models (Opus 4, in your case). It's served behind Cloudflare and resolves to `50.87.93.246` in the US.

The connection path:

```
Claude Code CLI (Node.js)
  → https_proxy http://127.0.0.1:7890 (mihomo)
    → mihomo: no explicit rule for sssaicode.com → DIRECT
      → cloudflare → claude2.sssaicode.com
```

When I tested just now, it works — returns a valid response in ~2.8s. So the issue was temporary (the server was down for a few minutes, Cloudflare was re-routing, or there was a DNS hiccup).

**Why you see "ConnectionRefused" instead of a more descriptive error**: the Anthropic SDK's Node.js HTTP client reports TCP-level failures as "ConnectionRefused" when the `fetch`/`https` module can't establish a connection — transient server downtime, DNS failures, proxy routing blips all get lumped into this same message. There's no retry/backoff at the SDK level that would mask a brief hiccup.

**To make this more robust**, you could:

1. **Add an explicit proxy rule** for sssaicode.com so it always routes through your SS/Hysteria2 tunnels (not DIRECT), in case the direct connection from China is flaky:

   ```
   - DOMAIN-SUFFIX,sssaicode.com,Proxy
   ```

2. **Switch to the official Anthropic API** (harder from China without reliable proxy) with `ANTHROPIC_API_KEY` instead of the third-party proxy. Though the third-party proxy seems to work fine otherwise — you got a response just now with Opus 4 costing $0.27 per request.

3. **Just retry** — the error is transient. If you see it again, wait a minute and try again.