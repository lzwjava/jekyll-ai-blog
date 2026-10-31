---
audio: false
generated: true
image: false
lang: en
layout: post
title: Gitignore to keep only source files
translated: false
type: note
---

Created `.gitignore` in `/Users/lzwjava/projects/video-factory/.gitignore`. Git status confirms only source/text files remain visible — all binaries and generated artifacts are now ignored:

- **macOS junk**: `.DS_Store`
- **Audio + derived transcription files**: `deliver.m4a`, `deliver.wav`, `deliver.wav.{srt,txt,vtt}`
- **Generated dirs**: `whisper_out/`, `output/` (video + segments), `slides/` (rendered PNGs)
- **Font binaries**: `fonts/`

Keeping in version control: `build_video.py`, `render_slides.py`, `scenes.json`, `transcript.md`, `deliver-transcription.md`, and `.gitignore` itself.

One note: I ignored `fonts/` since they're 2MB of binary files — if you'd rather commit them as build dependencies, remove that line.
