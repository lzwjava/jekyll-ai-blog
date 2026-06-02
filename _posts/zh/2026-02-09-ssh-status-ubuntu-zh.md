---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 在 Ubuntu 上检查 SSH 状态
translated: true
type: note
---

**Question:** 如何检查我的 Ubuntu 系统上 SSH service 是否正在运行/开启？

**Answer:**

以下是在 Ubuntu 机器（2024–2026 版本）上检查 SSH（通常是 OpenSSH server）是否正在运行并监听的最可靠且常用的方法：

### 最快 & 推荐的方法

1. **检查 service status（最推荐）**

```bash
sudo systemctl status ssh
```

或者

```bash
systemctl status ssh
```

查找以下关键行：

- `Active: active (running)` → SSH 正在 **running**
- `Active: inactive (dead)` → SSH 已 **stopped**
- `Active: failed` → SSH 启动失败（请查看下方的错误信息）

别名注意：在 Ubuntu 上，该 service 通常被称为 `ssh`（而不是 `sshd`）

2. **更简短的方法 – 仅检查是否 active**

```bash
systemctl is-active ssh
```

输出：

- `active`   → running
- `inactive` → stopped
- `failed`   → crashed

3. **检查 SSH port 是否正在监听（非常可靠）**

```bash
# 最流行且简洁的方法（推荐）
ss -tuln | grep :22

# 其他替代命令（均有效）
sudo netstat -tuln | grep :22
sudo lsof -i :22
sudo ss -tuln  | grep ':22.*LISTEN'
```

如果你看到类似以下的输出 → 说明 SSH **正在监听**：

```
tcp   LISTEN 0      128          0.0.0.0:22        0.0.0.0:*
# 或
tcp   LISTEN 0      128             [::]:22           [::]:*
```

如果没有输出 → 说明 SSH **没有监听**（可能未安装或未运行）

### 一行命令检查“我现在可以通过 SSH 连接吗？”

```bash
# 方法 A - 非常清晰
sudo systemctl is-active --quiet ssh && echo "SSH is RUNNING" || echo "SSH is STOPPED"

# 方法 B - 端口检查方式
ss -tuln | grep -q ':22 ' && echo "Port 22 is OPEN" || echo "Port 22 is CLOSED"
```

### 总结 – 最快记忆的命令

| Command | What it tells you | Recommendation |
|---------|-------------------|----------------|
| `systemctl is-active ssh` | 运行中或未运行 | ★★★ 日常检查首选 |
| `ss -tuln \| grep :22` | 确实在 port 22 上监听 | ★★★ 非常可信 |
| `sudo systemctl status ssh` | 详尽状态 + 最近日志 | 故障排查时首选 |

### 进阶 – 如果你想从外部查看

**从另一台电脑**运行此命令：

```bash
# 将 192.168.1.100 替换为你 Ubuntu 机器的 IP
nc -zv 192.168.1.100 22
```

输出：

- `succeeded!` → SSH port 已开启且可访问
- `Connection refused` / timeout → SSH 已关闭、受 firewall 拦截或存在网络问题

选择你最喜欢的风格 — 大多数 Ubuntu 用户只需使用：

```bash
systemctl is-active ssh && ss -tuln | grep -q :22 && echo "SSH looks good ✓" || echo "SSH has problem ✗"
```

**References:**

- 无需引用（标准 Ubuntu 命令，适用于 2024–2026 版本）
