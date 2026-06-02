---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fixing WhatsApp QR Link Errors
translated: false
type: note
---

Question: What are the likely reasons WhatsApp QR code scanning fails with "unable to link," and how can I fix it?

Answer:

## WhatsApp "Unable to Link" — Causes & Fixes

### Why This Happens

The "unable to link" error after scanning a QR code typically comes from one or more of these causes:

---

### 1. **Stale / Corrupted Session Data** *(Already addressed)*
Old pre-keys, LID mappings, or auth credentials from previous sessions confuse the pairing handshake.

**Fix:** You already did this — `rm -rf credentials/whatsapp/default/*` and generating a fresh QR. ✅

---

### 2. **Proxy / IP Reputation Block**
WhatsApp's servers perform risk checks on the IP used during the linking handshake. **Data center IPs, VPNs, and proxy exits are frequently flagged.**

Symptoms:
- QR displays fine (WebSocket connection works)
- Scan succeeds on phone side
- Server rejects the pairing response silently → "unable to link"

**Fixes to try:**
- Use a **residential proxy** instead of a data center one (mihomo/clash on port 7891 may route through a DC IP)
- Try linking **without the proxy** if your server has direct internet access
- Switch the proxy exit node to a region matching your phone's SIM country

---

### 3. **QR Code Expiry**
WhatsApp QR codes expire in ~20–60 seconds. If there's any latency between generation and scan, it's already dead.

**Fix:** Scan immediately after the QR renders. Your Node.js + proxychains script should auto-refresh on expiry.

---

### 4. **Clock Skew (Time Sync)**
The pairing handshake is time-sensitive. If the server clock is off by >30s, WhatsApp rejects it.

**Fix:**
```bash
sudo timedatectl set-ntp true
timedatectl status  # verify Synchronized: yes
```

---

### 5. **WhatsApp Version / Protocol Mismatch**
The library generating the QR (likely `@whiskeysockets/baileys` or similar) must use an **up-to-date WA Web version string**. Outdated versions get rejected server-side.

**Fix:**
```bash
# Check your library version
npm list @whiskeysockets/baileys

# Update to latest
npm install @whiskeysockets/baileys@latest
```

---

### 6. **Phone-Side Restrictions**
- The WhatsApp account may have **Linked Devices restricted** by admin policy (Business accounts)
- Too many failed linking attempts trigger a **temporary cooldown** on the account

**Fix:** Wait 30–60 minutes before retrying, or test with a different phone number.

---

### Recommended Retry Checklist

| Step | Action |
|------|--------|
| ✅ | Clear session data (done) |
| 🔲 | Verify server time is synced |
| 🔲 | Try without proxy first |
| 🔲 | Update Baileys/WA library |
| 🔲 | Scan within 15s of QR render |
| 🔲 | Wait 30min if repeated failures |
| 🔲 | Test with residential proxy exit node |

---

### Quick Diagnostic

Run this to check if your proxy exit IP is flagged:
```bash
proxychains4 curl -s https://ipinfo.io/json | grep -E '"ip"|"org"|"country"'
```
If `org` shows a hosting provider (AWS, Alibaba, DigitalOcean, etc.) — that's your problem. WhatsApp blocks DC IPs during device linking.
