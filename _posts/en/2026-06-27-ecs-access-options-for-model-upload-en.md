---
audio: false
generated: true
image: false
lang: en
layout: post
title: ECS access options for model upload
translated: false
type: note
---

I can't SSH to `iZj6civepr8vf1085n7x0uZ` — it's an Alibaba Cloud ECS and I don't have its IP or credentials. I need to reach it to analyze the model contents.

Two options:

1. Give me the IP (run `curl ifconfig.me` on that machine) + confirm root SSH is allowed from here
2. Upload directly from that machine — I'll give you the exact commands to run

For option 2, here's what to run on that ECS as root:

```bash
# Install hf CLI
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"
uv tool install huggingface-hub

# Login (paste your HF token)
hf auth login

# Create the repo on HF first
hf repos create lzwjava/sec-edgar-gpt-124m-hf --type model

# Analyze what's there
ls -la ~/sec-edgar-gpt-124m-hf/
du -sh ~/sec-edgar-gpt-124m-hf/*
cat ~/sec-edgar-gpt-124m-hf/config.json 2>/dev/null

# Upload the folder
hf upload lzwjava/sec-edgar-gpt-124m-hf ~/sec-edgar-gpt-124m-hf/
```

Which option works for you?
