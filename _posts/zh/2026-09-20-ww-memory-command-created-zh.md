---
audio: false
generated: true
image: false
lang: zh
layout: post
title: ww内存命令已创建
translated: true
type: note
---

一切工作正常。以下是所创建内容的摘要：

---

## ✅ 完成 —— 创建了 `ww memory {host}` 命令

### 修改的文件

| 文件 | 操作 |
|------|--------|
| `ww/machine/memory.py` | **已创建** —— 完整的内存诊断模块 |
| `ww/main.py` | **已编辑** —— 添加了 `memory` 组调度及帮助文本 |

### 用法

```bash
ww memory lzw@192.168.1.53
ww memory root@server -i ~/.ssh/key.pem
ww memory --help
```

### 功能说明

| 特性 | 描述 |
|---------|-------------|
| **内存使用情况** | `free -h` + `/proc/meminfo`（总量、空闲、可用、交换） |
| **SPD EEPROM 解码** | 从 I²C 读取 DRAM 模块信息（DDR3/DDR4/DDR5）：类型、部件编号、制造商、Rank、电压、速率、CAS 延迟、生产日期 |
| **硬件插槽** | 从 dmesg 获取 —— 显示已占用/总插槽数 |
| **CPU / 平台** | lscpu 输出 |
| **内核消息** | 与内存相关的 dmesg/journalctl |
| **健康状态摘要** | 使用率百分比、SPD 状态、内存块在线状态 |

### `lzw@192.168.1.53` 的测试输出

```
Memory Type:    DDR3 SDRAM
Module Type:    UDIMM
Part Number:    KB256082G
Manufacturer:   Fujitsu  (ID: 0x04 0x51)
Ranks:          2
Speed:          ~1330 MT/s
Grade:          DDR3-1330 (PC3-10640)
Module Size:    2.0 GB (from SPD)
Mfg Date:       2018 week 25
Slots populated: 2/2
Usage:  27%  (2.4 GB free / 3.2 GB total)
✅ SPD readable, all 32 memory blocks online
```