---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 代理网关：笔记本电脑还是路由器选择
translated: true
type: note
---

## 诚实评估：两者都能工作，但有非常不同的权衡取舍

---

## 选项 A：配备 Linux Mint 的 Lenovo 笔记本电脑（你已经尝试过的）

### ✅ 优势
- **x86 full-power CPU** — natively runs Clash/Mihomo with Hysteria2，无架构问题
- **更多 RAM 和存储** — 无软件包大小限制
- **更容易调试** — 完整的 Linux 工具集（`tcpdump`、`nftables`、`journalctl` 等）
- **你已经完成 95%** — 你粘贴的摘要显示架构完全正确。只剩下一步：iPad 续订 DHCP 租约以获取新的 DNS（`192.168.201.1`）

### ❌ 劣势
- 2013 年的 Lenovo 笔记本电脑 **功耗很高** 24/7 运行（~30–60W vs 路由器的 5–10W）
- iPad 的 USB 共享是权宜之计，不是干净的网络拓扑
- 不是“设置即忘”的设备 — 笔记本电脑可能休眠、合盖问题等

### 对你一夜尝试的评估
你很可能 **没有失败** — 只差一步。iPad 只需要续订 DHCP 租约。整个架构（DHCP → dnsmasq → Clash DNS → fake-IP → TUN → Hysteria2）构建正确。

---

## 选项 B：Xiaomi 路由器配备 OpenWrt

### ✅ 优势
- 干净、永久的路由器角色 — 始终开启，低功耗
- 家中所有设备通过 Wi-Fi/LAN 自然连接，无需 USB 共享
- OpenWrt 通过 `openwrt-passwall` LuCI 应用支持 Hysteria2，一旦知道路径，安装就很直接
- 还有一个名为 OpenWrt-nikki（Mihomo/Clash Meta）的项目，专为 OpenWrt 的透明代理设计，更现代且积极维护

### ❌ 劣势
- **MIPS/ARM 路由器 RAM 有限**（通常 128–256MB）— Clash Meta 带大量规则可能超出限制
- OpenWrt 软件包生态受限 — 出错时更难调试
- 你之前的经验显示配置困难 — 不过借助 AI 协助现在更可行
- 某些 Xiaomi 型号需要特定的刷机程序

### 关于你的特定 Xiaomi 路由器
答案取决于 **具体型号**。基于 MediaTek 平台的路由器最适合 OpenWrt，因为 MediaTek 向社区提供其 Wi-Fi 模块的开源驱动。如果你的 Xiaomi 使用 MediaTek 芯片组（如 MT7621、MT7622、MT7981），支持很稳固。

---

## 我的推荐：混合方法

针对你的情况，**最佳架构** 实际上是结合两者：

```
[ISP Modem] → [Xiaomi OpenWrt router] → (LAN)
                      ↓
           [Lenovo Laptop as "soft router" / proxy gateway]
                      ↓
         All devices route through Clash + Hysteria2
```

具体来说：
1. **保留 Xiaomi 作为主 Wi-Fi 路由器**（它为整个家庭处理 DHCP）
2. **在 Lenovo 笔记本电脑上运行 Clash + Hysteria2**，作为 LAN 上的透明代理网关
3. **在 Xiaomi 的 DHCP 设置中**，将 Lenovo 的 IP 推送到所有客户端作为默认网关和 DNS（option 3 和 option 6）

这样：
- iPad、手机、PC 都会自动代理 — 无需 USB 共享
- Lenovo 处理 Clash 规则匹配的重任
- Xiaomi 干净地处理 Wi-Fi 和路由
- 这是一个经过验证的模式：在始终开启的 Linux 设备上运行 Clash，然后配置 OpenWrt 路由器将该设备的 IP 作为 DHCP 默认网关和 DNS 推送到所有 LAN 客户端，因此设备无需手动更改任何设置

---

## 如果必须只选一个

## 如果必须只选一个

| 因素 | 笔记本电脑 (Linux Mint) | Xiaomi (OpenWrt) |
|---|---|---|
| Hysteria2 支持 | 原生，简单 | 通过 passwall/nikki |
| 设置难度 | 中等（你几乎成功了） | 中等-高 |
| 全家覆盖 | 仅 USB 共享设备 | 所有 Wi-Fi + LAN 设备 |
| 可靠性 | 需要盖子/休眠配置 | 优秀 |
| 功耗成本 | 高 | 低 |
| 调试便利性 | 高 | 低 |

**选择笔记本电脑**，如果你只需通过 USB 服务 iPad 并想快速完成 — 你已经很接近了。

**选择 OpenWrt**，如果你想干净覆盖家中所有设备，并愿意花时间初始设置。

---

## 立即下一步：修复当前的 iPad 问题

如果你想今晚完成笔记本电脑设置，只需在 iPad 上运行这个（或强制 DHCP 续订）：

```bash
# On the iPad: Settings → Wi-Fi → forget network → reconnect
# OR on the laptop:
sudo systemctl restart dnsmasq
# Then on iPad Settings → General → Transfer or Reset iPad → Reset → Reset Network Settings
```

然后测试：
```bash
nslookup google.com 192.168.201.1   # should return 198.18.x.x (fake-IP)
curl https://api.ipify.org           # should show your LA server IP
```

你距离成功只差一次 DHCP 续订。

参考资料：

- [Hysteria2 Installation — OpenWrt LuCI app (openwrt-passwall)](https://v1.hysteria.network/docs/installation/)
- [OpenWrt-nikki: Transparent Proxy with Mihomo on OpenWrt](https://github.com/nikkinikki-org/OpenWrt-nikki)
- [Clash Transparent Proxy on Linux Gateway — Chinese Blog](https://hellodk.cn/post/844)
- [Clash Transparent Proxy on Linux Router — DEV Community](https://dev.to/jysperm/setup-clash-redir-proxy-on-a-linux-router-4jnh)