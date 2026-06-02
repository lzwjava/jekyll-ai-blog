---
audio: false
generated: true
image: false
lang: en
layout: post
title: Add WhatsApp to OpenClaw Guide
translated: false
type: note
---

Question: How do I change or add a new channel in OpenClaw, specifically to add WhatsApp?

Answer:

## Adding WhatsApp as a Channel in OpenClaw

OpenClaw supports multiple channels (WhatsApp, Telegram, Discord, Slack, etc.) running from a single Gateway instance. Here is a complete guide to adding WhatsApp.

---

### How It Works

OpenClaw connects to WhatsApp using the Baileys protocol (WhatsApp Web-based). It uses the "Linked Devices" flow — the same feature used by WhatsApp Web. You scan a QR code and WhatsApp links your OpenClaw instance as a companion device. No official WhatsApp Business API is required.

---

### Method 1: Quick Setup via `openclaw onboard` (Recommended for New Setup)

Run the following command in your terminal:

```bash
openclaw onboard
```

After running this command, use arrow keys to navigate the interactive menu:
1. When prompted to **Select channel**, choose **WhatsApp (QR link)** and press Enter.
2. Select **Yes** when asked to confirm.
3. **Scan the QR code** with your WhatsApp phone — go to WhatsApp → Settings → Linked Devices → Link a Device.
4. If the QR code is distorted, try increasing screen brightness or adjusting page/zoom size.

---

### Method 2: Add WhatsApp to an Existing OpenClaw Setup (via Config)

**Step 1 — Edit your config file**

Open your config file and add the WhatsApp channel block:

```json
{
  "channels": {
    "whatsapp": {
      "dmPolicy": "pairing",
      "allowFrom": ["+15551234567"],
      "groupPolicy": "allowlist",
      "groupAllowFrom": ["+15551234567"]
    }
  }
}
```

The config file is typically located at `~/.openclaw/openclaw.json`.

**Step 2 — Log in / Link your WhatsApp account**

Run the login command:

```bash
openclaw channels login
```

A QR code will appear. Scan it using WhatsApp on your phone via **Settings → Linked Devices → Link a Device**. Credentials are saved to `~/.openclaw/credentials/whatsapp/`.

**Step 3 — Start the Gateway**

```bash
openclaw start
```

After the gateway is running, watch the logs for "WhatsApp connected" to confirm the link is active.

---

### Access / DM Policy Options

The `dmPolicy` field controls who can message your assistant:

- **`pairing`** (default) — Users must be approved via a pairing request. Pairing requests expire after 1 hour, and pending requests are capped at 3 per channel.
- **`allowlist`** — Only numbers listed in `allowFrom` can message.
- **`open`** — Anyone can message (requires `allowFrom` to include `"*"`).
- **`disabled`** — No DMs allowed.

---

### Running Multiple Channels at Once

You run one OpenClaw Gateway instance and configure multiple channels. Messages from each channel are routed into sessions, and replies go back through the originating channel. This means you can talk to the same assistant from WhatsApp on your phone, Telegram on your laptop, Discord with your team, and Slack at work — same brain, same memory, same agent.

---

### Troubleshooting

| Problem | Solution |
|---|---|
| QR code expired | Rerun `openclaw channels login` and scan immediately |
| Bot not responding | Run `openclaw channels status` to check link status |
| Connection dropping | Remove unused linked devices in WhatsApp → Linked Devices, then re-login |
| Not linked after restart | Delete `~/.openclaw/credentials/whatsapp/` and run `openclaw channels login whatsapp` again |
| General issues | Run `openclaw doctor` to diagnose environment/runtime problems |

---

### Security Note

Because WhatsApp integration relies on third-party packages, verify you are installing the **official Baileys package** and not a lookalike. In late 2025, a malicious npm package named "lotusbail" impersonated a WhatsApp Web API library and stole credentials. A dedicated phone number is also recommended to keep your personal chats separate from the bot.

References:

- [OpenClaw WhatsApp Official Docs](https://docs.openclaw.ai/channels/whatsapp)
- [Step-by-step QR Code Connection Guide – LumaDock](https://lumadock.com/tutorials/connect-openclaw-to-whatsapp-qr-code)
- [Multi-channel Setup Guide – LumaDock](https://lumadock.com/tutorials/openclaw-multi-channel-setup)
- [Getting Started with OpenClaw and WhatsApp – MarkTechPost](https://www.marktechpost.com/2026/02/14/getting-started-with-openclaw-and-connecting-it-with-whatsapp/)
- [OpenClaw Add WhatsApp – GoPenAI Blog](https://blog.gopenai.com/openclaw-add-whatsapp-27d9237d3872)
- [DataCamp OpenClaw Tutorial](https://www.datacamp.com/tutorial/moltbot-clawdbot-tutorial)
