---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 不受欢迎的网络技术观点
translated: true
type: note
---

问题：关于网络技术、TCP/IP、DDNS 和当前全球网络基础设施，有哪些不受欢迎的观点？

答案：

网络领域中不受欢迎的观点通常会挑战现有协议和基础设施的现状，指出效率低下、设计过时或被过度吹捧的替代方案。根据技术社区、专家和工程师的讨论，以下是一些关于 TCP/IP、DDNS（动态 DNS）和更广泛的全球网络基础设施的显著观点。为了清晰起见，我将它们按主题分组。

### 关于 TCP/IP 及其核心设计
- **TCP/IP 从根本上不适合现代内容驱动的应用程序，应该被 NDN（命名数据网络）等技术取代。**
  传统的 TCP/IP 基于主机地址路由数据包，导致效率低下，例如冗余数据获取和易受中断影响（例如，当一个热门网站在全球范围内崩溃时）。相比之下，NDN 专注于命名内容，能够实现更好的缓存、安全性和弹性——非常适合数据可用性优先于主机连接的物联网/人工智能时代。这种观点认为，这个有 45 年历史的协议栈是一个阻碍创新的遗物。

- **TCP 连接对于分布式系统中的 RPC（远程过程调用）来说是一种糟糕的抽象。**
  TCP 的可靠性功能（例如，重传）并没有显著改善基于服务的应用程序；它们增加了开销，而无助于微服务或云环境中的容错。像 QUIC（来自 Google）这样的现代替代方案已经取代了 TCP，实现了更快、更可靠的应用层传输，这表明 TCP 作为默认协议的日子屈指可数。

- **整个 TCP/IP 协议栈不足以应对以价值传输而非信息传输为核心的 AI/机器人驱动的未来。**
  它最初是为了共享数据包而构建的，无法处理自主机器和代币化经济世界中所需的低延迟、安全的价值交换。在此基础上升级全球基础设施效率低下；我们需要一个专门构建的协议叠加层或替代方案来避免瓶颈。

### 关于 DDNS 和 DNS 基础设施
- **DDNS 引入了不必要的复杂性和安全风险，其弊大于利，不适用于动态环境。**
  虽然 DDNS 自动化了 DHCP 密集型设置（例如，在 AD 集成网络中）的 IP 更新，但它创建了单点故障——例如黑客利用的主从依赖关系进行网络钓鱼或重定向。在静态或基于保留的网络中，它通常被完全跳过，这证明它对大多数现代基础设施来说并非必不可少。最好依靠像 SLAAC 这样的 IPv6 替代方案。

- **DNS 的去中心化“魔力”被夸大了；它的最终一致性和缓存层使其成为隐私噩梦和可靠性难题。**
  数十亿个查询通过递归解析器和缓存（包括浏览器、操作系统、ISP 和 CDN 中那些无视 TTL 的隐秘缓存）进行路由，创建了一个脆弱、不透明的系统，容易受到劫持或过时数据的影响。将所有东西路由到一个提供商（如 Cloudflare）可以提高速度，但会牺牲隐私——这证明该生态系统对用户的失败如此严重，以至于中心化似乎是一种进步。

### 关于当前全球网络基础设施
- **IPv6 的过度设计导致其未能普及；一个更简单的地址扩展就可以解决稀缺问题，而不会造成混乱。**
  通过基于路由器的转换（如 32 位到 64 位 ASNs）将八位字节加倍可以实现无缝的 IPv4 扩展，减少 NAT 漏洞和双栈冗余。相反，IPv6 的根本性改变造成了兼容性障碍，尽管关于耗尽的讨论不绝于耳，但 IPv4 在未来十年仍将占据主导地位。

- **推播式网络（例如，未经请求的入站流量）已经过时且不安全；所有内容都应默认为拉取式模型。**
  随着威胁的增加，假设入站数据包是恶意的符合零信任原则。这会将基础设施转向请求驱动的设计，淘汰传统协议，并迫使我们重新思考 BGP 等全球路由，无论如何，BGP 都只是 IP 地址的“美化广告”。

- **中心化的云巨头（AWS、Azure）是昨日的技术；区块链支持的去中心化基础设施是不可避免的未来。**
  为容易崩溃、浪费资源的服务支付高额费用，就像在智能手机世界中仍然使用固定电话一样。以太网的统治地位表明简单、可扩展的标准会胜出，但全球基础设施需要分布式替代方案来处理 AI 规模的负载，而不会出现被贪婪驱动的膨胀。

这些观点引发了争论，因为它们质疑了像 TCP/IP 的普遍性或 DNS 的弹性等根深蒂固的观念，经常引用现实世界中的痛点，如 IPv6 的缓慢推广或 DNS 中断。它们之所以“不受欢迎”，是因为它们暗示了昂贵的全面改革，但支持者认为，在一个数据爆炸的时代，坚持现状可能会导致停滞。

参考文献：
- [TCP/IP 在一个完美的世界里是理想的吗？ (Reddit)](https://www.reddit.com/r/networking/comments/1atenol/is_tcpip_ideal_in_a_perfect_world/)
- [总是 DNS 的问题 (Reddit)](https://www.reddit.com/r/networking/comments/1c5gpnl/its_always_dns/)
- [TCP/IP 与 NDN (BCS)](https://www.bcs.org/articles-opinion-and-research/tcp-ip-versus-ndn/)
- [TCP/IP 的未来是什么 (Reddit)](https://www.reddit.com/r/Network/comments/eig5sw/whats_the_future_for_tcpip_a_start_for_discussion/)
- [动态 DNS 的优点和缺点 (RF Wireless World)](https://www.rfwireless-world.com/terminology/dynamic-dns-advantages-disadvantages)
- [弥合差距：从 TCP/IP 到 NDN (Medium)](https://medium.com/ndn-link-official/bridging-the-gap-from-tcp-ip-to-ndn-bdb4fe4ea91d)
- [使用 DNS 的优点和缺点 (TinyDNS)](https://tinydns.org/advantages-and-disadvantages/)
- [哪种 DNS 方法是“最佳实践”？ (Reddit)](https://www.reddit.com/r/sysadmin/comments/1oyvyny/which_dns_approach_is_considered_best_practice/)
- [DNS 是最大的最终一致性系统 (X Post)](https://x.com/arpit_bhayani/status/1963087598882324658)
- [IPv6 像 IPsec 一样过度设计了 (X Post)](https://x.com/sdxsdx_/status/1979818454497559037)
- [热门观点：TCP 连接不适合 RPC (X Post)](https://x.com/DominikTornow/status/1903461669852021118)
- [TCP/IP 不适用于 AI/机器人 (X Post)](https://x.com/LordRaspyIII/status/1996376104526131366)
- [推播式网络已过时 (X Post)](https://x.com/nic_carter/status/1929649750200275275)
- [将 DNS 发送给 Cloudflare 不好但有改进 (X Post)](https://x.com/hdevalence/status/1177020193807011840)
- [IPv6 没有更简单的替代方案 (X Post)](https://x.com/noIPv6/status/1563165943693332480)
