---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 远程 WiFi 破解设置指南
translated: true
type: note
---

**问题：** 使用 OpenClaw 来破解 WiFi 密码，最好的方式是不是使用另一台电脑，让 OpenClaw 通过 SSH 连接到那台电脑在那上面进行破解？这是因为运行 OpenClaw 的电脑需要保持连接到网络，而 WiFi 黑客行为会中断正常的互联网连接，对吗？

**回答：**

是的，你的推理完全正确，这也是使用 OpenClaw 进行 WiFi 密码破解（握手捕获 + 使用工具如 `airodump-ng`、`aireplay-ng`、`aircrack-ng`、`hashcat` 等进行破解）的最干净、最实用的方式之一。

### 为什么 WiFi 黑客行为会中断正常连接
- 将无线接口置于 **monitor mode**（用于数据包注入、deauth 攻击和捕获握手所必需）会使其无法用于常规客户端流量。
- 大多数 Linux 发行版（Kali、Parrot 等）在你运行 `airmon-ng start wlan0` 的那一刻就会断开现有的 WiFi 连接。
- 如果你的主机关只通过同一个 WiFi 接口连接，OpenClaw（或其上的任何进程）会立即失去互联网访问权限，这可能会中断 LLM API 调用、文件下载等。

### 推荐架构（正是你描述的）
1. **专用的破解机**（例如，便宜的笔记本电脑、Raspberry Pi 5 + Alfa AWUS036ACH，或带 USB WiFi 适配器的旧台式机）：
   - 安装 Kali Linux 或最小化的 Arch/Debian，带有 `aircrack-ng` 套件 + `hashcat`。
   - 启用仅使用密钥认证的 SSH（无密码）。
   - 将这台机器物理放置在目标 AP 附近以获得良好信号。

2. **主要的 OpenClaw 主机**（你的日常驱动器、VPS 或云实例）：
   - 正常运行 OpenClaw（通过 Ethernet、二级 WiFi 或有线连接享有完整的互联网访问）。
   - 你通过 WhatsApp/Telegram 等或 web UI 与 OpenClaw 聊天。
   - OpenClaw 只是简单执行：
     ```bash
     ssh -i ~/.ssh/id_rsa user@cracker-box "sudo airmon-ng start wlan0 && sudo airodump-ng -c 6 --bssid XX:XX:XX:XX:XX:XX wlan0mon -w /tmp/capture"
     ```
     （或任何你想要的序列 — 捕获握手 → deauth → 使用 hashcat 破解等。）

3. **额外提示：让它更顺畅**
   - 使用 OpenClaw 内置的 `exec` 工具或自定义 skill 来包装 SSH。
   - 在 OpenClaw 主机上存储私钥，并使用密钥转发（`ssh -A`）。
   - 对于完全自治的操作，告诉 OpenClaw：“使用破解机从网络 XYZ 捕获 WPA2 握手，并使用 rockyou.txt + hashcat 破解它，然后告诉我密码。”
   - OpenClaw 将通过 SSH 处理整个链条，而不会触及其自身的 WiFi 接口。

### OpenClaw 原生支持的替代远程设置
- **SSH 隧道 + 远程 Gateway 模式**（参见文档）：在破解机上运行完整的 OpenClaw Gateway，并将端口 18789 隧道回你的主机器。然后代理会在破解硬件上本地执行工具，而你远程控制它。
- **Tailscale / WireGuard**：更干净 — 无需端口转发，全网格。

两种方法都实现相同目标：保持你的主要 OpenClaw 实例在线，而繁重工作（monitor-mode WiFi）在其他地方进行。

### 快速检查清单，避免麻烦
- 使用支持 monitor mode + injection 的专用 USB WiFi 卡（Atheros AR9271、Realtek RTL8812AU 等）。
- 以非 root 用户运行一切，在需要时使用 `sudo`。
- 始终使用 SSH 密钥认证，绝不用密码。
- 如果你在云 VPS 上做这件事，确保它有公网 IP 或 Tailscale 以便轻松访问。

你提出的方法不仅仅是“好” — 它是当你想从稳定机器上保持持久控制时进行无线 pentesting 的 **标准专业方式**。OpenClaw 只是让整个过程用自然语言编排变得异常简单。

**参考资料：**
- [OpenClaw 远程访问文档 (SSH 隧道、Tailscale、远程 Gateway)](https://docs.openclaw.ai/gateway/remote)
- [使用 OpenClaw + Kali 构建自治黑客装置](https://www.youtube.com/watch?v=C5ir_rQ4L4g)（展示了正是这种远程工具执行）