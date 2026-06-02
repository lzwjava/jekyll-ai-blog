---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Ansible 快速入门指南
translated: true
type: note
---

别担心！`ansible --help` 的输出确实很吓人，但 **99% 的时间你只需要几个选项**。

以下是在 2025 年使用 `ansible` ad-hoc（不编写 playbook）最简单的“入门”方法。

### 1. 最快的测试（在 localhost 上运行，无需 SSH，无需 inventory）

```bash
ansible localhost -m ping
```

你应该看到的输出：

```json
localhost | SUCCESS => {
    "changed": false,
    "ping": "pong"
}
```

恭喜 — Ansible 正在运行！

### 2. 在一台远程服务器上运行命令（最常见的初学者情况）

假设：

- 你有一台服务器 192.168.1.100
- 你通常以用户 `ubuntu` 的身份使用密钥 (~/.ssh/id_rsa) SSH 到它

```bash
ansible 192.168.1.100 -m command -a "uptime" -u ubuntu --private-key ~/.ssh/id_rsa
```

或者更短（如果你的 SSH key 已在 ssh-agent 中，并且 user 在 ~/.ssh/config 或 default 中是正确的）：

```bash
ansible 192.168.1.100 -m command -a "uptime"
```

### 3. 同时在多台服务器上运行相同的命令

只需提供一个逗号分隔的列表或一个模式：

```bash
ansible 192.168.1.10,192.168.1.11,192.168.1.12 -m command -a "df -h"

# 或者如果你以后使用 inventory 文件，带有通配符
ansible webservers -m ping
```

### 4. 你每天都会用到的最有用的初学者单行命令

```bash
# 检查哪些主机可达
ansible all -m ping

# 重启所有服务器并等待它们恢复
ansible all -m reboot --forks 20

# 更新所有包 (Debian/Ubuntu)
ansible all -m apt -a "name=* state=latest" -b

# 更新所有包 (RHEL/CentOS/Rocky/Fedora)
ansible all -m dnf -a "name=* state=latest" -b
# 或者在旧系统上使用 yum
ansible all -m yum -a "name=* state=latest" -b

# 复制文件到所有服务器
ansible all -m copy -a "src=./motd dest=/etc/motd backup=yes" -b

# 使用 sudo 运行原始 shell 命令
ansible all -m shell -a "tail -20 /var/log/syslog" -b
```

`-b` 表示“成为 root”（像 sudo）。如果它要求你的 sudo 密码，添加 `-K`：

```bash
ansible all -m apt -a "name=* state=latest" -b -K
```

### 5. 让它变得更容易 — 创建一个微型 inventory 文件（可选但推荐）

在你当前目录下创建一个名为 `inventory.ini` 的文件：

```ini
[webservers]
web1.example.com
web2.example.com
web3.example.com

[dbservers]
db1.example.com ansible_user=centos ansible_ssh_private_key_file=~/.ssh/special.pem
```

然后只需执行：

```bash
ansible webservers -m ping -i inventory.ini
```

或者将它放在 `~/.ansible/hosts` 或 `/etc/ansible/hosts` 中，你就可以完全跳过 `-i`。

### TL;DR — 作为初学者你需要记住的 3 个命令

```bash
# 1. 本地测试
ansible localhost -m ping

# 2. 测试远程服务器（替换 IP 或主机名）
ansible your.server.com -m ping

# 3. 做一些有用的事情（示例：更新所有内容）
ansible all -m apt -a "name=* state=latest" -b    # Ubuntu/Debian
# 或者
ansible all -m dnf -a "name=* state=latest" -b    # RHEL 8+/Rocky/Fedora
```

就是这样！一旦你熟悉了这些，你就会自然而然地转向真正的 playbook。但是 ad-hoc 命令 `ansible` 已经可以为你每周节省数小时。🚀

告诉我你接下来想做什么（更新服务器、部署文件、安装 Docker 等），我将为你提供确切的单行命令！
