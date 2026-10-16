---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 近视逆转 v1.0.0 已安装
translated: true
type: note
---

✅ **已安装到您的 iPhone 13 (lzwjava13)。**

**Myopia Reversal** v1.0.0 (`com.lzwjava.myopiaApp`) 现已安装到设备上 — 已通过 devicectl 验证：

```
Name              Bundle Identifier       Version
Myopia Reversal   com.lzwjava.myopiaApp   1.0.0
```

## 过程中发生了什么

1. **最初设备选错** — 您的 Mac 配对了两个 iPhone：`lzwjava` (iPhone 14 Pro Max) 和 `lzwjava13` (iPhone 13, `D20B05C1-…`)。我现在已定位到正确的设备 (`00008110-001159DC0CD3801E`)。
2. **签名/描述文件** — iOS 26 要求每个应用都有对应的 provisioning profile。您的旧描述文件仅覆盖了 `com.quzhibo.LiveIos`，因此构建失败，提示 *"No profiles for com.lzwjava.myopiaApp"*。注册新描述文件（team `976YQN9M2D`，对应我们的 bundle id，覆盖两个设备）后，应用成功构建并签名。
3. 通过无线部署使用 `flutter install -d 00008110-001159DC0CD3801E` 完成安装。

## 备注

- 应用图标应出现在主屏幕上 — 打开 **Myopia Reversal**。首次使用“扫描验光单”时会弹出相机/相册权限提示。
- 扫描、图表和完整指南均为 **Premium（高级版）**。Unlock 按钮需要在 App Store Connect 和 Google Play Console 中配置商店产品 (`com.lzwjava.myopia.premium`)，之后才能完成真实购买。
- 您的 iPhone 14 Pro Max 现在也已配置好描述文件，所以如果您需要，同样的 `flutter install` 命令也可以在那里使用。

需要我也在 iPhone 14 Pro Max 上安装它，或者添加一个隐藏的测试开关，让您无需商店即可预览 Premium 功能吗？
