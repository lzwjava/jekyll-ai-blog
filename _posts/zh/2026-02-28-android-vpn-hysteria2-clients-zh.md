---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Hysteria 2 的 Android VPN 客户端
translated: true
type: note
---

Question: 支持 Hysteria 2 的 Android 客户端 VPN 有哪些？

Answer: 

几个 Android 应用支持 **Hysteria 2**（一种基于 QUIC 的代理/VPN 协议）。Hysteria 2 本身的核心项目没有官方的全功能 Android APK（仅存在低级二进制文件），因此第三方客户端是主要选项。这些应用集成了 Hysteria 2 支持，通常以完整 VPN 模式（使用 Android 的 VPN 服务）或系统代理模式运行。

以下是最常用推荐和官方列出的支持 Hysteria 2 的 Android 客户端（截至 2026 年初，根据官方 Hysteria 文档和社区使用情况）：

- **Hiddify**（因易用性而经常被推荐）  
  一个流行的多协议 VPN/代理应用，具有良好的 Hysteria 2 支持。它允许轻松导入 `hy2://` 链接，并在完整 VPN 模式下工作。  
  下载：GitHub releases (https://github.com/hiddify/hiddify-app/releases) 或有时通过其他来源获取。

- **NekoBox for Android**  
  一个通用代理工具链应用，从版本 1.2.4 开始支持 Hysteria 2。广泛用于高级配置。  
  GitHub: https://github.com/MatsuriDayo/NekoBoxForAndroid

- **Sing-box / SFA (sing-box for Android)**  
  Android 的官方 sing-box 客户端（Play Store 上的 io.nekohasekai.sfa）。原生支持 Hysteria 2，并经常被提及用于干净的 Hysteria 2 设置。  
  Play Store：搜索 "sing-box" 或使用上述包名。

- **V2Box**  
  多协议代理客户端，从版本 2.6.1 开始支持 Hysteria 2。可直接在 Google Play Store 下载。  
  链接：https://play.google.com/store/apps/details?id=dev.hexasoftware.v2box

社区中其他提及包括 fork 或专用应用，如 GitHub 上的自定义 Hysteria 2 专用客户端（例如 lry127/Android-Hysteria-2-client），但这些不如上述应用完善且推荐度较低。

要获取最新和完整列表，请查看官方 Hysteria 2 文档中的第三方应用页面。

参考资料：  

- [https://v2.hysteria.network/docs/getting-started/3rd-party-apps](https://v2.hysteria.network/docs/getting-started/3rd-party-apps)
- [https://fornex.com/help/hysteria2-vpn-android](https://fornex.com/help/hysteria2-vpn-android)
- [https://github.com/MatsuriDayo/NekoBoxForAndroid](https://github.com/MatsuriDayo/NekoBoxForAndroid)
- [https://play.google.com/store/apps/details?id=dev.hexasoftware.v2box](https://play.google.com/store/apps/details?id=dev.hexasoftware.v2box)