---
audio: false
generated: true
image: false
lang: zh
layout: post
title: TCP慢启动详解（针对scp）
translated: true
type: note
---

**问题：** 为什么 `scp` 刚开始很慢（约 300 KB/s），然后逐渐加速到全速（约 5 MB/s）？

**答案：**

这是由于 TCP 慢启动——一种内置于内核中的拥塞控制机制。

## TCP 慢启动

TCP 不会立即以全速发送数据。它会探测网络：

```
cwnd（拥塞窗口）从约 10 个段（约 14 KB）开始
每收到一个 ACK → cwnd 翻倍（指数增长）
直到 cwnd 达到 ssthresh（慢启动阈值）→ 转为线性增长
```

你的传输时间线：

```
t=0s:   cwnd=14KB   → 可见速度约 300 KB/s
t=0.5s: cwnd=112KB  → 约 2 MB/s
t=1s:   cwnd=896KB  → 约 5 MB/s（达到链路容量）
t=2s+:  稳态约 6 MB/s（你的局域网上限）
```

你看到的“加速过程”实际上就是指数翻倍阶段。

## 为什么局域网仍然有慢启动

即使在 `192.168.x.x` 上，TCP 在探测之前并不知道自己在局域网内。内核无论接口类型都使用相同的拥塞控制算法（cubic/bbr）。

```bash
# 在工作站上检查拥塞控制算法
sysctl net.ipv4.tcp_congestion_control
# 可能是：cubic
```

BBR 在低延迟链路上比 CUBIC 加速更快，因为它直接建模带宽，而不是等待丢包。

## 为什么特别是 scp

`scp` 使用 SSH → TCP。SSH 层为每个数据包增加了一些加密开销，但不会改变 TCP 的行为。慢启动完全是内核层面的。

## 解决方法：跳过加速阶段

对于局域网内的大文件，可以使用带有更大缓冲区的 `rsync` over SSH，或者直接接受——27 MB 以 5 MB/s 传输需要 4 秒，加速阶段只花费约 1-2 秒。

```bash
# 或者使用 netcat 获得原始速度（无加密）：
# 发送端：
nc -l 9999 < junhong.m4a
# 接收端：
nc 192.168.x.x 9999 > junhong.m4a
```

或者调整 SSH 套接字缓冲区：

```bash
scp -o "IPQoS=throughput" ~/Downloads/junhong.m4a lzw@192.168.x.x:~/
```

加速过程是物理规律——TCP 在尚未了解网络时表现得彬彬有礼。
