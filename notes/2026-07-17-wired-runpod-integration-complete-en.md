---
audio: false
generated: true
image: false
lang: en
layout: post
title: Wired RunPod Integration Complete
translated: false
type: note
---

Done. The integration is wired end-to-end:

- `ww runpod --help` shows all subcommands and GPU shortcuts
- `ww runpod gpus` maps to `runpodctl gpu list`
- `ww runpod start rtx4000ada` maps to `runpodctl pod create --gpu-id NVIDIA-RTX-4000-Ada --image runpod/pytorch:2.8.0-py3.11-cuda12.8.1-cudnn-devel-ubuntu22.04`
- All the other verbs (`stop`, `delete`, `list`, `ssh`, `send`, `receive`, `user`, `billing`, `raw`) pass through to `runpodctl`

It just needs a RunPod API key now. Set it with:

```bash
runpodctl config --apiKey=<YOUR_RUNPOD_API_KEY>
# or
export RUNPOD_API_KEY=***
```

After that `ww runpod start rtx4000ada` will spin up the pod directly.
