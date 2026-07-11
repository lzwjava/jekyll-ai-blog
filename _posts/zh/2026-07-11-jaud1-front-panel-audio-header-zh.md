---
audio: false
generated: true
image: false
lang: zh
layout: post
title: JAUD1前面板音频排针
translated: true
type: note
---

**问题：** MSI MAG B760M Mortar WiFi 主板上的 JAUD1 是什么意思？

**答案：**

`JAUD1` 是 MSI（以及大多数主板厂商）用于标识**前置面板音频接口**的标准标签——这是一个位于 PCB 上的 9 针（2x5，其中一个针脚移除作为防呆设计）排针。

命名规则解析：

- `J` = Jumper/连接器（主板上任意排针的通用前缀）
- `AUD` = Audio（音频）
- `1` = 实例编号（第一个；主板很少会有第二个）

**物理用途：** 这里是连接机箱前面板音频插孔（机箱顶部/前方的耳机输出+麦克风输入）线缆的位置。该线缆通常标记为 `HD AUDIO`（在非常老的机箱上可能是 `AC'97`——不要在现代主板上使用该模式）。

**引脚定义**（标准 Intel HD Audio 前置面板规格，MSI 遵循此规格）：

```
Pin 1: MIC2_L
Pin 2: GND（接地）
Pin 3: MIC2_R
Pin 4: -ACJ_DETECT（存在检测，许多主板上不连接）
Pin 5: LINE2_R
Pin 6: GND（感应）
Pin 7: FP_IO_R（保留/防呆——这是缺失的针脚位置）
Pin 8: KEY（无针脚，物理阻挡）
Pin 9: LINE2_L
Pin 10: GND（感应）
```

**装机实际操作步骤：**

1. 在主板的左下边缘找到 `JAUD1`（MSI 几乎总是将其放在此处，并有丝印标识）。
2. 找到机箱的前置面板音频线缆——接口上应标有 `HD Audio`。
3. 插入——接口为防呆设计（缺失第 8 针），因此只能以一个方向插入。
4. 在 BIOS 中，通常在 Advanced → Onboard Devices 下有一个设置，用于切换 HD Audio 与老式 AC97 模式——对于现代机箱线缆，保持默认的 HD Audio 即可。

如果机箱线缆是旧的且标有 `AC'97`，不要强行使用——它在默认的 HD Audio 设置下无法正常工作，而且现代主板通常也不再支持老式模式。

该主板上其他排针（如用于电源/复位/LED 的 `JFP1`、`JFP2`，用于 USB 接口的 `JUSB1-4`，用于机箱入侵检测的 `JCI1`）不会与此命名模式巧合重复——这只是 MSI 在整个产品线中一致的 `J + 功能 + 数字` 方案，因此一旦了解这一点，无需查阅手册就能解读主板上任何其他丝印排针。
