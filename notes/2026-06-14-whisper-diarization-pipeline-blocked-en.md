---
audio: false
generated: true
image: false
lang: en
layout: post
title: Whisper Diarization Pipeline Blocked
translated: false
type: note
---

Got it. Here's what happened last time:

== SUMMARY ==

1. Created ww/audio/whisper_diarize.py — a new module using whisperx Python API
   with 3-step pipeline: transcribe → align timestamps → diarize with pyannote.

2. Wired it into ww/main.py as `ww whisper diarize <file>` (alongside existing
   `ww whisper`, `ww whisper refine`, `ww whisper organize`).

3. Added help text in main.py and updated zsh completions at
   /home/lzw/projects/ww/completions/_ww

4. Installed whisperx into ~/projects/whisper-playground/.venv/ (the playground's
   venv, not the ww project's venv).

5. Tested with ~/projects/whisper-playground/yangyang/yangyang.mp4 but BLOCKED:
   - The faster-whisper-large-v3 model (~3GB) download kept stalling mid-download
     (network/proxy issue to HuggingFace CDN)
   - Got to ~2.8GB multiple times then froze
   - The `base` model loaded fine (small ~150MB), proving CUDA works on the RTX 4070

6. Session ended with two options presented:
   A) Download large-v3 with aria2c (multi-connection, faster)
   B) Use `medium` model (~1.5GB, still good accuracy for Chinese)

   You never picked — the session ran out of iterations.

== WHAT'S LEFT ==

- Unblock the large-v3 model download (aria2c is the cleanest path)
- Run the actual diarization on yangyang.mp4
- Verify output in yangyang/out/

Want me to pick up where we left off? I'd go with aria2c for the large-v3 download — it's the proven workaround for this machine's HF download stalling issue (noted in memory).
