---
audio: false
generated: true
image: false
lang: en
layout: post
title: OpenClaw WhatsApp Setup Guide
translated: false
type: note
---

Here's the deal for WhatsApp on your setup, Boss:

## WhatsApp in OpenClaw

OpenClaw uses **WhatsApp Web (Baileys)** — it links to your WhatsApp account by scanning a QR code from the server. This works with both regular WhatsApp and WhatsApp Business on iOS.

### Steps

**1. Install the WhatsApp plugin** (if not already):

```bash
openclaw plugins install @openclaw/whatsapp
```

**2. Configure access policy** in your `openclaw.json`:

```json5
{
  channels: {
    whatsapp: {
      dmPolicy: "pairing",       // or "allowlist" if you pre-add your number
      allowFrom: ["+852XXXXXXXX"], // your phone number (E.164 format)
    },
  },
}
```

**3. Link via QR code:**

```bash
openclaw channels login --channel whatsapp
```

This will display a QR code in your terminal. On your iPhone:

- Open **WhatsApp** (or WhatsApp Business)
- Go to **Settings → Linked Devices → Link a Device**
- Scan the QR code

**4. Start the gateway:**

```bash
openclaw gateway
```

**5. First message = pairing** (if using `pairing` policy):
Message your linked WhatsApp number from your phone, it'll give you a code, then:

```bash
openclaw pairing list whatsapp
openclaw pairing approve whatsapp <CODE>
```

### A few notes

- **Dedicated number recommended** — using a separate WhatsApp number for OpenClaw avoids self-chat confusion. But personal number works too.
- **WhatsApp Business is fine** — same linking process, no difference.
- Since you keep hitting the pairing code expiry problem, consider using `dmPolicy: "allowlist"` with your number pre-filled — skips pairing entirely.
- After linking, the session persists (Baileys stores creds in `~/.openclaw/credentials/whatsapp/`). No need to re-scan unless you unlink.

Want me to set this up for you? I can edit the config and kick off the login flow. 🦞
