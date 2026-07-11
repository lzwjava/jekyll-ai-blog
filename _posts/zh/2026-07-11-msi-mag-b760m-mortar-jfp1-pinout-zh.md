---
audio: false
generated: true
image: false
lang: zh
layout: post
title: MSI MAG B760M Mortar JFP1 引脚定义
translated: true
type: note
---

问题：MSI MAG B760M Mortar 主板上的 JFP1（前面板）接口的引脚定义是什么？

答案：

MAG B760M Mortar（所有三个 SKU：Mortar、Mortar WIFI、Mortar MAX WIFI）上的 JFP1 是标准的前面板开关/LED 接口——它控制电源开关、复位开关以及机箱上的 LED，包含电源开关/复位开关引脚（用于电源和复位按钮）、电源 LED 引脚和硬盘活动指示灯（HDD LED）引脚。这是一个 2×5 针的接口，第 9 针物理缺失作为防呆/方向标识，因此共有 9 个可用引脚。

这是 MSI 对 Intel 前面板 I/O 连接设计指南接口的实现，其引脚定义表在几乎所有现代 MSI 主板上（B650、B760、Z790 等）都是相同的——以下标准表格来自 MSI 使用同一连接器的主板官方手册：

```
JFP1 引脚定义（2x5 接口，第 9 针为无针/防呆键）

 1  3  5  7  9(键)
 2  4  6  8  10

引脚 | 信号          | 描述
----+---------------+---------------------------------------------
 1  | HD_LED+       | 硬盘 LED 正极，上拉
 2  | FP PWR/SLP+    | 电源 LED 上拉
 3  | HD_LED-       | 硬盘活动 LED 阴极
 4  | FP PWR/SLP-    | 电源 LED 上拉（第二根 LED 引线）
 5  | RST_SW-       | 复位开关低参考端，下拉至 GND
 6  | PWR_SW+       | 电源开关高参考端，上拉
 7  | RST_SW+       | 复位开关高参考端，上拉
 8  | PWR_SW-       | 电源开关低参考端，下拉至 GND
 9  | (无引脚)      | 键——防呆方向标识
10  | RSVD_DNU      | 保留，请勿连接
```

机箱跳线的实际接线方式：

- **Power Switch（2 针，无极性）** → 引脚 6 + 8
- **Reset Switch（2 针，无极性）** → 引脚 5 + 7
- **Power LED（2 针，有极性）** → 引脚 2 + 4（若机箱使用双色电源/休眠 LED 则为 4 针，跨接相同的信号对）
- **HDD LED（2 针，有极性）** → 引脚 1 + 3

装机注意事项：

- 电源和复位开关为瞬时触点——极性无关，正反接均可工作。
- LED 有极性：接反仅导致 LED 不亮，不会损坏硬件。
- 在主板上，JFP1 位于 JTPM1、SATA7/8、JUSB1/JUSB2 附近，即主板右下角区域（这与 MSI 典型的 mATX 布局一致，JFP1 在右下角靠近 SATA 接口处）。
- JFP2（单独的 8 针接口）仅用于蜂鸣器/扬声器——启动时不必要，但可用于传统的 POST 蜂鸣码诊断。

参考资料：

- [MSI MAG B760M MORTAR MAX WIFI / WIFI / MORTAR 主板手册](https://www.manualslib.com/manual/3270648/Msi-Mag-B760m-Mortar-Max-Wifi.html)
- [MSI PRO B760M-A WIFI DDR4 — JFP1 描述](https://www.manualslib.com/manual/3085563/Msi-Pro-B760m-A-Wifi-Ddr4.html?page=35)
- [MSI JFP1 引脚定义表（MS-7346 手册，MSI 系列通用）](https://www.manualslib.com/manual/360307/Msi-Ms-7346.html?page=31)
- [MSI 前面板连接器（JFP1）安装教程 — 视频](https://youtu.be/DPELIdVNZUI)
