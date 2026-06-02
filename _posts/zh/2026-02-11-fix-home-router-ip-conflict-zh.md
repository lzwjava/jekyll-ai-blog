---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 家用路由器 IP 冲突修复指南
translated: true
type: note
---

Question: 如果出现 IP conflict (IP 地址冲突)，且没有响应，而我只能连接到一个路由器，而该路由器又连接到家中的一个 Access Point (AP 接入点) 路由器，该怎么办？

Answer:

如果你在家庭网络设置中遇到 **IP address conflicts**（常见错误：Windows 上的“IP 地址冲突”，或设备无法上网、网速慢/无网络、无法访问路由器管理页面），特别是当一台路由器作为 **Access Point (AP)** 连接到主路由器时，通常会发生以下情况。以下是逐步修复的方法。

### 你的设置中最常见的原因
你的配置如下：
- **Main Router**（主路由器，例如连接到调制解调器，负责 DHCP，分配如 192.168.0.x 或 192.168.1.x 的 IP）。
- **Second Router**（第二台路由器，你的 TP-Link XDR3050 或 AX3000）设置为 **Access Point mode**（或者错误地保留在 Router mode）。

**问题场景**：
1. 第二台路由器 **仍处于 Router mode**（未切换到 AP mode） → 它运行自己的 DHCP server → 它分配与主路由器相同的 IP 范围 → 导致 IP conflict（例如，两个设备都在争夺谁来分配 192.168.0.100）。
2. 两台路由器具有 **相同的 LAN IP**（例如，两者都设置为 192.168.0.1） → 管理地址上发生直接 IP 冲突。
3. AP mode 设置不正确（例如，使用了 WAN port 而不是 LAN port，或者 DHCP 未禁用），它仍然试图充当路由器。
4. 在 Mesh/EasyMesh 设置中，某个节点配置错误或 Firmware Bug 导致 DHCP 重叠。

**你看到的症状**：
- 可以连接到一个路由器的 Wi-Fi，但无法连接到另一个。
- 出现“No internet”或“IP conflict”提示。
- 无法打开路由器管理页面（tplinkwifi.net 或 192.168.0.1 超时或冲突）。
- 部分设备可以工作，其他设备不行（取决于它们从哪个路由器的 DHCP 获取 IP）。

### 逐步修复（从最简单的开始）
1. **物理断开第二台路由器**（拔掉其电源和连接到主路由器的 Ethernet 网线）
   → 这会立即停止冲突的 DHCP。
   → 此时只有主路由器在运行 → 大多数设备应该能很快恢复上网。

2. **将电脑直接连接到主路由器**（Wi-Fi 或 Ethernet）
   → 确保你可以上网并能打开其管理页面（通常是 192.168.0.1 或 tplinkwifi.net）。

3. **对第二台路由器进行 Factory reset**（你想要作为 AP 使用的那台）
   - 在通电状态下按下 RESET 孔 10 秒以上 → 指示灯闪烁/重启。
   - 这将清除所有错误的设置。

4. **正确将第二台路由器设置为 Access Point mode**（避免 IP 冲突的关键步骤）
   **方法 A：通过 Web 界面（推荐）**
   - 暂时只将电脑连接到第二台路由器（Wi-Fi 或 Ethernet 连接到其 LAN port 之一）。
   - 打开浏览器 → 访问 http://tplinkwifi.net 或 192.168.0.1（重置后的默认地址）。
   - 登录（admin/admin 或设置新密码）。
   - 前往 **Advanced > Operation Mode**（或 System > Operation Mode）。
   - 选择 **Access Point** 模式 → Save → 路由器将重启。
   - **重要提示**：重启后，它的 IP 通常会变为类似 192.168.0.2（由主路由器自动分配）。
   - 查看贴纸、App 或在主路由器的“Connected Devices”列表中找到新的 IP。

   **方法 B：使用 TP-Link App**（如果 Web 操作不便）
   - 打开 TP-Link Wi-Fi App → Add device → 在设置过程中选择 AP mode。

5. **重新正确连接第二台路由器**
   - 使用 **Ethernet 网线**：主路由器的 **LAN port** → 第二台路由器的 **LAN port**（切勿连接到 WAN port！）。
   - 开启第二台路由器电源。
   - 它现在应该从主路由器获取 IP（不再运行 DHCP）。
   - Wi-Fi 名称/密码可以设置成与主路由器相同（实现无缝漫游）或不同。

6. **验证是否还存在冲突**
   - 在电脑/手机上：打开 cmd (Windows) 或 terminal → 输入 `ipconfig` (Windows) 或 `ifconfig`/`ip addr` (其他系统)。
   - Default gateway（默认网关）应该只有主路由器的 IP（例如 192.168.0.1）。
   - 尝试 ping 两台路由器的 IP → 应该都有响应。
   - 分别打开两台路由器的管理页面 → 应该可以正常访问且互不冲突。

### 如果重置后仍然没有响应/无法连接
- **尝试主路由器上的不同 Ethernet 端口**。
- **临时更改主路由器的 LAN IP 范围**（例如从 192.168.0.1 改为 192.168.1.1） → 如果第二台路由器卡在旧 IP 上，这会有所帮助。
- **在电脑上使用 Static IP** 以便在重置后访问第二台路由器：
  IP: 192.168.0.100
  Subnet: 255.255.255.0
  Gateway: 192.168.0.1
  → 然后访问 http://192.168.0.1 来设置 AP mode。
- **Firmware bug**：从 TP-Link 中国官网更新两台路由器的最新 Firmware（特别是 XDR3050 的 EasyMesh 版本）。

### 快速预防技巧
- 在连接网线之前，务必先将第二台路由器设置为 **AP mode**。
- 永远不要在 AP 路由器上使用 WAN port。
- 在使用 EasyMesh 时：如果你想要 Mesh 而不是传统 AP，请使用一键 EasyMesh 配对（但 AP mode 更简单，且零冲突风险）。

按照这些步骤操作——家庭 AP 设置中 90% 的 IP 冲突 + 无响应问题都可以通过步骤 4 和正确的线路连接解决。如果仍然无法解决，请告诉我：主路由器和 AP 路由器的具体型号，以及你的设备目前获取到的 IP（通过 ipconfig 查看）。

References:

- [https://www.tp-link.com.cn/support/faq/1384/](https://www.tp-link.com.cn/support/faq/1384/) (关于 AP 模式设置的中文 FAQ)
- [https://www.tp-link.com/support/faq/1384/](https://www.tp-link.com/support/faq/1384/) (Archer 系列的英文对应说明，流程类似)
