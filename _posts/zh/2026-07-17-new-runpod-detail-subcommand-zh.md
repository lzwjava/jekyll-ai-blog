---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 新 runpod 详细子命令
translated: true
type: note
---

新增了一个 `ww runpod detail <pod_id>` 子命令。

文件变更：
- `/Users/lzwjava/projects/ww/ww/runpod/runpod.py`

用法：
- `ww runpod detail n4pqpw4h5fe3bb`

现在此命令可以：
- 通过 `runpodctl ssh info` 获取 SSH 元数据
- SSH 进入 pod
- 打印 hostname、OS、CPU、memory、disk、GPU、uptime、Python、`nvcc` 以及 docker 信息
- 如果 pod 未运行，则清晰报告 pod 状态

一个已修复的坑：runpodctl 之前会受到 shell 中本地代理环境变量的影响。新子命令在调用 runpodctl 之前会剥离代理环境变量，从而实现直接连接。