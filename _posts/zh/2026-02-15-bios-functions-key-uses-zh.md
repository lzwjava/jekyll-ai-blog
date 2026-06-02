---
audio: false
generated: true
image: false
lang: zh
layout: post
title: BIOS 功能与主要用途
translated: true
type: note
---

Question: What can we use BIOS for?

Answer:

**BIOS** (Basic Input/Output System) 是存储在计算机主板上的 firmware。它是你在开启电脑时运行的第一个软件。虽然大多数现代计算机（特别是 2012-2020 年之后）已经用 **UEFI**（一种更先进的继任者）取代了传统的 **legacy BIOS**，但即使在 UEFI 系统上，“BIOS”一词仍被广泛用于指代设置界面。

以下是 BIOS 的主要用途：

### 启动过程中的核心功能（自动运行）

- 执行 **Power-On Self-Test (POST)** —— 检查必要的 hardware（CPU、RAM、graphics card、storage devices、keyboard 等）是否存在并正常工作。
- 初始化并配置 hardware 组件，使其为 operating system 做好准备。
- 查找 boot device（hard drive、SSD、USB 等）并加载 bootloader，然后由其启动你的 operating system（Windows、Linux 等）。

如果没有这个过程，你的计算机根本无法启动。

### 实际用途 —— 用户在 BIOS 设置界面中做什么

你可以进入 BIOS 设置（通常在启动期间按下 Del、F2、F10 或 Esc 键 —— 取决于主板）来手动控制几个重要的设置：

- 更改 **boot order**（例如，首先从 USB 启动以安装 Windows 或从 flash drive 体验 Linux）
- 启用或禁用 **Secure Boot**（主要在 UEFI 模式下 —— 有助于防止启动期间的 malware）
- 开启/关闭 hardware 功能（integrated graphics、onboard audio、某些 USB ports、用于安全性的 TPM 等）
- 对 CPU、memory 进行 Overclock，或调整 voltages 和 timings（常见于游戏玩家和性能爱好者 —— 需要谨慎操作）
- 设置系统日期和时间
- 启用/禁用 **Fast Boot** 或其他启动优化
- 配置 **fan speeds** 和冷却配置文件（在许多现代主板上）
- 如果系统在更改后变得不稳定，将设置重置为默认值
- 查看基础 hardware 信息（CPU temperature、检测到的 RAM 容量、storage devices 等）

### 其他/较少见的用途

- 更新 BIOS/UEFI firmware 本身，以增加对新 CPU 的支持、修复 bugs、提高稳定性或解锁新功能。
- 排除 hardware 问题（POST beeps 或代码通常指向 BIOS 检测到的问题）。
- 在非常古老的系统（pre-UEFI 时代）中，BIOS 为 DOS 程序提供了直接操作 hardware（keyboard、screen、disks）的底层访问 —— 这在今天几乎不再需要。

**2026 年重要说明**：
大多数新主板和 PC 使用 **UEFI** 而不是传统的 BIOS。UEFI 提供更快的启动时间、对大于 2 TB 驱动器的支持、图形化的鼠标友好界面、更好的安全性和更多功能。然而，即使人们指的是 UEFI 设置程序，通常仍会说“进入 BIOS”。

简而言之 —— BIOS（或 UEFI）主要用于：

- 确保计算机每次都能正常启动
- 自定义启动行为和 hardware 设置
- 解决启动或兼容性问题

References:

- [https://en.wikipedia.org/wiki/BIOS](https://en.wikipedia.org/wiki/BIOS)
- [https://www.techtarget.com/whatis/definition/BIOS-basic-input-output-system](https://www.techtarget.com/whatis/definition/BIOS-basic-input-output-system)
- [https://superops.com/blog/what-is-bios](https://superops.com/blog/what-is-bios)
- [https://www.trentonsystems.com/en-gb/blog/what-is-bios](https://www.trentonsystems.com/en-gb/blog/what-is-bios)
