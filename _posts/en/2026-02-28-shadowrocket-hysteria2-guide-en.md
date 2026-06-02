---
audio: false
generated: true
image: false
lang: en
layout: post
title: Shadowrocket Hysteria 2 Setup Guide
translated: false
type: note
---

Question: How to use Shadowrocket on iOS to connect to a Hysteria 2 proxy server?

Answer:

**Shadowrocket** is a popular paid iOS app (available on the App Store) that supports **Hysteria 2** as a protocol since version **2.2.35** (and later). As of 2026, it works reliably for connecting to Hysteria 2 servers.

### Prerequisites

- Shadowrocket installed and updated (check for version ≥ 2.2.35).
- Your Hysteria 2 server is running and accessible (from previous setup: UDP port open, domain or IP, password auth, etc.).
- You have the server details ready:
  - Server address (domain or IP)
  - Port (usually 443)
  - Password (from your server's `auth.password`)
  - Optional: SNI (usually same as domain if using TLS/ACME)
  - Optional: Obfuscation (salamander) password if enabled in server config

### Step-by-Step: Adding Hysteria 2 in Shadowrocket (Manual Setup)

1. Open **Shadowrocket** on your iPhone/iPad.

2. Go to the **Home** tab (or **Nodes** / proxy list screen).

3. Tap the **+** (plus) icon in the top right to add a new node/server.

4. In the "Type" / Protocol dropdown, select **Hysteria 2** (it appears as "Hysteria2" or "HY2").

5. Fill in the fields:
   - **Server** / Address: your-domain.com (or server IP)
   - **Port**: 443 (or whatever UDP port you configured)
   - **Password**: your-strong-password-here (single password auth)
   - **SNI** (Server Name Indication): your-domain.com (important if using TLS; usually matches the server domain)
   - **Obfs** / Obfuscation: If you enabled salamander obfuscation on server, select "salamander" and enter the obfs password; otherwise leave disabled/none.
   - **ALPN**: Usually leave default or set to `h3` (for HTTP/3 masquerade compatibility)
   - **Up Mbps** / **Down Mbps**: Optional bandwidth limits (e.g., 100–200 for stability; set 0 for unlimited)
   - **Remarks** / Name: Give it a friendly name like "HY2 Home Server"
   - Other advanced options (congestion control, etc.): Defaults are usually fine (Brutal is recommended)

6. Tap **Save** or **Done**.

7. Back on the main list, select your new Hysteria 2 node.

8. Turn on the main **Connect** switch (top of the screen).

9. Grant VPN permissions if prompted (Shadowrocket uses Apple's VPN framework in TUN mode for full-device proxying).

10. Test: Open Safari or any app → visit a site like whatismyipaddress.com to confirm your IP changed.

### Alternative: Import via URI (Easiest if You Have a hy2:// Link)

Many Hysteria 2 setups (panels like H-UI, custom scripts) generate a share link in this format:

```
hy2://password@your-domain.com:443/?sni=your-domain.com&insecure=0
```

(or with obfs: &obfs=salamander&obfs-password=xxx)

- Copy the full `hy2://...` link.
- Shadowrocket auto-detects it from clipboard → tap to import when prompted.
- Or: In Shadowrocket → + → Import from Clipboard (or Scan QR if you have a QR code).

### Common Tips & Troubleshooting

- **Connection fails?**
  - Double-check UDP 443 is not blocked (test server reachability with another client like sing-box desktop).
  - Ensure SNI matches exactly (case-sensitive).
  - If using self-signed cert: enable "Allow Insecure" / insecure=1 in URI or toggle insecure in app.
  - Firewall on server allows UDP inbound.
- **Slow speed?** Try lowering bandwidth caps or test different congestion settings.
- **Full device proxy**: Shadowrocket uses TUN mode by default (routes all traffic); use "Config" → "Global Routing" for rules if you want per-app/proxy only.
- **Update app**: If Hysteria 2 option is missing → update Shadowrocket.

This setup gives excellent performance and strong censorship resistance on iOS.

References:

- [Hysteria 2 Official - 3rd-party Apps](https://v2.hysteria.network/docs/getting-started/3rd-party-apps)
- [GitHub Discussion - Hysteria2 with Shadowrocket](https://github.com/apernet/hysteria/discussions/1325)
- [Hysteria 2 One-Click Script Repo (client notes)](https://github.com/missuo/Hysteria2/blob/main/README.md)
