---
audio: false
generated: true
image: false
lang: en
layout: post
title: Bots Don't Appear as Contacts
translated: false
type: note
---

**Question:** In Nextcloud Talk, why does enabling a bot in conversation settings not show the bot as a contact or participant — it seems like nothing happened?

**Answer:**

This is a very common point of confusion, and it comes down to how Nextcloud Talk bots are fundamentally designed. They work **completely differently from regular user contacts**.

---

## Why Bots Don't Appear as Contacts

### 1. Bots Are Webhook Listeners, Not Users

Nextcloud Talk bots are webhook-based. When you enable a bot in a conversation, Nextcloud Talk will send HTTP POST requests to the bot's registered webhook URL every time a message is sent in that room. The bot is not a Nextcloud user account — it has no profile, no avatar in the contacts list, and no presence indicator. It is simply an external service listening for events.

### 2. Enabling the Bot Just "Arms" the Listener

When you click **Enable** in the conversation's bot settings (as shown in your screenshot), you are telling Nextcloud Talk: *"For this conversation, start forwarding messages to the bot's webhook."* After adding the bot to a channel in Talk's settings, each input in that conversation is sent to the webhook URL. The webhook request includes important security headers — `X-Nextcloud-Talk-Signature` and `X-Nextcloud-Talk-Random` — which the bot uses to validate that messages are legitimate.

Nothing visually "joins" the conversation from the participants list. This is by design.

### 3. Bots Only React When Triggered

The bot will only appear to do something (e.g., post a message back into the conversation) **when the external webhook service actually responds**. When the bot receives a message, it validates the signature using the shared secret, processes the message, and then sends a response back to the conversation via the Talk API. If the bot's backend service is down, misconfigured, or not listening — you will see absolutely nothing happen, which makes it look like enabling the bot did nothing.

---

## Common Reasons It Looks Like "Nothing Happened"

| Reason | Explanation |
|---|---|
| Bot backend not running | The webhook URL points to a service that is offline or unreachable |
| Webhook URL not accessible | Nextcloud cannot reach the URL (e.g., firewall, wrong IP) |
| Signature mismatch | Bot rejects messages due to wrong shared secret |
| No trigger condition met | Some bots only respond to specific commands (e.g., `@bot hello`) |
| Missing AI/Assistant config | For AI-powered bots like the Assistant Talk Bot, the Nextcloud Assistant must be fully configured and working, and the bot must be enabled per room — the setup is not straightforward |

---

## What You Should Actually See After Enabling

- The bot **does not appear** in the participants/contacts list
- The bot **does not show** as online
- You should only see the bot's effect when it **posts a message** into the chat in response to a trigger
- Even mentioning the bot with `@botname` may not work if the bot is not correctly configured end-to-end

---

## How to Verify the Bot Is Working

1. Check that the external service the bot points to is running and reachable from your Nextcloud server
2. Run `occ talk:bot:list` on the server to confirm the bot is registered and check its `error_count`
3. Send a message in the conversation that the bot is supposed to react to
4. Check Nextcloud server logs for any webhook delivery errors

---

## Summary

Enabling a bot in Nextcloud Talk conversation settings is **not the same as adding a contact or participant**. The bot is an invisible webhook integration — it only becomes visible when it actively posts a message in response to a trigger. If you see nothing after enabling it, the issue is almost always that the bot's backend service is not reachable or not correctly set up.

**References:**

- [Nextcloud Talk Bots and Webhooks — Official Docs](https://nextcloud-talk.readthedocs.io/en/latest/bots/)
- [Assistant Talk Bot not responding — Nextcloud Community](https://help.nextcloud.com/t/assistant-talk-bot-not-responding-in-conversation-nextcloud-32-aio/235498/1)
- [Unable to mention bot on Nextcloud Talk — Nextcloud Community](https://help.nextcloud.com/t/unable-to-mention-bot-on-nextcloud-talk/241841)
- [Nextcloud Custom Bot walkthrough — Raspi Playground](https://koscis.wordpress.com/2025/12/07/nextcloud-custom-bot-part-1/)