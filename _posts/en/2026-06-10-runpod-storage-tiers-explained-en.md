---
audio: false
generated: true
image: false
lang: en
layout: post
title: RunPod Storage Tiers Explained
translated: false
type: note
---

**Question:** What do Container disk, Volume disk, and Network volume mean in RunPod?

**Answer:**

These are RunPod's three storage tiers, differing in lifecycle (when data gets wiped) and shareability:

**Container disk** — the ephemeral root filesystem of your pod (everything outside `/workspace`: `/root`, `/tmp`, installed apt/pip packages, etc.). It's wiped every time you **stop** the pod, not just terminate it. Think of it like a Docker container's writable layer. Anything you `pip install` or download here is gone on stop.

**Volume disk** — persistent storage mounted at `/workspace`, tied to that specific pod. Survives **stop/start** cycles (so your checkpoints and datasets in `/workspace` persist when you stop the pod to save GPU costs), but is deleted on **terminate**. Only that one pod can use it. Note it costs *more* when the pod is stopped ($0.20/GB/mo) than running ($0.10/GB/mo) — RunPod charges a premium for holding storage on a GPU host you're not paying compute for.

**Network volume** — persistent storage mounted at `/workspace`, but independent of any pod. Survives termination, and can be attached to multiple pods or serverless endpoints. Cheaper too ($0.07/GB/mo, $0.05 over 1TB). The tradeoff: it's network-attached (slower I/O than local NVMe volume disk, noticeable for heavy random reads like dataloader-bound training), and it pins you to the datacenter region where the volume lives — you can only spin up pods in that region.

**Practical pattern for your training workflow:**

```bash
# Network volume at /workspace: datasets, model checkpoints, venvs you want to keep
/workspace/
├── data/fineweb/          # survives terminate
├── checkpoints/gpt2-760m/ # survives terminate
└── venv/                  # reusable across pods

# Container disk: scratch only — anything here dies on stop
/tmp/  /root/
```

Rule of thumb: use a **network volume** if you terminate pods between sessions (cheapest, most flexible — same model as keeping a persistent disk on AMD Dev Cloud while killing the droplet), **volume disk** if you stop/start the same pod, and treat **container disk** as throwaway scratch. Re-run your environment setup (apt/pip installs) in a startup script since container disk resets — or bake them into a custom Docker image.

One gotcha: terminating a pod with only a volume disk deletes your data with zero recovery. If checkpoints matter, either use a network volume or `rsync` them off-box before terminating.
