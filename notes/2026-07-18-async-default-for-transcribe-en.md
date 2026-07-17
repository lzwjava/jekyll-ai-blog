---
audio: false
generated: true
image: false
lang: en
layout: post
title: Async default for transcribe
translated: false
type: note
---

Committed and pushed: `c4371e3`.

Now `ww gcp-speech transcribe` defaults to **async mode** — uploads file, submits the job, prints the GCS output path and console link, then exits immediately. No waiting.

```bash
# Async (default) — submit and go check the console later
ww gcp-speech transcribe wh1_merged.mp3 --lang cmn-Hans-CN

# Wait mode — blocks until done, downloads, prints transcript
ww gcp-speech transcribe wh1_merged.mp3 --lang cmn-Hans-CN --wait
```

The console link points to the GCS bucket folder where results will appear. Once done, you can also grab results manually with `gsutil cp` and convert with `ww transcript`.
