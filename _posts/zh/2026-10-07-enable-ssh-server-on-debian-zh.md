---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在 Debian 上启用 SSH 服务器
translated: true
type: note
---

问题：如何在Debian上启用SSH服务器？

答案：

在Debian上，安装并启动OpenSSH server：

```bash
sudo apt update
sudo apt install openssh-server
```

检查 status：

```bash
sudo systemctl status ssh
```

如果它没有 running：

```bash
sudo systemctl start ssh
```

在 boot 时 enable 它：

```bash
sudo systemctl enable ssh
```

检查 listening port：

```bash
ss -tlnp | grep ssh
```

默认 SSH port 是 **22**。

从另一台机器 connect：

```bash
ssh username@debian_ip_address
```

查找 Debian 的 IP：

```bash
ip addr
```

示例：

```bash
ssh lzw@192.168.1.100
```

### 如果 firewall 是 enabled

对于 `ufw`：

```bash
sudo ufw allow ssh
```

或：

```bash
sudo ufw allow 22/tcp
```

### 有用的 configuration

Edit SSH server config：

```bash
sudo nano /etc/ssh/sshd_config
```

常见 changes：

```text
Port 22
PermitRootLogin no
PasswordAuthentication yes
```

在 changes 后 restart：

```bash
sudo systemctl restart ssh
```

### 对于 AI/GPU machines (common setup)

通常 you want：

```bash
sudo apt install openssh-server tmux htop nvtop
sudo systemctl enable --now ssh
```

然后你可以 SSH into the Debian box 并 leave long PyTorch/LLM training jobs running with `tmux`：

```bash
tmux new -s train
python train.py
```

Detach：

```
Ctrl+B then D
```

Reconnect later：

```bash
tmux attach -t train
```

这是 remote GPU servers 的 typical workflow。