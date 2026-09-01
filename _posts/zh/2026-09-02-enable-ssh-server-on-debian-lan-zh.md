---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在Debian局域网中启用SSH服务器
translated: true
type: note
---

问题：如何在 Debian 上启用 SSH 服务器，以便同一局域网内的另一台计算机可以连接。

答案：

在您想要通过 SSH **进入**的 Debian 机器上：

### 1. 安装 OpenSSH 服务器

```bash
sudo apt update
sudo apt install openssh-server
```

### 2. 启动并启用 SSH

```bash
sudo systemctl enable --now ssh
```

检查状态：

```bash
systemctl status ssh
```

您应该看到：

```text
Active: active (running)
```

### 3. 查找 Debian 机器的局域网 IP

```bash
ip addr
```

或者更简单：

```bash
hostname -I
```

例如：

```text
192.168.1.123
```

### 4. 从另一台计算机进行 SSH 连接

从 Linux/macOS：

```bash
ssh your_username@192.168.1.123
```

例如：

```bash
ssh zhiwei@192.168.1.123
```

首次连接时，您会看到主机密钥确认提示。输入：

```text
yes
```

然后输入 Debian 用户的密码。

### 5. 如果无法连接

检查 SSH 是否正在监听：

```bash
sudo ss -lntp | grep ':22'
```

您应该看到类似这样的输出：

```text
LISTEN 0 128 0.0.0.0:22
```

检查防火墙：

```bash
sudo nft list ruleset
```

如果您在使用 `ufw`：

```bash
sudo ufw status
```

如有必要，执行：

```bash
sudo ufw allow 22/tcp
```

### 6. 有用的测试：从另一台机器执行

```bash
ping 192.168.1.123
```

然后：

```bash
nc -vz 192.168.1.123 22
```

如果返回：

```text
Connection to 192.168.1.123 22 port [tcp/ssh] succeeded!
```

说明网络路径和 SSH 端口均正常工作。

**对于普通的家庭/局域网 Debian 机器，基本上只需要这些：** 安装 `openssh-server` → 启动 `ssh` → 查找其局域网 IP → `ssh user@IP`。

出于安全考虑，我建议使用 **SSH 密钥** 而非暴露密码认证，特别是如果这台机器将来可能从局域网外部访问。
