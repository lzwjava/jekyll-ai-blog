---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: TP-Link AX3000 路由器重置指南
translated: true
type: note
---

Question: 如何对 TP-Link AX3000 (Archer AX3000 系列 Wi-Fi 6 router) 进行完整的 factory reset (hard reset)？

Answer:

对 TP-Link AX3000 系列 Wi-Fi 6 router 执行 **complete factory reset**（也称为 factory default reset 或 hard reset）将清除所有自定义设置，包括 Wi-Fi 名称 (SSID)、密码、admin password、port forwarding、parental controls 以及任何其他配置。router 将恢复到原始的出厂状态。

主要有两种方法。强烈建议使用 **hardware reset**，特别是当你忘记了 admin password 或无法访问 web interface 时。

### Method 1: Hardware Reset (最可靠且彻底 – 推荐)

1. 确保 router 已接通电源（power 指示灯亮起）。
2. 在 router 的背面或底部找到小孔状的 **RESET** 键（这是一个微小的针孔，不是凸起的按钮）。
3. 使用回形针、牙签或笔尖等细长物体按住孔内的 reset 按钮。
4. **持续按住 8–10 秒**（某些型号可能需要 10 秒以上；建议完整按住 10 秒以确保成功）。
5. 观察以下代表 reset 正在进行的迹象：
   - SYS (system) 灯或其他状态灯通常会开始 **fast blinking**。
   - 所有指示灯可能会短暂熄灭，然后重新亮起或开始闪烁。
   - router 将自动 reboot（通常需要 30 秒到 1 分钟）。
6. 到达规定时间后松开 reset 工具。
7. 等待 router 完全重启且指示灯恢复稳定。

**成功 reset 后：**

- 默认 Wi-Fi 名称 (SSID) 和密码 → 印在 router 底部或背面的标签上（通常以 **TP-Link_XXXX** 开头，并配有随机密码）。
- Web management 地址 → http://tplinkwifi.net 或 http://192.168.0.1 或 http://192.168.1.1
- 默认登录信息 → username: **admin** / password: **admin** 
  (注意：在许多较新的 firmware 版本上没有默认的 admin/admin；第一次登录会强制你创建一个新密码。)

**Tip:** 如果你没看到指示灯有任何变化（没有快闪或重启），可能是按钮没有按到位。请尝试加大力度或使用更尖锐的工具。少数用户反馈在某些设备上需要按住 12–15 秒。

### Method 2: Software Reset (通过 web interface – 仅限仍能登录的情况)

1. 将你的电脑或手机连接到 router 当前的 Wi-Fi 网络，或者通过 Ethernet cable 直接连接到其中一个 LAN port。
2. 打开浏览器并访问 http://tplinkwifi.net 或 http://192.168.0.1 (或 http://192.168.1.1)。
3. 使用当前的 admin username 和 password 登录。
4. 进入 **Advanced** → **System Tools** (或 **System**) → **Backup & Restore** 或 **Factory Defaults**。
5. 点击 **Factory Defaults** / **Restore to Factory Default Settings** 并确认操作。
6. 等待 router 重启（通常 1–2 分钟）。

无论使用哪种方法，你都需要重新设置 router：
- 重新输入你的 ISP broadband 凭据（如果需要，输入 PPPoE username/password）。
- 创建新的 Wi-Fi 名称和密码。
- 在首次设置期间设置新的 admin password。

**Troubleshooting notes:**

- 如果 reset 后 router 仍不广播默认的 Wi-Fi SSID，或指示灯表现异常，可能表明存在硬件故障。
- 请在 TP-Link 官方支持网站上根据确切型号（例如 Archer AX55, AX3000 Pro 等）查询特定型号的 LED 行为和 reset 时间。
- 不同 firmware 版本和子型号之间存在细微差异，但按住 RESET 10 秒对于 AX3000 系列几乎是普遍有效的。

References:  

- 无（信息基于标准的 TP-Link Archer AX 系列 factory reset 程序，与截至 2026 年的 TP-Link 官方文档和用户手册一致）