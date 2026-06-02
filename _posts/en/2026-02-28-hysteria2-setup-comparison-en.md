---
audio: false
generated: true
image: false
lang: en
layout: post
title: Hysteria2 Setup and Comparison Guide
translated: false
type: note
---

Question: How to install Hysteria, the proxy protocol, on an Ubuntu server? And compare Hysteria and Hysteria2.

Answer:

**Hysteria** refers to a fast, QUIC-based proxy protocol designed for high performance on lossy networks and strong censorship resistance. There are two main versions: the original **Hysteria 1.x** (often just called "Hysteria") and **Hysteria 2** (the modern, recommended version).

As of 2026, **Hysteria 2** is the actively maintained version with better protocol design, improved masquerading as HTTP/3, and overall superior performance and resistance. **Hysteria 1** is considered legacy.

### Installing Hysteria 2 on Ubuntu Server (Recommended)

The official one-click installation script is the easiest and most reliable method for Ubuntu (works on 20.04, 22.04, 24.04, etc.).

1. **Run the installation script** (installs latest version, sets up systemd service):
   ```bash
   bash <(curl -fsSL https://get.hy2.sh/)
   ```

   - This downloads the binary, creates `/etc/hysteria/config.yaml`, and sets up `hysteria-server.service`.

2. **Edit the configuration file**:
   ```bash
   nano /etc/hysteria/config.yaml
   ```

   Minimal working example (replace values):
   ```yaml
   listen: :443   # UDP port (usually 443)

   acme:
     domains:
       - your-domain.com
     email: your@email.com

   auth:
     type: password
     password: your-strong-password-here

   masquerade:
     type: proxy
     proxy:
       url: https://news.ycombinator.com/
       rewriteHost: true
   ```

   - For self-signed certs or manual certs, use the `tls` section instead of `acme`.
   - Full config options → official docs.

3. **Start and enable the service**:
   ```bash
   systemctl daemon-reload
   systemctl enable --now hysteria-server
   ```

4. **Check status and logs**:
   ```bash
   systemctl status hysteria-server
   journalctl -u hysteria-server -ef
   ```

5. **Firewall** (if using ufw):
   ```bash
   ufw allow 443/udp
   ```

6. **Update later** → just re-run the same install command.

**Note**: If GitHub is blocked, download the binary manually from https://github.com/apernet/hysteria/releases and use:
```bash
bash <(curl -fsSL https://get.hy2.sh/) --local /path/to/hysteria-linux-amd64
```

### Installing Original Hysteria 1.x (Legacy – Not Recommended)

Use the old repo/script if you specifically need compatibility with old clients:
```bash
bash <(curl -fsSL https://raw.githubusercontent.com/apernet/hysteria/master/scripts/install_server.sh)
```

But in 2026 this is strongly discouraged — switch to Hysteria 2.

### Comparison: Hysteria 1 vs Hysteria 2

| Feature / Aspect              | Hysteria 1.x (legacy)                  | Hysteria 2 (current)                              |
|-------------------------------|----------------------------------------|---------------------------------------------------|
| **Protocol**                  | Custom QUIC + own obfuscation          | Redesigned QUIC-based, masquerades as real **HTTP/3** |
| **Censorship resistance**     | Good                                   | Significantly better (looks like normal HTTP/3 traffic) |
| **Congestion control**        | Custom (very aggressive)               | **Brutal** (custom) + BBR support, more stable    |
| **Performance**               | Excellent on lossy networks            | Usually better/faster + more consistent           |
| **Compatibility**             | Only with Hysteria 1 clients           | Only with Hysteria 2 clients (not backward compatible) |
| **Codebase**                  | Older, less maintained                 | Almost complete rewrite, actively developed       |
| **Masquerade**                | Basic HTTP proxy masquerade            | Much more advanced (proxy, files, string, etc.)   |
| **Missing in v2**             | —                                      | No client-side ACL (yet), no FakeTCP (niche)      |
| **Recommendation in 2026**    | Avoid for new setups                   | **Strongly recommended** for all new deployments  |

**Summary**: Use **Hysteria 2** unless you have a specific reason to stay on 1.x (e.g., old client compatibility). It offers better speed, much stronger censorship resistance, and is the future-proof choice.

References:

- [Hysteria 2 Official Installation](https://v2.hysteria.network/docs/getting-started/Installation)
- [Hysteria 2 Server Installation Script](https://v2.hysteria.network/docs/getting-started/Server-Installation-Script)
- [Hysteria 2 vs Hysteria 1 Comparison](https://v2.hysteria.network/docs/misc/2-vs-1)
