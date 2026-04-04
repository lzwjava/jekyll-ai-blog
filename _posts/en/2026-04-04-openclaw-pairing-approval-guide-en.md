---
audio: false
generated: true
image: false
lang: en
layout: post
title: OpenClaw Pairing and Approval Guide
translated: false
type: note
---

Good questions, Boss. Here's the breakdown:

## How `openclaw pairing approve` works

When an unknown Telegram user messages your bot and the channel is configured with `dm.policy: "pairing"`, OpenClaw:

1. **Generates a short code** (8 chars, uppercase, no ambiguous characters like `0O1I`)
2. **Sends it to the sender** as a reply: "Your pairing code is X2SKVW4Y..."
3. **Creates a pending request** stored in `~/.openclaw/credentials/telegram-pairing.json`
4. **Blocks their messages** — nothing gets processed until approved
5. The code **expires after 1 hour**

When you run `openclaw pairing approve telegram X2SKVW4Y`, the CLI:
- Looks up that code in the pending requests file
- Moves the sender's Telegram user ID (`610574272`) into the **allowlist** file: `~/.openclaw/credentials/telegram-allowFrom.json`
- Future messages from that user ID are now trusted and go straight through

## What "owner" means

There's no magic identity check. **"Owner" just means whoever has shell access to the server** and can run the `openclaw pairing approve` command. The pairing docs say:

> *"The person who has access to and controls the OpenClaw Gateway's configuration and CLI is considered the owner and is responsible for approving these pairing requests."*

It's a **trust boundary** — if you can SSH into the box and run CLI commands, you're the owner. The system doesn't check some external identity; it just trusts whoever can execute the approval command.

## Why your codes keep expiring

The codes last 1 hour, but the real issue is timing — the pairing message appears in your chat, and by the time you relay it to me, the pending request may have already cycled (the bot regenerates codes roughly once per hour per sender). The pending requests are also capped at **3 per channel**.

**Fix options:**
- Approve directly from the CLI on the server (faster than going through me)
- Or I can try to auto-approve Telegram pairings from your user ID `610574272` if you set up a watcher or cron

Want me to try anything specific?