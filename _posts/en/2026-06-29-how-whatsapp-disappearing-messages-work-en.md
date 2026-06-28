---
audio: false
generated: true
image: false
lang: en
layout: post
title: How WhatsApp Disappearing Messages Work
translated: false
type: note
---

Question: How do disappearing messages in WhatsApp work?

Answer:

Disappearing messages auto-delete after a set timer (24 hours, 7 days, or 90 days) from when they're sent. Here's the mechanics:

**Timer is sender-controlled, applied per-chat (or default)**
- You enable it per-conversation, or set a global default for new chats.
- When enabled, the timer starts at **send time**, not read time. A 7-day message sent Monday vanishes the following Monday regardless of whether the recipient opened it.

**It's metadata in the message envelope, enforced client-side**
WhatsApp uses the Signal Protocol for E2EE. The disappearing-message setting is propagated as a protocol-level field. Two relevant pieces:
- An `ephemeralSettingTimestamp` / expiration field travels with messages so all clients in the chat agree on the timer.
- Each client runs a local expiration job that deletes the message from its own SQLite store (`msgstore.db` on Android) when the timer fires.

Because enforcement is client-side, the guarantee is **cooperative, not cryptographic**. The server doesn't hold plaintext (it can't — E2EE), but nothing stops a non-cooperating client from retaining the message.

**What it does NOT protect against**
- **Screenshots / screen recording** — no detection or blocking on standard messages (unlike View Once, which now blocks screenshots on supported clients).
- **Forwarding before expiry** — a forwarded disappearing message loses the timer in the destination chat.
- **Quoting** — replying-with-quote can preserve the quoted text past expiry.
- **Backups** — messages already written to a cloud/local backup before deletion may survive there.
- **Notifications** — message preview text can linger in OS notification logs.
- **A modified/patched client** that simply ignores the expiration field.

**Group chats**
Any member can change the timer (unless the admin restricts it to admins). Changes apply going forward, not retroactively.

**Threat model takeaway**
Disappearing messages reduce *passive accumulation* of history on honest devices. They are not a defense against a motivated recipient. If you need stronger guarantees, the architectural truth is that **you can't enforce deletion on a device you don't control** — the recipient's client has the plaintext, so any "self-destruct" is a UX convention, not a security primitive. View Once is slightly stronger (single render + screenshot blocking) but still defeatable by a second camera.

References:

- [WhatsApp Help: About disappearing messages](https://faq.whatsapp.com/673193694148537)
- [Signal Protocol overview](https://signal.org/docs/)
