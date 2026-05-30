---
audio: false
generated: true
image: false
lang: en
layout: post
title: WeChat Group Aliases Versus Mini Programs
translated: false
type: note
---

**Question:** In WeChat, can you set a group alias (like `#小程序：疗愈手帐`) so that when people @ that person, the text message contains a clickable link that opens a Mini Program directly?

**Answer:**

No, that's not how it works. You're conflating two separate WeChat features:

## What `#小程序：疗愈手帐` actually is

That's a **Mini Program message card** shared into a group chat — not a person's alias. When someone shares a Mini Program into a chat, it renders as a rich card with the `#小程序` prefix and the app name. Tapping it launches the Mini Program.

It looks like a message, but it's a **special message type** (`miniprogram` type in the WeChat message protocol), not a text message with a link.

## What "group alias" actually does

WeChat's group alias (群昵称) lets you set a **display name for yourself within a specific group** — e.g., you show up as "张工" in a work group instead of your real name. When someone @s you, the `@张工` text appears. That's it — plain text mention, no Mini Program link.

## Can you @ trigger a Mini Program?

**No.** There's no native WeChat feature that lets you set a group alias such that @-mentioning you inserts a Mini Program deep link. The two systems are completely separate:

| Feature | What it does |
|---|---|
| Group alias | Changes your display name in one group |
| Mini Program share card | Sends a `miniprogram` message type into chat |
| @ mention | Inserts plain text `@name` into message box |

## If you want people to easily open a Mini Program from a group

The right approach is:

1. **Share the Mini Program card directly** — tap `+` → Mini Programs → share to group. People tap the card to launch it.
2. **Use a Mini Program URL Scheme / URL Link** — generate a link via WeChat's API (`urllink.generate`) that opens in browser and redirects to the Mini Program. But WeChat intentionally blocks these from being tappable in group chat text messages.
3. **WeChat Channel / official account post** — embed Mini Program links there; those are tappable.

The bottom line: what you saw (`#小程序：疗愈手帐`) was someone sharing the Mini Program as a message card, not a person being @-mentioned.