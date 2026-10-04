---
audio: false
generated: true
image: false
lang: zh
layout: post
title: i3-2130 Onda H61N 台式机规格
translated: true
type: note
---

以下是 `192.168.1.45`（Onda H61N 台式机）的硬件配置详情：

## 🧠 CPU — Intel Core i3-2130 @ 3.40 GHz
- **Socket**: LGA1155 · **Generation**: Sandy Bridge (2nd gen, 2011)
- **Cores**: 2 physical / 4 threads (Hyper-Threading) · **TDP**: 65W
- L2 512KB, L3 3MB · 最大内存带宽：DDR3-1333

## 🧩 Motherboard — Onda Technology **H61N**
- **Chipset**: Intel **H61 Express**（在 lspci 中确认：`H61 Express Chipset LPC Controller`）
- Socket LGA1155，支持第 2/3 代 Core，2× DDR3 DIMM 插槽，最大 16 GB，1× PCIe x16，SATA II
- 这是该平台的关键规格：**H61 = 仅支持 DDR3，最高 1333 MT/s**

## 💾 Memory chip — DDR3, ~8 GiB
- **物理内存总计**: **8320 MiB**（约 8.1 GiB，来自 lshw 获取的 SMBIOS 信息）
- **Linux 识别到**: 7.1 GiB（`MemTotal 7,486,648 kB`）——约 0.8 GiB 的差额预留给 **Intel HD Graphics iGPU 共享内存**（Sandy Bridge 会占用系统 RAM 作为 VRAM，通常为 512 MB–1.7 GB）
- 平台规定：**DDR3-1333**（H61 的额定规格）

**⚡ 注意**：具体内存条信息（制造商、部件编号、速度等级如 PC3-10600、单条 8G 还是 2×4G 双条）都在 SMBIOS SPD 中，但 `dmidecode` 需要 **root** 权限，而这台机器没有免密 sudo。如果你想要完整的 SPD 转储，让我以交互方式运行 `sudo dmidecode -t memory` — 或者从机器自己的终端运行：
```
sudo dmidecode -t memory | grep -E "Size|Speed|Manufacturer|Part Number|Locator"
```

**TL;DR**：2011 年时期的 Sandy Bridge 台式机 — **i3-2130** CPU，搭载于 **Onda H61N**（H61 chipset，LGA1155）motherboard，配备 **约 8 GB DDR3** 系统内存，DDR3-1333 级别。