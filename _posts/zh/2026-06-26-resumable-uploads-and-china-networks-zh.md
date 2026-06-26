---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 断点续传与中国网络
translated: true
type: note
---

这里有两个不同的问题：

**1. `hf upload` — 是否支持断点续传？部分支持。**

`hf upload-large-folder` 明确设计用于断点续传（它使用本地缓存来跟踪进度）。对于单个475MB的文件，`hf upload` 内部通过 `huggingface_hub` 使用分片上传——但如果传输中断，重试时并不能干净地从断点处恢复。

**2. 为什么 SCP 也会卡住 — 这是中国网络的问题，而非工具的问题。**

SCP 使用的是单个长期存在的 TCP 流。中国的 GFW 加上 ISP 的流量整形（尤其是中国电信）会严重限制长期国际连接的速度。连接不会直接“失败”，而是会变得几乎停滞，最终超时。SCP 和 `hf upload` 都遇到了同一个障碍：**持续的跨国带宽被限速了。**

**真正的解决方案：使用支持断点续传的协议加上良好的路由。**

带续传功能的 rsync 比 SCP 更好：
```
rsync -avz --progress --partial model.safetensors amd-cloud:~/
```
`--partial` 会保留已传输的部分文件，以便重试时从中断处继续。但即使是 rsync，通过同一网络通道传输仍然会很慢。

**从中国实际有效的方案：**

1. **hf-mirror.com** — 针对中国优化的 Hugging Face 端点，专门解决此问题：
   ```
   HF_ENDPOINT=https://hf-mirror.com hf upload lzwjava/sec-edgar-gpt-124m model.safetensors model.safetensors
   ```

2. **DMIT 代理（洛杉矶）** — 你的 hysteria2 代理具有比原始中国电信更好的国际路由：
   ```
   https_proxy=http://127.0.0.1:<port> hf upload lzwjava/sec-edgar-gpt-124m model.safetensors model.safetensors
   ```

3. **GCS → HF** — 你已经上传到 GCS。从一台美国机器（AMD Dev Cloud）上，从 GCS 拉取再推送到 HF。两者都位于美国，因此速度很快：
   ```
   # 在 AMD Dev Cloud 上执行
   gsutil cp gs://lzwjava1/sec-edgar-gpt-124m/model.safetensors .
   hf upload lzwjava/sec-edgar-gpt-124m model.safetensors model.safetensors
   ```

现在要我立即尝试方案1（hf-mirror）吗？