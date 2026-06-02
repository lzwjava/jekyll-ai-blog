---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 避免Docker守护进程代理循环
translated: true
type: note
---

### 为什么在 Docker 的 `daemon.json` 中配置 `"no-proxy": "localhost,127.0.0.1,.local"` 至关重要

当您使用类似 `"http-proxy": "http://localhost:7890"` 的代理设置（常见于本地运行的 Clash 等工具）配置 Docker 守护进程时，默认情况下守护进程会将这些规则应用于**所有**出站网络流量。这包括连接到外部注册中心（例如从 `registry-1.docker.io` 拉取 `hello-world` 这类镜像）。

然而，若缺少 `no-proxy` 指令，Docker 守护进程也会尝试通过同一代理路由**本地连接**——比如与您代理服务器本身在 `localhost:7890` 的初始 TCP 握手。这就形成了典型的**代理循环**：

1. Docker 需要从 `registry-1.docker.io` 获取镜像。
2. 它尝试通过位于 `localhost:7890` 的代理进行连接。
3. 但为了连接到 `localhost:7890`，代理设置再次生效，强制 Docker... 通过位于 `localhost:7890` 的代理进行连接。
4. 这种无限递归在 TCP 层级会失败，因为代理无法代理到自身的连接（这导致无解的自引用循环）。
5. 连接意外中止，产生 `proxyconnect tcp: EOF` 错误（EOF 意为“文件结束”，表示在代理协商/握手期间发生了过早关闭）。

添加 `"no-proxy": "localhost,127.0.0.1,.local"` 明确告知守护进程对发往以下地址的流量**绕过代理**：

- `localhost`（您机器的环回主机名），
- `127.0.0.1`（IPv4 环回地址），
- `.local` 域（常用于 mDNS/本地网络解析）。

这使得 Docker 能够**直接**连接到本地主机上的代理服务器，而无需经过自身循环。一旦连接建立，代理便可以正常处理到 Docker 注册中心的外部请求（例如，对于 HTTPS 流量通过 HTTP CONNECT 方法）。

简而言之：它防止了守护进程“代理代理服务器自身”，确保本地代理访问正常工作，同时仍将通过它路由发往互联网的流量（如镜像拉取）。

如果您的设置涉及其他本地服务（例如，内部注册中心或本地通信的容器），在 `no-proxy` 中扩展这些域名/IP 可以防止类似问题。

[Docker 守护进程代理配置](https://docs.docker.com/engine/daemon/proxy/)
[Docker 代理设置论坛讨论](https://forums.docker.com/t/proxy-settings-for-the-docker-daemon/132089)
[面向企业防火墙的 Docker 代理指南](https://www.datacamp.com/tutorial/docker-proxy)
