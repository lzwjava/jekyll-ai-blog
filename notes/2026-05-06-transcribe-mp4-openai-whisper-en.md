---
audio: false
generated: true
image: false
lang: en
layout: post
title: Transcribe MP4 with OpenAI Whisper
translated: false
type: note
---

No transcription command is wired into `ww main.py` yet. The existing `ww/audio/speech_to_text.py` uses Google Cloud Speech-to-Text with GCS uploads — heavyweight for a one-off local file.

For a 2-hour MP4, the easiest path is **OpenAI Whisper** (local, free, no cloud setup):

```bash
# Install once
pip install openai-whisper

# Run (large model = best accuracy, ~10-20 min on CPU)
whisper ~/Downloads/your-video.mp4 --model large --output_dir ~/Downloads
```

Or if you'd like a `ww transcribe` command built into the toolkit (using Whisper or the OpenAI Whisper API), I can add one. Which would you prefer?