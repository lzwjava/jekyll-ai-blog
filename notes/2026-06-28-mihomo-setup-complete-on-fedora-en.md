---
audio: false
generated: true
image: false
lang: en
layout: post
title: Mihomo Setup Complete on Fedora
translated: false
type: note
---

All done. Mihomo is running on the Fedora machine:

```
HTTP proxy:  127.0.0.1:7890
SOCKS proxy: 127.0.0.1:7891
Mixed:       127.0.0.1:7892
API:         0.0.0.0:9090
```

**Test results:**
- Cloudflare 204: ✅ (proxy works)
- Google: ✅ (HTTP 200)
- Exit IP: `69.63.219.52` (going through your Hysteria2 proxy, not direct)

**What I did:**
1. Downloaded mihomo v1.19.27 RPM on Air (GitHub slow from China), scp'd to Fedora
2. Extracted RPM contents (avoided sudo), installed binary to `~/bin/mihomo`
3. Copied config from `~/.config/mihomo/config.yaml` (same as Air)
4. Copied `geoip.metadb` from Air (avoided slow download)
5. Changed DNS port from 53 → 1053 (no root needed)
6. Started with `nohup ~/bin/mihomo -d ~/.config/mihomo`

**To use proxy on the Fedora machine:**
```bash
export https_proxy=http://127.0.0.1:7890
export http_proxy=http://127.0.0.1:7890
```

Or for a single command: `curl -x http://127.0.0.1:7890 https://google.com`

Note: mihomo is running via `nohup`, not as a systemd service. It'll stop if the machine reboots. Want me to set up a systemd service for auto-start?
