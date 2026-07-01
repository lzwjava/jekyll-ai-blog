---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 用于 iOS 调试的 Charles Proxy
translated: true
type: note
---

Question: Charles 是 iOS 开发中使用的网络应用，其全面介绍是什么？

Answer:

## What is Charles Proxy?

Charles 是一个代理服务器，它允许开发者查看 iOS 应用与互联网之间的网络流量。您可以将 iOS 模拟器或设备配置为通过 Charles Proxy 传递其网络请求和响应，从而在测试和调试期间检查甚至修改数据。

代理是一个充当客户端请求资源和提供该资源的服务器之间中介的应用。客户端不是直接连接到服务器，而是将请求定向到代理，代理执行请求、接收响应，然后将响应定向回客户端。

---

## Why Do iOS Developers Use Charles?

使用 Charles，您可以窥探应用发送和接收的网络请求和响应。这个工具可以节省大量调试时间。它特别有用，当：

- 调试 API 集成
- 再现难以复制的网络 bug
- 模拟缓慢或差的网络条件
- 为测试边缘情况模拟服务器响应

---

## Platform & Pricing

Charles 是一个基于 Java 的应用，支持 macOS、Windows 和 Linux。Charles Proxy 不是免费的，但提供 30 天免费试用。在试用模式下，您每 30 分钟需要重启 Charles Proxy。

App Store 上还有 Charles for iOS 应用，可用于直接从 iOS 设备监控网络流量。

---

## Core Concepts

### How It Works (Man-in-the-Middle)

Charles 位于 web 浏览器或应用与 API 之间。它使用自己的根证书（也称为证书颁发机构 CA），动态创建并签署发送到本地浏览器的证书，从而让您以纯文本查看网络流量。

### Traffic Views

一旦配置了 SSL proxying，Charles 会以两种视图显示所有网络流量。**Structure View** 按域以树状层次组织请求 — 您可以展开任何域查看单个端点和资源。**Sequence View** 按时间顺序显示请求并附带计时信息，帮助识别慢请求并理解请求顺序。

---

## Setup: iOS Simulator

监控应用进出的网络流量就像在 iOS Simulator 中测试应用时打开 Charles Proxy 一样简单。当您打开 Charles Proxy 时，代理会监控您运行的任何应用的网络流量。

Charles 启动后立即开始记录网络事件，因此您应该已经看到左侧窗格中弹出事件。

---

## Setup: Real iOS Device

您可以在实际 iOS 设备上测试应用，并从笔记本上的 Charles 直接查看其发出的网络调用和应用接收到的响应。iOS 设备和笔记本必须连接到同一无线网络。

然后，将 iOS 设备的 Wi-Fi 代理设置配置为指向 Mac 的 IP 地址和端口 **8888**（Charles 的默认端口）。

---

## SSL Proxying (Decrypting HTTPS)

通过 HTTPS 通信时，加密会阻止代理服务器和其他中间件窃听敏感数据。SSL/TLS 使用受信任证书颁发机构生成的证书加密网络流量。为了绕过此限制，Charles 使用自己的根证书。

对于 HTTPS 流量，Charles 使用 SSL 证书解密内容，您必须在 iOS 设备或模拟器上安装该证书。

在真实设备上：打开移动浏览器并访问 `chls.pro/ssl` 下载并安装证书。在 iOS 上，您还必须转到 **Settings > General > About > Certificate Trust Settings** 并为 Charles 证书启用完全信任。

---

## Key Features

### 1. Breakpoints

Breakpoints 工具允许您在请求和响应通过 Charles 之前拦截它们。您可以检查和编辑请求或响应，然后决定是否允许其继续或阻止它。

这对于以下情况很有用：

- 负面测试（例如，将有效参数更改为无效参数）
- 在响应中模拟不同的服务器状态
- 测试错误处理逻辑

### 2. Rewrite Tool

Charles 支持使用简单规则动态重写请求和响应。Rewrite 规则可以执行文本替换、修改标头、重定向到不同主机，或从本地文件提供静态响应。Rewrite 规则可以切换开启和关闭、导入和导出，并组织成不同调试场景的集合。

### 3. Map Local

Map Local 使用本地文件覆盖远程资源。每个远程资源的请求都可以提供您的本地开发版本。您可以测试针对生产数据的代码更改，而无需部署。

### 4. Map Remote

Map Remote 将请求重定向到不同端点，从而在不更改实际服务器的情况下启用多样化场景测试。

### 5. Throttling (Network Simulation)

Charles 可用于调整网络连接的带宽和延迟。这允许您在差的网络条件下测试应用。转到 **Proxy → Throttle Settings** 查看可用选项。您可以将 throttling 应用于所有请求或仅特定主机，从而避免其他网络请求变慢。

Throttle 预设包括 3G、4G、Fiber 和自定义配置文件。

### 6. Repeat & Compose

**Repeat** 和 **Compose** 功能允许您重放 API 调用并进行编辑，以测试不同场景。这有助于在不依赖特定应用流程的情况下复制 bug。

### 7. Session Saving & Sharing

会话导出可保存和共享捕获的会话，用于离线分析或协作。会话可以保存为 Charles 的原生 `.chls` 格式或标准 HAR 文件。

### 8. WebSocket Support

Charles 会捕获 WebSocket 消息以及标准 HTTP 流量。这对于调试实时功能非常有价值。

---

## Common Issues & Tips

| Issue | Solution |
| --- | --- |
| HTTPS 流量显示为加密 | 安装并信任 Charles SSL 证书 |
| 移动设备无法连接 | 确保两者在同一 Wi-Fi 上，并手动设置代理 |
| Charles 激活时应用崩溃 | 应用可能使用证书固定；需要代码级绕过 |
| Charles 捕获过多噪声 | 使用 **Proxy → Recording Settings** 只包含特定主机 |

记住，当您停止使用 Charles 时，请在设备设置中禁用 HTTP Proxy，否则应用中会出现令人困惑的网络失败。

---

## Summary

Charles 是每个 iOS 开发者调试工具包中的必备工具。它让您完全了解应用实际在网络上发送和接收的内容 — 仅从 Xcode 无法看到这一点。从检查 JSON 负载，到模拟 API 响应，再到模拟 3G 连接，Charles 大大加快了识别和修复网络相关问题的过程。

References:

- [Charles Proxy Tutorial for iOS – Kodeco](https://www.kodeco.com/21931256-charles-proxy-tutorial-for-ios)
- [Quick Guide on Charles Proxy for iOS Development – tanaschita.com](https://tanaschita.com/20220228-quick-guide-on-charles-proxy-for-ios/)
- [Charles for iOS – Official Documentation](https://www.charlesproxy.com/documentation/ios/)
- [Tutorial: Using Charles Proxy With Your iOS Development – CodeWithChris](https://codewithchris.com/tutorial-using-charles-proxy-with-your-ios-development-and-http-debugging/)
- [Advanced Charles Proxy Tutorial for iOS – Kodeco](https://www.kodeco.com/22070831-advanced-charles-proxy-tutorial-for-ios)
- [Setting Up Charles Proxy with iOS Devices and Emulators – Medium](https://medium.com/@mayurkadampro/setting-up-charles-proxy-with-ios-devices-and-emulators-bdc2124b6ad9)
- [What is Charles Proxy and How to Use it – BrowserStack](https://www.browserstack.com/guide/charles-proxy)
- [How to Use Charles Proxy in 2026 – Roundproxies](https://roundproxies.com/blog/how-to-use-charles-proxy/)
- [SSL Proxying – Official Charles Docs](https://www.charlesproxy.com/documentation/proxying/ssl-proxying/)
