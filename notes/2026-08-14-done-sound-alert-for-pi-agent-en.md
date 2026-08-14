---
audio: false
generated: true
image: false
lang: en
layout: post
title: Done Sound Alert for PI Agent
translated: false
type: note
---

Everything works. Here's what I built.

## Summary

I created a pi extension that plays a sound when the agent finishes a turn and is waiting for input.

**File:** `/home/lzw/.pi/agent/extensions/done-sound.ts`

### How it works

- It hooks the **`agent_settled`** event. Per the pi docs, this is the right hook for "agent is truly done" — unlike `agent_end` (which the bundled `notify.ts` example uses), `agent_settled` fires only *once*, after all retries, auto-compaction, and queued steering/follow-up messages are drained. So you won't get spurious beeps mid-work.
- On settle, it auto-detects an available Linux player (`pw-play` → `paplay` → `ogg123` → `aplay` → `ffplay` → `mpv` → `vlc`) and plays a default sound (`/usr/share/sounds/freedesktop/stereo/complete.oga`), falling back across GNOME/Yaru sound themes.
- It spawns the player **detached** (`child.unref()`) so it never blocks pi or keeps the process alive, and swallows errors (sound is best-effort).
- It skips in `print` mode (`-p`) where there's no human waiting.

### Commands it adds

- `/done-sound` — play a test beep
- `/done-sound on` / `/done-sound off` — enable/disable for this process
- `/done-sound status` — show current state, file, and player

### Configuration (optional env vars)

- `PI_DONE_SOUND_FILE` — path to a custom sound file
- `PI_DONE_SOUND_CMD` — a full custom play command, e.g. `aplay /custom/done.wav` (overrides file detection)
- `PI_DONE_SOUND_ENABLED=0` — start disabled

### Verification

I confirmed the module loads under jiti (pi's loader) and registers the `agent_settled` handler plus the `/done-sound` command, and that `pw-play` + `complete.oga` actually plays on your system.

### Activate it

Since it's in `~/.pi/agent/extensions/` (the global auto-discovery location), either **restart pi** or run **`/reload`** inside a running session. Then just talk to pi — when it finishes responding, you'll hear the sound. Run `/done-sound` to test it immediately, and `/done-sound status` to confirm the detected player.

Want a different sound (e.g. a custom chime), or to *also* fire on per-turn completion (each `turn_end`) instead of only when fully settled? I can adjust it.
