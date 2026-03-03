---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 通过屏幕图案扫描眼镜处方
translated: true
type: note
---

**问题：** Framery DEV iOS app 如何使用 laptop、card、eyeglasses、computer graphics 等测量眼镜的 prescription？

**答案：** 

提到的 app 是 iOS 上的 "The Framery"（App Store ID 1153638659），以前称为 GlassesOn（由 6over6 开发，现已更名为 1-800 Contacts/The Framery）。它与 "Framery" 办公室 pod 公司无关。"DEV" 可能指其开发起源或旧版/测试名称，但当前公开 app 是 "The Framery"。

该 app 通过使用 iPhone 相机上的 **computer vision** 和 **graphics techniques** 扫描您当前的眼镜对，来测量您的眼镜 **prescription**（Rx 值：sphere/power、cylinder/astigmatism、axis）。它 **不**直接使用 laptop（过程仅通过 app 移动端），但 prescription 提取特别要求将眼镜举到显示 app 生成的特定 patterns 或 graphics 的 **flat computer screen**（laptop 或 monitor，大小 12"–27"）前。

### prescription 测量工作原理 (Rx scan)：
- **要求**：
  - 您当前的眼镜对（要测量的镜片）。
  - 一张标准信用卡大小的带有 **magnetic strip** 的 card（例如，library card、club card；优先选择浅色以便可见；**不**一定是信用卡）。
  - 平面 computer screen（laptop、desktop monitor 等，12–27 英寸）。
  - 良好照明并遵循屏幕/语音指示。

- **过程**：
  1. 打开 app 并选择 prescription/Rx 扫描功能。
  2. app 在您的 computer screen 上显示 **calibrated computer graphics/patterns**（可能是 grids、dots、lines 或 interference patterns）。
  3. 将眼镜举到 screen 前，使镜片与显示的 patterns 对齐。
  4. 将 magnetic strip card 举到旁边或视野内（用于 scale/reference，其已知真实世界大小用于图像中的 pixel-to-mm 转换）。
  5. iPhone 相机捕捉透过镜片的视图，检测由 prescription 镜片与 screen graphics 交互引起的 distortions、refractions 或 moiré patterns。
  6. 使用 **computer vision algorithms**（图像处理、edge detection、pattern recognition 和 optical calculations），app 分析镜片如何弯曲或改变显示的 graphics，从而计算光学功率参数（sphere、cylinder、axis）。
  7. card 的已知大小提供绝对 scale 以实现准确测量（Rx 精度 ±0.25 diopters）。

此方法从 single-vision 镜片中提取关键 prescription 值（精度：Rx 0.25D 内，PD 2 mm 内）。它是 FDA-listed、CE-marked 等，但不能替代专业眼科检查——它仅读取现有镜片。

### 独立但相关的：PD 测量
- PD（pupillary distance）仅使用手机相机 + 相同的 magnetic card（举到眉毛上方用于 scale）。
- PD 无需 laptop/screen。
- 它捕捉您的脸部 + card 的照片/视频，使用 computer vision 检测瞳孔并通过 card 的已知尺寸进行 scale。

laptop/screen + graphics 专门用于 **prescription (Rx) 提取** 部分，通过显示的 test patterns 实现镜片功率分析。

**参考资料：**  

- [The Framery on the App Store](https://apps.apple.com/us/app/the-framery/id1153638659)
- [The Framery PD tool page (mentions card usage)](https://www.theframery.com/pupillary-distance)
- [App description mentioning screen for Rx scan](https://glasseson-ios.soft112.com/)