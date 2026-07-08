---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 崩溃后重启RunPod
translated: true
type: note
---

RunPod 实例已宕机 — SSH 连接被拒绝。服务器可能崩溃或被终止（可能是客户端构建进程导致 OOM，或 Node 进程达到资源上限）。

要恢复，请重新创建 RunPod pod，然后运行：

```bash
bash runpod/start_services.sh
```

如果 pod 的文件系统已持久化，此命令将使用现有的 `/workspace/LibreChat`（其中已包含所有构建内容）。如果是全新 pod，请先运行 `build_librechat.sh` 重建客户端，再运行 `start_services.sh`。

重启 pod 后请告知我，我会检查并修复需要关注的问题。