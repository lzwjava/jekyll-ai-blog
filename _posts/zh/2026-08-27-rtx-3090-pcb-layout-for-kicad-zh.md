---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 适用于KiCad的RTX 3090 PCB布局
translated: true
type: note
---

问题：如何找到用于 KiCad 的 RTX 3090 PCB 布局/原理图？

回答：

找到官方 RTX 3090 PCB 布局用于 KiCad 非常困难，因为 NVIDIA 对其 GPU 板设计保持专有。不过，以下是一些实际可行的选择：

**1. 社区/开源仓库**
- 在 GitHub 上搜索关键词如 `RTX 3090 PCB`、`GA102 PCB` 或 `GPU PCB KiCad`
- 查看 [Hackaday.io](https://hackaday.io) 上关于 GPU 的硬件破解项目
- 浏览 [EEVblog 论坛](https://www.eevblog.com/forum/) — 硬件拆解帖子有时会包含追踪到的原理图

**2. 逆向工程原理图**
- 像 **schematics.com** 或 **elektrotanya.com** 这样的网站偶尔会托管维修技术人员上传的 GPU 板原理图
- 搜索 `RTX 3090 schematic PDF` — 一些专注于维修的社区会分享部分原理图
- YouTube 上的 GPU 维修频道（例如 *northridgefix*）有时会引用或链接到板级文档

**3. 将现有文件转换为 KiCad 格式**
- 如果你找到 Altium、Eagle 或 PDF 格式的原理图，你可以：
  - 使用 **KiCad 的 Altium 导入器**（自 KiCad 6 起内置）
  - 通过 KiCad 的导入工具使用 **Eagle 转 KiCad 转换器**
  - 手动将 PDF 原理图描摹到 KiCad 的原理图编辑器中

**4. GPU 维修/Boardview 文件**
- 搜索 RTX 3090 的 `.brd` 或 `.bdv` 板视图文件（维修技术人员使用）
- 像 **OpenBoardView** 这样的工具可以读取这些文件，你可以在 KiCad 中构建时参考它们
- 搜索：`RTX 3090 boardview` 或 `GA102 boardview`

**5. 从参考设计入手**
- NVIDIA 发布了 **PCIe x16 参考指南** — 如果你在设计载板，这会很有用
- 使用 KiCad 内置的 PCIe 连接器封装作为起点

> ⚠️ **注意：** 重新分发 NVIDIA 的专有 PCB 设计可能侵犯其知识产权。请自行决定使用社区追踪的原理图，并验证你找到的任何文件的准确性。

---

参考资料：
- [KiCad EDA 官方网站](https://www.kicad.org/)
- [OpenBoardView（板视图查看器）](https://github.com/OpenBoardView/OpenBoardView)
- [EEVblog 硬件/维修论坛](https://www.eevblog.com/forum/repair/)
- [Hackaday.io 项目](https://hackaday.io)