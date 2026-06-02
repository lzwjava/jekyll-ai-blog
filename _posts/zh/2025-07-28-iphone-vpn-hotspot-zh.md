---
audio: false
generated: true
image: false
lang: zh
layout: post
title: iPhone开启VPN热点共享故障排查
translated: true
type: note
---

是的，通常情况下，你可以在 iPhone 14 Pro Max 上开启 5G 蜂窝数据并使用 Shadowrocket 等 VPN 应用的同时，为 Mac 笔记本电脑共享个人热点。这种设置通常不存在冲突，因为 iOS 系统设计上可以同时处理这两项功能而不会相互禁用。

关于你的具体问题：连接到 iPhone 个人热点的设备（如你的 Mac 笔记本电脑）产生的流量不会经过 iPhone 上配置的 VPN。相反，热点会直接共享原始蜂窝网络连接，绕过 VPN 隧道。这意味着：

- 你 iPhone 自身的应用和流量会使用 VPN（如 Shadowrocket 的代理或隧道）
- 但 Mac 笔记本电脑的网络流量将直接通过蜂窝网络传输，不会应用 VPN 的加密或路由

如果你希望 Mac 的流量也使用 VPN，需要在 Mac 设备上单独配置 VPN 服务。

[VPN 是否会监控我的热点流量？- Accountable2You 技术支持](https://support.accountable2you.com/article/791-faq-does-the-vpn-monitor-my-hotspot-traffic)
[如果在笔记本电脑上连接手机热点且手机已开启 VPN，笔记本电脑是否能获得 VPN 安全保护？- Quora](https://www.quora.com/If-I-am-connected-to-my-phones-hotspot-on-my-laptop-and-VPN-is-activated-on-the-phone-does-the-laptop-also-get-VPN-security-protection)
[为什么从 iPhone 共享给笔记本电脑的 WiFi 连接（个人热点）不经过 VPN？- Apple Stack Exchange](https://apple.stackexchange.com/questions/400853/why-does-shared-wifi-connection-from-iphone-to-laptop-personal-hotspot-not-go)
