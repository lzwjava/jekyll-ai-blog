---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: SSH 配置 Host 别名指南
translated: true
type: note
---

Question: 如何在 `~/.ssh/config` 中创建 aliases，以便在 ssh 命令中使用短名称而不是输入完整的 IP 地址或长主机名？

Answer: 

你可以轻松地在 `~/.ssh/config` 文件中为服务器创建简短且便于记忆的名称（aliases/Host shortcuts）。

### 最常用且整洁的方式（推荐）

```bash
# ~/.ssh/config

Host myserver          # ← 这是你将要输入的短名称
    HostName 192.168.1.45
    User username
    Port 22            # 可选 - 仅在不使用默认端口 22 时使用
    # IdentityFile ~/.ssh/my_special_key   # 可选

Host web
    HostName 10.55.3.120
    User ubuntu

Host prod-db
    HostName 172.31.45.189
    User ec2-user
    IdentityFile ~/.ssh/prod-db-key.pem

Host jump
    HostName bastion.company.com
    User admin
    ForwardAgent yes
```

添加这些条目后，你只需通过以下方式连接：

```bash
ssh myserver
ssh web
ssh prod-db
ssh jump
```

### 快速极简版本（仅 IP → 名称）

```bash
Host home-nas
    HostName 192.168.178.55

Host rpi
    HostName 192.168.178.88
```

然后：

```bash
ssh home-nas
ssh rpi
```

### 实际应用中的有用示例

```bash
# 1. 短名称 + 不同用户 + key
Host forge
    HostName 85.236.12.44
    User git
    IdentityFile ~/.ssh/forge_key

# 2. 使用通配符（适用于多个相似的服务器）
Host *.staging
    User deploy
    IdentityFile ~/.ssh/staging_key.pem

Host web-*
    User ubuntu
    IdentityFile ~/.ssh/web-servers.pem

# 然后你可以执行：
# ssh web-03.staging
# ssh web-17

# 3. Jump host / bastion 示例
Host internal-*
    ProxyJump jump.company.com
    User ubuntu

# 然后：ssh internal-db01
```

### 设置步骤

1. 打开或创建文件：

```bash
nano ~/.ssh/config
# 或者
code ~/.ssh/config
# 或者
vim ~/.ssh/config
```

2. 添加你的 Host 块（确保不同的 Host 条目之间有空行）

3. 设置正确的权限（非常重要！）：

```bash
chmod 600 ~/.ssh/config
```

4. 立即开始使用 — 无需重启 ssh

```bash
ssh myserver
# 甚至连 tab-completion（自动补全）通常也能工作
```

这是处理几十个甚至几百个服务器时最整洁、最流行的方法。

References:  

- [OpenSSH official documentation - ssh_config](https://man.openbsd.org/ssh_config)
- [Common SSH config patterns](https://linux.die.net/man/5/ssh_config)