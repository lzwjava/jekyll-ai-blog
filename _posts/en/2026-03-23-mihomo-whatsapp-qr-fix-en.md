---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fixing WhatsApp QR Code with Mihomo
translated: false
type: note
---

Question: How do I fix the WhatsApp macOS QR code not loading issue when using a Mihomo proxy?

Answer:

Based on your conversation log, the root cause is your **Mihomo proxy interfering with WhatsApp's connection to its servers**. Here is the complete step-by-step fix:

---

## Step 1 — Fix the Mihomo Config (Route WhatsApp Correctly)

Your config already has the WhatsApp rules, but they were toggled between `DIRECT` and `Proxy`. The right choice depends on your network situation:

**Option A: Route WhatsApp through the proxy (recommended if direct internet is restricted in your region)**

Edit `~/.config/mihomo/config.yaml` and make sure these lines exist **before** the `RULE-SET,Global` line:

```yaml
- DOMAIN-SUFFIX,whatsapp.com,Proxy
- DOMAIN-SUFFIX,whatsapp.net,Proxy
- DOMAIN-SUFFIX,wa.me,Proxy
```

**Option B: Route WhatsApp directly (bypass proxy)**

```yaml
- DOMAIN-SUFFIX,whatsapp.com,DIRECT
- DOMAIN-SUFFIX,whatsapp.net,DIRECT
- DOMAIN-SUFFIX,wa.me,DIRECT
```

---

## Step 2 — Properly Restart Mihomo

The session log shows mihomo was killed mid-command. Do it cleanly:

```bash
# Kill existing mihomo process
pkill -f mihomo

# Wait a moment
sleep 2

# Restart mihomo (adjust path to your actual binary)
nohup /Users/lzwjava/projects/mihomo-darwin-amd64-v1-alpha-3035ae8 \
  -d /Users/lzwjava/.config/mihomo > /tmp/mihomo.log 2>&1 &

# Verify it's running
ps aux | grep -i mihomo | grep -v grep
```

---

## Step 3 — Reset WhatsApp Camera Permission

The conversation log also reveals the camera permission was reset with the wrong bundle ID. The correct one was already fixed:

```bash
tccutil reset Camera net.whatsapp.WhatsApp
```

---

## Step 4 — Restart WhatsApp

```bash
# Fully quit WhatsApp
osascript -e 'quit app "WhatsApp"'
sleep 2

# Reopen it
open -a WhatsApp
```

When WhatsApp opens, it should now prompt for camera permission — click **Allow**.

---

## Step 5 — Verify Connectivity

Test that WhatsApp servers are reachable through your proxy:

```bash
curl -I --proxy http://127.0.0.1:7890 https://web.whatsapp.com
```

If you get an HTTP `301` or `200` response, the proxy routing is working correctly.

---

## Fallback — Use Phone Camera Instead (No Mac Camera Needed)

If the QR code still does not appear, you can use WhatsApp Web in your browser instead — go to `web.whatsapp.com`, then scan the QR code using your phone's WhatsApp app via Settings > Linked Devices > Link a Device. This completely bypasses the Mac camera permission issue.

---

## Summary of Root Causes Found in Your Log

| Issue | Status | Fix |
| --- | --- | --- |
| Wrong bundle ID (`com.whatsapp.WhatsApp`) | ✅ Fixed | Use `net.whatsapp.WhatsApp` |
| WhatsApp domains not in proxy rules | ✅ Fixed | Added to config |
| Mihomo not restarted cleanly | ⚠️ Incomplete | Use `pkill -f mihomo` then restart |
| Camera permission not granted | ⚠️ Pending | Reset + reopen WhatsApp |

References:

- [How to fix WhatsApp not working on Mac - MacPaw](https://macpaw.com/how-to/fix-whatsapp-not-working-on-mac)
- [WhatsApp Web QR Code Not Working - TechViral](https://techviral.net/whatsapp-web-qr-code-not-working/)
- [WhatsApp Web QR Code Fix - HelpDeskGeek](https://helpdeskgeek.com/whatsapp-web-qr-code-not-working-8-fixes-to-try/)
