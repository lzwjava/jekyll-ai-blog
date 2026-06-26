---
audio: false
generated: true
image: false
lang: en
layout: post
title: RunPod CLI and P2P File Transfer
translated: false
type: note
---

Yes. RunPod has an official CLI called `runpodctl`.

It's pre-installed on every RunPod pod. For local install:

```bash
# macOS (Air)
brew install runpod/runpodctl/runpodctl

# Linux (workstation)
wget -qO- cli.runpod.net | sudo bash
```

Auth and core usage:

```bash
runpodctl config --apiKey <​API_KEY>

# Pods
runpodctl get pod
runpodctl create pod --name dev --imageName runpod/pytorch:latest --gpuType "NVIDIA A100"
runpodctl start pod <POD_ID>
runpodctl stop pod <POD_ID>
runpodctl remove pod <POD_ID>

# File transfer (peer-to-peer, no SSH needed)
runpodctl send model.pt        # prints a one-time code
runpodctl receive <CODE>       # on the other machine
```

The `send`/`receive` pair is the genuinely useful part — it's a croc-based P2P transfer that works across NAT without configuring SSH keys, handy for moving checkpoints between your workstation and a rented pod.

For programmatic control (spinning pods up/down inside an agent), the GraphQL API and the `runpod` Python SDK (`pip install runpod`) give finer control than the CLI — serverless endpoints, autoscaling, and `runpod.create_pod()` calls you can wire into automation.

References:

- [runpodctl GitHub](https://github.com/runpod/runpodctl)
- [RunPod CLI docs](https://docs.runpod.io/cli/overview)
- [RunPod Python SDK](https://github.com/runpod/runpod-python)
