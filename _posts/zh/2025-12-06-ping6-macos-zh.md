---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 在 macOS 上使用 ping6
translated: true
type: note
---

问题：如何在 macOS 上使用 `ping6` 命令？

答案：

`ping6` 是 macOS（以及其他一些类 Unix 系统）上经典 `ping` 工具的 IPv6 版本。与 GNU/Linux 版本不同，macOS 的 `ping6`（由 Apple 提供）的语法略有不同，并且不支持 `--help` 或长选项。

### 基本用法
```bash
ping6 ipv6-address
ping6 hostname
```

### 常用选项（macOS 版本）

| 选项              | 含义                                         | 示例                                |
|-------------------|----------------------------------------------|-------------------------------------|
| `-c count`        | 仅发送 `count` 次 ping 然后退出              | `ping6 -c 10 2606:4700:4700::1111`  |
| `-i wait`         | 两次 ping 之间等待 `wait` 秒（默认 1）       | `ping6 -i 0.2 2001:db8::1`          |
| `-s packetsize`   | 设置数据包大小，单位为字节（默认 56）        | `ping6 -s 1000 2606:4700:4700::1111`|
| `-I interface`    | 源接口（在多宿主 Mac 上很有用）             | `ping6 -I en0 2001:db8::1`          |
| `-b boundif`      | 将套接字绑定到特定接口 (Apple)             | `ping6 -b en0 2001:db8::1`          |
| `-D`              | 禁用分段（设置 DF 位）                       | `ping6 -D 2606:4700:4700::1111`     |
| `-n`              | 仅显示数字（不进行主机名解析）              | `ping6 -n 2001:db8::1`              |
| `-a addrtype`     | 提示音 ping（收到回复时发出蜂鸣声）— `aabr` 等 | `ping6 -aa 2001:db8::1`             |
| `-W timeout`      | 等待 `timeout` 毫秒以获得回复                | `ping6 -W 500 2001:db8::1`          |
| `-t timeout`      | 在 `timeout` 秒后退出，无论如何               | `ping6 -t 30 2001:db8::1`           |

### 有用的日常示例

```bash
# 简单 ping Cloudflare DNS
ping6 2606:4700:4700::1111

# 仅用 10 个数据包 ping Google DNS
ping6 -c 10 2001:4860:4860::8888

# 快速 ping (0.1 秒间隔)
ping6 -i 0.1 2606:4700:4700::1111

# 大数据包（可帮助测试 MTU 问题）
ping6 -D -s 1450 2606:4700:4700::1111

# 强制使用 Wi-Fi 接口 (en0) 而不是以太网
ping6 -b en0 2001:db8::1
```

### 快速测试您的 Mac 是否具有 IPv6 连接

```bash
ping6 -c 4 ipv6.google.com
```

如果您收到回复 → IPv6 正在工作。
如果您收到“No route to host”或 100% 的丢包率 → IPv6 被禁用或您的 ISP 未提供。

这基本上就是您在 macOS 上日常使用 `ping6` 所需的全部内容！
