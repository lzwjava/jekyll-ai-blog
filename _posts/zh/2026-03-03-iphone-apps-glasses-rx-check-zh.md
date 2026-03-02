---
audio: false
generated: true
image: false
lang: zh
layout: post
title: iPhone 应用测量眼镜处方度数
translated: true
type: note
---

**问题：我们能否使用 iPhone 相机来检测眼镜的处方强度（diopters），例如阅读眼镜（+1.5D）或普通眼镜？如果我们有多个眼镜但不知道它们的强度，有没有简单的方法来找出？我们能否设计一个 app，根据相机透过眼镜时的模糊程度来确定度数？**

**回答：**

是的，使用 iPhone 相机测量现有眼镜的处方强度（diopters）是可能的，而且已经有几个 app 做得相当有效，不需要从头构建一个新的。

最实用和准确的现有方法**不**主要依赖于分析透过镜片拍摄的普通照片中的“blur”。相反，它们使用 computer vision 技术来：

- 以特定方式拍摄镜片（通常使用信用卡等参考物体来提供比例）。
- 分析镜片的放大、扭曲、棱镜效应、反射或边缘图案。
- 估计 sphere power（近视/远视）、cylinder（散光）、axis，有时还有 add power。

流行 app 包括：

- **GlassesOn**（某些版本现在也称为 The Framery）——被广泛认为是最好的之一。它使用手机相机扫描您的眼镜，并给出处方参数，准确度良好（某些地区有 FDA/CE 认证）。许多用户报告结果与专业测量相差 0.25–0.50 D。
- **GlassesUSA Prescription Scanner**——免费工具，使用智能手机相机扫描眼镜并读取处方值。
- **Eyerim Lens Scan**——类似的功能，通过智能手机相机读取镜片。
- 专业工具如 **My Call Bag Lensometer**（更适合专业人士）——使用透过镜片查看的 Amsler grid；AI 分析扭曲图案来估计 sphere、cylinder 和 axis。

这些 app 对于单焦点镜片（包括基本的阅读眼镜如 +1.5 D）效果最佳，需要您遵循屏幕上的指示，例如将眼镜放在桌子上、使用良好照明，并包含已知大小的物体进行校准。

**关于纯基于 blur 的方法**（透过眼镜拍摄照片并测量模糊程度）：

- 理论上，是的——+1.5 D 阅读镜片会导致相机尝试透过它对焦远处物体时出现明显的 defocus/blur（因为镜片增加了会聚能力）。
- 您可以设计一个 app 来：
  - 在已知距离显示清晰目标（例如文本或网格）。
  - 捕获带和不带镜片的相机图像。
  - 测量 blur 指标（例如边缘锐度、Laplacian variance 或 FFT-based focus measures）。
  - 根据引入的 defocus 量使用光学公式（如 lensmaker's equation 或经验校准）估计屈光度。
- 然而，在实践中，这种方法准确性和可靠性较低，因为：
  - iPhone 相机具有非常强的 autofocus 和 stabilization。
  - 镜片的小偏移、倾斜、散光或划痕会产生复杂的 blur 图案。
  - 它难以处理低度数（±0.50 D）或散光。
  - 现有 app 使用更稳健的功能（magnification/distortion）而不是纯 blur 来获得更好精度。

**目前最简单的方法（无需编码）：**

1. 从 App Store 下载免费 app，如 GlassesOn / The Framery 或 GlassesUSA Prescription Scanner。
2. 遵循指示扫描每副眼镜（通常每副需 1–3 分钟）。
3. 比较您的 3–5 副眼镜的结果。

对于非常基本的阅读眼镜（+1.00 到 +3.50 D 范围），这些 app 通常给出可靠的 sphere power 估计。结果足够好，用于在线订购类似替换眼镜，尽管仍推荐专业 optometrist 检查以获得精确的视力护理。

如果您对研究/DIY 方面感兴趣，请查看关于“smartphone lensometer”或“autorefractor”的 computer vision 论文——但消费者 app 已很好地解决了这个问题。

**参考资料：**

- [GlassesOn app 官网](https://6over6.com/glasses-on)
- [GlassesUSA Prescription Scanner](https://www.healthline.com/health/how-to-find-out-what-prescription-your-glasses-are)
- [My Call Bag Lensometer 概念](https://www.youtube.com/watch?v=SX0oIHR-CHQ)
- [Eyerim Lens Scan](https://www.prnewswire.com/news-releases/eyerim-introduces-lens-scan-an-online-way-of-getting-a-prescription-301352414.html)