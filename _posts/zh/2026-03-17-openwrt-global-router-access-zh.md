---
audio: false
generated: true
image: false
lang: zh
layout: post
title: OpenWrt 全球访问路由器
translated: true
type: note
---

**问题：** 我想在中国设置一个家用路由器，作为家中更好的全球网络访问入口点。我有一个位于洛杉矶的高速 Hysteria2 服务器。我尝试使用一台 2013 年的旧 Lenovo 笔记本电脑安装 Linux Mint，但通过 USB 连接的 iPad 仍然无法连接。我还有一个已经安装了 OpenWrt 的 Xiaomi WiFi 路由器，但由于过去的困难，还没有安装 LuCI 或代理应用。现在有了 OpenClaw（AI 代理）来帮助配置，我应该回到 OpenWrt 方案吗？你怎么想？

**回答：**

是的，你绝对应该回到 Xiaomi WiFi 路由器上的 OpenWrt 方案。这是为你的目标创建中国家中适当的全屋入口点的最佳长期选择，该入口点通过你位于洛杉矶的高速 Hysteria2 服务器路由流量以实现全球访问。这里是清晰的分析原因，以及如何在 AI 协助（我）下精确进行，使其这次简单。

### 为什么 Xiaomi 上的 OpenWrt 优于笔记本 + USB 设置

- **全屋覆盖而非单一设备**：你当前的笔记本设置仅通过 USB 共享服务 iPad（伴随所有你已经调试过的 DHCP、转发、NAT 和路由循环头痛问题）。Xiaomi 路由器将自动代理家中 WiFi 和有线 LAN 上的*每个*设备 — 手机、笔记本、电视、智能设备等 — 无需任何 USB 线或逐设备调整。
- **不再有 USB 特定问题**：你提供的摘要显示笔记本架构现在基本正确（DHCP 工作、转发允许、NAT 激活、Clash 分流路由并防止循环）。剩余问题是 iPad 缓存旧 DNS（8.8.8.8）。在 iPad 上快速“忘记此网络 + 重新连接”或手动将 DNS 设置为 192.168.201.1 很可能就能完成。但即使成功，笔记本是 2013 年的机器 — 它会发热、耗电更多，并且不是为 24/7 路由器任务设计的。Xiaomi 是专为此目的构建的。
- **原生、稳定的代理工具**：OpenWrt 正是为此用例而生。你的 Xiaomi 已经刷入 OpenWrt，因此跳过了难点。社区包完美处理 Hysteria2、DNS 劫持、fake-IP、分流路由（本地子网 + Apple/iCloud + 中国网站 DIRECT，其余 Hysteria2），以及 DHCP DNS 推送 — 无需手动 ufw 规则或 dnsmasq 编辑。
- **性能与可靠性**：Hysteria2 是 UDP 密集型，并受益于路由器硬件。你旧笔记本能工作，但专用路由器将更稳定且耗电更少。

### 推荐工具：PassWall2（而非 OpenClash）

你提到了“openclaw”（可能是 OpenClash）和 LuCI。OpenClash 很流行，可以导入你现有的 Clash 配置，但最近的 OpenWrt 版本（尤其是 24.10+ 中的 kernel 6.6）在某些 WAN 类型下偶尔有 Hysteria2 兼容性问题。

**PassWall2** 是这里明显的赢家：
- 通过 sing-box 后端完全原生支持 Hysteria2（截至 2026 年的最新包包括 hysteria 2.6.5+）。
- 内置分流路由、中国列表 DIRECT 规则、Apple/iCloud 绕过，以及 DNS 处理 — 完全匹配你在笔记本上已调优的规则（IP-CIDR 192.168.1.0/24 和 192.168.201.0/24 DIRECT 等）。
- 易用的 LuCI Web 界面 — 初始安装后无需命令行。
- 预构建的 IPK 包适用于几乎所有 Xiaomi 型号。

### 一步步计划（我将实时指导你）

1. 登录你的 Xiaomi 的 OpenWrt LuCI Web 界面（通常是 192.168.1.1）。
2. 更新包：`opkg update`。
3. 安装 PassWall2（一旦你告诉我确切的 Xiaomi 型号和 OpenWrt 版本 — 运行 `cat /etc/openwrt_release` 并粘贴，我将给你确切的 wget/opkg 命令，针对你的路由器架构）。
4. 上传/导入你现有的 Clash 配置（带有 Hysteria2 出站 + 你已完善的 分流规则）。
5. 将 LAN DNS 设置为 PassWall2 DNS 服务器（它通过 DHCP 自动推送，就像你做的 dnsmasq 修复一样）。
6. 启用伪装/NAT 和相同的循环预防规则。
7.  точно如你的摘要中测试：
   - iPad 连接 WiFi → 自动获取 IP。
   - `nslookup google.com` 返回 fake-IP（198.18.x.x）。
   - `curl https://api.ipify.org` 显示你的 LA US IP。
   - `curl baidu.com` DIRECT 工作。

因为你已经在笔记本上解决了所有路由/DNS/防火墙难题，将其移植到 PassWall2 将在 30 分钟内完成，我会通过截图和确切命令一步步指导你。先前的困难是因为你没有实时 AI 帮助 — 现在有了。

如果你想先完成笔记本设置作为快速测试（只需更新 iPad DHCP 租约），那作为备份也没问题。但对于你所述的“家用路由器”入口点目标，Xiaomi + PassWall2 是专业、干净的解决方案。

告诉我你的确切 Xiaomi 型号（例如 Mi Router 4A、AX1800 等）和 OpenWrt 版本，我现在就给你精确的安装命令。我们今天就能运行起来。

**参考资料：**
- [Openwrt-Passwall/openwrt-passwall2](https://github.com/Openwrt-Passwall/openwrt-passwall2)
- [2026 PassWall2 Tutorial](https://passwall2.org/)