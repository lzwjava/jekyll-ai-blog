---
audio: false
generated: true
image: false
lang: en
layout: post
title: Done-Sound Extension Installed
translated: false
type: note
---

Installed. The `done-sound` extension is now in place at `~/.pi/agent/extensions/done-sound.ts` (live config), alongside the existing `note` extension.

Notes on this extension's behavior on macOS:

- It plays a sound when the agent truly settles (`agent_settled` event), after queued follow-ups are drained.
- Defaults to Linux sound paths and Linux audio players. On your Mac you'll likely want to override with:
  - `PI_DONE_SOUND_FILE` (e.g. `/System/Library/Sounds/Glass.aiff`)
  - `PI_DONE_SOUND_CMD` (e.g. `afplay /System/Library/Sounds/Glass.aiff`) — this bypasses player auto-detection entirely, which is the simplest reliable option on macOS.
- You can test/toggle with `/done-sound`, `/done-sound on|off`, `/done-sound status`.

Restart pi (or reload the session) for the new extension to be picked up.
