---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: TripMode 安装方法详解
translated: true
type: note
---

问题：如果我不记得安装过TripMode.app，我的Mac上怎么会有它？

回答：

TripMode.app是一个合法的第三方macOS应用程序，**并非**由Apple预装在任何Mac上。它也不会与其他软件捆绑或在没有用户交互的情况下自动安装。所有安装方法都需要用户明确操作：

### 常见的安装方法

- **Mac App Store**：您（或有权访问您的Apple ID的人）直接从App Store下载并安装它。它提供7天免费试用，之后需要订阅或一次性购买。
- **Setapp订阅**：如果您有（或曾经有）Setapp账户（一个包含250多种Mac应用程序的订阅服务），您可以通过Setapp应用程序一键安装TripMode。许多用户会尝试Setapp的免费试用，安装多个应用程序（包括TripMode），然后忘记它们——尤其因为Setapp应用程序即使在订阅结束后也可以保留安装（尽管它们会停止完全运行）。
- **从官方网站直接下载**：您从tripmode.ch下载.pkg安装程序并手动运行它（旧版本使用此方法；当前版本重定向到App Store或Setapp）。
- **Homebrew（高级用户）**：通过命令行使用`brew install --cask tripmode`安装。

### 为什么您可能不记得安装过它

- 您在一段时间前尝试了免费试用（App Store/直接下载提供7天免费试用，或通过Setapp），然后忘记了。
- Setapp是“被遗忘”安装的常见来源：用户注册试用，浏览并安装多个应用程序，然后取消或忘记。
- 其他有权访问您的Mac的人（家人、IT管理员或共享设备）安装了它。
- 在设置过程中，macOS会提示权限（例如，网络过滤扩展），这可能会让过程感觉是自动的，但它仍然需要批准。

TripMode需要系统级的网络扩展，因此安装总是涉及可见的步骤和权限授予——您不可能完全意外地安装它。

如果您担心未经授权的安装，请检查：

- “系统设置”>“通用”>“登录项与扩展”>“网络扩展”中是否有TripMode。
- 应用程序文件夹中是否有其应用程序图标。
- App Store购买历史记录或Setapp账户中的记录。

要安全地移除它：退出TripMode，将应用程序拖到废纸篓（这也会正确移除其扩展），然后清空废纸篓。

参考资料：

- [TripMode官方网站](https://tripmode.ch/)
- [Mac App Store上的TripMode](https://apps.apple.com/us/app/tripmode/id1513400665?mt=12)
- [Setapp上的TripMode](https://setapp.com/apps/tripmode)
- [TripMode支持/常见问题](https://tripmode.ch/support/)
