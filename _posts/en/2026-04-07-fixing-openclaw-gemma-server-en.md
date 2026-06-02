---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fixing OpenClaw's Gemma Server Issues
translated: false
type: note
---

## What happened

OpenClaw has a `llama-server` provider configured in `openclaw.json` pointing to `http://192.168.1.36:8081/v1` with the model `gemma-4-26B-A4B-it-UD-IQ3_S.gguf`. When you sent "hi" via OpenClaw, it failed because of two issues:

### Issue 1: llama-server wasn't running

The process wasn't started. The old `~/llama.sh` script starts a different model (DeepSeek-R1-Distill-Llama-8B) on port 8000, not Gemma on 8081. So the config update to switch to Gemma was done, but nobody started the actual server.

### Issue 2: Gemma 4's thinking mode

Even after starting llama-server, Gemma 4 has a built-in "thinking" mode. By default (`--reasoning auto`), llama-server detects this from the model template and splits output into:
- `message.reasoning_content` — the thinking/chain-of-thought
- `message.content` — the final answer

With the default `auto` setting, the `content` field came back empty and all text went to `reasoning_content`. OpenClaw reads `content`, so it looked like the model returned nothing.

With `--reasoning-format none`, the thinking tokens leaked into `content` as raw `<|channel>thought` markup — still broken.

### The fix

Started llama-server with `--reasoning off`, which disables thinking entirely:

```bash
nohup /home/lzw/projects/llama.cpp/build/bin/llama-server \
  -m /home/lzw/projects/llama.cpp/models/gemma-4-26B-A4B-it-UD-IQ3_S.gguf \
  --port 8081 -c 32768 --reasoning off \
  >> /home/lzw/llama-server.log 2>&1 &
```

This produces clean responses in `content` with no thinking artifacts.

### What to watch out for

- The server won't survive a reboot. You may want to update `~/llama.sh` or create a systemd service for persistence.
- `--reasoning off` disables chain-of-thought entirely, which may reduce quality on complex reasoning tasks. If you want thinking but also want OpenClaw compatibility, the alternative is to configure the model as `"reasoning": true` in `openclaw.json` so OpenClaw reads `reasoning_content`, then use `--reasoning-format deepseek` instead.
- Context window is set to 32K (`-c 32768`) matching the openclaw.json config. The model's native training context is 262K, but the quantized IQ3_S at 26B params would need significant RAM for larger contexts.
