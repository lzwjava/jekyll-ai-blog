---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 通过 WAN IP 地址访问 OpenWrt
translated: true
type: note
---

**Question:** 对于连接到主路由器的 OpenWrt 路由器，连接到 OpenWrt 的电脑是否可以通过访问 OpenWrt 的 WAN IP 地址来登录（例如访问 LuCI Web 界面）？我尝试过但没有成功——这可能是 Firewall 问题吗？

**Answer:**

不，在典型的 OpenWrt 设置中，这通常是**默认无法实现的**，而且在大多数情况下，这**主要不是 Firewall 问题**。

以下是失败的原因以及你可以采取的措施：

### 典型的家庭网络设置（最常见的失败原因）
- 主路由器：192.168.1.1（或类似地址）
- OpenWrt WAN 端口连接到主路由器 LAN → OpenWrt 获取私网 WAN IP（例如 192.168.1.50）
- OpenWrt LAN：192.168.2.1（或你设置的任何地址；应与主路由器处于不同网段）
- 你的电脑连接到 OpenWrt LAN → 获取类似 192.168.2.100 的 IP

当你的电脑尝试访问 OpenWrt **WAN IP** (192.168.1.50) 时：

- 数据包发送到 OpenWrt 路由器（因为它是默认网关）
- OpenWrt 发现目标地址是其自身的 WAN IP
- 但 Linux Kernel（以及 OpenWrt）倾向于从**最近的/所属的接口**进行响应 → 它会通过 **LAN 接口**而不是 WAN 进行响应
- 返回的数据包通过 LAN 接口发出 → 源 IP = 192.168.2.1（而不是 192.168.1.50）
- 你的电脑收到了来自错误源 IP 的回复 → 连接失败或表现异常

这是正常的 Linux Routing 行为（并非 OpenWrt 特有）。NAT Loopback / Hairpinning 仅在**从内部访问你自己的公网 IP** 时有效，而对访问私网 WAN IP 无效。

### 解决方案（任选其一）

1. **推荐且最简单的方案**  
   直接使用 OpenWrt 的 **LAN IP**（例如 http://192.168.2.1 或 http://openwrt.lan）。  
   几乎没有理由强行从内部网络通过 WAN IP 进行访问。

2. **如果你确实想通过 WAN IP 访问**  
   - 创建一条 Firewall **Traffic Rule**，允许从 **LAN** 区域到路由器自身目标端口 80/443 (LuCI) 的输入。  
     Network → Firewall → Traffic Rules → Add  
     - Name: Allow LuCI from LAN to WAN IP  
     - Protocol: TCP  
     - Source zone: lan  
     - Destination zone: Device (input)  
     - Destination port: 80, 443  
     - Action: ACCEPT  
   - 但仅靠这一点通常**仍然会失败**，原因就是上述的路由响应路径问题。

   要修复路由/响应路径（高级方法）：  
   - 为源自 LAN 且目的地为 WAN IP 的流量添加 SNAT/Masquerade 规则。  
     （或者使用 Policy Routing + Marks —— 对此目的而言过于复杂）

3. **将 OpenWrt 更改为 "Dumb AP" 模式**（如果你不需要独立的子网 / NAT）  
   - 连接主路由器 LAN → OpenWrt **LAN** 端口（而非 WAN）  
   - 禁用 OpenWrt 上的 DHCP  
   - 将 OpenWrt LAN IP 设置为与主路由器同一网段的静态 IP（例如 192.168.1.2）  
   - 将 WAN 接口分配给 LAN Firewall 区域或将其移除  
   → 这样 OpenWrt 只有一个 IP（LAN IP），你可以正常访问它。

4. **快速 Firewall 测试（仅当上游网络可信时！）**  
   暂时将 WAN 区域的 **Input** 策略设置为 **ACCEPT** (Network → Firewall → Zones → wan → edit → Input: ACCEPT)。  
   如果突然可以访问了 → 说明 Firewall 之前在拦截。  
   **警告：** 仅当 "WAN" 实际上是你信任的家庭 LAN（而非真实的互联网）时才这样做。测试后请务必恢复。

**底线**  
在几乎所有情况下，你应该直接使用连接到 OpenWrt 路由器的设备访问其 LAN IP。尝试从内部 LAN 客户端访问自身的 WAN IP 很难在没有额外配置的情况下干净利落地工作，而且通常是没有必要的。

**References:**  

- https://forum.openwrt.org/t/solved-routed-ap-from-wan-instead-of-lan/228578
- https://openwrt.org/docs/guide-user/network/openwrt_as_routerdevice
- https://forum.openwrt.org/t/22-03-2-nat-reflection-hairpinning/146458
- https://www.reddit.com/r/openwrt/comments/1gmsr17/how_to_access_my_openwrt_router_from_wan_when_im