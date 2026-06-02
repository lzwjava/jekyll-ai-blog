---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 团队ID是公共标识符
translated: true
type: note
---

不，这不是安全问题。团队 ID 是一个公开标识符，而非机密信息。

具体情况如下：
- 它只是苹果分配给开发者账户的唯一字符串
- 任何下载你 .app 文件的人都能看到它：`codesign -dvv YourApp.app`
- 你发布到 App Store 的每个应用中都包含它
- 它类似于用户名，而非密码

它无法做到的事情：
- 无法签署应用（需要钥匙串中的私钥）
- 无法访问你的苹果开发者账户
- 无法配置设备
- 无法窃取你的身份

真正的机密信息是你存储在 Mac 钥匙串中的私钥（即 `8802945277F81B11FB1744BBFE9F2E961CC5C508` 背后的密钥）。它永远不会离开你的设备。

同理，像 `com.lzw.TabsKiller` 这样的包标识符也是公开的——它们是标识符，而非凭证。
