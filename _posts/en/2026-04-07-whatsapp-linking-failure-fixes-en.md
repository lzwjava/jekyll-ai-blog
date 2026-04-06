---
audio: false
generated: true
image: false
lang: en
layout: post
title: WhatsApp Linking Failure and Fixes
translated: false
type: note
---

Here's the rundown of what we've tried and where things stand:

## What's working
- `proxychains4 -f /etc/proxychains4.conf` successfully tunnels WhatsApp Web traffic through mihomo (port 7891)
- Node.js script reliably generates WhatsApp QR codes as PNG files

## What's NOT working
- **`openclaw channels login`** — CLI hangs during plugin loading (nextcloud-talk was the culprit — already removed from config)
- **Terminal QR display** — no tools available to render QR as ASCII art in the terminal (`qrcode-terminal` not installed, Python qrcode library installed but can't help since Baileys QR data only comes as PNG)
- **WhatsApp linking** — QR scans but WhatsApp says "unable to link" — this is the core problem

## Most likely cause of the linking failure
WhatsApp actively blocks logins from known proxy/VPN IPs. The mihomo proxy exit IP is likely flagged as a数据中心 (data center) or VPN IP, and WhatsApp rejects the link request at the server level — before even getting to the QR scan step.

## Options to try
1. **Direct connection** (no proxy) — if your server has a clean residential IP
2. **Different proxy** — a residential proxy instead of mihomo exit
3. **Phone hotspot** — run OpenClaw on your phone, or SSH from your phone's hotspot
4. **Link via phone** — some WhatsApp versions let you link via QR from within the app without going through web.whatsapp.com

The PNG QR approach still works fine for viewing/scanning — it's just not live in the terminal.