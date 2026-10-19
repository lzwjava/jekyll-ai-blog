---
audio: false
generated: true
image: false
lang: en
layout: post
title: Newmine microphone fully detected
translated: false
type: note
---

Confirmed — your **Newmine** microphone is fully detected and usable:

- **System audio profile**: `Newmine` (MUSIC-BOOST), USB, 48 kHz, 1 channel
- **ffmpeg input device**: listed as `[1] Newmine` alongside your other mics

It's ready to record. For example, to capture 5 seconds of audio from it:

```bash
ffmpeg -f avfoundation -i ":1" -t 5 ~/test-newmine.wav
```

or a longer test:

```bash
ffmpeg -f avfoundation -video_size 1280x720 -i ":1" -t 10 ~/newmine-test.wav
```

Want me to run a quick recording test to make sure it's capturing sound properly?
