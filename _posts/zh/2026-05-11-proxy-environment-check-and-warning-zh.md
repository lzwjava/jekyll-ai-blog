---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 代理环境检查与警告
translated: true
type: note
---

添加了 `warn_if_proxy_set()` 函数：

- 检查 `http_proxy`、`https_proxy`、`HTTP_PROXY`、`HTTPS_PROXY`、`all_proxy`、`ALL_PROXY` 环境变量。
- 如果其中任何一个被设置，则打印出哪些变量及其值，说明 hf-mirror.com 不需要代理，并显示精确的 `unset` 命令。
- 运行 `curl -m 5 https://www.google.com`（该命令会继承用户的代理环境变量）并报告 HTTP 状态码 — `200` 表示代理虽然工作但不需要；非 200 表示它可能已经坏了。
- 优雅地处理 `curl` 缺失的情况（`FileNotFoundError`）。
- 在 `main()` 开始时调用一次，在任何下载发生之前。

不会中止程序 — 只是发出警告，因此用户仍然可以继续，如果他们确实想这么做。
