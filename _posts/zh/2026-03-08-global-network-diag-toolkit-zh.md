---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 全球网络诊断工具包
translated: true
type: note
---

问题：什么是 ping.pe，它做什么？

答案：

## ping.pe 概述

**ping.pe** 被描述为有史以来最好的 Ping + MTR 组合，加上 TCP port checker、带有 `dig` 的 DNS 诊断，以及实时 BGP looking glass——均可从多个全球位置访问。

它是一个**免费的、基于浏览器的网络诊断平台**，无需安装，被网络工程师、系统管理员和开发者广泛使用。

---

## 核心功能

### 1. Ping (Multi-location)
ping.pe 允许用户同时从超过 20 个全球节点执行 ping 测试。它使用颜色编码的结果矩阵提供网络性能的可视化表示，便于解释。这特别有助于确定服务器是否可从世界各地的不同区域访问。

### 2. MTR (My TraceRoute)
ping.pe 以其出色的 MTR 和图表以及内置截图功能而备受赞誉。MTR 将传统的 `ping` 和 `traceroute` 结合成一个诊断工具，实时显示网络路径上的每个跳跃，包括每个跳跃的延迟和丢包率。

### 3. TCP Port Check
ping.pe 允许您测试远程主机上的特定 TCP port 是否开放且可达。这对于排查防火墙、网络服务如 web servers、SSH、databases 等问题至关重要。

### 4. DNS Lookup with `dig`
`dig` (Domain Information Groper) 功能允许用户查询任何域名的 DNS 记录（A、AAAA、MX、TXT、CNAME 等），有助于诊断 DNS 传播问题或配置错误。

### 5. BGP Looking Glass (Real-time)
BGP Looking Glass (LG) 服务器充当 BGP-speaking routers 的用户友好前端。它向特定 Autonomous System (AS) 内的选定 BGP routers 发送只读命令，并在网页上显示输出。

BGP Looking Glass 提供的信息包括 AS path information、对等信息、prefix information、next-hop information 和 BGP community information。AS path information 显示 BGP routes 在穿越不同 autonomous systems 时的路径。

ping.pe 的 BGP Looking Glass 可在 `bgp-lg.ping.pe` 访问，允许用户检查互联网流量如何全球路由到任何 IP 或 prefix。

---

## 谁在使用 ping.pe？

- **网络管理员** 排查连接或路由问题
- **服务器/VPS 所有者** 检查其 IP 是否可从世界不同地区访问
- **开发者和 DevOps 工程师** 诊断延迟或 DNS 问题
- **游戏玩家和远程工作者** 验证稳定的低延迟连接

---

## 主要优势

| 功能 | 优势 |
|---|---|
| No installation needed | Works directly in browser |
| Multi-location testing | Identifies regional network issues |
| MTR + Ping combined | Deep hop-by-hop diagnosis |
| BGP Looking Glass | Advanced routing visibility |
| Free to use | No account required |
| Results retained 24 hours | Easy sharing and reference |

---

## 如何使用

只需访问 **https://ping.pe/** 并输入域名或 IP 地址。该工具将自动从多个全球节点运行 ping 和 MTR 测试，并在颜色编码的表格中显示结果。您还可以导航到子工具进行 TCP port checks、DNS lookups 和 BGP analysis。

参考：

- [ping.pe - Official Site](https://ping.pe/)
- [ping.pe BGP Looking Glass](https://bgp-lg.ping.pe/)
- [Ping.pe Overview - coolexplore.com](https://www.coolexplore.com/en/item/ping-ip)
- [What BGP Looking Glass servers are - noction.com](https://www.noction.com/blog/bgp-looking-glass-servers)
- [BGP Looking Glass explained - vpsie.com](https://vpsie.com/knowledge-base/bgp-looking-glass-comprehensive-list/)