---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fix OpenClaw Secure Context Error
translated: false
type: note
---

Question: OpenClaw Control UI shows "requires device identity (use HTTPS or localhost secure context)" — how do I fix this?

Answer:

## Root Cause

Modern browsers **block certain JavaScript APIs** (like device identity/fingerprinting used by OpenClaw) on non-secure origins. A page served over plain `http://` on a non-localhost address is considered **insecure context** by the browser.

You have **3 options** to fix this:

---

## Option 1 — Use SSH Tunnel (Easiest, No Config Change)

This is the **simplest fix**. Instead of opening `http://192.168.1.36:18789` directly, tunnel it through SSH so your browser sees it as `localhost`:

**On your main PC**, run:

```bash
ssh -N -L 18789:127.0.0.1:18789 lzw@192.168.1.36
```

Then open browser:

```
http://localhost:18789
```

`localhost` is always treated as a **secure context** by browsers — no HTTPS needed. ✅

---

## Option 2 — Enable HTTPS in OpenClaw with a Self-Signed Certificate

### Step 1 — Generate a self-signed cert

```bash
mkdir -p ~/.openclaw/certs
cd ~/.openclaw/certs

openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem \
  -days 3650 -nodes \
  -subj "/CN=192.168.1.36" \
  -addext "subjectAltName=IP:192.168.1.36"
```

### Step 2 — Configure OpenClaw to use HTTPS

```bash
nano ~/.openclaw/openclaw.json
```

Add the `tls` block inside `gateway`:

```json
{
  "gateway": {
    "bind": "lan",
    "port": 18789,
    "tls": {
      "cert": "/home/lzw/.openclaw/certs/cert.pem",
      "key": "/home/lzw/.openclaw/certs/key.pem"
    },
    "controlUi": {
      "allowedOrigins": ["*"]
    }
  }
}
```

### Step 3 — Restart gateway

```bash
openclaw gateway stop
openclaw gateway start
```

### Step 4 — Open in browser

```
https://192.168.1.36:18789
```

⚠️ Browser will show a **certificate warning** (because it's self-signed). Click **Advanced → Proceed anyway**. After accepting once, it works as secure context.

---

## Option 3 — Use Caddy as Reverse Proxy with Auto HTTPS (Most Proper)

If you want a **clean HTTPS** with no browser warning, use Caddy which auto-generates trusted local certs.

### Install Caddy

```bash
sudo apt install -y debian-keyring debian-archive-keyring apt-transport-https
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | sudo gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | sudo tee /etc/apt/sources.list.d/caddy-stable.list
sudo apt update
sudo apt install caddy -y
```

### Configure Caddyfile

```bash
sudo nano /etc/caddy/Caddyfile
```

```
:18790 {
    tls internal
    reverse_proxy 127.0.0.1:18789
}
```

### Start Caddy

```bash
sudo systemctl restart caddy
sudo systemctl enable caddy
```

### Trust Caddy root CA on your main PC

```bash
# On the SERVER - export the cert
cat $(caddy environ | grep DATA_DIR | cut -d= -f2)/pki/authorities/local/root.crt
```

Copy and install that cert into your main PC's browser trusted store.

Then access:

```
https://192.168.1.36:18790
```

---

## Recommendation Summary

| Option | Difficulty | Browser Warning | Best For |
|---|---|---|---|
| **SSH Tunnel** (`localhost`) | ✅ Easiest | None | Quick access, single user |
| **Self-signed cert** | 🟡 Medium | Once per browser | Always-on LAN access |
| **Caddy reverse proxy** | 🟡 Medium | None after CA install | Cleanest setup |

## ✅ Quickest Fix Right Now

Just revert `gateway.bind` back to `loopback` and **always use SSH tunnel**:

```bash
openclaw gateway stop
openclaw config set gateway.bind loopback
openclaw gateway start
```

Then from your main PC:

```bash
ssh -N -L 18789:127.0.0.1:18789 lzw@192.168.1.36
```

Open: `http://localhost:18789` — works perfectly, no HTTPS needed, most secure.