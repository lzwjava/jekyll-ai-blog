---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 验证安装后sshd是否运行
translated: true
type: note
---

**问题：安装 OpenSSH 服务器后，如何验证 `sshd` 是否正在运行？**

答案：

在 Ubuntu/Debian 系统上，检查 SSH 服务状态：

```bash
sudo systemctl status ssh
```

预期输出：

```
● ssh.service - OpenBSD Secure Shell server
     Loaded: loaded
     Active: active (running)
```

快速检查：

```bash
systemctl is-active ssh
```

输出：

```
active
```

---

检查 `sshd` 是否在某个端口上监听：

```bash
sudo ss -tlnp | grep ssh
```

示例：

```
LISTEN 0 128 0.0.0.0:22 0.0.0.0:* users:(("sshd",pid=1234,fd=3))
LISTEN 0 128 [::]:22    [::]:*    users:(("sshd",pid=1234,fd=4))
```

这表示 SSH 守护进程正在端口 22 上接受连接。

---

直接检查进程：

```bash
ps aux | grep sshd
```

示例：

```
root  1234  0.0  sshd: /usr/sbin/sshd -D
```

---

如果你手动创建了 `/run/sshd` 并运行了 `which sshd`，你只是验证了二进制文件的存在：

```bash
which sshd
# /usr/sbin/sshd
```

你仍然需要启动守护进程：

```bash
sudo systemctl start ssh
```

设置开机自启：

```bash
sudo systemctl enable ssh
```

---

对于容器/云虚拟机环境（常见于 GPU 实例），可能没有 `systemctl`。请使用：

```bash
sudo /usr/sbin/sshd -t   # 验证配置
sudo /usr/sbin/sshd      # 启动 sshd
```

然后：

```bash
ps aux | grep sshd
ss -tlnp | grep :22
```

---

从另一台机器测试：

```bash
ssh username@server_ip
```

或：

```bash
ssh -v username@server_ip
```

`-v` 会显示连接握手过程，通常是调试 SSH 问题最快的方法。