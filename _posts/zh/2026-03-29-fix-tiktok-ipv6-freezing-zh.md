---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 通过禁用 IPv6 修复 TikTok 卡顿问题
translated: true
type: note
---

**Question:** TikTok (抖音) 在刷视频时经常卡顿。有人说在路由器上禁用 IPv6 DHCP（这样就不会分配 IPv6 地址）可以解决这个问题——这正确吗？该如何操作？

**Answer:**

## 为什么禁用 IPv6 DHCP 可以解决 TikTok/抖音卡顿问题

是的，这是一个**有效且常见的修复方案**。原因如下：

一些 ISP 和设备并不完全支持 IPv6，这会导致 Streaming 延迟或中断。禁用 IPv6 会强制设备改用 IPv4，而 IPv4 在大多数情况下更加稳定。

当你的路由器通过 DHCPv6 分配 IPv6 地址时，你的手机可能会尝试通过 IPv6 访问 TikTok 的 CDN 服务器。如果你的 ISP 的 IPv6 Routing 不稳定或配置错误，连接就会在播放中途断开，从而导致卡顿或停顿。关闭 IPv6 DHCP 意味着不分配 IPv6 地址，因此你的设备会完全回退（Fall back）到 IPv4。

---

## 如何在路由器上禁用 IPv6 DHCP

大多数路由器允许你通过其 Web Interface 禁用 IPv6。打开浏览器并输入路由器的 IP 地址来访问路由器设置，使用用户名和密码登录。找到 IPv6 设置——通常位于“Advanced”或“Network”设置下。然后选择禁用 IPv6 的选项并保存更改。

**常规步骤：**

1. 打开浏览器，进入路由器管理页面——通常是 `192.168.1.1` 或 `192.168.0.1`
2. 登录（默认凭据通常在路由器标签上）
3. 导航至 **Advanced** → **IPv6**（或 **WAN** → **IPv6**）
4. 将 IPv6 设置为 **Disabled**（或将 DHCPv6 设置为 **Off**）
5. 保存并重启路由器

> **Note:** 具体的菜单位置因路由器品牌（TP-Link, Xiaomi, ASUS, Huawei 等）而异。查找诸如“IPv6 Enable/Disable”、“DHCPv6 Server”或“IPv6 Address Assignment”之类的标签。

---

## 替代方案：仅在手机上禁用 IPv6（不改动路由器）

如果你不想影响网络中的其他设备，可以在设备级别禁用 IPv6：

- **Android:** 前往 **Settings → Wi-Fi → 长按你的网络 → Modify Network → Advanced → IP Settings → Static**（这可以防止 DHCPv6 分配，但具体支持程度取决于 Android 版本）
- **iPhone/iPad:** Apple 不允许直接在 iPhone 或 iPad 上禁用 IPv6，你只能在路由器端进行操作。

---

## 这样做安全吗？

安全。禁用 IPv6 不会导致你断网。你的连接将继续通过 IPv4 工作，这是目前最标准且兼容性通常更好的协议。

Microsoft 建议在设置中使用“Prefer IPv4 over IPv6”而不是完全禁用 IPv6，以避免某些系统组件出现潜在问题。然而，对于主要用于 Streaming 的家用路由器，完全禁用 IPv6 通常是安全的。

---

## 总结

| Action | Effect |
|---|---|
| 在路由器上禁用 IPv6 DHCP | 设备无法获取 IPv6 地址 → 强制使用 IPv4 → 修复卡顿 |
| 仅在设备上禁用 IPv6 | 效果相同，但仅针对该设备有效 |
| 保持 IPv6 开启 | 如果 ISP 的 IPv6 Routing 较差，存在 Streaming 不稳定的风险 |

**结论：** 是的，你的方法是正确的。在路由器上禁用 IPv6 DHCP 是最彻底的解决方案——它通过从源头阻止分配 IPv6 地址，修复了网络中所有设备的 TikTok 卡顿问题。

**References:**

- [Disable IPv6 to Fix Streaming Buffering Issues – OSN+](https://support.osnplus.com/hc/en-us/articles/9116545086618-Disable-IPv6-on-Your-TV-to-Fix-OSN-Buffering-Issues-Troubleshooting-Guide)
- [How to Disable IPv6 on Routers, iPhone & Android – RapidSeedbox](https://www.rapidseedbox.com/blog/disable-ipv6)
- [How to Enable/Disable IPv6 – NordVPN](https://nordvpn.com/blog/ipv6-enable-or-disable/)
