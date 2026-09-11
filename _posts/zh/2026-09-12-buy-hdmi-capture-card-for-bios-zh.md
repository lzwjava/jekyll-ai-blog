---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 购买HDMI采集卡用于BIOS
translated: true
type: note
---

问题：在京东上购买用于AI控制BIOS机器的HDMI采集卡时，应该搜索什么关键词？

答案：中文名称是**HDMI 视频采集卡**。针对你的使用场景，请搜索以下精确关键词：

```text
HDMI 视频采集卡 USB
HDMI 转 USB 采集卡
USB3.0 HDMI 视频采集卡
UVC HDMI 视频采集卡
HDMI 采集卡 1080P 60Hz
```

京东目前有很多商品明确标注为**“HDMI视频采集卡…转USB”**以及**UVC**采集设备。([京东][1])

### 我会买什么

对于你的BIOS/GPU维修项目，**不要为4K专业采集卡花钱**。你不需要4K。

寻找以下规格：

```text
HDMI IN
    ↓
USB 3.0
    ↓
UVC
    ↓
1080p60
```

理想情况下，商品描述会写：

> **USB 3.0 HDMI 视频采集卡，1080P 60Hz，UVC免驱**

关键词是**UVC**。这意味着Linux/macOS/Windows通常可以将其视为标准USB视频设备，而无需专用软件。

例如，京东上有绿联（UGREEN）的型号，提供HDMI输入→USB/Type-C采集，包括1080p60版本。([京东][2])

### 不要混淆这两者

**你需要的：**

```text
HDMI OUT ──► [ HDMI 视频采集卡 ] ──USB──► AI PC
```

**不是：**

```text
USB ──► HDMI OUT
```

后者是USB转HDMI显示适配器，方向相反。

### 对于你的第一个原型

我会在京东搜索：

```text
USB3.0 HDMI采集卡 1080P60 UVC 免驱
```

然后选择** ¥50–150左右的通用/UVC设备**，而不是昂贵的专业采集卡。

AI不在乎采集卡是¥50还是¥500。重要的是Linux能给你类似这样的设备：

```bash
/dev/video0
```

然后：

```bash
v4l2-ctl --list-devices
ffplay /dev/video0
```

你的代理就能获取到BIOS像素数据。

如果你愿意，**请发给我2–3个你找到的京东商品页面/截图**，我可以告诉你哪一个实际上适合BIOS采集，而不仅仅是营销上的“4K采集卡”。

参考资料：

* [京东UVC采集卡搜索](https://www.jd.com/hprm/670ea21d4c988274b9d.html?utm_source=chatgpt.com)
* [京东UVC采集卡品牌/型号](https://www.jd.com/brand/670ea21d4c988274b9d.html?utm_source=chatgpt.com)

[1]: https://www.jd.com/hprm/670ea21d4c988274b9d.html?utm_source=chatgpt.com "uvc采集卡 - 京东"
[2]: https://www.jd.com/hprm/670ea21d4c988274b9d.html?brand=%E7%BB%BF%E8%81%94%EF%BC%88UGREEN%EF%BC%89&electedExtAttrSet=&extAttrValue=expand_name%2C&sort_type=sort_default&utm_source=chatgpt.com "uvc采集卡 - 京东"