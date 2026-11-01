---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Unix套接字冒烟测试结果
translated: true
type: note
---

冒烟测试完成。工作目录是干净的（HEAD = `482279b server：添加对 .sock 通信的支持`），因此我对 `whisper-server` 中新的 `.sock`（AF_UNIX）支持进行了冒烟测试。

## 结果 — 成功

| Test | Command | Result |
|---|---|---|
| 构建 | `cmake --build build --target whisper-server whisper-cli` | 成功 |
| 启动 socket 服务 | `whisper-server -m models/ggml-tiny.en.bin --host /tmp/whisper-smoke.sock` | socket 已创建，`whisper server listening at unix://...` |
| 静态文件 `GET /` | `curl --unix-socket .../` | 200, 2130 字节 |
| `GET /health` | | `{"status":"ok"}` |
| `POST /inference` (multipart) | `-F file=@samples/jfk.wav` | JFK 样本的转录结果正确 |
| `POST /inference` 流式传输 | `-F stream=true` | 转录结果正确 |
| `POST /load` | `-F model=...` | `Load was successful!` |
| 3 个并发推理请求 | parallel curl | 全部 3 个均正确 |
| 相对路径 | `--host rel.sock` | 成功 |
| 抽象命名空间 | `--host @whisper-smoke.sock` + `curl --abstract-unix-socket` | 成功（无文件系统条目） |
| TCP 回归测试 | `--host 127.0.0.1 --port 18089` | `/health` + `/inference` 保持不变 |

## 发现的问题

1. **过期的 socket 文件会阻止重启**（主要问题）。关闭（无论是 SIGINT 还是 SIGTERM）后，`.sock` 文件会留在磁盘上，因此下次在同一路径启动时会失败：
   ```
   couldn't bind to unix socket: /tmp/whisper-smoke.sock   (exit code 1)
   ```
   `httplib.h` 在 `bind`/`close` 时从未调用 `unlink()`，而 `examples/server/server.cpp:1305` 中的 `clean_up` lambda 只打印计时结果并释放 ctx。崩溃或被终止的服务器留下的陈旧文件也会产生同样的效果。目前的解决方法：先 `rm` 该文件，或者使用抽象命名空间（`--host @name.sock`）。

2. **路径过长时错误提示不明显。** 当路径超过 107 字节时，`httplib.h:3544` 中的 `create_socket()` 会静默返回 `INVALID_SOCKET`，因此用户只会看到通用的 `couldn't bind to unix socket: <long path>` 错误，没有任何关于 `sun_path` 限制的提示。父目录不存在时也是如此。

这两个问题都属于表面到中等程度的问题；传输层本身和 TCP 路径没有问题。是否需要我来为问题 #1 提供一个修复方案（在 `clean_up` 中添加 `unlink`，以及在 `bind` 之前检查并删除陈旧文件）？