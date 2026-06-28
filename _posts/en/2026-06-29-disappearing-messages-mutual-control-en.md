---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Disappearing Messages: Mutual Control"
translated: false
type: note
---

Question: Both parties can set disappearing messages, right? (i.e., it's mutual control)

Answer:

Yes — in a 1:1 chat, **either party can turn it on or off, and either party can change the timer**. It's not owned by whoever started it.

Key points:

- **Symmetric control.** Both sides have equal power over the setting. If you set 7 days and the other person switches it to off (or to 24 hours), that change applies to the whole conversation going forward.
- **Last-write-wins.** The setting is a shared per-chat state synced via the message protocol. The most recent change by either party is the active one. There's no "my preference vs. yours" — it's one shared value.
- **Both get notified.** When either side changes it, an in-chat system message appears ("X changed the disappearing message timer..."), so it can't be done silently.
- **Not retroactive.** Changing the timer only affects messages sent *after* the change. Messages already sent keep their original timer.
- **No override / lock.** Neither party can force the other to keep it on. There's no admin role in a 1:1 chat, so you can't prevent the other person from disabling it.

So practically: if you want messages to disappear, the other person can unilaterally undo that. It only "works" as long as both sides cooperate — which ties back to the threat-model point from before: it's a mutual convention, not something one party can enforce on the other.

In **groups**, it differs — by default any member can change it, but admins can restrict the setting to admins-only via group permissions.

References:

- [WhatsApp Help: About disappearing messages](https://faq.whatsapp.com/673193694148537)
