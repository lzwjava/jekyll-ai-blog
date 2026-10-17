---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 信任开发者证书以运行应用
translated: true
type: note
---

**App 已成功安装在 `lzwjava13` 上**（iPhone 13，bundle `com.quzhibo.LiveIos`），但 iOS 阻止了启动——开发者证书尚未被信任。

**解决方法，在 iPhone 上操作：**
1. 打开 **设置 → 通用 → VPN 与设备管理**（在较新的 iOS 上：*描述文件与设备管理*）
2. 点击你的开发者描述文件（Apple Development / lzwjava）
3. 点击 **信任** 并确认

然后运行 App——或者你也可以在完成上述操作后，让我再尝试启动一次。