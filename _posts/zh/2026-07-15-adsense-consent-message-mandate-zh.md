---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AdSense 同意消息强制要求
translated: true
type: note
---

这是一则关于 **Google AdSense** 功能的通知，与 Anthropic 无关。由于 AdSense 政策不断变化，我来核实一下当前的具体细节。

**问：** AdSense 中“为您的网站创建同意消息”的提示是什么意思？

**答：** 这是一项 GDPR/TCF 合规要求，并非可选的界面装饰。自 2024 年 1 月 16 日起，Google 强制要求所有面向欧洲经济区、英国或瑞士的 AdSense/Ad Manager/AdMob 流量，必须使用与 IAB Europe 的 TCF 集成的经过认证的 CMP（同意管理平台）。瑞士的相同要求于 2024 年 7 月 31 日生效。不合规将导致这些地区的广告投放立即暂停——这正是该提示所警告的“潜在广告收入损失”。

从机制上讲：CMP 会检测用户的位置，在广告/分析标签加载前显示同意横幅，记录用户的选择，并生成一个以标准化格式编码同意偏好的 TC 字符串。Google 的广告投放管道会检查来自经过认证的 CMP 的有效 TC 字符串，然后才会向该流量投放个性化广告——没有有效字符串，就没有个性化广告，有时甚至根本没有广告。

根据 Google 自己的文档，您的选择包括：使用 Google CMP、第三方 CMP，或创建自己的同意对话框。如果您自己构建，它必须独立通过 Google 的 TCF 认证——您旧的 Cookie 横幅无法满足要求，因为它缺少 IAB TCF v2.2 集成和 Google Consent Mode v2 支持。

对于您控制的网站，实际操作路径是：最快的办法就是直接在 AdSense 的“隐私与消息” → “创建消息”中启用内置的 Google CMP。它是免费的，已预先认证，无需集成额外的 JS 库。第三方（如 Secure Privacy、CookieYes、Cookiebot 等）仅在您需要对 AdSense 以外的多个广告网络进行更精细的供应商管理时才有意义。

一个需要注意的点：Google 可以在“标准”阻塞式消息和“有限”非阻塞式消息之间自动优化，具体取决于哪种方式能为您的流量带来更多收入——值得检查一下这个设置，而不是认为每个欧盟访客都必须面对一个全页面的同意墙。

**参考资料：**

- [同意管理要求（发布商）](https://support.google.com/adsense/answer/13554116?hl=en)
- [设置和管理您的 CMP - AdSense](https://support.google.com/adsense/answer/7670013?hl=en-GB)
- [Google CMP 的工作原理](https://support.google.com/adsense/answer/16918505?hl=en)
- [关于同意优化](https://support.google.com/adsense/answer/16878447?hl=en)
