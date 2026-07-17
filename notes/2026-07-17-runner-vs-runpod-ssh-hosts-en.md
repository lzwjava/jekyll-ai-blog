---
audio: false
generated: true
image: false
lang: en
layout: post
title: Runner vs RunPod SSH Hosts
translated: false
type: note
---

Depends on the task:

- `runner` (`213.173.99.50`) — your own box, persistent, fixed IP. Use it for files, repos, long-running services, anything you want always-on. Direct path is faster too (4.8s vs RunPod’s 2.3s).
- `runpod` (`ssh.runpod.io`) — ephemeral cloud GPU pod. Use it only when you need a GPU that isn’t on your workstation. If the pod gets stopped/recreated, the hostname/IP changes.

Rule of thumb:

- General work, git, config → `ssh runner`
- Training on H200/A100/etc, GPU inference → `ssh runpod-gpu-<podId>`
