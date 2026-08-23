---
audio: false
generated: true
image: false
lang: zh
layout: post
title: VGA转HDMI需要主动式转换器
translated: true
type: note
---

是的，**VGA 转 HDMI 转接器确实存在**，但有一个重要细节：

* **VGA → HDMI** 并非简单的**无源转接头**。VGA 是模拟信号，HDMI 是数字信号，你需要一个内置芯片的**有源转换器**。

典型用法：

```
PC / 笔记本电脑 VGA 输出
        |
        | 模拟 VGA 线缆
        v
[VGA → HDMI 有源转换器]
        |
        | HDMI 线缆
        v
显示器 HDMI 输入
```

注意：

* 通常需要 **USB 供电**（5V），因为转换过程需要电子元件。
* 支持常见分辨率，例如：

  * 1920×1080 @ 60Hz
  * 1280×720
* 音频：

  * VGA 没有音频。
  * 部分转换器会通过 3.5mm 音频输入将音频注入 HDMI。

针对你之前提到的 **联想 LI2364A 显示器**：

* 如果显示器只有 **VGA 输入接口**，那么从现代 GPU/笔记本电脑出发，你需要的是 **HDMI → VGA**（反向转换）。
* 如果你的电脑只有 HDMI/DP 输出，而显示器只有 VGA 接口，则方案如下：

```
GPU HDMI/DP
    |
    v
HDMI → VGA 转换器
    |
    v
联想 VGA 接口
```

不要购买不带转换盒的 VGA 转 HDMI 线缆，通常无法正常工作。