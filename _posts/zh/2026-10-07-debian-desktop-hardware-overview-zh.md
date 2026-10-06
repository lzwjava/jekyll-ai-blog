---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Debian 桌面硬件概览
translated: true
type: note
---

这是 **192.168.1.137（Debian 13 trixie，主机名 `debian`）** 的完整硬件报告：

## 🖥️ 系统 / 主板

| 组件 | 详情 |
|---|---|
| 厂商 | **MSI** |
| 主板 | **MSI Z170A GAMING M3（MS-7978）** v2.0 |
| 机箱 | 台式机（类型 3） |
| BIOS | American Megatrends Inc. **A.50**（2016-02-23） |

## 🧠 CPU

| 组件 | 详情 |
|---|---|
| 型号 | **Intel Core i5-6500** @ 3.20GHz（Skylake，第 6 代） |
| 核心数 / 线程数 | **4 核 / 4 线程**（无超线程），1 个插槽 |
| 睿频 | 最高 3.60 GHz，空闲可降至 0.80 GHz |

## 💾 内存

| 组件 | 详情 |
|---|---|
| 总内存 | **7.7 GiB**（8057 MB），约 6.5 GiB 可用 |
| 交换空间 | 2.9 GiB（未使用） |

*（注：dmidecode 未能读取内存模块详情——`lzw` 不在 sudoers 中。如需获取确切的 DDR4 频率/部件号，请告知。）*

## 💽 存储

| 设备 | 容量 | 型号 | 挂载点 |
|---|---|---|---|
| sda | **55.9 GB** | **faspeed K5-60G**（SSD） | `/boot/efi`（976M），`/`（52.1G），swap（2.9G） |

## 🎮 GPU / 外设

| 设备 | 详情 |
|---|---|
| GPU | **Intel HD Graphics 530**（集成，rev 06）——无独立 GPU |
| 音频 | Intel 100 Series/C230 HD Audio |
| 网卡 | **Qualcomm Atheros Killer E2400** 千兆以太网 |

## ⚙️ 内核
`Linux debian 6.12.111+deb13-amd64`（2026-09-28 构建）

**简而言之：** 一台 MSI Z170A GAMING M3 台式机——Skylake i5-6500、8GB DDR4 类内存（Z170 主板容量）和一块 60GB faspeed SSD。它是一个紧凑的家用实验室/服务器主机。需要我提取内存模块详情（需要管理员账户）、检查磁盘 SMART 健康状况，或者在上面安装点什么吗？