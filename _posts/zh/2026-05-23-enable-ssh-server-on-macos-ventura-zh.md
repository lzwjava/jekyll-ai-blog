---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在 macOS Ventura 上启用 SSH 服务器
translated: true
type: note
---

**问题：** 如何在 macOS Ventura 上设置 SSH 服务器，使其他局域网主机能够连接？

**回答：**

macOS 内置了 OpenSSH 服务器。启用它的命令：

```bash
sudo systemsetup -setremotelogin on
```

验证是否正在运行：

```bash
sudo systemsetup -getremotelogin
# Remote Login: On

sudo launchctl list | grep ssh
# 应显示 com.openssh.sshd
```

查看你的局域网 IP：

```bash
ipconfig getifaddr en0   # Wi-Fi
ipconfig getifaddr en1   # 以太网
```

从另一台局域网机器连接：

```bash
ssh zhiwei@192.168.1.x
```

---

**可选强化（推荐）：**

编辑 `/etc/ssh/sshd_config`：

```
PasswordAuthentication no        # 仅密钥认证
PermitRootLogin no
AllowUsers zhiwei
```

更改配置后重启 sshd：

```bash
sudo launchctl stop com.openssh.sshd
sudo launchctl start com.openssh.sshd
```

---

**防火墙说明：** 如果 macOS 防火墙已开启（`系统设置 → 网络 → 防火墙`），启用远程登录时 SSH（端口 22）会自动允许，无需手动添加规则。

**以后关闭：**

```bash
sudo systemsetup -setremotelogin off
```