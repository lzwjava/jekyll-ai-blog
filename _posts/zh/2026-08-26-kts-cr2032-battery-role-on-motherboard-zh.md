---
audio: false
generated: true
image: false
lang: zh
layout: post
title: KTS CR2032 电池在主板上的作用
translated: true
type: note
---

**问题：** 什么是 KTS CR2032 锂电池，它在主板中起什么作用？

**回答：**

**KTS** 是印在电池上的品牌/制造商名称。CR2032 是电池型号——一种小型纽扣电池。以下是对其的详细说明：

**什么是 CR2032？**

- **C** = 锂化学
- **R** = 圆形
- **20** = 直径 20mm
- **32** = 厚度 3.2mm
- 电压：**3V**

**它在主板上的作用是什么？**

它为主板上的 **CMOS**（互补金属氧化物半导体）芯片供电。具体来说：

1. **保持 BIOS/UEFI 设置不丢失**——启动顺序、系统时钟和硬件配置等信息存储在 CMOS 内存中。即使电脑断电，该电池也能维持这些内存供电。
2. **维持实时时钟（RTC）运行**——确保电脑在关机后也能知道正确的日期和时间。
3. **保存硬件设置**——超频配置、风扇配置等。

**CMOS 电池耗尽的表现：**

- 关机后电脑时间/日期丢失
- 每次启动时 BIOS 恢复为出厂默认设置
- 启动时提示 *"CMOS checksum error"* 等错误信息

**KTS CR2032 规格（典型值）：**

| 规格 | 数值 |
| --- | --- |
| 电压 | 3V |
| 容量 | ~220 mAh |
| 类型 | 锂纽扣电池 |
| 接口 | 部分型号带有 2 针插头（用于笔记本电脑） |

带 2 针插头的 KTS CR2032 专用于笔记本电脑和台式机主板的 CMOS/BIOS。不带插头的标准 CR2032 则放置于台式机主板的电池座上，可在几秒内完成更换。

**参考资料：**

- [Newegg上的 KTS CR2032](https://www.newegg.com/p/14R-09B4-00B06)
- [eBay上的 KTS CR2032 10粒装](https://www.ebay.com/itm/236013234233)
- [KTS CR2032 CMOS 电池套件 (Latinafy)](https://latinafy.com/products/kts-cr2032-3v-cmos-bios-battery-kit-for-motherboards-10-units/)
