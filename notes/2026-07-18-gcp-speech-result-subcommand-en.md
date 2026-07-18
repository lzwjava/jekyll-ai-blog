---
audio: false
generated: true
image: false
lang: en
layout: post
title: GCP speech result subcommand
translated: false
type: note
---

All changes are in place. Here's a summary of what was done:

**Changes made:**

1. **`ww/gcp_speech/result.py`** (new file) — the `ww gcp-speech result <job-id>` command:
   - Looks up the job ID in `~/.ww_gcp_jobs.json` (the local jobs registry)
   - Checks GCS for completed transcription JSON files
   - If results exist: downloads them, prints the transcript, and saves a `.md` file alongside the original audio
   - If not yet complete: prints the console URL and suggests `--wait` to poll
   - Supports `--wait` flag for blocking mode (polls every 10s)

2. **`ww/gcp_speech/transcribe.py`** — modified to:
   - Print a clear `Job ID:` line in the output (the basename/filename-stem)
   - Save job info to `~/.ww_gcp_jobs.json` (operation name, GCS folder, audio file, language)
   - Direct users to `ww gcp-speech result <job-id> --wait` instead of `gsutil cp`

3. **`ww/main.py`** — added `result` subcommand routing and help text

4. **`~/.zsh/completions/_ww`** — added `result` to `gcp_speech_cmds` for tab completion

**Usage flow:**

```
ww gcp-speech transcribe ~/Downloads/recording.mp3
  → Prints: Job ID: recording
  → Saves job to ~/.ww_gcp_jobs.json

ww gcp-speech result recording
  → Checks GCS for results, prints transcript if ready

ww gcp-speech result recording --wait
  → Polls until complete, then prints transcript
```
