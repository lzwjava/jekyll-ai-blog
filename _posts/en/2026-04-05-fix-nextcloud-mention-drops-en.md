---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fix Nextcloud Talk Mention Drops
translated: false
type: note
---

Here's the flow that causes the drop:

1. `extensions/nextcloud-talk/src/inbound.ts:206-211` — for group rooms, `resolveNextcloudTalkRequireMention()` is called
2. `extensions/nextcloud-talk/src/policy.ts:105-116` — this defaults to `true` if no room-level or wildcard config overrides it
3. `extensions/nextcloud-talk/src/inbound.ts:220-222` — if `mentionGate.shouldSkip` is true, the message is dropped with the log you're seeing

The mention check uses `buildMentionRegexes` to look for patterns like `@OpenClaw` in the message body. If no match → `wasMentioned = false` → gate drops it.

## How to fix it (without code changes)

Set `requireMention: false` on the room or wildcard config:

```bash
openclaw config set channels.nextcloud-talk.rooms.eu42ecdy.requireMention false
```

Or for all rooms:

```bash
openclaw config set channels.nextcloud-talk.rooms.*.requireMention false
```

## How to check / debug

- Watch the gateway log for the `nextcloud-talk: drop room` line — that confirms messages are arriving but being gated
- To verify mention detection, send a message with `@OpenClaw hello` in the Nextcloud room — if the bot's display name matches the mention regex, it should pass the gate
- Check what mention patterns are configured: look at `channels.nextcloud-talk.mentions` in your config (or the global `mentions` config)

The simplest path: either set `requireMention: false` for that room, or use the bot in a 1:1 DM where the mention gate is skipped entirely (`isGroup` would be `false` at line 206).
