---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GFW 屏蔽了你的原始 IP
translated: true
type: note
---

## 是的——几乎可以肯定是 GFW IP 封锁

您的症状是 **典型的 GFW（中国防火长城）IP 封锁**。以下是发生情况和原因的分解。

---

## 🔍 为什么这指向 GFW，而不是其他问题

<br/>

| 症状 | 含义 |
|---|---|
| Ping / traceroute → Operation timed out | ICMP 数据包在 **GFW 层面被丢弃** |
| Telnet → Unable to connect | TCP 连接被 GFW **重置或丢弃** |
| 域名正常 | DNS 不是问题——是 **IP 层** 被封锁 |
| 更换 IP 后 → 一切正常 | 新 IP 尚未被标记；确认是 **特定 IP 的封锁** |

由于您的域名解析正确，更换 IP 后一切正常，问题显然出在 **IP 地址层面**，而非服务器配置、Hysteria2 设置或 DNS。

---

## 🧱 GFW 如何封锁 Hysteria2

Hysteria2 基于 **QUIC（UDP 协议）**。GFW 已观察到会标记产生大量 UDP 流量超过一定时间窗口的 IP。标记并非立即发生——例如，15 小时前更换的 IP 可能仍未被标记，而固定 IP 会在特定时间框架内被标记。被标记的机器会经历 **UDP 数据包被丢弃**，针对从海外到国内 IP 的任何流量，无论端口或协议，而 TCP 和 ICMP 流量最终也可能受影响。

简而言之：GFW **检测到 Hysteria2/QUIC UDP 流量模式**，标记了该 IP，并开始丢弃其所有进出数据包。

---

## ⚠️ 重要警告：更换 IP 仅是临时修复

GFW 会在更换后最终继续封锁您的 IP 地址。更换 IP 不是推荐的长期解决方案。您的全新 IP 很可能在使用一段时间后再次被封锁。

---

## ✅ 长期缓解措施

**1. 启用端口跳跃（Hysteria2 内置功能）**  
Hysteria2 有一个名为“port hopping”的功能，可帮助避免 UDP 限速和封锁。配置它定期轮换端口，使流量模式更难被 GFW 指纹识别。

**2. 如果可用，使用 IPv6**  
IPv6 当前限制较少——“IPv6 上的墙更低”。您可以在 IPv6 上使用 Hysteria2 而无需端口跳跃，即使下载大文件也不会限速，不过取决于所用网络。

**3. 设置合理的带宽限制**  
使用 Hysteria2 时，确保设置合理的带宽限制——某些提供商将大量 UDP 流量视为攻击。高持续 UDP 流量是 GFW 标记 IP 的主要触发因素之一。

**4. 考虑替代协议**  
除了 Hysteria2，您可以尝试 Xray 搭配 VLESS+REALITY+XTLS-RPRX-VISION，这是一个强大的组合。支持此功能的客户端应用包括 V2rayNG（Android）、V2rayN（Windows）和 Shadowrocket（iOS）。

---

## 🛠️ 如何验证 GFW 封锁

您可以使用工具如 **[ping.pe](https://ping.pe)** 或 **[check.greatfire.org](https://check.greatfire.org)** 从中国境内测试您的原 IP，并确认它被 GFW 封锁，然后再请求更换。

参考资料：

- [GFW UDP Blocking and Hysteria2 Issue – GitHub](https://github.com/apernet/hysteria/issues/1157)
- [IO Zoom – China GFW Block Explanation](https://www.iozoom.com/client/knowledgebase/127/China-Great-Firewall-GFW-block.html)
- [WireGuard/Hysteria2 in China – LowEndSpirit Discussion](https://lowendspirit.com/discussion/8008/wireguard-vpn-in-china)
- [Hysteria2 Official Troubleshooting Docs](https://v2.hysteria.network/docs/advanced/Troubleshooting/)