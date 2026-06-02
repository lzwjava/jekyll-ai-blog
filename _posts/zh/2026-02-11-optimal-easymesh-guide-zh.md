---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: EasyMesh 最佳设置指南
translated: true
type: note
---

Question: 假设有一台主路由器（中国电信天翼网关，使用 PPPoE 账号如 <020xxx@163.gd>），以及两台子路由器（均为 TL-XDR3050 易展版）。我想让它们全部以 wired repeater（有线中继）/ wireless repeater（无线中继）模式工作，并考虑使用 DHCP mode 连接上游。

Answer:

您的配置如下：

- **主路由器** = 中国电信天翼网关（光猫/ONT，通常是中兴或类似型号，使用 PPPoE 拨号，账号类似 <020xxx@163.gd>）。
- **Sub1 和 Sub2** = 两台 TL-XDR3050 易展版路由器。
- 目标：将所有设备组网以获得更好的 Wi-Fi 覆盖（全屋无死角），支持有线或无线中继，同时避免 IP 冲突或无法上网的问题。

TL-XDR3050 易展版支持三种主要模式：

- **Router mode**（默认模式，开启自带的 DHCP）。
- **AP (有线中继) mode** —— 有线中继/接入点（推荐用于稳定性，wired backhaul 无速率损耗）。
- **Wireless repeater / EasyMesh mode** —— 无线中继/Mesh（通过“易展”按键一键配对，支持多级跳跃/级联）。

您可以混合使用这些模式：例如，使用 EasyMesh 进行无线扩展，或使用经典的 AP 模式进行有线连接。既然您有两台子路由器并提到“DHCP 模式连接上游”，如果需要无线连接，最安全且性能最好的方式是使用 **EasyMesh wireless**（或有线+无线混合）；如果您可以布线，则使用 **AP mode**。

### 推荐方案：使用 EasyMesh（无线或混合型）—— 最简单且支持多台子设备

XDR3050 上的 EasyMesh 最多支持 8 个节点（主路由 + 子路由），并支持多级跳跃（例如：主路由 → sub1 无线 → sub2 无线）。它会自动处理 DHCP（仅主路由拨号并运行 DHCP；子路由同步设置并禁用自身的 DHCP）。

**步骤**：

1. **准备主天翼网关**：
   - 保持其为 **Router mode**（默认）—— 它使用您的 <020xxx@163.gd> 账号进行 PPPoE 拨号，并提供上网功能和 DHCP（通常 LAN IP 为 192.168.1.1）。
   - 除非您想让 XDR3050 拨号，否则**不要**改为桥接模式（虽然性能可能更好，但如果出现账号/VLAN 问题，风险较大）。
   - 先不要连接任何设备。

2. **将一台 XDR3050 设置为“主/扩展”路由器（可选，但推荐以便更好控制）**：
   - 将两台 XDR3050 恢复出厂设置（按住 RESET 键 10 秒以上）。
   - 将一台 XDR3050 临时连接到 PC（通过 Wi-Fi 或 LAN 线）。
   - 登录：<http://tplinkwifi.net> 或 192.168.0.1。
   - 如果您希望它代替网关处理 PPPoE（以获得完整的 Wi-Fi 6 速度并减少二级 NAT）：
     - 进入 Advanced > Internet > 更改为 PPPoE > 输入 <020xxx@163.gd> 账号/密码 > 保存。
     - 但首先要测试网关是否可以桥接（使用电信超级管理员密码登录网关 192.168.1.1，将 WAN 设置为 Bridge；搜索“天翼网关 桥接”查看具体型号教程）。
   - 大多数用户保留网关作为主拨号器以避免复杂化。

3. **一键 EasyMesh 配对（用于无线中继）**：
   - 将 sub1 放置在网关附近（信号覆盖良好的区域）。
   - 开启网关和 sub1 XDR3050 的电源。
   - 按下**任意一个**设备上的 **EasyMesh button**（背板上标记为“易展”，按住 1-3 秒）。
   - 指示灯闪烁（搜索中）→ 常亮/蓝色/绿色 = 配对成功。
   - Sub1 将从网关同步 Wi-Fi 名称/密码（或者您稍后设置统一的 SSID）。
   - 对 sub2 重复此操作：将 sub2 放在 sub1（或网关）附近，再次按下 EasyMesh 按键 —— 它将加入网络（自动选择最佳父节点，支持 2 级及以上跳跃）。
   - 结果：无缝漫游，单一 SSID，主网关处理 DHCP/上网，子路由作为扩展器运行且无 IP 冲突。

4. **如果您偏好有线中继（速度更佳/更稳定，无多跳损耗）**：
   - 在每台 XDR3050 上（复位后）：
     - 登录 → Advanced > Operation Mode > 选择 **AP (有线中继)** → 保存并重启。
     - 重启后，它会自动禁用 DHCP 并成为纯接入点。
   - 连接方式：网关 LAN 口 → 网线 → XDR3050 **LAN 口**（不是 WAN 口！）。
   - 对 sub2 执行相同操作（可以级联：网关 → sub1 LAN-to-LAN → sub2 LAN-to-LAN）。
   - 为实现漫游，设置与网关相同的 Wi-Fi SSID/密码（如果需要区分，也可以设为不同）。
   - 因为只有网关运行 DHCP，所以不会产生 IP 冲突。

5. **避免 IP 冲突和“无响应”问题**：
   - 连接时**千万不要**让子路由处于 Router mode —— 它们会运行重复的 DHCP 并导致冲突（设备会获取错误的网关 IP，导致无法上网）。
   - 在 EasyMesh 模式下：自动处理（子路由不运行 DHCP）。
   - 在 AP mode 模式下：DHCP 已禁用。
   - 如果发生冲突：断开子路由 → 重置它们 → 设置为 AP/EasyMesh → 重新连接。
   - 检查 IP：在 PC 上运行 `ipconfig` (Windows) —— Default Gateway 应该仅为天翼网关的 IP（例如 192.168.1.1）。

**如何选择？**

- **仅限无线** → EasyMesh 一键配对（支持 sub1 → sub2 跳跃，适合未布线的房屋）。
- **部分有线** → 混合模式：sub1 有线连接到网关（更快的背传），sub2 无线连接到 sub1。
- **全有线** → 两台子路由均使用 AP mode（最快、最稳定，无速率减半）。

分步测试：先从一台子路由开始，确认其 Wi-Fi 下可以上网，再添加第二台。如果配对失败，请从 TP-Link 中国官网更新所有设备的 firmware。如果尝试桥接时出现 PPPoE 问题，请坚持使用网关拨号。

References:

- [https://www.tp-link.com.cn/product_2196.html](https://www.tp-link.com.cn/product_2196.html)
- [https://service.tp-link.com.cn](https://service.tp-link.com.cn) (TP-Link EasyMesh/AP 设置通用支持)
