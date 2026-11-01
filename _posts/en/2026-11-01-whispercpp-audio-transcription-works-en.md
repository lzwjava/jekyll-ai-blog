---
audio: false
generated: true
image: false
lang: en
layout: post
title: Whisper.cpp Audio Transcription Works
translated: false
type: note
---

Smoke run of whisper.cpp itself — audio → text. Everything works.

## 1. Basic transcription (WAV)

```
./build/bin/whisper-cli -m models/ggml-tiny.en.bin -f samples/jfk.wav
```

```
[00:00:00.000 --> 00:00:07.960]   And so my fellow Americans ask not what your country can do for you
[00:00:07.960 --> 00:00:10.760]   ask what you can do for your country.

load time = 148.84 ms | encode = 890.24 ms | decode = 38.99 ms | total = 1951.03 ms
```

Correct transcript, ~1.95 s for 11 s of audio (tiny.en, 4 threads, Vulkan backend present but CPU path used).

## 2. MP3 input (miniaudio decode path)

```
./build/bin/whisper-cli -m models/ggml-tiny.en.bin -f samples/jfk.mp3 -nt
→ And so my fellow Americans ask not what your country can do for you, ask what you can do for your country.
```

## 3. Output formats

`-osrt -ovtt -oj -of /tmp/jfk` produced valid `.srt`, `.vtt`, `.json`:

```
1
00:00:00,000 --> 00:00:07,960
 And so my fellow Americans ask not what your country can do for you

2
00:00:07,960 --> 00:00:10,760
 ask what you can do for your country.
```

## 4. Other flags / examples

| Run | Result |
| --- | --- |
| `-t 2 -bs 1 -np` (greedy, 2 threads) | same text, segments snapped to 8.0/11.0 s |
| `-ml 1` (word timestamps) | OK |
| `whisper-vad-speech-segments -vm models/for-tests-silero-v6.2.0-ggml.bin -f samples/jfk.wav` | detected 4 speech segments (0.32–2.27 s, 3.27–4.41 s, 5.38–7.68 s, 8.16–10.62 s) |

## Notes

- Only real model on disk is `models/ggml-tiny.en.bin` (English-only), so no multilingual/translate test; the `for-tests-ggml-*.bin` files are empty stubs (they load but produce `""`, as intended for CI).
- Only `samples/jfk.wav` / `jfk.mp3` are available; no `espeak`/`ffmpeg`/`sox` installed to synthesize extra audio.
- Working tree left clean (temp outputs written to `/tmp`).

Verdict: audio→text works end to end (WAV + MP3 in, plain/SRT/VTT/JSON out, VAD segmentation OK).
