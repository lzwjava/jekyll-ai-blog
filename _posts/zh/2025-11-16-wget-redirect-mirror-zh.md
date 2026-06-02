---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 镜像站mirror.accum.se的常规wget重定向
translated: true
type: note
---

你的 `wget` 命令正在访问 `https://mirror.accum.se/mirror/wikimedia.org/dumps/...` 并收到指向 `https://laotzu.ftp.acc.umu.se/...` 的 **302 重定向**。这对 **accum.se** 镜像站来说是完全正常且预期的行为——以下是原因说明：

### 重定向发生的原因

`mirror.accum.se` 只是瑞典于默奥大学学术计算机俱乐部（ACC）运营的**重定向器/负载均衡器**。
它本身**并不托管文件**，而是：

- 根据你 IP 的地理位置（或有时根据负载情况）
- 自动将你重定向到其镜像阵列中速度最快/距离最近的实际存储服务器
- 在你的案例中，它选择了 `laotzu.ftp.acc.umu.se`（这是真正存储数据的 FTP/HTTP 服务器）

这是他们沿用多年的系统架构。其他常见可能重定向到的主机名包括：

- `issac.ftp.acc.umu.se`
- `laotzu.ftp.acc.umu.se`（你遇到的这个）
- `morpork.ftp.acc.umu.se`
- 等等

因此，即使你在脚本中写的是 `mirror.accum.se`，最终几乎总是从某个 `*.ftp.acc.umu.se` 后端服务器下载数据。

### 首个文件出现“206 Partial Content”的原因

由于你（或某人/某脚本）之前已开始下载该相同文件，`wget -c` 检测到本地存在部分文件后发送了 `Range` 请求。服务器正确恢复了下载 → 返回 206 部分内容状态。这是正常现象！

### 是否存在问题？

没有。所有操作都按设计正常运行。

- 重定向是正常且无害的
- 最终服务器（`laotzu.ftp.acc.umu.se`）仍是官方的 ACC/维基媒体镜像站
- 无论重定向到哪个后端服务器，文件校验值都将保持一致

### 如需避免重定向（可选方案）

你可以完全跳过重定向器，直接指定真实主机地址，例如：

```bash
# 以下三个服务器本身就在 mirror.accum.se 后端轮询调度
wget -c https://laotzu.ftp.acc.umu.se/mirror/wikimedia.org/dumps/enwiki/20251101/...
# 或
wget -c https://issac.ftp.acc.umu.se/mirror/wikimedia.org/dumps/enwiki/20251101/...
```

但大多数人仍继续使用 `mirror.accum.se`，因为重定向器会自动为你选择最优服务器。

### 总结

你的脚本运行正常。从 `mirror.accum.se` 到 `laotzu.ftp.acc.umu.se` 的 302 重定向是该镜像站的正常预期行为。不存在任何问题，你下载的仍然是正版维基媒体数据包。建议继续使用 `mirror.accum.se`——这是全球范围内最快速可靠的镜像站之一。
