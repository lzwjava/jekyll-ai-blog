---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Docker DNS 如何解析容器名称
translated: true
type: note
---

好问题。当你 `docker network connect` 时，Docker 不会触碰容器内的 `/etc/hosts`。它通过 Docker 的 **built-in DNS server**（容器内为 `127.0.0.11`）工作。就是这样。下面是它的工作原理：

### 容器内的 `/etc/hosts`

容器自身的 hostname（`32bb25fb32c8`）与每个连接网络的所有 IP 一起列出。但是 **`LibreChat` 不在 `/etc/hosts` 中**。

### 那么它是如何解析的？

1. **`/etc/resolv.conf`** 指向 `nameserver 127.0.11` — 那是 Docker 的 **embedded DNS resolver**，运行在每个容器的 network namespace 内。

2. 当你对 `LibreChat` 进行 DNS lookup 时，它会去 `127.0.0.11`，那是 Docker 的 DNS。Docker 知道每个网络上的所有容器 — 当你 `docker network connect librechat_default uptime-kuma` 时，DNS resolver 现在在那个共享网络上看到 `LibreChat` 并返回其 IP（`172.18.0.6`）。

3. 如果容器不在 `librechat_default` 上，Docker 的 DNS 将 **不知道** `LibreChat`，查询将失败 — 这正是之前发生的情况。

**TL;DR：** 不是 `/etc/hosts`。是 Docker 在 `127.0.0.11` 的 internal DNS 来解析容器名称，只有当两个容器至少共享一个网络时才有效。