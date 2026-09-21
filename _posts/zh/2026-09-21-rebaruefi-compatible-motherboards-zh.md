---
audio: false
generated: true
image: false
lang: zh
layout: post
title: ReBarUEFI兼容主板
translated: true
type: note
---

**问题：** ReBarUEFI 项目推荐或确认支持哪些主板？

**回答：**

ReBarUEFI 项目并未官方“推荐”特定主板供购买——而是维护了一份由社区提供的已确认支持的主板列表。以下是来自[支持主板问题列表](https://github.com/xCuri0/ReBarUEFI/issues/11)中最常报告且支持良好的主板摘要：

**华硕（ASUS，占比最大的品牌）：**

- Z170 系列：Z170-A、Z170-AR、Z170-DELUXE、Z170-WS、Z170-E、Z170I Pro Gaming、Z170-P、Z170 Sabertooth MARK 1
- Z97/Z270 系列：Z97-Pro、Z97-DELUXE、Z97-K、Z270-A、Maximus VII/VIII/IX Hero/Gene
- X99 系列：X99-A、X99-A II、X99-DELUXE、X99-DELUXE II、X99M-WS、ROG RAMPAGE V EDITION 10、Sabertooth X99、STRIX X99 GAMING
- 较旧型号：P8Z77-V PRO、P8H61-M LX2 R2.0、H110M-K/D、B150M-C、H170M-PLUS、EX-B150M-V3

**微星（MSI）：**

- Z97 Gaming 3/5、Z170-A PRO、Z170A Gaming M5、Z270-A PRO、Z270 GAMING M5
- B150M Bazooka/Plus、H110M Gaming、C236M WORKSTATION、H97M-G43

**华擎（ASRock）：**

- Z97 Extreme9、Z97 Anniversary、Fatal1ty Z97 Killer
- Z170 Extreme4、Z270M Extreme4、H77 Pro4-M/MVP
- X99 Extreme4、X99 Taichi、X299 Steel Legend

**技嘉（Gigabyte）：**

- B75M-D3H、Z170-HD3、Z68MA-D2H-B3、GA-Z270P-D3
- B450 AORUS ELITE/M、B550M Pro-P、X470 AORUS GAMING 5 WiFi、AB350 Gaming、A320M-S2H

**华南智（Huananzhi）/ 玛雅（Machinist）（AliExpress X99）：**

- 华南智 X99-QD4、X99-TF、X99-F8、X79 “绿色版”
- 玛雅 X99-MR9A PRO V2、精鲨（Jingsha）X79M-S/X99 D8

**超微（Supermicro，服务器主板）：**

- X9SRA、X9DRI-LN4F、X9DRD-7LN4F、X11DPH-T、X11DPU、X11SPH-nCTF、X10SRH-CLN4F、H11DSI

几点关键说明：

- ReBarUEFI 是一个 UEFI DXE 驱动，用于在不官方支持 Resizable BAR 的系统上启用该功能。
- 不支持至少 2GB BAR 大小的主板被该项目视为“不支持”。
- 许多主板需要 **UEFIPatch** 和/或 **DSDT 补丁**——尤其是 Sandy/Ivy Bridge（Z68、Z77、H77）和 Haswell（Z97、H97）主板。
- 华硕 Z170 和 X99 主板出现频率最高，且支持最大的 BAR 大小（最高可达 16–32GB），因此从社区结果来看，可以说是最“值得推荐”的。

**参考：**

- [ReBarUEFI GitHub 仓库](https://github.com/xCuri0/ReBarUEFI)
- [支持主板列表（Issue #11）](https://github.com/xCuri0/ReBarUEFI/issues/11)
