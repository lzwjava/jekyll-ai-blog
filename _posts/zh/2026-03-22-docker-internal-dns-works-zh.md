---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Docker 内部 DNS 解析是如何工作的
translated: true
type: note
---

就是这样。这是它的工作原理：

### 容器中的 `/etc/hosts`

容器的自身主机名 (`32bb25fb32c8`) 与其每个连接网络的所有 IP 一起列出。但是 **`LibreChat` 不在 `/etc/hosts` 中**。

### 那么它是如何解析的？

1. **`/etc/resolv.conf`** 指向 `nameserver 127.0.0.11` — 那是 Docker 的 **embedded DNS resolver**，运行在每个容器的 network namespace 中。

2. 当你对 `LibreChat` 执行 DNS lookup 时，它会转到 `127.0.0.11`，那是 Docker 的 DNS。Docker 知道每个网络上的所有容器 — 当你执行 `docker network connect librechat_default uptime-kuma` 时，DNS resolver 现在在该共享网络上看到 `LibreChat` 并返回其 IP (`172.18.0.6`)。

3. 如果容器不在 `librechat_default` 上，Docker 的 DNS 将 **不知道** `LibreChat`，lookup 将失败 — 正好是之前发生的情况。

**TL;DR:** 不是 `/etc/hosts`。是 Docker 在 `127.0.0.11` 的 internal DNS 来解析容器名称，只有当两个容器共享至少一个网络时才有效。