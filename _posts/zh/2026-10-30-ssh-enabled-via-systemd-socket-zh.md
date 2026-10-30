---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 通过 systemd 套接字启用 SSH
translated: true
type: note
---

确认。SSH **已开启并通过 systemd socket activation 启用**：

- `ssh.socket` → **active（listening）** 于端口 22，IPv4 + IPv6，绑定到所有接口（`0.0.0.0` / `[::]`）。
- `sshd-unix-local.socket` → active（AF_UNIX 本地套接字）。
- 还没有持久的 `sshd` 进程在运行——这是正常的：systemd 会在客户端连接时按需生成 `sshd`。

因此其他机器**可以**通过端口 22 访问这个笔记本的 SSH 服务。如果你想确认它是否真的可用，请运行：

```bash
ssh localhost
```

（如果防火墙处于活跃状态，请注意，开放的监听端口仍可能被外部阻止——如果需要外部访问，请用 `sudo ufw status` 或 `sudo nft list ruleset` 检查。）