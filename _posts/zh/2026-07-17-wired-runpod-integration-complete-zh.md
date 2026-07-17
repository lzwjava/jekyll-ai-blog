---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 有线RunPod集成完成
translated: true
type: note
---

完成。集成已端到端连通：

- `ww runpod --help` 显示所有子命令和 GPU 快捷方式
- `ww runpod gpus` 映射到 `runpodctl gpu list`
- `ww runpod start rtx4000ada` 映射到 `runpodctl pod create --gpu-id NVIDIA-RTX-4000-Ada --image runpod/pytorch:2.8.0-py3.11-cuda12.8.1-cudnn-devel-ubuntu22.04`
- 所有其他动词（`stop`、`delete`、`list`、`ssh`、`send`、`receive`、`user`、`billing`、`raw`）都透传到 `runpodctl`

现在只需要一个 RunPod API 密钥。通过以下方式设置：

```bash
runpodctl config --apiKey=<YOUR_RUNPOD_API_KEY>
# 或
export RUNPOD_API_KEY=***
```

之后 `ww runpod start rtx4000ada` 将直接启动 pod。