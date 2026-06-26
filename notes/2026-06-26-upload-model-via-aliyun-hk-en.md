---
audio: false
generated: true
image: false
lang: en
layout: post
title: Upload model via Aliyun HK
translated: false
type: note
---

No Aliyun CLI. Two paths:

**Quick path — web console (5 min):**

1. Go to ecs.console.aliyun.com
2. Create instance: Hong Kong, Ubuntu 22.04, 2C4G, pay-as-you-go
3. Set security group: allow SSH (22)
4. SSH in, install `hf` CLI, upload

**CLI path — install aliyun CLI:**

```
brew install aliyun-cli
aliyun configure
# then script the ECS creation
```

The web console is faster for a one-shot. Want me to write you a complete shell script to run on the HK instance once it's up?

```bash
# On the Aliyun HK instance:
pip install huggingface-hub
hf auth login  # paste your token
# then upload directly from there
hf upload lzwjava/sec-edgar-gpt-124m model.safetensors model.safetensors
```

But first you need to get the 475MB file to HK. Two ways:

1. **SCP from Mac → HK** (fast via CN2, ~50 MB/s)
2. **Download from GCS on HK** (if GCS upload completed)

Want me to spin up the instance via CLI, or you want to use the web console?
