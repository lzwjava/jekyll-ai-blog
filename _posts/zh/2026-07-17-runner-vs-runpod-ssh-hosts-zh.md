---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Runner 与 RunPod SSH 主机
translated: true
type: note
---

根据任务不同：

- `runner`（`213.173.99.50`）—— 你自己的盒子，持久化，固定IP。用于文件、仓库、长期运行的服务，以及任何你需要始终在线的任务。直接路径也更快（4.8秒 vs RunPod的2.3秒）。
- `runpod`（`ssh.runpod.io`）—— 临时云端GPU Pod。仅当你需要使用工作站上没有的GPU时才使用。如果Pod被停止/重建，主机名/IP会发生变化。

经验法则：
- 常规工作、git、配置 → `ssh runner`
- 在H200/A100等上进行训练、GPU推理 → `ssh runpod-gpu-<podId>`