---
audio: false
generated: true
image: false
lang: en
layout: post
title: Whisper Low Memory Module Wired Up
translated: false
type: note
---

All done. `ww whisper <file> --low-memory` is wired up. Summary of changes:

## Changes

**1. New module — `ww/audio/whisper_low_mem.py`**
Adapted your `transcribe.py` memory-safe loader (CPU checkpoint → GPU fp16 only, ~3.2 GB for large-v3) into a proper `main()` module. `whisper` is imported lazily with a friendly error if `openai-whisper` isn't installed. CLI:
```
ww whisper file.mp4 --low-memory [--model large-v3] [--language zh] [--task transcribe|translate] [--device cuda]
```
Writes `<stem>.txt/.srt/.json/.vtt/.tsv` next to the audio, same as your script.

**2. `ww/main.py`**
- Routing: `--low-memory` anywhere in argv is stripped and dispatched to `whisper_low_mem` (before the default `whisper_translate` fallback).
- Help text: added `ww whisper <file> --low-memory` line under the Whisper section.

**3. `~/.zsh/completions/_ww`**
The `whisper` file-completion case now also offers `--low-memory`, `--model`, `--language`, `--task`, `--device` flags. (Reload with `autoload -Uz compinit && compinit`.)

**4. `pyproject.toml`**
Added `openai-whisper>=20240930` — `uv sync` already run, installed `openai-whisper==20250625` cleanly (torch was already present via whisperx).

## Verified
- `uv run ruff check` — pass; `pyright` — 0 errors
- `uv run ww whisper --low-memory` → routes correctly (argparse shows the new module's usage)
- Missing-file error path works
- `zsh -n` completion syntax OK

Note: the model must be cached at `~/.cache/whisper/large-v3.pt` (download once with `whisper large-v3`); the loader will tell you if it's missing. The full transcription path needs your CUDA GPU, so test it on the workstation.
