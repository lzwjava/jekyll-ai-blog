---
audio: false
generated: true
image: false
lang: zh
layout: post
title: MSI 前面板引脚标签详解
translated: true
type: note
---

**SW = Switch（开关）。**

因此：
- **PWR SW** = **Power Switch（电源开关）** — 机箱物理电源按钮引出的线对
- **RESET SW** = **Reset Switch（重置开关）** — 机箱物理重置按钮引出的线对

这只是微星（以及业界普遍）在引脚标识中使用的缩写——接针上的 `PWR_SW+` / `PWR_SW-` 仅表示“电源开关接触回路的两根引脚”。按下按钮时，它会短暂桥接这两根引脚，主板逻辑将其解读为“用户按下了电源”，并触发 ATX 上电序列。