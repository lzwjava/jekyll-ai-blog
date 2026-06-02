---
audio: false
generated: true
image: false
lang: zh
layout: post
title: macOS 实况文本 OCR 功能
translated: true
type: note
---

问题：在 macOS 预览中，你可以从图片中选择文本。这是使用了 OCR 技术吗？

回答：

是的，你所看到的确实基于 OCR（光学字符识别）技术，但苹果将其称为 **Live Text**。从 **macOS Monterey (12)** 开始，苹果集成了一个系统级功能，能够识别图片、截图甚至 iOS 设备相机视图中的文字。当你在预览（或照片、Safari 等）中打开一张图片时，macOS 会实时分析图像，检测其中的文字，并使其可选中、可复制。

关键点：

* 这是**原生 OCR**，完全内置于系统中，并非独立应用。
* 它适用于图片、截图，以及文本作为图像一部分而非嵌入文字的 PDF 文件。
* 苹果使用设备上的机器学习模型来实现这一功能，因此文字识别无需网络连接。
* 除了复制，你还可以对图片中检测到的文字进行**查询、翻译或拨打**电话号码。

简而言之，从用户角度看这几乎像魔法，但背后是依靠 **ML 模型驱动的设备端 OCR** 技术。

参考文献：

* [Apple：在 Mac 上使用 Live Text](https://support.apple.com/guide/mac-help/use-live-text-mchl3f2f7b0a/mac)
* [Apple 在 macOS Monterey 中引入 Live Text](https://www.apple.com/newsroom/2021/10/macos-monterey-introduces-powerful-new-features/)
