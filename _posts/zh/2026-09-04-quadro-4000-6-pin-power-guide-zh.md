---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Quadro 4000 6针电源指南
translated: true
type: note
---

**问题：** Quadro 4000 需要哪种 PCIe 电源线，如何连接？

**回答：**

NVIDIA Quadro 4000 需要**一个 6 针 PCIe 电源接口**。该显卡所需的电源线为 6 针 PCI-E 接口。

操作步骤如下：

**具体步骤：**

1. **完全关闭电脑** — 关闭操作系统，将电源开关拨至 OFF（若有），并拔掉电源线。
2. **在电源上找到 6 针 PCIe 线缆** — 这是一个 6 孔接口，线缆上有时标有“VGA”或“PCIe”。
3. **检查电源是否有 8 针（6+2）接口** — 许多电源配备带 8 针（6+2）接口的线缆；如果只需 6 针，拆下 2 针部分即可。
4. **将 6 针端牢固插入显卡** — 接口只能单向插入（防呆设计）。应能听到/感觉到咔哒声。
5. **请勿使用 SATA 转 PCIe 转接线** — SATA 转 PCIe 和 Molex 转 PCIe 转接线无法提供足够电流；更换新电源更安全。
6. 重新连接电源线并开机。

**关于附带的转接线**（如果显卡附带了双 4 针 Molex 转接线）：该转接线适用于没有专用 PCIe 电源接口的电源——仅在没有其他选择时使用，最好使用电源自带的原生 PCIe 线缆。

**参考：**

- [NVIDIA Quadro 电源指南 (PNY)](https://www.pny.com/file%20library/company/support/product%20brochures/nvidia%20quadro/quadro-power-guidelines.pdf)
- [如何将 Quadro 4000 连接到电源 – Tom's Hardware 论坛](https://forums.tomshardware.com/threads/how-to-connect-quadro-4000-to-psu.791303/)
- [Quadro K4000 电源接口指南 – BleepingComputer](https://www.bleepingcomputer.com/forums/t/795216/nvidia-quadro-k4000-power-connector-needed/)
