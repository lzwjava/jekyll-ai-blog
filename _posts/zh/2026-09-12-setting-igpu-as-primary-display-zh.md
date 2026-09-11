---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 将iGPU设置为主显示屏
translated: true
type: note
---

问题：在华南B75主板的AMI BIOS中，如何将**集成显卡（iGPU）**设置为主显示设备，而不是独立显卡？

答案：

在B75主板上，在BIOS中查找如下设置：

```text
Advanced
  → Chipset Configuration
      → Primary Display
      → Initiate Graphic Adapter
      → IGD / PEG / PCI
```

具体名称因华南BIOS版本而异。

典型值：

```text
IGD   = 集成显卡 / Intel iGPU
PEG   = PCI Express显卡 / 独立显卡
PCI   = 传统PCI显卡
```

因此你需要：

```text
Primary Display / Initiate Graphic Adapter = IGD
```

然后：

```text
F10 → Save & Exit → Yes
```

### 针对你的B75 + Xeon设置的重要提示

如果你使用的是**Xeon E3-12xx**，请先确认具体型号。许多Xeon E3 CPU**没有集成显卡**。

例如：

```text
E3-1230 / E3-1230 v2 → 无iGPU
E3-1260L / E3-1260L v2 → Intel HD Graphics
```

如果CPU没有iGPU，选择`IGD`将无法获得视频输出。

另外，选择IGD后，请将显示器连接到**主板上的视频输出接口**，而不是独立显卡：

```text
CPU iGPU
   ↓
B75主板 HDMI / DVI / VGA
   ↓
显示器
```

如果你给我一张你的**具体华南B75 BIOS屏幕**的照片，我可以准确告诉你需要更改哪个菜单/选项。