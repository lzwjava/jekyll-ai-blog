---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 管理小型局域网IP地址
translated: true
type: note
---

在一个大约有5–10台电脑的小型LAN中，我该如何管理网络——查看每台设备的IP，以及应该使用哪些工具？

对于这么小的网络，你不需要企业级工具。一个简单实用的方案：

**1. 给每台设备一个已知、稳定的IP**
- 最简单的方法：在你的router上设置**DHCP reservations**（大多数家用/小型办公router都在其admin页面支持此功能，通常位于192.168.1.1或192.168.0.1）。这样设备仍然使用DHCP，但会根据其MAC地址始终获得相同的IP。
- 替代方案：在每台设备上手动分配**static IPs**，并避开你的router的DHCP范围以避免冲突。

**2. 查看当前连接了什么**
- **Router的admin页面** — 几乎所有router都有一个“connected devices”或“DHCP client list”页面，显示IP、MAC地址和hostname。
- **Nmap**（免费，跨平台） — 运行`nmap -sn 192.168.1.0/24`扫描整个subnet并列出在线主机。
- **Fing**（移动/桌面应用） — 非常易用的GUI，用于扫描你的LAN，显示设备名称、厂商和IP。
- **Angry IP Scanner** — 免费、简单的GUI扫描器，适用于Windows/Mac/Linux。

**3. 长期跟踪分配情况**
- 对于只有5–10台机器的情况，一个简单的电子表格（hostname、MAC、分配的IP、用途）其实就足够了。
- 如果你想要更自动化的方式，像**Pi-hole**（也提供广告拦截和DNS）这样的工具可以显示实时设备列表，并允许你分配本地hostname。

**4. 可选：集中管理**
- 如果这些是你要远程监控/管理的工作电脑，使用**TeamViewer**、**AnyDesk**，或设置一个轻量级**NAS with network monitoring**（例如Synology/QNAP dashboard）会有帮助，但对5–10台机器来说可能有点大材小用。

**建议的最小方案：** router的DHCP reservations + 用Fing或Nmap进行不定期扫描 + 电子表格日志。这就能清楚地覆盖“哪个IP对应哪台设备”，无需额外的基础设施。

References:
- [Nmap Official Site](https://nmap.org/)
- [Fing Network Scanner](https://www.fing.com/)
- [Angry IP Scanner](https://angryip.org/)
- [Pi-hole](https://pi-hole.net/)