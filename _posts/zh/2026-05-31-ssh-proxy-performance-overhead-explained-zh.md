---
audio: false
generated: true
image: false
lang: zh
layout: post
title: SSH代理性能开销解析
translated: true
type: note
---

旧的 SSH 路径是这样的：

```
git → ssh → ncat (子进程) → SOCKS5 → mihomo (:7891) → Hysteria2 → DMIT LA → GitHub
```

而新的 HTTPS 路径：

```
git → HTTP 代理 → mihomo (:7890) → Hysteria2 → DMIT LA → GitHub
```

SSH 路径较慢的原因有三点：

1. 额外的进程跳转。ncat 通过 `ProxyCommand` 以子进程方式启动。SSH 与 ncat 的 stdin/stdout 通信，ncat 再转发到 SOCKS5。每个字节都要经过两次额外的上下文切换（内核 → ncat → 内核 → mihomo）。而 HTTP 路径直接进入 mihomo 的 socket —— 没有中间进程。

2. TCP-over-TCP 崩溃。SSH 运行在 TCP 之上，SOCKS5 也运行在 TCP 之上。因此，git 数据封装在 SSH 的 TCP 流中，而该流本身又位于与 SOCKS5 代理的另一条 TCP 连接内。两个独立的 TCP 拥塞控制算法相互竞争——当发生丢包时，两层都会重传并退避，放大减速效果。HTTP CONNECT 是单次 TCP 跳转：mihomo 建立隧道，与 GitHub 的底层 TLS 连接通过单个 TCP 流端到端运行。

3. ncat 的中继缓冲区。从我阅读的源代码（`ncat.h:140`）中可以看到：`DEFAULT_TCP_BUF_LEN = 8192` —— 在 select() 循环中以 8KB 读取。每个数据块都需要一次 read 系统调用、一次 write 系统调用和一次上下文切换。对于一个 30MB 的 git 包，大约需要 3,700 次系统调用对。而 HTTP 代理路径让内核通过自身的缓冲区管理更直接地处理数据，无需额外的用户空间中继。

HTTP 代理（mihomo 在 :7890 端口）本质上只是一个 HTTP CONNECT 隧道——它接收 CONNECT 请求，打开一条到 GitHub 的 TCP 连接，响应 "200 OK"，然后 mihomo 直接透传原始字节。比 SSH/SOCKS5/ncat 链的开销小得多。