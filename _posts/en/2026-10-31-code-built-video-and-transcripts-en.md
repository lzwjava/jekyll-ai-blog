---
audio: false
generated: true
image: false
lang: en
layout: post
title: Code-Built Video and Transcripts
translated: false
type: note
---

Done. Everything is shipped. Here's what you have in `/Users/lzwjava/projects/video-factory`:

## 🎬 Video (code-built, no CapCut)

**`output/announcement.mp4`** — 1920×1080, 30fps, **55 seconds**, silent track (record your own voiceover over it if you want)

- 5 scenes: Intro → Truth Lab → Truth Software → Blog/Portfolio → CTA
- **Bilingual: every slide and caption shows English + 中文** (`求真实验室` / `Truth Lab`, etc.), so it works muted on WeChat too
- Dark typographic style matching truthlab.cc (#0a0a0b + gold #e3b341), Inter + Menlo + Hiragino fonts, subtle Ken-Burns motion, caption bars with fade in/out

**Rebuild anytime** — all content lives in `scenes.json` (durations, titles, bullets, captions EN+ZH). Just edit and run:

```bash
python3 render_slides.py && python3 build_video.py
```

## 📝 Transcripts

- **`transcript.md`** — the full English narration script (WeChat + YouTube copy, hashtags, chapter timestamps)
- **`deliver-transcription.md`** — transcription of your voice memo `deliver.m4a` (8:45), bilingual: cleaned Chinese with timestamps + English translation, plus raw ASR appendix

## 🔊 About the memo transcription

`deliver.m4a` was the user speaking — so I went to the RTX 4070 box (`lzw@192.168.1.36`), copied the memo over, and ran **openai-whisper large-v3** (GPU, 74s) — much cleaner than the local small model. Local CPU saw 90MB free VRAM earlier which was transient; large-v3 fit fine on retry. Raw outputs: `whisper_out/` (txt/vtt/srt/json). Your story came through well: 平方根科技 (2016–19), HSBC 16 months, housing debt, 13 exams + IELTS, CSTU master's, relaunching 求真软件 + 求真实验室, token-based pricing.

Note: your voice memo (8:45) tells a much bigger story than the 55s video — if you want a longer version or the memo translated into an English voiceover draft, just say the word.
