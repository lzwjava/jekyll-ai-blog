---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Fedora 上 SSH 服务器设置
translated: true
type: note
---

问题：逐行解释这个 bash 脚本的作用。

答案：

该脚本在 Fedora/RHEL 系列的 Linux 系统上设置 SSH 访问（使用 `dnf`，所以不是 Debian/Ubuntu）。

```bash
# 安装 OpenSSH 服务器包（接受传入 SSH 连接的守护进程）
sudo dnf install -y openssh-server
```

`dnf` 是包管理器。`openssh-server` 提供 `sshd`。`-y` 自动确认。注意：`openssh-clients`（用于*传出*连接的 `ssh` 命令）通常已安装——这是*服务器*端，以便其他机器可以*传入*连接。

```bash
# 在启动时启用服务并立即启动，一条命令完成
sudo systemctl enable --now sshd
```

`enable` 创建符号链接，使 `sshd` 在每次启动时运行。`--now` 也立即启动它，省去单独执行 `systemctl start sshd`。如果没有 `--now`，它会启用但不会运行，直到重启。

```bash
# 验证守护进程是否处于活动状态（查找“active (running)”）
sudo systemctl status sshd
```

显示状态、PID、最近的日志行。如果运行中则退出码为 0，否则为非零——在脚本中可通过 `systemctl is-active sshd` 使用。

```bash
# 打印机器的 IP 地址，以便知道 SSH 到哪个地址
ip addr show | grep "inet "
```

`ip addr show` 输出所有接口。`grep "inet "`（末尾有空格）仅过滤出 IPv4 行——排除 `inet6`。你会看到类似 `inet <IP_ADDRESS>/24` 的内容，位于 LAN 接口（如 `eth0`/`enp3s0`）上，以及环回接口的 `127.0.0.1`。LAN 上的那个地址是你用来连接的。

然后从另一台机器：`ssh user@<IP_ADDRESS>`。

脚本省略了一些实际中重要的内容：

- **防火墙。** Fedora 默认启用 `firewalld`，即使 `sshd` 运行，也会阻止端口 22。添加：`sudo firewall-cmd --add-service=ssh --permanent && sudo firewall-cmd --reload`。
- **更干净的 IP 查找。** `ip -4 -br addr` 给出每个接口一行摘要，或者 `hostname -I` 仅打印以空格分隔的 IP 地址——比使用 `grep` 过滤 `ip addr` 更容易在脚本中使用。
- **确认它正在监听。** `sudo ss -tlnp | grep :22` 证明 `sshd` 确实绑定了端口，这比 `systemctl status` 更有说服力。

对于你的设置（`lzw@192.168.1.36`），一旦该脚本运行并添加了防火墙规则，你就可以从 Air 上使用 `ssh lzw@192.168.1.36` 连接。使用 `ssh-copy-id` 放置 SSH 密钥可以完全跳过密码认证。
