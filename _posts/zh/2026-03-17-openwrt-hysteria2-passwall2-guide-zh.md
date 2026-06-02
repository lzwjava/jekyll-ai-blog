---
audio: false
generated: true
image: false
lang: zh
layout: post
title: OpenWrt 通过 PassWall2 使用 Hysteria2 指南
translated: true
type: note
---

我将搜索有关 OpenWrt 对 Hysteria2 支持的信息。让我搜索更多关于 OpenWrt 包和 Hysteria2 库的具体信息。问题：OpenWrt 是否有支持 Hysteria2 的库？

答案：

是的，OpenWrt 确实有 Hysteria2 的库支持，主要通过 **PassWall2** 插件生态系统。以下是您需要了解的内容：

## 官方支持

OpenWrt 通过 LuCI 应用 openwrt-passwall 支持 Hysteria2，这是实现在 OpenWrt 路由器上实现 Hysteria2 的主要方式。

## PassWall2 包

PassWall2 包含 Hysteria 和 Hysteria2，用于高性能 UDP 传输。最新的 PassWall2 版本包括 Hysteria 包版本 2.7.1，使其在包仓库中轻松可用。

## 安装方法

您可以通过从 releases 页面下载 IPK 包，并通过 SCP、LuCI 上传或 wget 将其上传到路由器来安装 PassWall2。包格式取决于您的路由器的包管理器（opkg 或 apk）。

## 协议支持

Hysteria2 通过 PassWall2 中的 sing-box 实现获得特定支持，该实现处理 Hysteria2 协议支持。

## 编译说明

官方 OpenWrt 仓库中报告了一些编译问题，但 PassWall2 生态系统维护着跨各种路由器架构可靠工作的预构建二进制包。

## 总结

OpenWrt 的核心库中不原生包含 Hysteria2，但社区维护的 **PassWall2 插件** 提供了全面支持，通过预编译包，使大多数 OpenWrt 用户无需手动编译即可轻松使用 Hysteria2。

参考资料：

- [PassWall2 GitHub Repository](https://github.com/Openwrt-Passwall/openwrt-passwall2)
- [Hysteria Official Installation Page](https://v1.hysteria.network/docs/installation/)
- [OpenWrt PassWall Build - SourceForge](https://sourceforge.net/projects/openwrt-passwall-build/files/)
