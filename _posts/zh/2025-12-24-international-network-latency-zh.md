---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 国际网络延迟解析
translated: true
type: note
---

问题：在 traceroute 到 twitter.com 的过程中，跳数 8 和 9 之间存在较大的延迟差距，它们之间是什么？

回答：

从跳数 8（约 10-20 毫秒）到跳数 9（约 197-199 毫秒）的延迟大幅增加，是因为这是流量离开中国国内网络并进入国际路由的点。

- 跳数 1 到 9 位于中国电信骨干网（CHINANET，AS4134）上，使用 202.97.x.x 等 IP 范围，这些 IP 分配给中国电信用于其国家基础设施。
- 跳数 10 (81.173.23.18) 是国际网关或对等点，可能位于中国境外（通常在欧洲或某个中转枢纽），连接到全球网络。
- 随后的跳数（11-12）位于 Cloudflare 的网络上（使用 162.158.x.x 和 162.159.x.x 等任播 IP），该网络托管 twitter.com（现为 x.com）。

约 180 毫秒的跳跃代表了跨越国际链路（通常是中国到美国或其他地区（Twitter/X 服务器所在地）的海底光缆）所需的额外往返时间。对于源自中国大陆访问外国网站的流量来说，这是正常的，原因是地理距离和通过有限的国际网关路由。这些链路上的拥塞或优先级也会导致更高的延迟。

在跳数 8 和 9 之间没有特定的中间跳数可见，因为 traceroute 只显示响应 ICMP 的路由器；长距离链路本身不会增加额外的响应跳数。

参考文献：

- [https://ipinfo.io/AS4134](https://ipinfo.io/AS4134)
- [https://bgpview.io/prefix/202.97.32.0/24](https://bgpview.io/prefix/202.97.32.0/24)
- [https://en.wikipedia.org/wiki/Great_Firewall](https://en.wikipedia.org/wiki/Great_Firewall)