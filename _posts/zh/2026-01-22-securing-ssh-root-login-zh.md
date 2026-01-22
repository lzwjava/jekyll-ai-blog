---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 保障 SSH 安全：Root 登录最佳实践
translated: true
type: note
---

**Question:** 如何移除 SSH root key (从 authorized_keys 中)，以及 "PermitRootLogin" 是什么意思？禁用通过 SSH 登录 root 有什么好处？

**Answer:**

这里涉及两个相关但不同的概念：

1. **移除特定的 SSH public key**（针对 root 用户，使 root 无法再使用该特定密钥登录）。
2. **完全禁用 root 登录**（或对其进行限制），通过 SSH 中的 `PermitRootLogin` 设置来实现 —— 这通常是人们所说的“移除 SSH root 登录”或“禁用 root SSH 访问”的意思。

### 1. 如何移除 root 的特定 SSH public key

允许登录的 public keys 存储在：

```
/root/.ssh/authorized_keys
```

（在极少数旧系统中可能是 `/root/.ssh/authorized_keys2`）

**移除一个密钥的步骤：**

- 以 root 身份或具有 sudo 权限的用户通过 SSH 登录服务器
- 打开文件：

```bash
sudo nano /root/.ssh/authorized_keys
# 或
sudo vim /root/.ssh/authorized_keys
```

- 找到以 `ssh-rsa`、`ecdsa-sha2-nistp256` 或 `ssh-ed25519` 开头的那一行 —— 这就是一个 public key
- 删除你想要移除的密钥所对应的整行内容
- 保存并退出

**更快捷的命令行方式**（如果你知道密钥的部分内容）：

```bash
# 示例：移除包含 "AAAAB3NzaC1yc2EAAAADAQABAAABAQ..." 的密钥
sudo sed -i '/AAAAB3NzaC1yc2EAAAADAQABAAABAQ/d' /root/.ssh/authorized_keys
```

**若要移除所有密钥**（完全停止基于密钥的 root 登录）：

```bash
sudo mv /root/.ssh/authorized_keys /root/.ssh/authorized_keys.bak
# 或直接删除
sudo rm /root/.ssh/authorized_keys
```

更改 authorized_keys 后，通常**不需要**重启 sshd。

### 2. 什么是 `PermitRootLogin` 以及如何禁用 root 登录

此设置位于 `/etc/ssh/sshd_config`（或现代系统中的 `/etc/ssh/sshd_config.d/` 文件）。

常见取值：

- `yes` → root 可以通过 password **或** key 登录（非常不安全）
- `prohibit-password`（或旧称：`without-password`）→ root **仅能**通过 key 登录，**不能**通过 password
- `forced-commands-only` → root 仅能通过 key + 强制命令（forced command）登录（很少使用）
- `no` → root 完全无法通过 SSH 登录（出于安全考虑，推荐此设置）

**推荐的安全设置（适用于大多数服务器）：**

```bash
sudo nano /etc/ssh/sshd_config
```

修改或添加：

```
PermitRootLogin no
```

然后重启 SSH 服务：

```bash
# Ubuntu/Debian
sudo systemctl restart ssh

# CentOS/RHEL/AlmaLinux/Rocky
sudo systemctl restart sshd
```

更改后：
- 任何人无法通过 `ssh root@server` 登录
- 你必须先通过 `ssh normaluser@server` 登录 → 然后使用 `sudo -i` 或 `sudo su -` 切换为 root

### 禁用通过 SSH 登录 root 的好处 (`PermitRootLogin no`)

- **阻断大多数 brute-force attacks** —— 机器人（bots）通常只尝试用户名 "root" + 常用密码。
- **大幅增加攻击难度/耗时** —— 攻击者需要先获得有效的普通用户账号 + password/key **+** 然后再进行权限提升（privilege escalation）到 root（从一步变成两步）。
- **更好的审计日志（audit logging）** —— 使用 `sudo` 时，日志会记录谁执行了哪条命令（例如："user zhiwei ran rm -rf /"）。
- **更易于撤销访问权限** —— 只需禁用/锁定一个普通用户账号，而无需更改所有地方的 root 密码。
- **符合安全最佳实践** —— 几乎所有的云服务商（AWS, GCP, DigitalOcean 等）和安全标准（CIS benchmarks）都采用了这一做法。

**快速总结 —— 现今大多数安全服务器的做法：**

- 设置 `PermitRootLogin no`
- 设置 `PasswordAuthentication no`（仅允许基于密钥的登录）
- 使用具有 sudo 权限的普通用户
- 使用强 SSH keys（首选 ed25519）

这种组合可以防御约 99% 的自动化 SSH 攻击。

**References:**

- [https://man7.org/linux/man-pages/man5/sshd_config.5.html](https://man7.org/linux/man-pages/man5/sshd_config.5.html)
- [https://www.baeldung.com/linux/root-login-over-ssh-disable](https://www.baeldung.com/linux/root-login-over-ssh-disable)
- [https://security.stackexchange.com/questions/34915/what-is-the-actual-value-of-disabling-remote-root-login-using-ssh](https://security.stackexchange.com/questions/34915/what-is-the-actual-value-of-disabling-remote-root-login-using-ssh)