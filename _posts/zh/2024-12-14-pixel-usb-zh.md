---
audio: false
generated: false
image: true
lang: zh
layout: post
title: Pixel USB、iOS开发者工具、滑动手势输入
translated: true
type: post
---

### 目录

1. [Pixel 的 USB 选项](#pixels-usb-options)
   - 将 Pixel 用作网络摄像头
   - 在设置中启用开发者模式
   - 激活 USB 调试以进行连接
   - 使用 ADB 命令验证连接

2. [iOS 开发者模式和 ideviceinstaller](#developer-mode-of-ios-and-ideviceinstaller)
   - 通过 Xcode 查看已安装的应用程序
   - 使用 Xcode 进行截图和日志
   - 使用 xcrun 命令列出应用程序
   - 安装和使用 ideviceinstaller 工具

3. [快速滑动输入](#quick-swipe-typing)
   - 通过在字母上滑动来输入单词
   - 偶然发现的功能
   - 快速触摸时会出现线条

## Pixel 的 USB 选项

<div style="text-align: center;">
    <img class="responsive" src="/assets/images/pixel/pixel.jpg" alt="Pixel" width="50%" />
</div>

Pixel 提供了多种 USB 选项，其中一个特别有趣的功能是它能够充当网络摄像头。在 macOS 上，QuickTime 可以将 Android 网络摄像头作为视频源访问，提供了一个简单而有效的解决方案。

设置步骤如下：

1. 在设置中导航到“关于手机”，然后点击“版本号”七次以启用开发者模式。
2. 打开“开发者选项”并启用“USB 调试”。
3. 通过 USB 将您的 Pixel 连接到电脑，并在终端中运行以下命令以验证连接：
   ```bash
   adb devices
   ```

---

## iOS 开发者模式和 ideviceinstaller

*2024.12.03*

## 开发者模式

我曾是 iOS 开发者一段时间。但我的职业重心已转向其他技术。然而，即使我现在不是专业的 iOS 开发者，应用 iOS 开发知识仍然非常有用。

最近，我想要分享我安装的应用程序。但如果我从主屏幕或设置中的应用程序列表截取所有应用程序的屏幕截图，那会很混乱。所以我需要找到一种方法来查看所有已安装的应用程序。

以下是使用 Xcode 查看所有已安装应用程序的步骤：

1. 通过 USB 将您的 iPhone 连接到 Mac
2. 打开 Xcode
3. 转到窗口 → 设备和模拟器（或者按下 Shift + Cmd + 2）
4. 从左侧边栏选择您的 iPhone
5. 在主面板中，向下滚动到“已安装的应用程序”部分

它还有其他有用的功能：

1. 截取屏幕截图
2. 打开最近的日志
3. 打开控制台

## xcrun

```bash
(base) lzwjava@192 Downloads % xcrun devicectl device info apps --device 00008120-xxxx --verbose
Using verbose logging.
2024-12-03 16:24:18.579+0800  Enabling developer disk image services.
2024-12-03 16:24:18.637+0800  Acquired usage assertion.
Apps installed:
  - 0 elements

Command Completed, took 0.120 seconds
```

## ideviceinstaller

```bash
brew install ideviceinstaller
ideviceinstaller -l
```

```bash
(base) lzwjava@192 Downloads % ideviceinstaller -l
CFBundleIdentifier, CFBundleVersion, CFBundleDisplayName
com.huawei.smarthome-ios, "14.1.1.325", "HUAWEI AI Life"
com.sf-express.waybillcn, "9.70.0.1", "顺丰速运"
com.roblox.robloxmobile, "2.652.762", "Roblox"
co.alphaexploration.clubhouse, "3273", "Clubhouse"
com.dbs.mbanking.cn, "11", "DBS digibank"
global.longbridge.ios, "59579", "Longbridge"
imgurmobile, "416", "Imgur"
com.creditkarma.mobile, "17316145", "Credit Karma"
...
```

---

## 快速滑动输入

*2024.12.01*

如果你想在 iOS 中输入“threads”，你只需快速滑动以覆盖字母“threads”的位置即可得到结果。让我们看看它是如何工作的。

<video width="50%" controls>
  <source src="/assets/images/input/in.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

我是偶然发现这个功能的。当我的手指快速触碰输入区域时，它会显示一条线。我不知道那是什么意思。经过一些实验后，我发现了上面的发现。
