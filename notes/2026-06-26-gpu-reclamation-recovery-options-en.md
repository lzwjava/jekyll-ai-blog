---
audio: false
generated: true
image: false
lang: en
layout: post
title: GPU Reclamation Recovery Options
translated: false
type: note
---

This is a RunPod error, not something to fix in code. When a stopped Pod's GPUs get reclaimed by another user, your exact GPU config is gone. Your options:

**1. Migrate to new GPUs (keeps your data)**
The dialog usually offers a "Migrate" or "Deploy on new GPUs" button. This keeps your network volume / persistent disk but assigns different physical GPUs. Click that if available.

**2. Deploy a fresh Pod with your volume attached**
If migration isn't offered or fails (your GPU type is out of stock in that datacenter):
- Note your Pod's region and network volume ID
- Spin up a new Pod, attach the same network volume, pick the same or equivalent GPU
- Your `/workspace` data persists if it was on the network volume — anything on the container disk only is lost

**3. Switch GPU type or datacenter**
If your original GPU (e.g. MI300X / specific A100 config) is unavailable in that region, pick a different datacenter or GPU tier. Use the filters to find availability.

**Key thing to check:** Was your work on a **network volume** or just **container disk**?
- Network volume → safe, just reattach
- Container disk only → lost on migration, this is the usual gotcha

**Prevention going forward:**
- Always put code/checkpoints on a network volume mounted at `/workspace`
- For training, checkpoint to the volume frequently (`torch.save` every N steps)
- Consider on-demand vs spot — spot pods get reclaimed more aggressively

Given your setup, this is also a nudge toward the AMD Dev Cloud MI300X for the heavier runs — it's a more stable allocation than RunPod spot capacity.

What GPU type and storage config were you running? I can give exact recovery steps.
