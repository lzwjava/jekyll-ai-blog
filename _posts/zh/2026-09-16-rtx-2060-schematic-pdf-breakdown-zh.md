---
audio: false
generated: true
image: false
lang: zh
layout: post
title: RTX 2060 电路图PDF详解
translated: true
type: note
---

我通过提取其完整矢量文本（55页，~242 KB标签）阅读了该PDF。注意：该文件是**原理图（Схема = 俄语中的"schematic"）**，而非板图。以下是内容。

## 文档标识
- **文件：** `Gigabyte RTX 2060 Gaming OC Pro 6GB (GV-N2060GAMINGOC PRO-6GD) Rev 2.0 Схема.pdf`（1.1 MB，55页，A4横向）
- **来源：** NVIDIA参考设计 **PG161-A00**，Rev 2.0，日期2019-03，由技嘉定制为 **GV-N2060GAMINGOC PRO-6GD**（标题栏显示"Custom GV-N2060GAMINGOC PRO-6GD 2.0"，Rev 2.0）。
- **板卡描述：** TU106 6GB GDDR6，192-bit，PCIe x16，输出接口 **DVI-D/DP + DP + HDMI**
- **主要部件：**
  - GPU：**TU104-400-A1**，BGA2228（跨图纸标注为G1A–G1U）
  - 内存：**6× Micron MT61K256M32JE-12:A**，FBGA180 GDDR6（M9A/B/C/D，M10A/B/C/D，M11/M12）
  - ROM：**U11 W25Q80EW**（8 Mb SPI），27 MHz晶振（Y1/Y2）

## 页码映射

| 页码 | 内容 |
|---|---|
| 1–2 | 目录 / 框图 |
| 3–4 | PCI Express x16边缘连接器 + PCIe RC端接 |
| 5–14 | GPU↔内存总线 FBA/FBB/FBC/FBD，CMD/CLK/WCK，数据，DBI/EDC |
| 15–17 | GPU电源/地，去耦 |
| 18–23 | 显示I/O：DVI-D，DP（A/B/C/D），HDMI，USB-C NC |
| 24–25 | NVHS/帧锁定， thermal，JTAG，GPIO，立体声 |
| 26 | MISC2：ROM，XTAL，配置/ RAMCFG |
| 27–31 | 电源：1V8_AON（U15 GS9216TQ），5V（U4 MP1475DJ），PEXVDD（U13 GS9216TQ），FBVDDQ（U3 uP1666QQKF，2相） |
| 32–36 | NVVDD控制器（U504 uP9512R）+ 6相（uPi DrMOS） |
| 37–39 | 输入电源平衡切换器，滤波/监控，转向/UPB/热插拔 |
| 40–42 | Type-C升降压，PD PPC，12V & 3V3_A切换器（此SKU上主要为标题栏占位） |
| 43–47 | 上电时序：5V/1V8/NV3V3使能，NV/PEX/FB使能，电压监控，放电，杂项 |
| 48–50 | 徽标LED，LED驱动器及升压，风扇 |
| 51–53 | 预滤波器，MECH，PTC |
| 54–55 | **技嘉定制页面：** MCU（U634 HT32F52241）+ RGB LED / 风扇控制 |

## 故障排查关键器件
- **U504 uP9512R** – NVVDD PWM控制器（VQFN5×5-40L）
- **U3 uP1666QQKF** – FBVDDQ控制器（1.35 V，2相）
- **U15 GS9216TQ** – 1V8_AON降压；**U13 GS9216TQ** – PEXVDD降压（~1.0 V）
- **U4 MP1475DJ** – 5V降压；**U507/U510 NCP114AMX330** – 3V3_SEQ LDO
- **U503 NCP45491** – 输入电源监控/平衡器（GPU_ADC_IN_P/N，RSENSE）
- **U505/U506/U508/U509** – M74VHC1GT08使能逻辑
- NVVDD相使用uPi DrMOS（INS17xxxxx），0.15 µH电感，330 µF/820 µF聚合物电容
- **U634 HT32F52241** + **U633 APL431** + **U849 APL3552** – 技嘉MCU/LED/风扇控制

## 电源轨/上电时序
`12V (PCIe 8-pin) → 5V → 3V3/3V3_SEQ → 1V8_AON → NV3V3 → PEXVDD → NVVDD / FBVDDQ`，根据第43–44页通过PGOOD链（`PS_5V_PGOOD`、`PS_1V8_AON_PGOOD`、`PS_PEXVDD_PGOOD`、`PS_NVVDD_PGOOD`、`PS_VMON_PGOOD`、`PS_FBVDDQ_EN`）使能。

注意：从矢量原理图提取的文本可能会使某些小数值/网络名称出现乱码，因此在操作前请务必对照实际PDF页面核对任何具体的电阻/电容值。

我已将按页清理后的文本保存在 `%TEMP%\clean.txt`，并且如有需要可以将任何页面渲染为PNG。您想用它做什么——定位网络、追踪电源轨，还是诊断故障？