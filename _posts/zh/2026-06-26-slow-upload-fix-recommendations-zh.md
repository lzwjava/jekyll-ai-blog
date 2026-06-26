---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 慢速上传修复推荐
translated: true
type: note
---

以下是冒烟测试结果：

```
config.json (831B)  →  1.7秒  ✓
tokenizer.json (3.4MB) → 17.9秒  ≈ 190 KB/s
```

**当前连接吞吐量为190 KB/s。** 按此速度计算：

```
model.safetensors (475MB) → 预计约42分钟
```

而且很可能会在传输中途卡住（就像你在GCS上看到的那样）。

**建议方案（按优先级排序）：**

1. **hf-mirror.com** — 针对中国优化的HuggingFace镜像。尝试：

   ```
   HF_ENDPOINT=https://hf-mirror.com hf upload lzwjava/sec-edgar-gpt-124m model.safetensors model.safetensors
   ```

2. **DMIT代理（洛杉矶）** — 通过你的hysteria2代理路由。`hf` CLI支持`https_proxy`：

   ```
   https_proxy=http://127.0.0.1:<hysteria端口> hf upload lzwjava/sec-edgar-gpt-124m model.safetensors model.safetensors
   ```

3. **AMD开发云中继** — rsync到亚特兰大，从那里上传（美国→HF速度很快）

需要我尝试方案1（hf-mirror）或方案2（DMIT代理）进行实际上传吗？还是直接在当前连接上启动475MB上传，希望它不会卡住？
