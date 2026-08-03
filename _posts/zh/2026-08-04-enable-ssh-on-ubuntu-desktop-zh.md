---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在Ubuntu桌面上启用SSH
translated: true
type: note
---

问题：如何在一台本地局域网中的 Ubuntu 桌面机上启用 SSH 访问？

答案：

在 Ubuntu Desktop 上安装并启用 OpenSSH 服务器。

### 1. 安装 SSH 服务器

```bash
sudo apt update
sudo apt install openssh-server
```

检查状态：

```bash
systemctl status ssh
```

你应该看到：

```
Active: active (running)
```

如果没有：

```bash
sudo systemctl enable --now ssh
```

---

### 2. 查找 Ubuntu 机器的局域网 IP

运行：

```bash
ip addr
```

示例：

```
enp3s0:
    inet 192.168.1.100/24
```

你的 SSH 地址为：

```
192.168.1.100
```

或：

```bash
hostname -I
```

---

### 3. 从另一台机器 SSH 连接

从另一台 Linux/macOS 机器：

```bash
ssh username@192.168.1.100
```

示例：

```bash
ssh lzw@192.168.1.100
```

首次连接：

```
The authenticity of host '192.168.1.100' can't be established.
Are you sure you want to continue connecting?
```

输入：

```
yes
```

然后输入 Ubuntu 用户密码。

---

### 4. 如果防火墙已启用

检查：

```bash
sudo ufw status
```

如果已激活：

```bash
sudo ufw allow ssh
```

或：

```bash
sudo ufw allow 22/tcp
```

---

### 5. 更好的做法：使用 SSH 密钥（免密码）

在客户端机器上：

```bash
ssh-keygen
```

复制密钥：

```bash
ssh-copy-id username@192.168.1.100
```

然后：

```bash
ssh username@192.168.1.100
```

无需密码。

---

### 6. 可选：使用主机名简化操作

安装 mDNS：

```bash
sudo apt install avahi-daemon
```

然后从另一台机器：

```bash
ssh username@ubuntu-desktop.local
```

查看主机名：

```bash
hostname
```

---

### 7. 连接失败时的调试

在 Ubuntu 服务器上：

```bash
sudo ss -tlnp | grep ssh
```

预期输出：

```
LISTEN 0 128 0.0.0.0:22
```

从客户端：

```bash
ping 192.168.1.100
```

然后：

```bash
ssh -v username@192.168.1.100
```

常见问题：

| 问题                   | 解决                                         |
| ---------------------- | -------------------------------------------- |
| Connection refused     | `sudo systemctl restart ssh`                 |
| Timeout                | 防火墙/网络问题                              |
| Wrong IP               | `hostname -I`                                |
| Permission denied      | 错误的用户名/密码或 SSH 配置                 |

对于家庭 AI 实验室（Ubuntu + GPU 服务器），我还会设置 SSH 密钥并在路由器中配置静态 DHCP 租约，这样机器始终保持相同的局域网 IP。