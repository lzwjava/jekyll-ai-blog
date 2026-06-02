---
audio: false
generated: true
image: false
lang: zh
layout: post
title: iOS Shadowrocket代理共享
translated: true
type: note
---

**问题：** 在 iOS 版 Shadowrocket 中使用代理共享功能，能否方便地让电脑或另一台手机使用同一连接？

**回答：**

可以。在 iOS 上使用 Shadowrocket 的代理共享功能，可以允许其他设备（如电脑或另一台手机）使用同一代理连接，从而将其网络流量通过你 iPhone 的代理设置进行路由。具体原理及注意事项如下：

1. **功能说明：**
   * Shadowrocket 可以在 iPhone 上创建一个本地 HTTP/SOCKS 代理。
   * 处于同一 Wi-Fi 网络下的其他设备可以连接到 iPhone 的代理，从而像使用 iPhone 配置的代理一样访问互联网。

2. **基本设置：**
   * 在 Shadowrocket 设置中启用“代理共享”或“本地 HTTP 代理”。
   * 记下 iPhone 在 Wi-Fi 网络中的 IP 地址以及 Shadowrocket 使用的端口。
   * 在其他设备上，将网络设置中的代理配置为上述 IP 和端口。

3. **优点：**
   * 方便那些无法直接运行 Shadowrocket 的设备使用。
   * 集中管理：你可以通过 iPhone 控制哪些网站或流量通过代理路由。

4. **局限与考虑：**
   * 两台设备通常需要处于同一本地网络中，除非你额外设置端口转发以实现远程访问。
   * 性能取决于 iPhone 的网络速度；流量过大可能导致 iPhone 或连接设备变慢。
   * 安全性：如果与不可信设备共享需谨慎，因为所有流量都将经过你的 iPhone。

因此，该功能确实很方便，但更适合小规模使用或临时共享，而非高带宽或长期共享场景。

**参考来源：**

* [Shadowrocket 用户指南（iOS 代理共享概述）](https://shadowrocket.app/)
* [通过 iPhone 为多设备设置代理](https://medium.com/@proxyguide/using-iphone-as-proxy-server-2f0f1b2a1e1b)
