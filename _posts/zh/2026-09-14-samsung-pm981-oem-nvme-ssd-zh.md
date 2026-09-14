---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 三星PM981 OEM NVMe固态硬盘
translated: true
type: note
---

**问题：** 三星 MZVLB512HAJQ-000L7 驱动器是什么？

**回答：**

**三星 MZVLB512HAJQ-000L7** 是一款 OEM 企业/笔记本电脑 NVMe SSD，属于 **三星 PM981（Polaris）** 系列。后缀 `-000L7` 是一个变体代码，表明它供应给特定的 OEM 合作伙伴（常见于联想 ThinkPad/ThinkCentre 系统中）。

以下是完整解析：

**身份**

- **型号系列：** 三星 PM981
- **代号：** Polaris
- **类型：** OEM 内部 SSD（非零售）
- **OEM 目标：** 联想、戴尔、惠普及其他系统集成商

**物理规格**

- **外形尺寸：** M.2 2280（22 mm 宽 × 80 mm 长）
- **接口：** PCIe 3.0 x4，NVMe 1.2
- **尺寸：** 约 22 × 80 × 2.38 mm
- **重量：** 约 0.32 盎司（约 9 g）

**存储**

- **容量：** 512 GB
- **NAND 类型：** 3D V-NAND（TLC/MLC，取决于供应商来源）
- **控制器：** 三星 Phoenix（自研）
- **DRAM 缓存：** 有（板载 LPDDR4）

**性能**（根据三星官方数据表）

- **顺序读取：** 最高 3,200 MB/s；**顺序写入：** 最高 2,400 MB/s
- **随机读取：** 最高 380K IOPS；**随机写入：** 最高 440K IOPS（4K 块，4 通道）

**安全性**

- **加密：** 256-bit AES-XTS 硬件加密，TCG Opal 2.0，自加密驱动器（SED）

**可靠性**

- **MTBF：** 1,500,000 小时；**不可纠正位错误率：** 每 10¹⁵ 位 1 次

**备注**

- 作为 OEM 产品，它没有零售包装、消费者保修或官方规格表。三星魔术师软件不支持此驱动器。
- 它本质上是消费级 **三星 970 EVO** 的 OEM 前身，以更低的 OEM 价格提供几乎相同的性能。
- PM981 后来被 **PM981a** 取代，后者使用更新的 92 层 V-NAND，能效稍优。

---

**参考资料：**

- [三星 PM981 SSD 评测 — Tom's Hardware](https://www.tomshardware.com/reviews/samsung-pm981-980-nvme-ssd,5323.html)
- [PM981 数据表 v1.1 — compuram.biz](https://www.compuram.biz/documents/datasheet/Samsung_PM981_Rev_1_1.pdf)
- [三星 PM981 MZVLB512HAJQ — SHI 概述](https://www.shi.com/product/36935413/Samsung-PM981-MZVLB512HAJQ)
- [MZVLB512HAJQ-000L7 — HardDiskDirect](https://harddiskdirect.com/mzvlb512hajq-000l7-samsung-solid-state-drive.html)
