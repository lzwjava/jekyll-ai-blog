---
audio: false
generated: true
image: false
lang: en
layout: post
title: "RunPod CLI: runpodctl Overview"
translated: false
type: note
---

## Question: does RunPod have a CLI?

## Answer: Yes — `runpodctl`

Every pod ships with it pre-installed and a pod-scoped API key. Install locally too if you want remote orchestration from your own box.

**Install:**

```bash
wget -qO- cli.runpod.net | sudo bash
# or
brew install runpod/runpodctl/runpodctl
# or conda-forge
conda install conda-forge::runpodctl
```

**First-time setup:**

```bash
runpodctl doctor   # configures API key + SSH in one shot
# or manually:
runpodctl config --apiKey=<RUNPOD_API_KEY>
```

**Core commands (noun-verb pattern):**

```bash
runpodctl gpu list                          # available GPU types
runpodctl datacenter list                   # dc availability
runpodctl template search pytorch           # find templates
runpodctl pod create --image=runpod/pytorch:2.8.0-py3.11-cuda12.8.1-cudnn-devel-ubuntu22.04 --gpu-id=NVIDIA_A100
runpodctl pod list
runpodctl pod get <pod_id>
runpodctl pod start <pod_id>
runpodctl pod stop <pod_id>
runpodctl pod delete <pod_id>

runpodctl serverless ...   # alias: sls
runpodctl network-volume ...  # alias: nv
runpodctl registry ...     # alias: reg
runpodctl user             # account/balance info, alias: me
runpodctl billing          # billing history
```

**File transfer (no API key needed, uses one-time codes):**

```bash
runpodctl send data.txt
# Code is: 8338-galileo-collect-fidel
# on the other machine:
runpodctl receive 8338-galileo-collect-fidel
```

Old `get/create/remove/start/stop/exec/project/config` verbs are deprecated in favor of the noun-verb form (`pod create`, `pod start`, etc.) but still work.

For your MI300X/GPT-2 training runs, this is basically your whole ops loop: `pod create` → `ssh` → train → `pod stop`, scriptable end to end.

References:

- [Runpod CLI Overview](https://docs.runpod.io/runpodctl/overview)
- [runpodctl GitHub README](https://github.com/runpod/runpodctl)
- [runpodctl full command reference](https://github.com/runpod/runpodctl/blob/main/docs/runpodctl.md)
