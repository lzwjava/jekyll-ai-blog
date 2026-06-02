---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Hysteria 2 Server Setup Guide
translated: false
type: note
---

**Question:** How to set up Hysteria 2 on the server?

**Answer:**

Here is a clear, up-to-date guide (as of 2026) to deploy a **Hysteria 2** server on a Linux VPS (most common case, Ubuntu/Debian/CentOS/etc.).

### Prerequisites

- VPS with **public IP** (IPv4 and/or IPv6)
- A **domain name** pointed to the server's IP (A/AAAA record)
- Root or sudo access
- Port **443** (UDP) open in firewall (very important — Hysteria 2 uses QUIC/UDP)
- Optional but strongly recommended: ability to get a real TLS certificate (via ACME/Let's Encrypt)

### Recommended Method: Use the Official One-Click Installation Script

This is the easiest and most maintained way for Linux servers.

1. Run the official bash script (installs binary + creates systemd service):

   ```bash
   bash <(curl -fsSL https://get.hy2.sh/)
   ```

   - It downloads the latest Hysteria 2 binary for your architecture (amd64/arm64)
   - Installs to `/usr/local/bin/hysteria`
   - Creates `/etc/hysteria/config.yaml` (example config)
   - Sets up systemd service: `hysteria-server.service`

2. Edit the configuration file:

   ```bash
   nano /etc/hysteria/config.yaml
   ```

   **Minimal working example (ACME auto-cert + password auth):**

   ```yaml
   listen: :443

   acme:
     domains:
       - your.domain.com           # ← change to your domain
     email: your@email.com         # ← your email for Let's Encrypt

   auth:
     type: password
     password: YOUR_STRONG_PASSWORD_HERE   # ← change this!

   masquerade:
     type: proxy
     proxy:
       url: https://news.ycombinator.com/   # ← fake site to mimic (helps vs DPI)
       rewriteHost: true
   ```

   **Alternative (if you already have your own cert/key):**

   ```yaml
   listen: :443

   tls:
     cert: /path/to/fullchain.pem
     key: /path/to/privkey.pem

   auth:
     type: password
     password: YOUR_STRONG_PASSWORD_HERE

   masquerade:
     type: proxy
     proxy:
       url: https://www.bing.com/
       rewriteHost: true
   ```

   **Notes on config:**
   - Port 443 is default and strongly recommended (looks like normal HTTP/3)
   - `masquerade` makes the server respond like a real website → very hard to block
   - For personal use, you can remove `bandwidth` limits entirely (or set very high)
   - Save and exit

3. Start & enable the service:

   ```bash
   systemctl start hysteria-server
   systemctl enable hysteria-server
   ```

4. Check status and logs:

   ```bash
   systemctl status hysteria-server
   journalctl -u hysteria-server -e -f
   ```

   Look for: `server up and running` → success!

### Alternative: Manual Installation (No Script)

1. Download latest binary:

   ```bash
   wget https://download.hysteria.network/app/latest/hysteria-linux-amd64   # or -arm64
   chmod +x hysteria-linux-amd64
   mv hysteria-linux-amd64 /usr/local/bin/hysteria
   ```

2. Allow binding low ports without root:

   ```bash
   setcap cap_net_bind_service=+ep /usr/local/bin/hysteria
   ```

3. Create config file (e.g. `/etc/hysteria/config.yaml`) as above.

4. Run manually (for testing):

   ```bash
   hysteria server -c /etc/hysteria/config.yaml
   ```

5. Create systemd service yourself (or use the script method above).

### Firewall (ufw example)

```bash
ufw allow 443/udp
ufw reload
```

### After Setup

- The server prints (or logs) a `hysteria2://` URI → share it directly with clients (e.g. NekoBox, sing-box, Shadowrocket)
- Example client snippet:

  ```yaml
  server: your.domain.com:443
  auth: YOUR_STRONG_PASSWORD_HERE
  bandwidth:
    up: 30 mbps
    down: 200 mbps
  ```

### Common Tips / Troubleshooting

- Make sure **UDP 443** is not blocked by VPS provider/firewall
- If ACME fails → check DNS propagation, port 80 open temporarily (for http-01 challenge), or use DNS-01 challenge
- No masquerade = server returns 404 → still works but easier to detect
- For very high performance → tune `bandwidth` to realistic values (server upload = client download)

**References:**

- [Official Server Quick Start](https://v2.hysteria.network/docs/getting-started/Server/)
- [Official Installation Page](https://v2.hysteria.network/docs/getting-started/Installation/)
- [Server Installation Script](https://v2.hysteria.network/docs/getting-started/Server-Installation-Script/)
- [Full Server Configuration Reference](https://v2.hysteria.network/docs/advanced/Full-Server-Config/)
