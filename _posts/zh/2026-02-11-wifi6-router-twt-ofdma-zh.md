---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: WiFi 6 路由器 TWT 与 OFDMA 指南
translated: true
type: note
---

问题：在路由器中，“TWT 开关”和“OFDMA 开关”是什么意思？

回答：

**TWT 开关**和 **OFDMA 开关**是许多现代路由器（特别是 TP-Link、ASUS、H3C 等品牌的 Wi-Fi 6 (802.11ax) 或 Wi-Fi 7 型号）高级无线设置中的功能切换选项。

这些都是 Wi-Fi 6 标准的核心特性。

- **TWT 开关** (Target Wake Time switch)
  TWT 是一种节能技术。
  当开启（开关 = ON）时，路由器会与兼容的客户端设备（手机、平板、IoT 传感器等）进行协商，约定设备“唤醒”以发送或接收数据的具体时间。
  这允许设备在更多时间内处于睡眠模式，从而显著延长移动设备和电池供电设备的电池寿命。
  它还能减少不必要的 Wi-Fi 信道竞争（Airtime 竞争），有助于在拥有大量设备的家庭中让整体网络运行更顺畅。
  **建议**：如果你拥有 Wi-Fi 6 设备（尤其是智能手机或智能家居设备等电池供电设备），通常建议开启。部分用户反馈旧设备或不兼容设备可能会出现偶发断连，如果遇到稳定性问题，请将其关闭。

- **OFDMA 开关** (Orthogonal Frequency Division Multiple Access switch)
  OFDMA 是 Wi-Fi 6 中最重要的核心特性之一。
  当开启（开关 = ON）时，路由器可以将单个 Wi-Fi 信道划分为更小的子信道（称为 Resource Units 或 RUs）。这使得路由器能够同时与多个设备通信，而不是让它们轮流等待。
  其优势包括：
  - 在繁忙网络（同时连接多台手机、电脑、智能电视等）中表现出极高的效率
  - 降低 Latency（对于 Gaming、视频通话或 IoT 特别有用）
  - 当多个设备活跃时，提升整体网络容量和 Throughput
  **建议**：在现代 Wi-Fi 6 路由器中几乎总是建议开启。它对旧设备（Wi-Fi 5 或更早版本）几乎没有负面影响，且在存在 Wi-Fi 6 客户端时会带来明显提升。大多数专家和制造商都建议保持开启。

**快速总结表**：

| 特性 | 全称 | 主要优势 | 推荐设置 | 仅适用于 |
| :--- | :--- | :--- | :--- | :--- |
| TWT | Target Wake Time | 节省设备电量，减少 Airtime 浪费 | 通常开启（测试稳定性） | Wi-Fi 6 设备 |
| OFDMA | Orthogonal Frequency Division Multiple Access | 允许单信道同时与多设备通信 | 强烈推荐开启 | Wi-Fi 6 设备（但在混合网络中是安全的） |

在 2026 年典型的家庭网络环境下，除非你遇到旧设备的特定兼容性问题，否则你应该将 **两者都开启**。

References:

- [ASUS Wireless Router Professional Settings FAQ](https://www.asus.com/us/support/faq/1011438)
- [TP-Link WiFi AX Router Wireless Settings Optimization](https://cyberraiden.wordpress.com/2025/03/09/tp-link-wifi-axwifi-6-router-wireless-settings-for-better-connectivity-and-stability)
- [Reddit discussion on enabling OFDMA and TWT](https://www.reddit.com/r/TpLink/comments/13logv5/enabling_ofdma_and_twt_on_my_wifi_6_router_worth)
- [Explanation of Target Wake Time](https://www.turn-keytechnologies.com/blog/article/what-is-target-wake-time-2)
- [OFDMA in Wi-Fi 6](https://www.extremenetworks.com/resources/blogs/what-is-ofdma-and-how-does-it-enhance-802-dot-11ax-wi-fi-6-technologies)
