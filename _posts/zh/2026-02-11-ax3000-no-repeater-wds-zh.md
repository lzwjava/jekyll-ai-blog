---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: AX3000 无中继或 WDS 模式
translated: true
type: note
---

Question: TP-Link AX3000 (Archer AX3000 系列，例如 AX55/AX3000 Wi-Fi 6 路由器) 是否支持作为无线中继器 (Repeater) 或无线桥接 (WDS) 来扩展信号？

Answer: 

TP-Link AX3000 系列路由器，包括 Archer AX55 及类似的 AX3000 Wi-Fi 6 设备，**不支持传统的无线中继 (Repeater) 或 WDS 桥接模式**来无线扩展 Wi-Fi 信号。

许多用户反馈在管理页面 (tplinkwifi.net 或 192.168.0.1) 中找不到 "Wireless Repeater"、"WDS Bridging" 或 "扫描 Wi-Fi 进行桥接" 等选项。这是设计使然：AX 系列中较新的 Wi-Fi 6 路由器已经逐步淘汰了传统的 WDS 功能，转而支持更现代的 Mesh 解决方案，如 OneMesh 或 EasyMesh。

### 为什么无线设置页面缺少中继/桥接选项
- **Wireless** 部分通常只包含基础设置：SSID、密码、信道、访客网络等。
- 不存在“扫描其他 Wi-Fi 网络并转发”的按钮。
- 较旧的 TP-Link 型号（如 WR 系列，以及部分 Archer C 系列如 C80 或 C7）包含明确的 WDS/Repeater 选项。
- AX 系列路由器主要设计为**主路由器**或**有线 Access Point (AP mode)** —— 它们需要通过 Ethernet cable 连接到上级路由器来进行扩展。

要使用 AX3000 进行信号扩展，通常需要一个专门的 Range Extender（例如 TP-Link RE 系列）。

### 它能否用于二次（级联）无线中继？
- **不能**，因为它甚至无法执行单级无线转发。
- 即使在支持 WDS 的旧款路由器上，级联 2-3 次在理论上可行，但性能极差：
  - 由于接收/发送共用信道，每一跳的带宽会减半（甚至更多）。
  - 延迟增加、信号不稳定、频繁掉线。
  - 级联超过两次极少能成功，且不建议这样做。
- TP-Link 建议使用兼容 OneMesh/EasyMesh 的设备进行多跳扩展（尽管信号仍会随跳数衰减；建议最多限制在 2-3 台）。

### 推荐的解决方案
1. **最佳选择**：购买兼容 TP-Link OneMesh 或 EasyMesh 的 Range Extender 或 Mesh 节点。
   - 示例：RE705X 或 RE715X (AX3000 Wi-Fi 6 扩展器) —— 支持 OneMesh，配对简单，实现无缝漫游。
   - 如果你的主路由器支持 OneMesh（部分 AX55/AX 系列在固件更新后支持），可直接配对。
   - 对于双重扩展：主路由器 → 扩展器 1 → 扩展器 2 (Mesh 允许多跳，但需预料到衰减)。
2. **强力替代方案（有线，最稳定）**：将 AX3000 设置为 **Access Point (AP) mode**。
   - 进入 Advanced > Operation Mode > Access Point。
   - 通过 Ethernet cable 连接：主路由器 LAN 端口 → AX3000 LAN 端口（非 WAN）。
   - 多个 AP 可以串联（主路由器 → AP1 → AP2），且无速度损失。
3. **如果坚持使用无线**：
   - 使用支持 WDS 的旧款 TP-Link 型号（但会失去 Wi-Fi 6 的优势和速度）。
   - 或者安装第三方固件如 OpenWrt（对 AX3000 的支持有限且有风险；不建议普通用户尝试）。
4. **排查你的设置**：
   - 确认具体型号（例如 Archer AX55 Vx）并更新固件 (Advanced > System Tools > Firmware Upgrade)。
   - 主路由器的无线页面不会显示扫描选项 —— 这是正常的（它负责广播，不扫描其他信号）。
   - 中继/桥接设置仅适用于从属设备，而 AX3000 缺少此特征。
   - 如果重置后尝试无线扩展他人的 Wi-Fi，它无法以无线方式实现。

为了获得更精确的建议，请提供具体的型号（例如 Archer AX55 V1/V2）以及你想扩展的主路路由器的品牌和型号。

References:  
- [TP-Link Community: AX3000/AX55 no WDS option](https://community.tp-link.com/us/home/forum/topic/244588)
- [TP-Link Community: Archer AX55 does not support WDS](https://community.tp-link.com/en/home/forum/topic/623082)
- [TP-Link OneMesh Compatible Devices List](https://www.tp-link.com/onemesh/product-list)
- [TP-Link WDS Bridging FAQ (applies to older models only)](https://www.tp-link.com/us/support/faq/1555)