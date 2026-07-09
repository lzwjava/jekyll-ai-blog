---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 开源iOS视频编辑资源
translated: true
type: note
---

问题：你在寻找一款 iOS 视频编辑器（最好开源），其编辑流程与 InShot 相似：从视频中提取音频、添加/删除音轨、插入视频，并且时间线上“添加”按钮位于左侧。同时，你也希望找到可以学习研究的开源编辑软件。

回答：

你描述的 UI 是标准的移动端非线性编辑器工作流程：

```
时间线

+ 添加视频   + 音频
----------------------------
视频轨道
音频轨道
文字轨道
贴纸轨道
```

InShot、CapCut 和 VN Video Editor 大致都遵循这种设计。

### 开源 iOS 视频编辑器

遗憾的是，App Store 上**非常缺乏成熟的开源 iOS 视频编辑器**。大多数商业应用（InShot、CapCut、VN、LumaFusion）都是闭源的。

值得学习研究的最佳开源项目有：

| 项目              | iOS | 时间线 | 音频编辑 | 备注                               |
| ---------------- | --- | ------ | -------- | --------------------------------- |
| Kdenlive         | 否  | ✅      | ✅        | 优秀的架构 (Qt/C++)                |
| OpenShot Studios | 否  | ✅      | ✅        | Python/C++，易于理解                |
| Olive Team       | 否  | ✅      | ✅        | 现代化时间线实现                    |
| Shotcut          | 否  | ✅      | ✅        | 使用 MLT 框架                      |

这些不是 iOS 应用，但它们包含扎实的时间线和编辑逻辑，可以进行移植。

---

### 开源 iOS 框架

如果你正在构建自己的编辑器，这些比寻找一个完整的应用更有用。

#### 1. GPUImage 2

由 Brad Larson 创建。

功能：

* 滤镜
* 相机
* 视频处理
* Metal/OpenGL

非常适合做特效。

---

#### 2. NextLevel

一个 Swift 框架，用于：

* 录制
* 裁剪
* 导出
* AVFoundation 封装

代码库非常整洁。

---

#### 3. VideoLab

Swift 时间线编辑。

支持：

* 多个剪辑
* 叠加层
* 音频
* 转场
* 导出

可能是最接近编辑器的开源库之一。

---

#### 4. PryntTrimmerView

非常流行的裁剪 UI。

提供了熟悉的界面：

```
|------视频------|
^                 ^
左侧手柄      右侧手柄
```

---

#### 5. BBMetalImage

GPUImage 的现代 Metal 替代方案。

---

### 值得研究的商业应用

尽管这些是闭源的，但它们的用户体验非常出色。

* InShot

  * 提取音频
  * 画外音
  * 音乐
  * 贴纸
  * 非常简洁的时间线

* CapCut

  * 多轨道
  * 关键帧
  * 音频提取
  * AI 功能

* VN Video Editor

  * 最接近桌面编辑器
  * 免费
  * 多轨道

* LumaTouch 的 LumaFusion

  * 可以说是最好的专业 iOS 编辑器
  * 优秀的时间线架构

---

### 如果你打算自己实现

Apple 已经通过 **AVFoundation** 提供了几乎所有功能。

典型的架构：

```
项目
├── 视频轨道
│     剪辑1
│     剪辑2
│
├── 音频轨道
│     提取的音频
│     music.mp3
│
├── 文字轨道
│
└── 贴纸轨道
```

操作变为：

```
插入剪辑

提取音频

删除音频

移动剪辑

分割剪辑

裁剪剪辑

导出
```

导出通常使用以下方式完成：

```
AVMutableComposition

AVMutableVideoComposition

AVAssetExportSession
```

许多商业编辑器内部也是以此方式构建的。

### 如果你的目标是构建一个类似 InShot 的编辑器

我建议按以下顺序进行研究学习：

1. **VideoLab**（Swift 时间线合成）
2. **NextLevel**（录制和捕获）
3. **PryntTrimmerView**（裁剪 UI）
4. Apple 的 AVFoundation 示例代码
5. Kdenlive/OpenShot（用于更大规模的时间线架构）

这种组合能让你更接近一个可投入生产的 iOS 编辑器，而不是寻找一个完全开源的 InShot 克隆版，因为目前还没有一个成熟的开源 iOS 应用能够匹敌 InShot 的功能集。

参考链接：

* [https://github.com/ruanjx/VideoLab](https://github.com/ruanjx/VideoLab)
* [https://github.com/NextLevel/NextLevel](https://github.com/NextLevel/NextLevel)
* [https://github.com/HHK1/PryntTrimmerView](https://github.com/HHK1/PryntTrimmerView)
* [https://github.com/BradLarson/GPUImage2](https://github.com/BradLarson/GPUImage2)
* [https://github.com/MetalPetal/BBMetalImage](https://github.com/MetalPetal/BBMetalImage)
* [https://developer.apple.com/documentation/avfoundation](https://developer.apple.com/documentation/avfoundation)