---
audio: false
generated: true
image: false
lang: zh
layout: post
title: JRGB1 接口简要说明
translated: true
type: note
---

问题：MSI MAG B760M Mortar WiFi 主板上的 JRGB1 接口是什么意思？

答案：

`JRGB1` 是主板上的一个 **4-pin 12V RGB LED 接口** —— 标准的（非可寻址）Mystic Light 连接器，与 `JARGB_V2` 接口不同。

**关键规格：**

- 连接标准的 12V 5050 RGB LED 灯带
- 支持最长 2 米的连续 5050 RGB LED 灯带，最大功率额定值 3A @ 12V
- 通过 MSI 的 **Mystic Light** 软件（MSI Center 的一部分）控制

**不要与 `JARGB_V2` 混淆：** 该主板还有 1-2 个 `JARGB_V2` 接口，用于可寻址 RGB（每个 LED 可独立控制，5V，3-pin，最多 240 个 LED）。JRGB 连接器和 JARGB_V2 连接器提供不同的电压，将 ARGB 5V LED 灯带连接到 JRGB 连接器会导致灯带损坏——因此这里的针脚/电压不匹配是真正的“冒烟”风险，而不仅仅是兼容性脚注。

**快速参考表：**

| 接口 | 电压 | 针脚 | 用途 |
| --- | --- | --- | --- |
| `JRGB1` | 12V | 4-pin | 标准非可寻址 RGB 灯带 |
| `JARGB_V2_1/2` | 5V | 3-pin | 可寻址（每个 LED 可独立控制）ARGB Gen1/Gen2 灯带 |

如果你在装机时接线，需要注意的实际故障模式：淘宝/阿里上一些便宜的“RGB”灯带标签有误 —— 插入前务必检查灯带本身的规格表是 12V/4-pin 还是 5V/3-pin，因为如果不小心，连接器外壳有时可能被强行插入错误的接口。

参考：

- [MSI MAG B760M MORTAR MAX WIFI 手册 - ManualsLib](https://www.manualslib.com/manual/3270648/Msi-Mag-B760m-Mortar-Max-Wifi.html)
- [MSI MAG B760M MORTAR WIFI - 官方产品页面](https://www.msi.com/Motherboard/MAG-B760M-MORTAR-WIFI)
