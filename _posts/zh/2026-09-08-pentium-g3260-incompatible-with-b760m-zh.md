---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 奔腾G3260与B760M不兼容
translated: true
type: note
---

**问题：** Pentium G3260 3.30 GHz 能否在 MSI B760M-E DDR5 上工作？

**回答：** **不能。❌**

**Pentium G3260** 是采用 **LGA1150** 的 **第4代 Haswell CPU**。

**MSI B760M-E DDR5** 使用 **LGA1700**，支持 Intel **12/13/14 代** CPU。

| CPU                | 插槽        | B760M-E DDR5 |
| ------------------ | ----------- | ------------ |
| Pentium G3260      | **LGA1150** | ❌            |
| Pentium G4560      | LGA1151     | ❌            |
| Pentium Gold G7400 | **LGA1700** | ✅            |
| Celeron G6900      | **LGA1700** | ✅            |
| i3-12100           | **LGA1700** | ✅            |
| i5-12400           | **LGA1700** | ✅            |

所以 **3.30 GHz 并不是关键**。物理/电气 CPU 插槽和平台必须匹配。

如果你看到 **G3260 与这款主板捆绑销售**，不要将其作为兼容套装购买。
