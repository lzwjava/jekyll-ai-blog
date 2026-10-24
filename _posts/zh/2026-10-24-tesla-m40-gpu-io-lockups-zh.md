---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Tesla M40 GPU I/O锁定
translated: true
type: note
---

所有信息已收集。以下是 **192.168.1.34 (lzw-MS-7996)** 的完整报告：

## System Overview

| 组件 | 详情 |
|---|---|
| **OS** | Ubuntu 26.04.1 LTS (resolute)，内核 7.0.0-38-generic，运行时间 10d 17h |
| **Board** | MSI **Z170A GAMING M5** (MS-7977) — 注意：主机名显示为 MS-7996，但 DMI 读数为 MS-7977 |
| **CPU** | Intel Core **i5-6600** @ 3.30 GHz — 1 个插槽，4 核 / 4 线程，睿频 3.9 GHz，Skylake 架构，VT-x |
| **RAM** | 共 11 GiB（已用 4.5 GiB），**swap 已用满 3.7 GiB** ⚠️ |
| **GPU** | **NVIDIA Tesla M40**（12 GB：11520 MiB）+ Intel HD 530（iGPU） |
| **Disk** | 1 TB WD Blue `WD10EZEX`（SATA）— `/` 分区 915G ext4，已用 139G（16%），`/boot/efi` 分区 1G vfat |
| **Network** | `enp3s0` → 192.168.1.34/24 |

## GPU 详情 (nvidia-smi, 驱动 580.178.04 / CUDA 13.0)

```
GPU 0:  Tesla M40          Off    41°C    P0    62W / 250W
        4 MiB / 11520 MiB used    0% util    Persistence Off
gnome-shell 是唯一使用它的进程（1 MiB）
```

## 注释 / 健康标志

- ⚠️ **GPU 存在 I/O 锁定**：`nvidia-smi` 挂起（进程处于 **D 状态** `Dl` — 不可中断，即使 SIGKILL 也无法终止）。18 分钟前的查询仍然卡住；已积累多个。GPU 间歇性响应（一次后台运行成功并返回了上表）。建议重启机器或检查显卡/驱动，尤其是在依赖它进行计算之前。
- ⚠️ Swap 已用满（3.7/3.7 GiB）。
- 🔄 一个 `python` 进程（PID 88699）占用 1 个核心达 99.9% — 负载平均值正好为 4.00（共 4 核），因此这台机器目前正忙。
- 🖥️ 这是一台桌面机器：正在运行 GNOME shell、Firefox、Ghostty（6 个用户登录）。
- 内存条详细信息（DMI）需要 root 权限；我只得到了总共 11 GiB。

希望我深入检查什么吗？例如，识别那个正在运行的 python 进程，检查卡住的 nvidia-smi D 状态进程，或运行 GPU 基准测试？