---
audio: false
generated: true
image: false
lang: en
layout: post
title: New runpod detail subcommand
translated: false
type: note
---

Added a new `ww runpod detail <pod_id>` subcommand.

File changed:

- `/Users/lzwjava/projects/ww/ww/runpod/runpod.py`

Usage:

- `ww runpod detail n4pqpw4h5fe3bb`

It now:

- gets SSH metadata via `runpodctl ssh info`
- SSHs into the pod
- prints hostname, OS, CPU, memory, disk, GPU, uptime, Python, `nvcc`, and docker info
- reports pod status cleanly if the pod is not running

One fixed gotcha: runpodctl was being affected by your local proxy env vars from shell. The new subcommand strips proxy env before invoking runpodctl, so it connects directly.
