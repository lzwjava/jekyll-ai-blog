---
audio: false
generated: true
image: false
lang: en
layout: post
title: Reality Proxy Setup Guide 2026
translated: false
type: note
---

Question: How to use <https://github.com/flq367/reality> to install a proxy program on a server?

Answer:

The repository **flq367/reality** provides a simple one-click installation script for setting up **Reality** (typically referring to the VLESS + XTLS-Reality protocol in Xray-core setups), which is commonly used to create censorship-resistant proxies.

### Installation Steps

1. **Connect to your server**
   Use SSH to access your Linux server (Ubuntu/Debian, CentOS, or Alpine are common choices for such scripts).

2. **Run the one-click installation command**
   Execute this command as root (or use `sudo`):

   ```bash
   bash <(curl -sL https://raw.githubusercontent.com/flq367/reality/main/r.sh)
   ```

   - This downloads and immediately runs the script `r.sh`.
   - The script usually handles:
     - Installing required dependencies
     - Downloading a pre-built Xray-core binary (with Reality support)
     - Generating keys and certificates
     - Creating a basic server configuration
     - Setting up systemd service (or equivalent) to run automatically

3. **During installation**
   The script is interactive in most similar Reality installers. You will likely be asked to:
   - Choose a port (default often 443)
   - Enter a domain name / SNI / serverName (for Reality camouflage)
   - Select a fallback destination website (e.g. <www.microsoft.com:443>)
   - Generate or input public/private keys for Reality
   - Choose whether to enable uTLS fingerprinting, etc.

   Follow the on-screen prompts carefully.

4. **After installation finishes**
   - The script typically shows:
     - Server configuration summary
     - VLESS Reality URL / share link (for clients like v2rayN, Nekobox, Hiddify, etc.)
     - Possibly login info if it installs a panel
   - Save the VLESS link immediately — it usually looks like:
     `vless://uuid@your-server-ip:443?security=reality&...`

5. **Common locations after install**
   - Config file: usually `/usr/local/etc/xray/config.json` or `/etc/xray/config.json`
   - Binary: `/usr/local/bin/xray`
   - Service: `systemctl status xray` (or similar name)

6. **Test & manage**
   - Check status: `systemctl status xray` (or the service name shown)
   - Restart: `systemctl restart xray`
   - View logs: `journalctl -u xray -ef` or check `/var/log/xray/`

### Important Notes & Requirements

- Use a **clean IP** (not previously used for proxies) — Reality works best with uncontaminated IPs.
- Port 443 is strongly recommended (mimics HTTPS traffic).
- You usually need a domain pointing to your server IP for best results (but short domain Reality setups are possible).
- The script was last notably updated around early 2025 — verify it still works in 2026.
- If the script fails → try on a fresh Ubuntu 22.04 / 24.04 or Debian 12 server.

### If the script doesn't work or you want alternatives

Popular maintained options in 2026 include:

- Hiddify-Manager (panel + Reality support)
- 3X-UI panel
- AmneziaVPN self-hosted installer
- Various one-click Xray-Reality scripts (search "xray reality one key install 2026")

References:

- [https://github.com/flq367/reality](https://github.com/flq367/reality)
