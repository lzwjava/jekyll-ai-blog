---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 2011年性能适中的台式机系统
translated: true
type: note
---

以下是 **lzw@192.168.1.45**（`lzw-AOC`）的完整系统信息：

## 🖥️ 系统概述

| 组件 | 详情 |
|---|---|
| **主机名** | lzw-AOC |
| **操作系统** | Ubuntu 26.04 LTS (Resolute Raccoon)，内核 `7.0.0-14-generic` x86_64 |
| **主板** | Onda Technology Corporation **H61N**（通用 OEM 台式机主板） |
| **运行时间** | 约 30 分钟，负载均值 0.16/0.20/0.28（3 个用户登录） |

## 🧠 CPU — Intel Core i3-2130 @ 3.40GHz
- **架构**：x86_64，Sandy Bridge（第 2 代，约 2011 年）
- **核心数**：2 物理 / 4 逻辑（Hyperthreading：每核 2 线程，4 插槽:1）
- **主频**：最高 3.40 GHz / 最低 1.60 GHz，当前缩放至约 78%

## 💾 内存
- **RAM**：总计 7.1 GiB，已用 1.2 GiB，**可用 5.9 GiB**
- **Swap**：4.0 GiB 交换文件（`/swap.img`），**未使用**

## 🎮 GPU — 仅集成显卡（无独立 GPU）
- **Intel HD Graphics (Sandy Bridge)**，PCI `00:02.0`，设备 `8086:0102`
- 无 NVIDIA/AMD 显卡 — 无 `nvidia-smi`
- 桌面环境为 GNOME（snap 包：firefox、gnome-46 等）

## 💽 存储

| 设备 | 大小 | 挂载点 | 使用率 |
|---|---|---|---|
| `/dev/sda` Seagate **ST500DM002** HDD | 465.8 GiB | — | — |
| `/dev/sda1`（EFI） | 1 GiB | `/boot/efi` | 1% |
| `/dev/sda2`（根目录） | 457 GiB | `/` | **3%**（已用 11G，可用 423G） |

**TL;DR**：这是一台性能普通的旧台式机（2011 年左右的 i3 双核），内存尚可（7.1 GB + 4 GB 交换空间），仅集成 Intel 显卡，465 GB 机械硬盘几乎未使用——适合轻量桌面工作，不适合游戏、GPU 计算或任何重负载任务。