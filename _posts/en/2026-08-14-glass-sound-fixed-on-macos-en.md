---
audio: false
generated: true
image: false
lang: en
layout: post
title: Glass Sound Fixed on macOS
translated: false
type: note
---

Fixed. You should have heard the Glass sound just now.

## What was wrong

The extension was written **Linux-only**. On your macOS machine:

- The default sound file `/usr/share/sounds/freedesktop/stereo/complete.oga` doesn't exist.
- The Linux players (`pw-play`, `paplay`, `aplay`, …) aren't on the PATH — only homebrew's `ffplay`/`vlc` were, and they were being handed a non-existent file path, so they failed silently (the extension swallows all errors by design).

Result: `detectPlayer()` returned `ffplay`/`vlc`, `resolveSoundFile()` returned the missing Linux file, the spawn failed, and you heard nothing.

## What I changed in `pi/agent/extensions/done-sound.ts`

1. Added `isMacOS = process.platform === "darwin"` detection.
2. Put macOS-native **`afplay`** first in the player candidates (only on macOS), ahead of the Linux players. `afplay` ships with macOS and handles `.aiff`/`.wav`/`.mp3`/`.m4a` natively.
3. Split the sound-file fallback chain by platform:
   - **macOS:** `/System/Library/Sounds/Glass.aiff` → `Hero` → `Ping` → `Submarine` → `Tink`
   - **Linux:** the original freedesktop/Yaru chain (unchanged).
4. The default file constant now points at `Glass.aiff` on macOS and the original Linux file otherwise.

Linux behavior is completely unchanged; macOS now works out of the box.

## Trying it in Pi

Reload the extension (restart Pi or `/reload` if available), then run:

```
/done-sound          # play a test sound
/done-sound status   # should show: enabled | file: /System/Library/Sounds/Glass.aiff | player: afplay
```

## Optional customization

If you want a different sound, set in `pi/agent/settings.json` env or your shell:

```
PI_DONE_SOUND_FILE=/System/Library/Sounds/Ping.aiff
```

or a custom command:

```
PI_DONE_SOUND_CMD=afplay /System/Library/Sounds/Hero.aiff
```

Want me to wire `PI_DONE_SOUND_FILE` into `pi/agent/settings.json` so it's set automatically, or pick a different default sound (e.g. `Hero` or `Ping`)?
