---
audio: false
generated: true
image: false
lang: en
layout: post
title: Proxy-Ready Fedora Shell
translated: false
type: note
---

All set. Copied and adapted `.bashrc` from workstation to Fedora.

**What's in the new `.bashrc`:**

- `start_proxy` / `stop_proxy` — toggle HTTP/HTTPS proxy via mihomo (127.0.0.1:7890)
- `start_git_proxy` / `stop_git_proxy` — toggle git proxy
- `checkproxy` — show current proxy status
- `gpa` / `gca` / `gpp` — git quick commands
- Proxy auto-enabled on shell startup
- `OPENROUTER_API_KEY`, `MODEL=deepseek/deepseek-v3.2` (masked)
- HISTSIZE bumped to 10000, color aliases, Python 3.14

**Verified:**

```
HTTP_PROXY: http://127.0.0.1:7890 ✅
Git proxy: 127.0.0.1:7890 ✅
curl via proxy: exit IP 69.63.219.52 ✅
Python 3.14.3 ✅
```

New shells on the Fedora machine will have proxy and API keys ready out of the box.
