---
audio: false
generated: true
image: false
lang: en
layout: post
title: GPU Snapshot Timeline Explained
translated: false
type: note
---

Here's the timeline from the forensic evidence:

**March 16, 2026** — AMD built the snapshot image:
- `rocm:latest` Docker image built with buildkit (26GB `setup.sh` = ROCm install layer)
- `droplet-agent` purged (standard image-building cleanup)

**May 20, 2026 04:39** — Your Droplet was created from that snapshot:
- Cloud-init ran, re-installed `droplet-agent`
- Host already had ROCm 7.2.0 at `/opt/rocm-7.2.0/` (22G, baked into the image)

**May 20, 2026 04:40** — Container `rocm` started:
- Ran Jupyter Lab with ROCm GPU access
- Exited ~May 21 (11 days ago)

**Answer to your question:** When you created the GPU Droplet, you chose an image like `Ubuntu 7.2-gpu-mi300x1-192gb-devcloud-atl1`. That image had **both**:
- ROCm 7.2.0 installed on the host (`/opt/rocm-7.2.0/`) — 22G
- `rocm:latest` Docker image pre-loaded (another 36G with ROCm inside) — with Jupyter Lab pre-configured

You didn't install anything manually. AMD Dev Cloud baked it all into the snapshot. The Docker image is just a containerized duplicate of what's already on the host — meant for running Jupyter Lab easily.

**Bottom line:** The 59G in containerd is entirely from the AMD Dev Cloud pre-loaded snapshot. The `rocm` container exited 11 days ago and you're not using it. The host ROCm at `/opt/rocm-7.2.0/` (22G) is what actually powers GPU workloads — the Docker image is redundant. Safe to nuke the Docker artifacts. Want me to clean them up?