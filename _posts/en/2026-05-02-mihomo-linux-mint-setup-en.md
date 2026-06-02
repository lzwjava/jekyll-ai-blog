---
audio: false
generated: true
image: false
lang: en
layout: post
title: Mihomo Setup and Configuration on Linux Mint
translated: false
type: note
---

## Comprehensive Review: mihomo Setup on Linux Mint 22.3

### What Was Done

**1. Binary Installation**

- Downloaded mihomo v1.19.24 (linux/amd64) from GitHub releases
- Installed to `~/.local/bin/mihomo` (user-space, no sudo)
- Added `~/.local/bin` to `$PATH` in `~/.bashrc`

**2. Configuration**

- Copied your full `~/.config/mihomo/config.yaml` from Mac to the Linux machine
- Config includes: SS proxy, Hysteria2 proxy, rule-sets (Global/China/ChinaIP), 20+ domain rules

**3. Systemd User Service**

- Created `~/.config/systemd/user/mihomo.service`
- Enabled (auto-starts on user login)
- Running as user `xiaoxin`, not root

**4. System Proxy (Cinnamon desktop)**

- Configured via `gsettings` (accessed over SSH using `/run/user/1000/bus`)
- Mode: `manual`, HTTP/HTTPS → `127.0.0.1:7890`

**5. Terminal Proxy**

- Added `http_proxy`, `https_proxy` etc. to `~/.bashrc`

---

### What's Working ✓

| Port | Protocol | Status |
|------|----------|--------|
| 7890 | HTTP proxy | ✓ listening |
| 7891 | SOCKS5 proxy | ✓ listening |
| 7892 | Mixed (HTTP+SOCKS) | ✓ listening |
| 9090 | REST API / dashboard | ✓ listening |

---

### Known Issues / Gaps

**DNS on port 53 — permission denied**

- Config sets `listen: 0.0.0.0:53`, but non-root can't bind port 53
- `fake-ip` mode is broken — DNS resolution falls back to system resolver
- Fix:

  ```bash
  sudo setcap cap_net_bind_service=+ep ~/.local/bin/mihomo
  systemctl --user restart mihomo
  ```

  Or change config to `listen: 0.0.0.0:5353` and redirect with iptables

**Sudo required for system binary path**

- Binary is in `~/.local/bin/` not `/usr/local/bin/` because `sudo` can't run non-interactively over SSH without password
- Consequence: `mihomo` only accessible from user `xiaoxin`, not system-wide

**User service vs system service**

- `systemctl --user` only runs when `xiaoxin` is logged in, unless `loginctl enable-linger xiaoxin` is set
- Without lingering, mihomo stops when xiaoxin logs out
- Fix:

  ```bash
  sudo loginctl enable-linger xiaoxin
  ```

**Rule-set downloads pending**

- On first start, mihomo downloads Global/China/ChinaIP rule sets from `cdn.jsdmirror.cn`
- These need internet access without proxy (chicken-and-egg) — but since CDN is in China, DIRECT works

**`allow-lan: true` but no firewall rules**

- Mihomo listens on `*:7890` (all interfaces), meaning LAN devices can use it as a proxy
- If that's unintended, add firewall rule: `sudo ufw deny from any to any port 7890 comment "limit mihomo"`

---

### Recommended Follow-up Actions

```bash
# 1. Enable linger so service survives logout
sudo loginctl enable-linger xiaoxin

# 2. Fix DNS port 53 binding
sudo setcap cap_net_bind_service=+ep ~/.local/bin/mihomo
systemctl --user restart mihomo

# 3. Verify proxy works
curl -x http://127.0.0.1:7890 https://www.google.com -I
```

---

### Process Issues (Meta)

- The download took ~5 minutes at ~45KB/s — the Linux machine's connection to GitHub was slow; could use a mirror next time
- `sudo` over non-TTY SSH is a common pain point — solutions: configure `NOPASSWD` in sudoers for specific commands, or use `scp` + manual sudo step
- Used many polling loops instead of a single blocking wait — the monitoring approach was noisier than ideal
