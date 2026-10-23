---
audio: false
generated: true
image: false
lang: en
layout: post
title: Rewrote README to fully match ww tool
translated: false
type: note
---

Done. I rewrote `README.md` to fully reflect the actual `ww` tool, verified against `uv run ww` help output.

**Key changes:**

1. **Martinized coverage — added 30+ missing command groups** (all verified against the tool's own help):
   - New groups: Help, Actions, AMD Dev Cloud, Appearance, Benchmark, Completion, Cook, Conversation, DB (command history), FFmpeg, Format, GCP Speech, Gen-video, HackerNews, Headphone, Hermes, Host, HuggingFace (hf), Inference, Keyboard, Maps, Markdown (md2img), Math, Memory, Monitor, News, Pi, Projects (replaced the outdated `update` group), Qwen, RunPod, SGLang, Torch, Transcript, Vision Model, Weather & Rain, X (Twitter), Zed

2. **Upgraded existing groups with missing subcommands**:
   - GitHub: `interests`, `profile`
   - Image: `face`
   - Ghostty: `focus`, `list`
   - Network: `speed`, `physical-speed`, `wifi-scan-best`
   - Linux: `screen-lock`, `switch-keys`
   - Sync: `ww`
   - Note: `--sync`, `--private`, `--code`, `process`, `status`, `clear`, `watch`, `html`
   - Whisper: `--low-memory`, `diarize`, `organize`
   - macOS: `alarm`
   - Screenshot: `--skip-analysis`, `--no-save`, `--area`

3. **Accuracy fixes**: corrected option defaults (`action` defaults to gh-pages.yml, `benchmark` SSH key path, `sglang` port, search engine flags, etc.) and added a `command groups` index with anchors for navigation.

Verified with a `comm` diff: every command in the README exists in the real tool, and no actual subcommands are missing.
