---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 使用黄色SATA 6Gb/s端口
translated: true
type: note
---

**问题：** 我应该将西部数据 1TB (WD10EZEX) 硬盘连接到华硕 H81M-K 主板的哪个 SATA 接口——黄色（SATA 6Gb/s）还是黑色/深棕色（SATA 3Gb/s）？

---

**答案：**

**使用黄色接口（SATA 6Gb/s）。**

原因如下：

**你的硬盘支持 SATA 6Gb/s。**
WD10EZEX 是一款 SATA 6Gb/s 硬盘，配备 64MB 缓存，转速为 7200 RPM。因此它原生运行在更快的标准上。

**主板接口颜色：**
华硕 H81M-K 主板拥有 2 个 SATA 6Gb/s 接口（黄色）和 2 个 SATA 3Gb/s 接口（深棕色/黑色）。

因此，请将 WD10EZEX 连接到标有 **SATA6G** 的两个**黄色接口**之一。

---

**对于机械硬盘，实际使用中影响大吗？**

说实话，在日常使用中影响不大。一块 7200 RPM 的机械硬盘顺序读写速度最高约为 150–180 MB/s，这完全在 SATA 3Gb/s（约 300 MB/s）的带宽范围内。对于机械硬盘，使用哪个接口其实差别不大——只有对 SATA SSD 才会有明显影响。

但最佳实践仍然是使用黄色 SATA 6Gb/s 接口——这是该硬盘正确的原生速度，同时也能为你将来添加 SSD 时保留更快的接口。

---

**总结表：**

| 接口颜色 | 速度 | 用途 |
|---|---|---|
| **黄色** ✅ | SATA 6Gb/s | WD10EZEX（推荐） |
| 黑色/深棕色 | SATA 3Gb/s | 光驱、旧款硬盘 |

---

**参考来源：**
- [ASUS H81M-K 技术规格](https://www.asus.com/rs-en/motherboards-components/motherboards/business/h81mk/techspec/)
- [WD10EZEX SATA-IO 认证](https://sata-io.org/product/8850)
- [Tom's Hardware – SATA 接口颜色讨论](https://forums.tomshardware.com/threads/asus-h81m-plus-sata-slots.3703153/)