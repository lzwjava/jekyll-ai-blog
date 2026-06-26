---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 中国上传瓶颈分析
translated: true
type: note
---

测试文件已清理。以下是摘要：

```
烟雾测试结果（中国 → HuggingFace）：

  直连：       约 190 KB/s（3.4MB 耗时 17.9s）
  通过代理 7890：约 157 KB/s（10MB 耗时 65s，伴有长时间停滞）

  预估 475MB：约 42-50 分钟，传输中途可能停滞
```

**两条路由都同样慢** — 瓶颈在于中国的国际带宽，而非路由路径。代理没有帮助。

**关于 model.safetensors 的实际可行方案：**

1. **夜间直接上传** — 直连上传，无需代理。虽然慢，但若不卡顿，约 50 分钟。`hf upload` 支持大文件的可续传行为（分片上传）。如果卡住，重新运行同一命令即可从断点处继续：

   ```
   cd ~/projects/sec-edgar-gpt-124m
   hf upload lzwjava/sec-edgar-gpt-124m model.safetensors model.safetensors
   ```

2. **AMD Dev Cloud** — 但从中国向亚特兰大上传 475MB（通过 scp）会遇到同样的问题。仅当能通过 GCS（同样受限）将文件传送到那里时才值得考虑。

3. **工作站（192.168.1.36）** — 同样在中国，问题相同。SSH 超时。

**结论：** 方案 1 是最佳选择。睡觉前开始上传，让它慢慢跑。如果卡住，重新运行 — `hf upload` 会重新上传文件。需要我后台启动它吗？
