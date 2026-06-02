---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fix Hysteria ACME IP Error Guide
translated: false
type: note
---

Question: The current date is February 28, 2026. How to fix the Hysteria server error: "invalid config: acme.domains: 64.186.xx.xx: >" and the service failing with exit-code 1?

Answer:

The error you're seeing in the logs:

```
invalid config: acme.domains: 64.186.xx.xx: >
...
hysteria-server.service: Main process exited, code=exited, status=1/FAILURE
```

indicates that Hysteria 2 failed to start because the **ACME configuration is invalid**. Specifically, you put an **IP address** (`64.186.xx.xx`) in the `acme.domains` list instead of a valid domain name.

### Why This Happens
- The `acme` section is for **automatic certificate issuance/renewal** via Let's Encrypt (or similar) using the ACME protocol.
- Let's Encrypt (and most ACME CAs) **cannot issue certificates for raw IP addresses** — they require **fully qualified domain names (FQDNs)** like `example.com` or `vpn.mydomain.net`.
- Hysteria 2 validates this during startup: if `acme.domains` contains something that isn't a valid domain (or if certificate issuance fails for other reasons), it treats the entire config as invalid and exits with status 1.
- Your partial error message cuts off (`64.186.xx.xx: >`), but it likely continues with something like "obtaining certificate: ... invalid domain" or a similar validation failure.

### How to Fix It

You have two main options depending on whether you have (or want) a domain name.

#### Option 1: Use a Real Domain Name (Recommended for Best Compatibility)
1. **Get a domain** (if you don't have one): Buy a cheap one from Namecheap, Porkbun, etc., and point its A record to your server's IP (64.186.xx.xx).
   - Example: `hy2.mydomain.com` → A record → 64.186.xx.xx

2. **Edit `/etc/hysteria/config.yaml`**:
   Replace the IP with your domain:
   ```yaml
   listen: :443

   acme:
     domains:
       - hy2.mydomain.com          # ← Change this to your actual domain
     email: your@email.com         # Required for Let's Encrypt notifications

   auth:
     type: password
     password: your-strong-password

   # ... rest of your config ...
   ```

3. **Restart the service**:
   ```bash
   systemctl restart hysteria-server
   ```

4. **Check logs**:
   ```bash
   journalctl -u hysteria-server -e
   ```
   - On first start, it will request a certificate (needs TCP port 80 open temporarily for HTTP-01 challenge, or use DNS-01 if port 80 is blocked).
   - If port 80 is firewalled: Add `ufw allow 80/tcp` temporarily, or switch to DNS challenge (see below).

#### Option 2: Use Self-Signed Certificates (No Domain Needed, Quick Fix)
If you don't have/want a domain, disable ACME and use manual/self-signed TLS.

1. **Generate a self-signed certificate** (for your IP or any CN):
   ```bash
   mkdir -p /etc/hysteria/certs
   openssl req -x509 -nodes -days 3650 -newkey rsa:2048 \
     -keyout /etc/hysteria/certs/server.key \
     -out /etc/hysteria/certs/server.crt \
     -subj "/CN=64.186.xx.xx" \
     -addext "subjectAltName = IP:64.186.xx.xx"
   ```

   (Or use the script from Hysteria docs for more options.)

2. **Update config.yaml** — remove `acme` entirely and add `tls`:
   ```yaml
   listen: :443

   tls:
     cert: /etc/hysteria/certs/server.crt
     key: /etc/hysteria/certs/server.key

   auth:
     type: password
     password: your-strong-password

   masquerade:
     type: proxy
     proxy:
       url: https://news.ycombinator.com/
       rewriteHost: true
   ```

3. **Restart**:
   ```bash
   systemctl restart hysteria-server
   ```

4. **In Shadowrocket (iOS client)**:
   - Enable **insecure** / **Allow Insecure** (or add `&insecure=1` to hy2:// URI).
   - Use SNI = your server's IP or leave blank (some clients allow empty SNI).
   - This works but browsers/apps may show warnings; it's fine for proxy use.

#### Optional: Advanced ACME with DNS Challenge (If Port 80 Blocked)
If you have a domain but can't open TCP/80:
```yaml
acme:
  domains:
    - hy2.mydomain.com
  email: your@email.com
  type: dns
  dns:
    name: cloudflare          # or godaddy, etc.
    config:
      cloudflare_api_token: your-api-token-here
```

See official docs for supported providers.

After fixing the config, the service should start normally (`systemctl status hysteria-server` shows active/running).

References:

- [Hysteria 2 Full Server Config (tls vs acme)](https://v2.hysteria.network/docs/advanced/Full-Server-Config)
- [Hysteria 2 ACME DNS Config (alternative to HTTP challenge)](https://v2.hysteria.network/docs/advanced/ACME-DNS-Config)
- [GitHub Issue - ACME failures and config examples](https://github.com/apernet/hysteria/issues/942)
