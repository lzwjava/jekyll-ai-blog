---
audio: false
generated: true
image: false
lang: en
layout: post
title: WeChat Mini Program Mentions Hack
translated: false
type: note
---

**Question:** In WeChat, there's a message like `@#小程序:疗愈手帐 社群已分享🎉` that is directly clickable to open a Mini Program — how does this work?

**Answer:**

You're right, I was wrong. Let me correct this.

## What this actually is

This is a **WeChat group member whose display name (group alias) is set to `#小程序:疗愈手帐`**.

When someone sets their **群昵称 (group nickname)** to `#小程序:疗愈手帐`, and another person @s them, WeChat renders the `@#小程序:疗愈手帐` as a **tappable link** that opens the Mini Program — because WeChat's client recognizes the `#小程序:` prefix pattern in names/mentions and auto-renders it as a Mini Program shortcut.

## The trick

```
群昵称 → #小程序:疗愈手帐
```

- Go to a group → tap your name → edit group nickname
- Set it to `#小程序:疗愈手帐` (exact Mini Program name)
- Now when anyone @s you, the mention becomes a clickable Mini Program entry point

## Why it works

WeChat's rich text rendering in chat scans for `#小程序:` prefix and treats the following string as a Mini Program name to resolve. It's essentially a **rendering hack** — the @ mention text triggers the same rendering pipeline as a shared Mini Program card.

This is a known growth hack used by Mini Program operators to embed "passive" Mini Program links inside group chat @-mentions, driving re-engagement without users needing to explicitly share a card.
